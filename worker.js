// getferry.net: serves the static site, the waitlist form ("Ferry for every AI")
// and the feedback form on the welcome and goodbye pages.
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

// Answers from the pages the extension opens: /welcome (after install) and /bye (after uninstall).
const MOTIVOS = {
  welcome: ['personal-work', 'work-personal', 'personal-personal', 'school', 'other-ai', 'other'],
  bye: ['done', 'broken', 'missing', 'hard', 'trust', 'trying', 'other'],
};

async function feedback(request, env) {
  if (request.method !== 'POST') return json({ ok: false }, 405);
  let data;
  try { data = await request.json(); } catch { return json({ ok: false, error: 'bad-request' }, 400); }
  if (data.website) return json({ ok: true });
  const tipo = data.tipo === 'bye' ? 'bye' : data.tipo === 'welcome' ? 'welcome' : null;
  if (!tipo) return json({ ok: false, error: 'bad-request' }, 400);
  const motivo = MOTIVOS[tipo].includes(data.motivo) ? data.motivo : '';
  const texto = String(data.texto || '').trim().slice(0, 2000);
  const email = String(data.email || '').trim();
  const version = /^\d{1,4}(\.\d{1,4}){0,3}$/.test(String(data.version || '')) ? String(data.version) : 'unknown';
  const lang = data.lang === 'es' ? 'es' : 'en';
  if (!motivo && !texto) return json({ ok: false, error: 'empty' }, 400);
  if (email && (email.length > 254 || !EMAIL_OK.test(email))) return json({ ok: false, error: 'email' }, 400);

  const now = new Date();
  const raw = [
    `From: Ferry feedback <${FROM}>`,
    `To: ${TO}`,
    ...(email ? [`Reply-To: ${email}`] : []),
    `Subject: Ferry ${tipo}: ${motivo || 'comment'}`,
    `Date: ${now.toUTCString()}`,
    `Message-ID: <${crypto.randomUUID()}@getferry.net>`,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=utf-8',
    '',
    tipo === 'welcome' ? 'Answer from the welcome page (after installing Ferry).' : 'Answer from the goodbye page (after removing Ferry).',
    '',
    `Option: ${motivo || '(none)'}`,
    `Comment: ${texto ? texto.replace(/\r?\n/g, '\r\n  ') : '(none)'}`,
    `Email: ${email || '(none)'}`,
    `Ferry version: ${version}`,
    `Language: ${lang}`,
    `Country: ${request.cf && request.cf.country ? request.cf.country : 'unknown'}`,
    `Time: ${now.toISOString()}`,
  ].join('\r\n');

  try {
    await env.AVISO.send(new EmailMessage(FROM, TO, raw));
  } catch (e) {
    console.error('feedback send failed', e && e.message);
    return json({ ok: false, error: 'send' }, 502);
  }
  return json({ ok: true });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/waitlist') return waitlist(request, env);
    if (url.pathname === '/api/feedback') return feedback(request, env);
    return env.ASSETS.fetch(request);
  },
};
