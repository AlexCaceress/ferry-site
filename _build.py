# Generates index.html (English) and es/index.html (Spanish) from one template.
# Run: python _build.py
import os

STORE = 'https://chromewebstore.google.com/detail/hflghkalnkgcmkpppfkpddelokimodag'
EMAIL = 'support@getferry.net'

def svg(body, stroke='currentColor', width='1.8'):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')

BARCO = '<path d="M4 14h16l-2.2 4.2a2 2 0 0 1-1.8 1.1H8a2 2 0 0 1-1.8-1.1z"/><path d="M7 14V9.5h8.5L18 14"/><path d="M10 9.5V6.5h3"/>'
CARPETA = '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'
CHAT = '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>'
DOC = '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/>'
ZIP = '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M12 3v2M12 7v2M12 11v2"/><rect x="10" y="14" width="4" height="4" rx="1"/>'
ESTRELLA = '<path d="M12 3l2.2 4.6 5 .7-3.6 3.5.9 5L12 14.5 7.5 16.8l.9-5L4.8 8.3l5-.7z"/>'
PERSONA = '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'
OK = '<path d="M5 12.5l4.5 4.5L19 7.5"/>'
NO = '<path d="M7 7l10 10M17 7L7 17"/>'
FLECHA = '<path d="M5 12h14M13 6l6 6-6 6"/>'
ESCUDO = '<path d="M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>'
OJO_NO = '<path d="M3 3l18 18"/><path d="M10.6 5.1A10 10 0 0 1 12 5c5 0 9 4.5 10 7a13 13 0 0 1-2.6 3.7M6.6 6.6C4.3 8 2.7 10.2 2 12c1 2.5 5 7 10 7a9.6 9.6 0 0 0 4.4-1.1"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/>'
LLAVE = '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>'

T = {
 'en': dict(
  lang='en', base='', other='es/', other_lang='es', other_name='Español', privacy='privacy.html', canon='https://getferry.net/',
  title='Ferry: move Claude projects, chats and memory to another account',
  desc='Ferry is a free Chrome extension that moves your Claude projects, chats and memory from one claude.ai account to another. Not affiliated with Anthropic.',
  skip='Skip to content', nav_how='How it works', nav_priv='Privacy', nav_faq='FAQ', add='Add to Chrome',
  chips=['Free', 'No sign-up', 'Runs in your browser'],
  h1='Move your Claude projects to another account',
  lead='Projects, chats and memory, between any two claude.ai accounts, even with different emails. Personal, work or school. You pick exactly what comes along.',
  cta="Add to Chrome, it's free", see='See how it works',
  c1='Product launch is now in your work account', c1s='Just now',
  c2='42 chats saved, 12 brought in', c2s='The rest stay in your ZIP',
  c3='Project memory added as CONTEXT.md',
  legal='Independent tool, not affiliated with Anthropic.',
  cmp_h='Stop rebuilding projects by hand', cmp_p='Claude only merges a personal account into a work one when both use the same email, and then it moves everything. Any other move meant doing it piece by piece.',
  hand_h='By hand', hand=['Download every file, one by one', 'Copy and paste the instructions', 'Create the project again from scratch', 'Paste old chats back in, one at a time', 'Lose what Claude remembered'],
  ferry_h='With Ferry', ferry=['Save the whole project as one ZIP', 'Log in to the other account', 'Bring it in with one click', 'Memory comes along as CONTEXT.md'],
  how_h='Three steps', how_p='Ferry opens in a side panel next to claude.ai, so you never leave the page.',
  s1h='Take it from the old account', s1='Pick a project or any chat and save it. You get one ZIP file with everything inside.',
  s1a='Product launch', s1b='Yesterday', s1c='Thesis research', s1d='3 days ago', s1btn='Save "Product launch"',
  s2h='Switch accounts', s2='Log in to claude.ai with the account you want to move to.',
  s2a='Personal', s2am='you@gmail.com', s2b='Work', s2bm='you@company.com',
  s3h='Bring it in', s3='Open Ferry again, choose the file and pick what to include. Then one click.',
  s3a='Instructions', s3b='Files', s3bn='6', s3c='Chats', s3cn='12 of 42', s3btn='Bring project',
  what_h='What comes with you', what_p='Ferry recreates the project as a private project in the new account.',
  w1h='Projects', w1='Instructions, knowledge files, project memory and the chats inside.',
  w2h='Single chats', w2='Search every chat, in a project or not, and continue it in the other account with its original title.',
  w3h='Account memory', w3tag='Optional', w3='What Claude remembers about you. Off by default, so personal details stay out of a work account.',
  priv_h='No servers in the middle', priv_p='Ferry runs in your browser. Your data goes from claude.ai to your computer and back, and nowhere else.',
  p1h='Nothing to sign up for', p1='Ferry uses the claude.ai session you already have. There is no Ferry account.',
  p2h='No tracking', p2='No analytics and no ads. Your data is never sold or shared.',
  p3h='Only your projects', p3='Ferry lists the projects you created, never ones other people in your organization shared with you.',
  priv_link='Read the privacy policy',
  faq_h='Questions',
  faq=[
   ('Is Ferry made by Anthropic?', 'No. Ferry is an independent tool. It is not made, endorsed or supported by Anthropic. Claude is a trademark of Anthropic.'),
   ('Is it free?', 'Yes. Ferry is free to install and use.'),
   ("Doesn't Claude already do this?", 'Only in one case: when you join a Team or Enterprise plan with the same email as your personal account, Claude can move that whole account into it. It cannot move between different emails, from a work account to a personal one, or between two personal accounts, and you cannot choose what moves. Ferry handles all of those.'),
   ('Which accounts does it work with?', 'Any claude.ai account you can log in to in Chrome. Ferry works on the claude.ai website, not inside the desktop or mobile apps.'),
   ('Does it move what Claude remembers?', 'Project memory comes as a CONTEXT.md file in the new project, so Claude can read it from the first chat. Account memory is optional and comes as an ABOUT-ME.md file.'),
   ('Why not bring every chat into the project?', 'Projects have a size limit and long chats fill it quickly. Ferry ticks the recommended items and shows the size before you import. Every chat stays saved in the ZIP file.'),
   ('Which browsers are supported?', 'Chrome. Other Chromium browsers such as Edge or Brave may work, but they are not tested yet.'),
   ('Will it keep working?', 'Ferry uses the same pages claude.ai uses. If claude.ai changes, a feature may stop working until Ferry is updated.'),
  ],
  nav_pro='Any AI', pro_tag='Coming next', pro_h='Ferry for every AI', pro_p='Move your chats, projects and memory between ChatGPT, Claude, Gemini and more. Tell us which move you need and we will email you when it is ready, with early access.',
  pro_label='Your email', pro_ph='you@example.com', pro_btn='Notify me', pro_note='One email when it is ready. Nothing else.',
  pro_from='I want to move from', pro_to='to', pro_other='Other',
  pro_ok="You're on the list. Thanks!", pro_err='That did not work. Check the email or write to support@getferry.net.',
  final_h='Ready to move your projects?', final_p='Install Ferry and bring your first project over in a couple of minutes.',
  foot='Ferry is an independent tool, not affiliated with Anthropic. Claude is a trademark of Anthropic.', foot_priv='Privacy policy',
 ),
 'es': dict(
  lang='es', base='../', other='../', other_lang='en', other_name='English', privacy='../privacy.html#es', canon='https://getferry.net/es/',
  title='Ferry: mueve proyectos, chats y memoria de Claude a otra cuenta',
  desc='Ferry es una extensión gratuita de Chrome que mueve tus proyectos, chats y memoria de Claude de una cuenta de claude.ai a otra. No afiliada a Anthropic.',
  skip='Ir al contenido', nav_how='Cómo funciona', nav_priv='Privacidad', nav_faq='Preguntas', add='Añadir a Chrome',
  chips=['Gratis', 'Sin registro', 'Funciona en tu navegador'],
  h1='Lleva tus proyectos de Claude a otra cuenta',
  lead='Proyectos, chats y memoria, entre dos cuentas de claude.ai cualesquiera, aunque tengan correos distintos. Personal, del trabajo o de la universidad. Tú eliges exactamente qué se lleva.',
  cta='Añadir a Chrome, es gratis', see='Mira cómo funciona',
  c1='Product launch ya está en tu cuenta del trabajo', c1s='Ahora mismo',
  c2='42 chats guardados, 12 traídos', c2s='El resto se queda en tu ZIP',
  c3='Memoria del proyecto añadida como CONTEXTO.md',
  legal='Herramienta independiente, no afiliada a Anthropic.',
  cmp_h='Deja de rehacer proyectos a mano', cmp_p='Claude solo une una cuenta personal a una de empresa si las dos usan el mismo correo, y entonces lo mueve todo. Cualquier otro cambio había que hacerlo pieza a pieza.',
  hand_h='A mano', hand=['Descargar los archivos uno a uno', 'Copiar y pegar las instrucciones', 'Crear el proyecto otra vez desde cero', 'Pegar los chats antiguos uno a uno', 'Perder lo que Claude recordaba'],
  ferry_h='Con Ferry', ferry=['Guardar el proyecto entero en un ZIP', 'Entrar en la otra cuenta', 'Traerlo con un clic', 'La memoria llega como CONTEXTO.md'],
  how_h='Tres pasos', how_p='Ferry se abre en un panel lateral junto a claude.ai, así que no sales de la página.',
  s1h='Llévatelo de la cuenta antigua', s1='Elige un proyecto o cualquier chat y guárdalo. Obtienes un único ZIP con todo dentro.',
  s1a='Product launch', s1b='Ayer', s1c='Thesis research', s1d='Hace 3 días', s1btn='Guardar "Product launch"',
  s2h='Cambia de cuenta', s2='Entra en claude.ai con la cuenta a la que quieres moverlo.',
  s2a='Personal', s2am='tu@gmail.com', s2b='Trabajo', s2bm='tu@empresa.com',
  s3h='Tráelo', s3='Abre Ferry otra vez, elige el archivo y marca qué incluir. Luego, un clic.',
  s3a='Instrucciones', s3b='Archivos', s3bn='6', s3c='Chats', s3cn='12 de 42', s3btn='Traer proyecto',
  what_h='Lo que viaja contigo', what_p='Ferry vuelve a crear el proyecto como proyecto privado en la cuenta nueva.',
  w1h='Proyectos', w1='Instrucciones, archivos de conocimiento, memoria del proyecto y sus chats.',
  w2h='Chats sueltos', w2='Busca cualquier chat, esté o no en un proyecto, y síguelo en la otra cuenta con su título original.',
  w3h='Memoria de la cuenta', w3tag='Opcional', w3='Lo que Claude recuerda de ti. Viene desmarcada, para que tus datos personales no acaben en la cuenta del trabajo.',
  priv_h='Sin servidores de por medio', priv_p='Ferry funciona en tu navegador. Tus datos van de claude.ai a tu ordenador y de vuelta, y a ningún otro sitio.',
  p1h='Sin registrarte', p1='Ferry usa la sesión de claude.ai que ya tienes. No existe una cuenta de Ferry.',
  p2h='Sin seguimiento', p2='Sin analíticas ni anuncios. Tus datos nunca se venden ni se comparten.',
  p3h='Solo tus proyectos', p3='Ferry muestra los proyectos que creaste tú, nunca los que otras personas de tu organización comparten contigo.',
  priv_link='Leer la política de privacidad',
  faq_h='Preguntas',
  faq=[
   ('¿Ferry es de Anthropic?', 'No. Ferry es una herramienta independiente. No está hecha, respaldada ni soportada por Anthropic. Claude es una marca de Anthropic.'),
   ('¿Es gratis?', 'Sí. Ferry es gratis de instalar y de usar.'),
   ('¿Claude no hace ya esto?', 'Solo en un caso: si te unes a un plan Team o Enterprise con el mismo correo que tu cuenta personal, Claude puede mover esa cuenta entera allí. No puede mover entre correos distintos, de una cuenta del trabajo a una personal ni entre dos cuentas personales, y no te deja elegir qué se mueve. Ferry hace todo eso.'),
   ('¿Con qué cuentas funciona?', 'Con cualquier cuenta de claude.ai en la que puedas entrar desde Chrome. Ferry funciona en la web de claude.ai, no dentro de las apps de escritorio o móvil.'),
   ('¿Se lleva lo que Claude recuerda?', 'La memoria del proyecto llega como un archivo CONTEXTO.md en el proyecto nuevo, así Claude la puede leer desde el primer chat. La memoria de la cuenta es opcional y llega como un archivo SOBRE-MI.md.'),
   ('¿Por qué no traer todos los chats al proyecto?', 'Los proyectos tienen un límite de tamaño y los chats largos lo llenan rápido. Ferry marca lo recomendado y te enseña el tamaño antes de importar. Todos los chats quedan guardados en el ZIP.'),
   ('¿Qué navegadores funcionan?', 'Chrome. Otros navegadores basados en Chromium, como Edge o Brave, pueden funcionar, pero aún no están probados.'),
   ('¿Seguirá funcionando?', 'Ferry usa las mismas páginas que usa claude.ai. Si claude.ai cambia, alguna función puede dejar de ir hasta que Ferry se actualice.'),
  ],
  nav_pro='Cualquier IA', pro_tag='Próximamente', pro_h='Ferry para cualquier IA', pro_p='Mueve tus chats, proyectos y memoria entre ChatGPT, Claude, Gemini y más. Dinos qué cambio necesitas y te escribiremos cuando esté listo, con acceso anticipado.',
  pro_label='Tu correo', pro_ph='tu@ejemplo.com', pro_btn='Avisarme', pro_note='Un único correo cuando esté listo. Nada más.',
  pro_from='Quiero pasar de', pro_to='a', pro_other='Otra',
  pro_ok='¡Ya estás en la lista! Gracias.', pro_err='No ha funcionado. Revisa el correo o escribe a support@getferry.net.',
  final_h='¿Listo para mover tus proyectos?', final_p='Instala Ferry y trae tu primer proyecto en un par de minutos.',
  foot='Ferry es una herramienta independiente, no afiliada a Anthropic. Claude es una marca de Anthropic.', foot_priv='Política de privacidad',
 ),
}

def palabras(texto):
    return ' '.join(f'<span class="palabra" style="--i:{i}">{w}</span>' for i, w in enumerate(texto.split()))

IAS = ['ChatGPT', 'Claude', 'Gemini', 'Copilot', 'Perplexity', 'Grok', 'DeepSeek']

def opciones(t, elegida):
    ops = [f'<option{" selected" if ia == elegida else ""}>{ia}</option>' for ia in IAS]
    ops.append(f'<option value="Other">{t["pro_other"]}</option>')
    return ''.join(ops)

def h2(id_, texto):
    return f'<h2 id="{id_}" data-aparece>{palabras(texto)}</h2>'

def page(t):
    b = t['base']
    ok_verde = svg(OK, '#16803C', '2.4')
    chips = ''.join(f'<span>{ok_verde}{c}</span>' for c in t['chips'])
    mano = ''.join(f'<li>{svg(NO, "#8A9398", "2")}{x}</li>' for x in t['hand'])
    ferry = ''.join(f'<li>{svg(OK, "#16803C", "2.2")}{x}</li>' for x in t['ferry'])
    check = f'<span class="check">{svg(OK, "#FFFFFF", "3.2")}</span>'
    faq = '\n'.join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    return f'''<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="{t['canon']}">
<link rel="alternate" hreflang="en" href="https://getferry.net/">
<link rel="alternate" hreflang="es" href="https://getferry.net/es/">
<link rel="alternate" hreflang="x-default" href="https://getferry.net/">
<meta property="og:type" content="website">
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{t['desc']}">
<meta property="og:image" content="https://getferry.net/img/og.png">
<meta property="og:url" content="{t['canon']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F3F4F5">
<link rel="icon" href="{b}icon.png">
<link rel="preload" href="{b}fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{b}site.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<a class="saltar" href="#contenido">{t['skip']}</a>

<main>
<div class="portada">
  <div class="marco">
    <div class="anillo anillo-1" aria-hidden="true"></div>
    <div class="anillo anillo-2" aria-hidden="true"></div>
    <div class="anillo anillo-3" aria-hidden="true"></div>
    <div class="brillo" aria-hidden="true"></div>
    <div class="orbita o1" aria-hidden="true">{svg(CARPETA)}</div>
    <div class="orbita o2" aria-hidden="true">{svg(CHAT)}</div>
    <div class="orbita o3" aria-hidden="true">{svg(DOC)}</div>
    <div class="orbita o4" aria-hidden="true">{svg(ESTRELLA)}</div>
    <div class="orbita o5" aria-hidden="true">{svg(ZIP)}</div>
    <div class="orbita o6 acento" aria-hidden="true">{svg(BARCO, '#0F1417', '1.9')}</div>

    <header class="barra">
      <nav aria-label="{'Principal' if t['lang'] == 'es' else 'Main'}">
        <a class="marca" href="./"><span>{svg(BARCO, '#F6C90E', '2')}</span>Ferry</a>
        <a class="ancla" href="#how">{t['nav_how']}</a>
        <a class="ancla" href="#privacy">{t['nav_priv']}</a>
        <a class="ancla" href="#faq">{t['nav_faq']}</a>
        <a class="ancla" href="#pro">{t['nav_pro']}</a>
        <a class="idioma" href="{t['other']}" lang="{t['other_lang']}" hreflang="{t['other_lang']}">{t['other_name']}</a>
        <a class="boton boton-oscuro boton-pequeno" href="{STORE}">{t['add']}</a>
      </nav>
    </header>

    <div class="centro" id="contenido">
      <div class="chips">{chips}</div>
      <h1>{palabras(t['h1'])}</h1>
      <p class="entrada">{t['lead']}</p>
      <div class="acciones">
        <a class="boton boton-oscuro" href="{STORE}">{t['cta']}</a>
        <a class="boton boton-claro" href="#how">{t['see']}</a>
      </div>
      <div class="pila" aria-hidden="true">
        <div class="aviso-tarjeta t1"><span class="icono">{svg(BARCO, '#0F1417', '1.9')}</span><span><strong>{t['c1']}</strong><small>{t['c1s']}</small></span></div>
        <div class="aviso-tarjeta t2"><span class="icono">{svg(CHAT)}</span><span><strong>{t['c2']}</strong><small>{t['c2s']}</small></span></div>
        <div class="aviso-tarjeta t3"><span class="icono">{svg(DOC)}</span><span><strong>{t['c3']}</strong></span></div>
      </div>
      <p class="legal">{t['legal']}</p>
    </div>
  </div>
</div>

<div class="envoltura">
  <section class="seccion" aria-labelledby="cmp-h">
    <div class="cabeza">{h2('cmp-h', t['cmp_h'])}<p data-aparece style="--retraso:.2s">{t['cmp_p']}</p></div>
    <div class="comparar">
      <div class="lado a-mano" data-aparece><h3>{t['hand_h']}</h3><ul>{mano}</ul></div>
      <div class="lado con-ferry" data-aparece style="--retraso:.15s"><h3>{t['ferry_h']}</h3><ul>{ferry}</ul></div>
    </div>
  </section>

  <section class="seccion" id="how" aria-labelledby="how-h">
    <div class="pasos-banda">
      <div class="cabeza">{h2('how-h', t['how_h'])}<p data-aparece style="--retraso:.2s">{t['how_p']}</p></div>
      <ol class="pasos">
        <li class="paso" data-aparece><h3>{t['s1h']}</h3><p>{t['s1']}</p>
          <div class="mini" aria-hidden="true">
            <div class="mini-fila"><span class="radio"></span><b>{t['s1a']}</b><small>{t['s1b']}</small></div>
            <div class="mini-fila"><span class="radio" style="border:1.5px solid #9AA3A8"></span>{t['s1c']}<small>{t['s1d']}</small></div>
            <div class="mini-boton">{t['s1btn']}</div>
          </div></li>
        <li class="paso" data-aparece style="--retraso:.12s"><h3>{t['s2h']}</h3><p>{t['s2']}</p>
          <div class="mini" aria-hidden="true">
            <div class="cuentas">
              <div class="cuenta"><b>{t['s2a']}</b><small>{t['s2am']}</small></div>
              {svg(FLECHA, '#0F1417', '2')}
              <div class="cuenta destino"><b>{t['s2b']}</b><small>{t['s2bm']}</small></div>
            </div>
          </div></li>
        <li class="paso" data-aparece style="--retraso:.24s"><h3>{t['s3h']}</h3><p>{t['s3']}</p>
          <div class="mini" aria-hidden="true">
            <div class="mini-fila">{check}{t['s3a']}</div>
            <div class="mini-fila">{check}{t['s3b']}<small>{t['s3bn']}</small></div>
            <div class="mini-fila">{check}{t['s3c']}<small>{t['s3cn']}</small></div>
            <div class="mini-boton">{t['s3btn']}</div>
          </div></li>
      </ol>
    </div>
  </section>

  <section class="seccion" aria-labelledby="what-h">
    <div class="cabeza">{h2('what-h', t['what_h'])}<p data-aparece style="--retraso:.2s">{t['what_p']}</p></div>
    <div class="carga">
      <article data-aparece><div class="icono">{svg(CARPETA)}</div><h3>{t['w1h']}</h3><p>{t['w1']}</p></article>
      <article data-aparece style="--retraso:.12s"><div class="icono">{svg(CHAT)}</div><h3>{t['w2h']}</h3><p>{t['w2']}</p></article>
      <article data-aparece style="--retraso:.24s"><div class="icono">{svg(PERSONA)}</div><h3>{t['w3h']} <em>{t['w3tag']}</em></h3><p>{t['w3']}</p></article>
    </div>
  </section>

  <section class="seccion" id="privacy" aria-labelledby="priv-h">
    <div class="privada">
      <div class="cabeza">{h2('priv-h', t['priv_h'])}<p data-aparece style="--retraso:.2s">{t['priv_p']}</p></div>
      <div class="privada-grid">
        <div data-aparece>{svg(LLAVE)}<h3>{t['p1h']}</h3><p>{t['p1']}</p></div>
        <div data-aparece style="--retraso:.12s">{svg(OJO_NO)}<h3>{t['p2h']}</h3><p>{t['p2']}</p></div>
        <div data-aparece style="--retraso:.24s">{svg(ESCUDO)}<h3>{t['p3h']}</h3><p>{t['p3']}</p></div>
      </div>
      <a class="enlace" href="{t['privacy']}">{t['priv_link']}</a>
    </div>
  </section>

  <section class="seccion" id="faq" aria-labelledby="faq-h">
    <div class="cabeza">{h2('faq-h', t['faq_h'])}</div>
    <div class="preguntas" data-aparece style="--retraso:.1s">
{faq}
    </div>
  </section>

  <section class="seccion" id="pro" aria-labelledby="pro-h">
    <div class="pro" data-aparece>
      <div class="pro-texto">
        <span class="pro-marca">{svg(ESTRELLA, '#0F1417', '2')}{t['pro_tag']}</span>
        {h2('pro-h', t['pro_h'])}
        <p>{t['pro_p']}</p>
      </div>
      <form class="pro-form" id="lista" novalidate>
        <div class="pro-ias">
          <label for="pro-desde">{t['pro_from']}</label>
          <select id="pro-desde" name="desde">{opciones(t, 'ChatGPT')}</select>
          <label for="pro-hacia">{t['pro_to']}</label>
          <select id="pro-hacia" name="hacia">{opciones(t, 'Claude')}</select>
        </div>
        <label for="pro-email">{t['pro_label']}</label>
        <div class="pro-fila">
          <input id="pro-email" name="email" type="email" autocomplete="email" required placeholder="{t['pro_ph']}">
          <button class="boton boton-oscuro" type="submit">{t['pro_btn']}</button>
        </div>
        <input class="trampa" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
        <p class="pro-nota" id="pro-estado" role="status" data-ok="{t['pro_ok']}" data-err="{t['pro_err']}">{t['pro_note']}</p>
      </form>
    </div>
  </section>

  <section class="final" aria-labelledby="final-h">
    <div>{h2('final-h', t['final_h'])}<p data-aparece style="--retraso:.25s">{t['final_p']}</p></div>
    <a class="boton boton-amarillo" href="{STORE}" data-aparece style="--retraso:.35s">{t['cta']}</a>
  </section>
</div>
</main>

<footer class="pie">
  <div class="envoltura">
    <p class="aviso">{t['foot']}</p>
    <a href="{t['privacy']}">{t['foot_priv']}</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <a href="{t['other']}" lang="{t['other_lang']}" hreflang="{t['other_lang']}">{t['other_name']}</a>
  </div>
</footer>
<script>
(function () {{
  var els = document.querySelectorAll('[data-aparece]');
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {{
    els.forEach(function (e) {{ e.classList.add('visible'); }});
    return;
  }}
  var io = new IntersectionObserver(function (entradas) {{
    entradas.forEach(function (e) {{
      if (e.isIntersecting) {{ e.target.classList.add('visible'); io.unobserve(e.target); }}
    }});
  }}, {{ threshold: 0.15, rootMargin: '0px 0px -40px 0px' }});
  els.forEach(function (e) {{ io.observe(e); }});
}})();
(function () {{
  var form = document.getElementById('lista');
  if (!form) return;
  var estado = document.getElementById('pro-estado');
  var boton = form.querySelector('button');
  form.addEventListener('submit', function (ev) {{
    ev.preventDefault();
    var email = form.email.value.trim();
    if (!form.email.checkValidity() || !email) {{ estado.textContent = estado.dataset.err; estado.className = 'pro-nota mal'; form.email.focus(); return; }}
    boton.disabled = true;
    fetch('/api/waitlist', {{ method: 'POST', headers: {{ 'content-type': 'application/json' }},
      body: JSON.stringify({{ email: email, desde: form.desde.value, hacia: form.hacia.value, lang: document.documentElement.lang, website: form.website.value }}) }})
      .then(function (r) {{ return r.json().then(function (d) {{ if (!r.ok || !d.ok) throw new Error('x'); }}); }})
      .then(function () {{ estado.textContent = estado.dataset.ok; estado.className = 'pro-nota bien'; form.reset(); }})
      .catch(function () {{ estado.textContent = estado.dataset.err; estado.className = 'pro-nota mal'; }})
      .then(function () {{ boton.disabled = false; }});
  }});
}})();
</script>
</body>
</html>
'''

here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(here, 'es'), exist_ok=True)
open(os.path.join(here, 'index.html'), 'w', encoding='utf-8').write(page(T['en']))
open(os.path.join(here, 'es', 'index.html'), 'w', encoding='utf-8').write(page(T['es']))
print('ok')
