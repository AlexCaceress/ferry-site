// getferry.net: serves the static site and handles the waitlist form ("Ferry for every AI").
// Each signup is emailed to the Ferry inbox through Cloudflare Email Routing (send_email binding "AVISO").
import { EmailMessage } from 'cloudflare:email';

const FROM = 'waitlist@getferry.net';
const TO = 'ferry.extension@gmail.com';
const EMAIL_OK = /^[^\s@<>"']{1,64}@[^\s@<>"']{1,190}\.[a-z]{2,24}$/i;

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  });
}

async function waitlist(request, env) {
  if (request.method !== 'POST') return json({ ok: false }, 405);
  let data;
  try { data = await request.json(); } catch { return json({ ok: false, error: 'bad-request' }, 400); }
  const email = String(data.email || '').trim();
  const lang = data.lang === 'es' ? 'es' : 'en';
  const IAS = ['ChatGPT', 'Claude', 'Gemini', 'Copilot', 'Perplexity', 'Grok', 'DeepSeek', 'Other'];
  const desde = IAS.includes(data.desde) ? data.desde : 'unknown';
  const hacia = IAS.includes(data.hacia) ? data.hacia : 'unknown';
  // Hidden field that people never fill in; bots usually do.
  if (data.website) return json({ ok: true });
  if (email.length > 254 || !EMAIL_OK.test(email)) return json({ ok: false, error: 'email' }, 400);

  const now = new Date();
  const raw = [
    `From: Ferry waitlist <${FROM}>`,
    `To: ${TO}`,
    `Reply-To: ${email}`,
    `Subject: Ferry waitlist: ${desde} -> ${hacia}`,
    `Date: ${now.toUTCString()}`,
    `Message-ID: <${crypto.randomUUID()}@getferry.net>`,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=utf-8',
    '',
    `New signup for "Ferry for every AI".`,
    '',
    `Email: ${email}`,
    `Move from: ${desde}`,
    `Move to: ${hacia}`,
    `Language: ${lang}`,
    `Country: ${request.cf && request.cf.country ? request.cf.country : 'unknown'}`,
    `Time: ${now.toISOString()}`,
  ].join('\r\n');

  try {
    await env.AVISO.send(new EmailMessage(FROM, TO, raw));
  } catch (e) {
    console.error('waitlist send failed', e && e.message);
    return json({ ok: false, error: 'send' }, 502);
  }
  return json({ ok: true });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/waitlist') return waitlist(request, env);
    return env.ASSETS.fetch(request);
  },
};
