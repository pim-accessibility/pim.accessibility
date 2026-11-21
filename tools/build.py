#!/usr/bin/env python3
"""Generates index.html (EN) and pt/index.html (pt-PT) from one template so both stay in sync."""
import html, pathlib, sys

REPO = pathlib.Path(sys.argv[1])
SITE = "https://pim-accessibility.github.io/pim.accessibility/"

T = {
 "en": dict(
  lang="en", base="", other_href="pt/", self_url=SITE, other_url=SITE + "pt/",
  title="Patrícia Magrinho — UX & Accessibility Specialist",
  desc="Patrícia Magrinho, UX and accessibility specialist in Lisbon. Accessible digital services, WCAG audits and research with people with disabilities.",
  skip="Skip to main content",
  anno_on="You are viewing accessibility annotations.",
  anno_off="Accessibility annotations are hidden.",
  hide="Hide", show="Show", anno_rest=" accessibility annotations",
  logo="Patrícia’s portfolio — home",
  nav_label="Main", lang_label="Language",
  nav=[("#about","About"),("#experience","Experience"),("resume.html","Résumé"),("#contact","Contact")],
  role="UX & Accessibility Specialist · Lisbon, Portugal",
  langs="Works in English, Portuguese and Spanish",
  bio="I make websites and apps that everyone can use, including people with disabilities. I check products against accessibility standards and design components that work for everyone.",
  cta="View my résumé",
  about_h="About",
  about="I help product teams build digital services that are accessible, meet the law and really work for people. That includes people with disabilities, cognitive differences or temporary limitations.",
  work_h="What I work on",
  work=[("i-eye","Designing accessible digital services"),("i-check-sq","Accessibility audits (WCAG 2.1 and 2.2)"),("i-person","Research sessions with people with disabilities"),("i-grid","Accessible design-system components")],
  statement="Good accessibility is good design. It is a practice, not a checklist.",
  exp_h="Experience",
  jobs=[
   ("2021 – present","UX & Accessibility Specialist","Agência para a Modernização Administrativa (AMA), via Tangível",["Accessibility across the whole product lifecycle","Audits and fixes (WCAG 2.1 and 2.2)","Research with people with disabilities"]),
   ("2019 – 2021","UX Designer","Instituto da Segurança Social",["User flows, information architecture, wireframes and prototypes","Usability tests and concept validation"]),
   ("2014","Design degree","Escola Superior de Artes e Design (ESAD), Caldas da Rainha",["Bachelor’s degree in Design"]),
  ],
  talk_h="Let’s talk", talk_lead="Email is the quickest way to reach me.",
  theme="Theme", light="Light", dark="Dark", top="Back to top",
  # annotation labels (visual only)
  a_skip="Skip link", a_btn="Button · label changes", a_logo="Link · aria-label",
  a_nav="<nav> · <ul> · 4 links", a_lang="lang · hreflang", a_link="Link",
  a_dec="Decorative · alt=\"\"", a_ul="<ul> · 4 items", a_ol="<ol> · 3 items",
  a_contact="Links · icon + text", a_radio="Radio group · <fieldset>",
 ),
 "pt": dict(
  lang="pt-PT", base="../", other_href="../", self_url=SITE + "pt/", other_url=SITE,
  title="Patrícia Magrinho — Especialista em UX e Acessibilidade",
  desc="Patrícia Magrinho, especialista em UX e acessibilidade em Lisboa. Serviços digitais acessíveis, auditorias WCAG e investigação com pessoas com deficiência.",
  skip="Saltar para o conteúdo principal",
  anno_on="Está a ver as anotações de acessibilidade.",
  anno_off="As anotações de acessibilidade estão ocultas.",
  hide="Ocultar", show="Mostrar", anno_rest=" anotações de acessibilidade",
  logo="Portfólio da Patrícia — página inicial",
  nav_label="Principal", lang_label="Idioma",
  nav=[("#about","Sobre mim"),("#experience","Experiência"),("../resume.html","Currículo"),("#contact","Contacto")],
  role="Especialista em UX e Acessibilidade · Lisboa, Portugal",
  langs="Trabalha em português, inglês e espanhol",
  bio="Crio sites e aplicações que todas as pessoas conseguem usar, incluindo pessoas com deficiência. Avalio produtos segundo as normas de acessibilidade e desenho componentes que funcionam para todos.",
  cta="Ver o meu currículo",
  about_h="Sobre mim",
  about="Ajudo equipas de produto a criar serviços digitais acessíveis, que cumprem a lei e funcionam mesmo para as pessoas. Isso inclui pessoas com deficiência, diferenças cognitivas ou limitações temporárias.",
  work_h="Em que trabalho",
  work=[("i-eye","Desenho de serviços digitais acessíveis"),("i-check-sq","Auditorias de acessibilidade (WCAG 2.1 e 2.2)"),("i-person","Sessões de investigação com pessoas com deficiência"),("i-grid","Componentes acessíveis para design systems")],
  statement="Boa acessibilidade é bom design. É uma prática, não uma lista de verificação.",
  exp_h="Experiência",
  jobs=[
   ("2021 – presente","Especialista em UX e Acessibilidade","Agência para a Modernização Administrativa (AMA), via Tangível",["Acessibilidade em todo o ciclo de vida do produto","Auditorias e correções (WCAG 2.1 e 2.2)","Investigação com pessoas com deficiência"]),
   ("2019 – 2021","UX Designer","Instituto da Segurança Social",["Fluxos de utilização, arquitetura de informação, wireframes e protótipos","Testes de usabilidade e validação de conceitos"]),
   ("2014","Formação em Design","Escola Superior de Artes e Design (ESAD), Caldas da Rainha",["Licenciatura em Design"]),
  ],
  talk_h="Vamos conversar", talk_lead="O email é a forma mais rápida de me contactar.",
  theme="Tema", light="Claro", dark="Escuro", top="Voltar ao topo",
  a_skip="Link de salto", a_btn="Botão · o texto muda", a_logo="Ligação · aria-label",
  a_nav="<nav> · <ul> · 4 ligações", a_lang="lang · hreflang", a_link="Ligação",
  a_dec="Decorativo · alt=\"\"", a_ul="<ul> · 4 itens", a_ol="<ol> · 3 itens",
  a_contact="Ligações · ícone + texto", a_radio="Grupo de opções · <fieldset>",
 ),
}

def e(s):  # escape text and attribute values
    return html.escape(s, quote=True)

def ann(text, t, pos=None, sm=None):
    a = f' data-a11y="{e(text)}" data-a11y-t="{t}"'
    if pos: a += f' data-a11y-pos="{pos}"'
    if sm is not None: a += f' data-a11y-sm="{e(sm)}"'
    return a

HEAD_JS = ("(function(){var d=document.documentElement;d.classList.add('js');"
  "function g(k){try{return localStorage.getItem(k)}catch(e){return null}}"
  "var m=window.matchMedia||function(){return{matches:false}};"
  "var t=g('pim-theme');if(t!=='light'&&t!=='dark')t=m('(prefers-color-scheme: dark)').matches?'dark':'light';"
  "d.setAttribute('data-theme',t);"
  "var a=g('pim-annotations');if(a?a==='on':m('(min-width: 80em)').matches)d.classList.add('anno-on');})();")

def page(k):
    c = T[k]; b = c["base"]; en = k == "en"
    icon = lambda cls, extra="": f'<span class="icon {cls}"{extra} aria-hidden="true"></span>'
    nav = "\n".join(f'          <li><a href="{e(h)}"' + (' hreflang="pt-PT"' if en and h.endswith("resume.html") else "") + f'>{e(t)}</a></li>' for h, t in c["nav"])
    if en:
        langs = ('          <li><a href="./" hreflang="en" lang="en" aria-current="page">English</a></li>\n'
                 '          <li><a href="pt/" hreflang="pt-PT" lang="pt-PT">Português</a></li>')
    else:
        langs = ('          <li><a href="../" hreflang="en" lang="en">English</a></li>\n'
                 '          <li><a href="./" hreflang="pt-PT" lang="pt-PT" aria-current="page">Português</a></li>')
    work = "\n".join(f'          <li><span class="work-ico">{icon(i)}</span>{e(t)}</li>' for i, t in c["work"])
    jobs = []
    for y, r, o, bl in c["jobs"]:
        items = "".join(f"<li>{e(x)}</li>" for x in bl)
        jobs.append(f'''        <li>
          <p class="year">{e(y)}</p>
          <div class="job">
            <h3>{e(r)}</h3>
            <p class="org">{e(o)}</p>
            <ul>{items}</ul>
          </div>
        </li>''')
    jobs = "\n".join(jobs)
    return f'''<!DOCTYPE html>
<html lang="{c["lang"]}" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(c["title"])}</title>
  <meta name="description" content="{e(c["desc"])}">
  <meta name="color-scheme" content="light dark">
  <link rel="canonical" href="{c["self_url"]}">
  <link rel="alternate" hreflang="en" href="{SITE}">
  <link rel="alternate" hreflang="pt-PT" href="{SITE}pt/">
  <link rel="alternate" hreflang="x-default" href="{SITE}">
  <link rel="icon" href="{b}favicon.ico">
  <link rel="preload" href="{b}assets/fonts/atkinson-hyperlegible-next-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{b}assets/fonts/atkinson-hyperlegible-next-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
  <script>{HEAD_JS}</script>
  <link rel="stylesheet" href="{b}css/site.css">
  <script src="{b}js/site.js" defer></script>
</head>
<body>
  <div class="skip-bar on-ink" id="top">
    <a href="#main" class="anno-skip"{ann(c["a_skip"], "note")}>{e(c["skip"])}</a>
  </div>

  <div class="anno-row wrap">
    <div class="anno-pill">
      <p class="anno-msg"{ann('role="status"', "note", sm="-")}>{icon("i-info")}<span id="anno-status" role="status" data-on="{e(c["anno_on"])}" data-off="{e(c["anno_off"])}">{e(c["anno_on"])}</span></p>
      <button type="button" class="anno-btn" id="anno-toggle" data-hide="{e(c["hide"])}" data-show="{e(c["show"])}"{ann(c["a_btn"], "button", "end", "-")}>{icon("i-eye-off")}{icon("i-eye")}<span><span class="anno-verb">{e(c["hide"])}</span><span class="anno-rest">{e(c["anno_rest"])}</span></span></button>
    </div>
  </div>

  <header class="site-header wrap"{ann("<header>", "landmark", "bleed")}>
    <a class="logo" href="./" aria-label="{e(c["logo"])}"{ann(c["a_logo"], "link", sm="-")}><span class="logo-badge"><img src="{b}assets/icons/fingerprint.svg" width="32" height="32" alt=""></span></a>
    <div class="header-navs">
      <nav aria-label="{e(c["nav_label"])}"{ann(c["a_nav"], "landmark", "top")}>
        <ul class="nav-list">
{nav}
        </ul>
      </nav>
      <span class="header-sep" aria-hidden="true"></span>
      <nav aria-label="{e(c["lang_label"])}"{ann(c["a_lang"], "link", "top", "-")}>
        <ul class="lang-list">
{langs}
        </ul>
      </nav>
    </div>
  </header>

  <main id="main" tabindex="-1"{ann("<main>", "landmark", "bleed", "-")}>
    <div class="hero wrap">
      <div class="hero-intro">
        <h1{ann("h1", "heading")}>Patrícia Magrinho</h1>
        <p class="role">{e(c["role"])}</p>
        <p class="langs">{e(c["langs"])}</p>
        <p class="bio">{e(c["bio"])}</p>
      </div>
      <div class="cta-area"{ann(c["a_link"], "link", "top")}>
        <a class="cta"{' hreflang="pt-PT"' if en else ''} href="{b}resume.html">{e(c["cta"])}{icon("i-arrow")}</a>
        <span class="cta-cursor"{ann(c["a_dec"], "image", "end", "-")}><img src="{b}assets/icons/cursor.svg" width="40" height="44" alt=""></span>
      </div>
    </div>

    <div class="cards wrap">
      <section class="card card-about on-accent" aria-labelledby="about">
        <h2 id="about"{ann("h2", "heading", "top")}>{e(c["about_h"])}</h2>
        <p>{e(c["about"])}</p>
        {icon("i-fingerprint about-mark")}
      </section>
      <section class="card card-work on-ink" aria-labelledby="work">
        <h2 id="work"{ann("h2", "heading", "top")}>{e(c["work_h"])}</h2>
        <ul class="work-list"{ann(c["a_ul"], "list", "top-end")}>
{work}
        </ul>
      </section>
    </div>

    <div class="statement on-ink">
      <p class="wrap">{e(c["statement"])}</p>
    </div>

    <section class="experience wrap" aria-labelledby="experience">
      <h2 id="experience"{ann("h2", "heading")}>{e(c["exp_h"])}</h2>
      <ol class="timeline"{ann(c["a_ol"], "list")}>
{jobs}
      </ol>
    </section>

    <section class="contact wrap on-accent" aria-labelledby="contact">
      <h2 id="contact"{ann("h2", "heading")}>{e(c["talk_h"])}</h2>
      <p class="lead">{e(c["talk_lead"])}</p>
      <ul class="contact-links"{ann(c["a_contact"], "link")}>
        <li><a href="mailto:pim.uxdesigner@gmail.com">{icon("i-mail")}pim.uxdesigner@gmail.com</a></li>
        <li><a href="https://www.linkedin.com/in/pimagrinho/" lang="en">{icon("i-linkedin")}linkedin.com/in/pimagrinho</a></li>
      </ul>
    </section>
  </main>

  <footer class="site-footer wrap"{ann("<footer>", "landmark", "bleed")}>
    <p class="copy">© 2026 Patrícia Magrinho</p>
    <div class="footer-tools">
      <fieldset class="theme"{ann(c["a_radio"], "button", "top")}>
        <legend>{e(c["theme"])}</legend>
        <div class="theme-options">
          <label class="theme-opt"><input type="radio" name="theme" value="light">{icon("i-check")}{icon("i-sun")}{e(c["light"])}</label>
          <label class="theme-opt"><input type="radio" name="theme" value="dark">{icon("i-check")}{icon("i-moon")}{e(c["dark"])}</label>
        </div>
      </fieldset>
      <a class="to-top" href="#top"{ann(c["a_link"], "link", "top-end", "-")}>{e(c["top"])}{icon("i-up")}</a>
    </div>
  </footer>
</body>
</html>
'''

(REPO / "index.html").write_text(page("en"), encoding="utf-8")
(REPO / "pt").mkdir(exist_ok=True)
(REPO / "pt" / "index.html").write_text(page("pt"), encoding="utf-8")
print("ok")
