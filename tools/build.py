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
  nav=[("#about","Sobre mim"),("#experience","Experiência"),("resume.html","Currículo"),("#contact","Contacto")],
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

def ann(*args, **kw):
    """Annotations are now drawn by js/annotations.js from ANNO_SPEC (see below)."""
    return ""

HEAD_JS = ("(function(){var d=document.documentElement;d.classList.add('js');"
  "function g(k){try{return localStorage.getItem(k)}catch(e){return null}}"
  "var m=window.matchMedia||function(){return{matches:false}};"
  "var t=g('pim-theme');if(t!=='light'&&t!=='dark')t=m('(prefers-color-scheme: dark)').matches?'dark':'light';"
  "d.setAttribute('data-theme',t);"
  "var a=g('pim-annotations');if(a?a==='on':m('(min-width: 80em)').matches)d.classList.add('anno-on');})();")


# ---------------------------------------------------------------------------
# Résumé content (from the previous résumé page, rewritten for v2.2).
# The phone number is intentionally not published: the v2.2 design offers email + LinkedIn only.
R = {
 "en": dict(
  title="Résumé — Patrícia Magrinho",
  desc="Résumé of Patrícia Magrinho, UX and accessibility specialist in Lisbon.",
  h1="Résumé",
  intro="Hi, I’m Patrícia, a UX and accessibility specialist at Tangível. I work with teams to make sure digital products and services are accessible, inclusive and compliant.",
  contact_h="Contact", loc_l="Location", loc="Lisbon, Portugal", email_l="Email", li_l="LinkedIn",
  focus_h="Current focus", focus=["Designing accessible digital services", "Accessibility audits (WCAG 2.1 and 2.2)"],
  exp_h="Experience",
  jobs=[
   ("May 2021 – present", "UX & Accessibility Specialist", "Agência para a Modernização Administrativa (AMA), via Tangível · Lisbon",
    ["Bring accessibility into every stage of the product lifecycle", "Accessibility audits and remediation advice (WCAG 2.1 and 2.2)", "Research sessions with people with disabilities", "Accessible, scalable components for design systems"]),
   ("Feb 2019 – Mar 2021", "UX Designer", "Instituto da Segurança Social · Lisbon",
    ["User flows, information architecture, wireframes and prototypes", "Close work with development teams", "Usability tests and concept validation"]),
  ],
  edu_h="Education and credentials",
  edu=[("Auditing Design Systems for Accessibility", "LinkedIn Learning · Feb 2023"), ("UXPM (Level 1)", "UXC · Jul 2023"), ("Design degree", "Escola Superior de Artes e Design (ESAD), Caldas da Rainha · 2014")],
  skills_h="Skills",
  skills=[("Research", ["Surveys and competitive analysis", "Information architecture", "Quantitative and qualitative research and testing"]),
          ("Design", ["UI design, wireframing and prototyping", "Accessible components"]),
          ("Tools", ["Figma, Adobe Creative Cloud, Jira", "Hotjar, Treejack, VS Code"])],
  back="Back to the home page",
 ),
 "pt": dict(
  title="Currículo — Patrícia Magrinho",
  desc="Currículo de Patrícia Magrinho, especialista em UX e acessibilidade em Lisboa.",
  h1="Currículo",
  intro="Olá, sou a Patrícia, especialista em UX e Acessibilidade na Tangível. Trabalho com equipas para garantir que produtos e serviços digitais são acessíveis, inclusivos e conformes.",
  contact_h="Contacto", loc_l="Localização", loc="Lisboa, Portugal", email_l="Email", li_l="LinkedIn",
  focus_h="Foco atual", focus=["Desenho de serviços digitais acessíveis", "Auditorias de acessibilidade (WCAG 2.1 e 2.2)"],
  exp_h="Experiência",
  jobs=[
   ("Maio 2021 – presente", "Especialista em UX e Acessibilidade", "Agência para a Modernização Administrativa (AMA), via Tangível · Lisboa",
    ["Integrar a acessibilidade ao longo do ciclo de vida do produto", "Auditorias e recomendações de correção (WCAG 2.1 e 2.2)", "Sessões com pessoas com deficiência", "Componentes acessíveis e escaláveis para design systems"]),
   ("Fev. 2019 – Mar. 2021", "UX Designer", "Instituto da Segurança Social · Lisboa",
    ["Fluxos, arquitetura de informação, wireframes e protótipos", "Trabalho próximo com as equipas de desenvolvimento", "Testes de usabilidade e validação de conceitos"]),
  ],
  edu_h="Formação e certificações",
  edu=[("Auditing Design Systems for Accessibility", "LinkedIn Learning · Fev. 2023"), ("UXPM (Nível 1)", "UXC · Jul. 2023"), ("Licenciatura em Design", "Escola Superior de Artes e Design (ESAD), Caldas da Rainha · 2014")],
  skills_h="Competências",
  skills=[("Investigação", ["Inquéritos e análise competitiva", "Arquitetura de informação", "Investigação e testes quantitativos e qualitativos"]),
          ("Design", ["UI design, wireframes e prototipagem", "Componentes acessíveis"]),
          ("Ferramentas", ["Figma, Adobe Creative Cloud, Jira", "Hotjar, Treejack, VS Code"])],
  back="Voltar à página inicial",
 ),
}


# ---------------------------------------------------------------------------
# Accessibility annotations — positions reproduce the Figma layer 60:1290 (desktop)
# and frame 57:1576 (mobile). Selectors that do not exist on a page are skipped,
# so one spec serves the home page and the résumé.
import json
AL = {
 "en": dict(skip="Skip link", btn="Button · label changes", link="Link", lang="lang · hreflang",
            logo="Link · aria-label", dec="Decorative", contact="Link · icon + text",
            radio="Radio group", links4="Link ×4"),
 "pt": dict(skip="Link de salto", btn="Botão · o texto muda", link="Ligação", lang="lang · hreflang",
            logo="Ligação · aria-label", dec="Decorativo", contact="Ligação · ícone + texto",
            radio="Grupo de opções", links4="Ligação ×4"),
}
def anno_spec(k):
    L = AL[k]
    d = [
      dict(m="bracket", sel=".skip-bar", l=L["skip"], t="note", it=6, ib=6),
      dict(m="left", sel=".anno-pill", l='role="status"', t="note", dx=4),
      dict(m="right", sel=".anno-btn", l=L["btn"], t="button"),
      dict(m="hb-top", sel=".nav-list", l="<nav>", t="landmark"),
      dict(m="top", sel=".nav-list li:nth-child(1) a", l=L["link"], t="link"),
      dict(m="top", sel=".nav-list li:nth-child(3) a", l=L["link"], t="link"),
      dict(m="top", sel=".lang-list li:nth-child(2) a", l=L["lang"], t="link"),
      dict(m="bracket", sel=".site-header", l="<header>", t="landmark", tsel=".logo", toff=-16, ib=8, stub=70),
      dict(m="hb-bottom", sel=".nav-list", l="<ul>", t="list"),
      dict(m="left", sel=".logo-badge", l=L["logo"], t="link", dx=4),
      dict(m="left", sel="main h1", l="h1", t="heading", y="line"),
      dict(m="right", sel=".cta", l=L["link"], t="link"),
      dict(m="dot", sel=".cta-cursor", t="image", fx=34, fy=36),
      dict(m="bracket", sel="main", l="<main>", t="landmark", it=4, ib=4, ssel="main h1"),
      dict(m="left", sel="#about, #r-contact", l="h2", t="heading", y="line"),
      dict(m="near-left", sel=".about-mark", l=L["dec"], t="image"),
      dict(m="right", sel="#work, #r-focus", l="h2", t="heading", y="line"),
      dict(m="right", sel=".work-list", l="<ul>", t="list"),
      dict(m="left", sel="#experience, #r-exp", l="h2", t="heading", y="line"),
      dict(m="left", sel=".timeline", l="<ol>", t="list", dx=4, ysel=".year", y="line"),
      dict(m="left", sel="#r-edu", l="h2", t="heading", y="line"),
      dict(m="left", sel=".edu-list", l="<ul>", t="list", dx=4, ysel=".edu-name", y="line"),
      dict(m="left", sel="#r-skills", l="h2", t="heading", y="line"),
      dict(m="left", sel="#contact", l="h2", t="heading", y="line"),
      dict(m="right", sel=".contact-links li:last-child a", l=L["contact"], t="link"),
      dict(m="top", sel=".theme-options", l=L["radio"], t="button", len=22),
      dict(m="bracket", sel=".site-footer", l="<footer>", t="landmark", it=8, ib=8),
    ]
    m = [
      dict(sel=".site-header", where="prepend", chips=[["<header>", "landmark"]]),
      dict(sel=".header-navs", chips=[["<nav>", "landmark"], ["<ul>", "list"], [L["links4"], "link"]]),
      dict(sel="main h1", chips=[["h1", "heading"]]),
      dict(sel=".cta", chips=[[L["link"], "link"]]),
      dict(sel="#about, #r-contact", chips=[["h2", "heading"]]),
      dict(sel=".about-mark", chips=[[L["dec"], "image"]]),
      dict(sel="#work, #r-focus", chips=[["h2", "heading"]]),
      dict(sel=".work-list", chips=[["<ul>", "list"]]),
      dict(sel="#experience, #r-exp", chips=[["h2", "heading"]]),
      dict(sel=".timeline", chips=[["<ol>", "list"]]),
      dict(sel="#r-edu", chips=[["h2", "heading"]]),
      dict(sel="#r-skills", chips=[["h2", "heading"]]),
      dict(sel="#contact", chips=[["h2", "heading"]]),
      dict(sel=".contact-links", chips=[[L["link"], "link"]]),
      dict(sel=".site-footer", where="prepend", chips=[["<footer>", "landmark"]], cls="a11y-footer-row"),
      dict(sel=".theme", chips=[[L["radio"], "button"]], cls="a11y-radio-row"),
    ]
    j = json.dumps(dict(desktop=d, mobile=m), ensure_ascii=False, separators=(",", ":"))
    return j.replace("</", "<\\/")

def icon(cls):
    return f'<span class="icon {cls}" aria-hidden="true"></span>'

def top(k, kind):
    """<head>, skip link, annotations control and header — identical on every page (3.2.3 / 3.2.4)."""
    c = T[k]; b = c["base"]; en = k == "en"; home = kind == "home"
    r = R[k]
    title, desc = (c["title"], c["desc"]) if home else (r["title"], r["desc"])
    path = "" if home else "resume.html"
    self_url = c["self_url"] + path
    pre = "" if home else "./"   # in-page anchors live on the home page
    def href(h):
        if h.startswith("#"): return (pre + h) if not home else h
        return h
    def cur(h):
        return ' aria-current="page"' if (not home and h == "resume.html") else ""
    nav = "\n".join(f'          <li><a href="{e(href(h))}"{cur(h)}>{e(t)}</a></li>' for h, t in c["nav"])
    en_href = ("./" if en else "../") + path
    pt_href = ("pt/" if en else "./") + path
    ac = ' aria-current="page"'
    ca_en, ca_pt = (ac, "") if en else ("", ac)
    langs = (f'          <li><a href="{en_href}" hreflang="en" lang="en"{ca_en}>English</a></li>\n'
             f'          <li><a href="{pt_href}" hreflang="pt-PT" lang="pt-PT"{ca_pt}>Português</a></li>')
    return f'''<!DOCTYPE html>
<html lang="{c["lang"]}" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="color-scheme" content="light dark">
  <link rel="canonical" href="{self_url}">
  <link rel="alternate" hreflang="en" href="{SITE}{path}">
  <link rel="alternate" hreflang="pt-PT" href="{SITE}pt/{path}">
  <link rel="alternate" hreflang="x-default" href="{SITE}{path}">
  <link rel="icon" href="{b}favicon.ico">
  <link rel="preload" href="{b}assets/fonts/atkinson-hyperlegible-next-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{b}assets/fonts/atkinson-hyperlegible-next-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
  <script>{HEAD_JS}</script>
  <link rel="stylesheet" href="{b}css/site.css">
  <script src="{b}js/site.js" defer></script>
  <script src="{b}js/annotations.js" defer></script>
  <script type="application/json" id="anno-spec">{anno_spec(k)}</script>
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
'''

def bottom(k):
    c = T[k]
    return f'''
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

def contact_links(c):
    return f'''<ul class="contact-links"{ann(c["a_contact"], "link")}>
        <li><a href="mailto:pim.uxdesigner@gmail.com">{icon("i-mail")}pim.uxdesigner@gmail.com</a></li>
        <li><a href="https://www.linkedin.com/in/pimagrinho/">{icon("i-linkedin")}linkedin.com/in/pimagrinho</a></li>
      </ul>'''

def home(k):
    c = T[k]; b = c["base"]
    work = "\n".join(f'          <li><span class="work-ico">{icon(i)}</span>{e(t)}</li>' for i, t in c["work"])
    jobs = "\n".join(f'''        <li>
          <p class="year">{e(y)}</p>
          <div class="job">
            <h3>{e(r)}</h3>
            <p class="org">{e(o)}</p>
            <ul>{"".join(f"<li>{e(x)}</li>" for x in bl)}</ul>
          </div>
        </li>''' for y, r, o, bl in c["jobs"])
    return top(k, "home") + f'''
  <main id="main" tabindex="-1"{ann("<main>", "landmark", "bleed", "-")}>
    <div class="hero wrap">
      <div class="hero-intro">
        <h1{ann("h1", "heading")}>Patrícia Magrinho</h1>
        <p class="role">{e(c["role"])}</p>
        <p class="langs">{e(c["langs"])}</p>
        <p class="bio">{e(c["bio"])}</p>
      </div>
      <div class="cta-area"{ann(c["a_link"], "link", "top")}>
        <a class="cta" href="resume.html">{e(c["cta"])}{icon("i-arrow")}</a>
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
      {contact_links(c)}
    </section>
  </main>
''' + bottom(k)

def resume(k):
    c = T[k]; r = R[k]
    jobs = "\n".join(f'''        <li>
          <p class="year">{e(y)}</p>
          <div class="job">
            <h3>{e(t)}</h3>
            <p class="org">{e(o)}</p>
            <ul>{"".join(f"<li>{e(x)}</li>" for x in bl)}</ul>
          </div>
        </li>''' for y, t, o, bl in r["jobs"])
    edu = "\n".join(f'          <li><p class="edu-name">{e(n)}</p><p class="org">{e(m)}</p></li>' for n, m in r["edu"])
    skills = "\n".join(f'''        <section class="skill" aria-labelledby="sk-{i}">
          <h3 id="sk-{i}">{e(h)}</h3>
          <ul>{"".join(f"<li>{e(x)}</li>" for x in items)}</ul>
        </section>''' for i, (h, items) in enumerate(r["skills"], 1))
    focus = "".join(f"<li>{e(x)}</li>" for x in r["focus"])
    return top(k, "resume") + f'''
  <main id="main" tabindex="-1"{ann("<main>", "landmark", "bleed", "-")}>
    <div class="hero resume-hero wrap">
      <div class="hero-intro">
        <h1{ann("h1", "heading")}>{e(r["h1"])}</h1>
        <p class="role">Patrícia Magrinho · {e(c["role"])}</p>
        <p class="bio">{e(r["intro"])}</p>
      </div>
    </div>

    <div class="cards wrap">
      <section class="card card-about on-accent" aria-labelledby="r-contact">
        <h2 id="r-contact"{ann("h2", "heading", "top")}>{e(r["contact_h"])}</h2>
        <dl class="facts">
          <div><dt>{e(r["loc_l"])}</dt><dd>{e(r["loc"])}</dd></div>
          <div><dt>{e(r["email_l"])}</dt><dd><a href="mailto:pim.uxdesigner@gmail.com">pim.uxdesigner@gmail.com</a></dd></div>
          <div><dt>{e(r["li_l"])}</dt><dd><a href="https://www.linkedin.com/in/pimagrinho/">linkedin.com/in/pimagrinho</a></dd></div>
        </dl>
      </section>
      <section class="card card-work on-ink" aria-labelledby="r-focus">
        <h2 id="r-focus"{ann("h2", "heading", "top")}>{e(r["focus_h"])}</h2>
        <ul class="work-list">
          <li><span class="work-ico">{icon("i-eye")}</span>{e(r["focus"][0])}</li>
          <li><span class="work-ico">{icon("i-check-sq")}</span>{e(r["focus"][1])}</li>
        </ul>
      </section>
    </div>

    <section class="experience wrap" aria-labelledby="r-exp">
      <h2 id="r-exp"{ann("h2", "heading")}>{e(r["exp_h"])}</h2>
      <ol class="timeline"{ann("<ol>", "list")}>
{jobs}
      </ol>
    </section>

    <section class="experience resume-block wrap" aria-labelledby="r-edu">
      <h2 id="r-edu"{ann("h2", "heading")}>{e(r["edu_h"])}</h2>
      <ul class="edu-list">
{edu}
      </ul>
    </section>

    <section class="experience resume-block wrap" aria-labelledby="r-skills">
      <h2 id="r-skills"{ann("h2", "heading")}>{e(r["skills_h"])}</h2>
      <div class="skills">
{skills}
      </div>
    </section>
  </main>
''' + bottom(k)

def notfound():
    """404 for GitHub Pages: served at any path, so every URL is absolute. Bilingual, no JS needed."""
    P = "/pim.accessibility/"
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page not found — Patrícia Magrinho</title>
  <meta name="robots" content="noindex">
  <meta name="color-scheme" content="light dark">
  <link rel="icon" href="{P}favicon.ico">
  <script>{HEAD_JS.replace("if(a?a==='on':m('(min-width: 80em)').matches)d.classList.add('anno-on');", "")}</script>
  <link rel="stylesheet" href="{P}css/site.css">
</head>
<body>
  <div class="skip-bar on-ink" id="top"><a href="#main">Skip to main content</a></div>
  <header class="site-header wrap">
    <a class="logo" href="{P}" aria-label="Patrícia’s portfolio — home"><span class="logo-badge"><img src="{P}assets/icons/fingerprint.svg" width="32" height="32" alt=""></span></a>
  </header>
  <main id="main" tabindex="-1" class="hero wrap notfound">
    <div class="hero-intro">
      <h1>Page not found</h1>
      <p class="bio">This address does not exist or has moved.</p>
      <p><a class="cta" href="{P}">Go to the home page{icon("i-arrow")}</a></p>
    </div>
    <div class="hero-intro" lang="pt-PT">
      <h2>Página não encontrada</h2>
      <p class="bio">Este endereço não existe ou mudou de sítio.</p>
      <p><a class="cta" href="{P}pt/">Ir para a página inicial{icon("i-arrow")}</a></p>
    </div>
  </main>
</body>
</html>
'''

(REPO / "pt").mkdir(exist_ok=True)
for k, d in (("en", REPO), ("pt", REPO / "pt")):
    (d / "index.html").write_text(home(k), encoding="utf-8")
    (d / "resume.html").write_text(resume(k), encoding="utf-8")
(REPO / "404.html").write_text(notfound(), encoding="utf-8")
print("ok")
