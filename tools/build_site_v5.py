"""Site v5 preview: the site cut to three pages, at the owner's request (2026-10-18), in English and
European Portuguese (2026-10-19).

    python3 tools/build_site_v5.py

  Home          /               /pt                       the hint of everything: services, convictions, insights
  Insights      /insights       /pt/publicacoes           the index and the articles under it, written in Markdown
                                                          in content/insights/ (PT in content/insights/pt/)
  Book a call   /book           /pt/marcar                one line and the calendar
  plus Privacy (/privacy, /pt/privacidade) and 404 (/404, /pt/404), linked from the footer only.

Every page is built from the same template in both languages: the copy lives in COPY["en"] and
COPY["pt"], and the EN/PT toggle in the header and footer goes to the page's own counterpart.
The Portuguese is European Portuguese (pt-PT, the 1990 spelling agreement as used in Portugal);
check_pt() fails the build on Brazilian forms and on English left in the page furniture.

The services, approach, about and contact pages are gone; their substance is a small section on
the homepage, and the contact details sit in every footer. Reuses site v4's parts
(tools/build_site_v4.py: head, hero, cards, closing, articles); writes explorations/site-v5/,
with its own copy of site v4's stylesheet plus a few rules (site-v5.css). Site v4 is unchanged.
"""
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_site_v4 as v4  # noqa: E402
import markdown_lite as md  # noqa: E402

ROOT = v4.ROOT
SITE = ROOT / "explorations/site-v5"
PREVIEW = "/explorations/site-v5"
v4.PREVIEW = PREVIEW            # head() and page() take the stylesheet and script from here
rep, dummy, esc = v4.rep, v4.dummy, v4.esc

MAIL = "miguelmonteiro@solvenadvisory.ai"     # the address the live site uses
# No partner line: Solven is Registered in the Claude Partner Network (Anthropic: "Partnership begins at Select")
# and enrolled without a tier in the OpenAI Partner Network, so no page names either programme until a tier or
# written approval from the lab allows it (docs/partner-section-research.md).

# Page addresses in each language: the key is the English path, the value the Portuguese one
PT_PATH = {"": "pt", "insights": "pt/publicacoes", "book": "pt/marcar", "privacy": "pt/privacidade", "404": "pt/404"}

# ---------------------------------------------------------------- the copy, in both languages

COPY = {
    "en": dict(
        html="en", locale="en_GB", ld_lang="en-GB",
        home="/", insights="/insights", book="/book", privacy="/privacy",
        skip="Skip to content", logo="Solven Advisory, home", menu="Menu", close_menu="Close",
        nav="Main", footer_nav="Footer", language="Language",
        nav_home="Home", nav_insights="Insights", nav_book="Book a call",
        lisbon="Lisbon, Portugal", linkedin="Solven Advisory on LinkedIn", email="Email Solven Advisory",
        privacy_link="Privacy", cookies_link="Cookie settings",
        dummy_text="Dummy text: replace before launch", dummy_date="Dummy date: replace before launch",
        image_tbc=("Image to be chosen", "Placeholder: choose a photograph for this insight"),
        months=None, min_read="{} min read",
        # Home
        title="Solven Advisory · AI enablement and implementation for investment firms",
        description=("Solven Advisory trains private equity teams on AI, builds it into their workflows, and runs AI projects in their "
                     "portfolio companies that lift EBITDA. Augmentation without cognitive atrophy."),
        ld_description="Solven Advisory trains private equity teams on AI, builds AI systems on their workflows, runs AI projects in their portfolio companies that lift EBITDA, and manages token economics.",
        knows_about=["AI enablement", "Private equity workflows", "Portfolio value creation", "Token economics", "Anthropic Claude", "OpenAI ChatGPT"],
        hero_title="Sharper judgment for the age of AI.",
        hero_lead="Solven trains private equity teams on AI, builds it into their workflows, and runs projects across their portfolio companies that lift EBITDA. The people making the call still own the reasoning behind it.",
        services_title="Four ways we work with a firm.",
        services=[
            ("Enablement", "Hands-on sessions on the leading AI platforms for the whole firm, analyst to managing partner, run monthly because the frontier moves weekly."),
            ("Build", "Agents and workflow systems on the fund's own work: contract redlining, IC memo interrogation, portfolio reporting."),
            ("Portfolio", "For any portfolio company, in any sector: we find what is holding back EBITDA and fix it, with AI where it helps and without it where it does not."),
            ("Token Economics", "Where the compute spend goes, what it returns, and how to pace it so the year's budget lasts the year."),
        ],
        thesis="Augmentation without cognitive atrophy.",
        convictions=[
            ("Judgment is the product.", "In an investment firm the deliverable is a defensible decision; AI should make that judgment sharper, never thinner."),
            ("Fluency is firm-wide.", "From the newest analyst to the managing partner, everyone should know where AI belongs in their own work, and where it does not."),
            ("The portfolio is where it pays.", "Whatever its sector, every portfolio company has a part of the business holding it back. We start from that problem, not from the technology, and sometimes the right answer is not AI at all."),
        ],
        insights_title="Insights.",
        insights_intro="Short notes on AI in investment firms: what we see in the work, and what it means for partners.",
        all_insights="All insights",
        close=("The edge is where the advantage is.",
               "What comes next in AI is still unwritten. We work at that edge every month, so your firm and its portfolio can step onto new ground without losing their footing."),
        write_to_us="Write to us",
        # Insights and articles
        insights_page_title="Insights · Notes on AI for investment firms · Solven Advisory",
        insights_page_description="Short notes from Solven Advisory on AI in private equity, real estate and venture firms: what we see in the work, and what it means for partners.",
        blog_name="Solven Advisory insights",
        article_title="{} · Insights · Solven Advisory", article="Article", about_insight="About this insight",
        # Book a call
        book_title="Book a call · Solven Advisory",
        book_description="Book thirty minutes with a Solven Advisory co-founder, by video or phone.",
        book_h1="Book a call.", calendar="Calendar",
        cal_note="If the calendar does not load, <a href=\"https://cal.eu/miguelmonteirosolven/30min\" target=\"_blank\" rel=\"noopener\">open it in a new tab</a>. Prefer to write? ",
    ),
    "pt": dict(
        html="pt-PT", locale="pt_PT", ld_lang="pt-PT",
        home="/pt", insights="/pt/publicacoes", book="/pt/marcar", privacy="/pt/privacidade",
        skip="Saltar para o conteúdo", logo="Solven Advisory, início", menu="Menu", close_menu="Fechar",
        nav="Principal", footer_nav="Rodapé", language="Idioma",
        nav_home="Início", nav_insights="Publicações", nav_book="Marcar uma chamada",
        lisbon="Lisboa, Portugal", linkedin="Solven Advisory no LinkedIn", email="Enviar um email à Solven Advisory",
        privacy_link="Privacidade", cookies_link="Definições de cookies",
        dummy_text="Texto provisório: substituir antes do lançamento", dummy_date="Data provisória: substituir antes do lançamento",
        image_tbc=("Imagem por escolher", "Provisório: escolher uma fotografia para esta publicação"),
        months=["jan.", "fev.", "mar.", "abr.", "mai.", "jun.", "jul.", "ago.", "set.", "out.", "nov.", "dez."],
        min_read="{} min de leitura",
        # Home
        title="Solven Advisory · Formação e implementação de IA para casas de investimento",
        description=("A Solven Advisory forma equipas de private equity em IA, integra-a nos seus fluxos de trabalho e conduz, "
                     "nas empresas do portefólio, projetos de IA que fazem crescer o EBITDA. Ampliação sem atrofia cognitiva."),
        ld_description="A Solven Advisory forma equipas de private equity em IA, constrói sistemas de IA sobre os seus fluxos de trabalho, conduz, nas empresas do portefólio, projetos de IA que fazem crescer o EBITDA, e gere a economia de tokens.",
        knows_about=["Formação em IA", "Fluxos de trabalho de private equity", "Criação de valor no portefólio", "Economia de tokens", "Anthropic Claude", "OpenAI ChatGPT"],
        hero_title="Critério mais apurado para a era da IA.",
        hero_lead="A Solven forma equipas de private equity em IA, integra-a nos seus fluxos de trabalho e conduz, nas empresas do portefólio, projetos que fazem crescer o EBITDA. Quem toma a decisão continua a ser dono do raciocínio que a sustenta.",
        services_title="Quatro formas de trabalharmos com uma casa de investimento.",
        services=[
            ("Formação", "Sessões práticas nas principais plataformas de IA para toda a casa, do analista ao managing partner, todos os meses, porque a fronteira avança todas as semanas."),
            ("Implementação", "Agentes e sistemas sobre o trabalho do próprio fundo: revisão de contratos, escrutínio de memorandos de comité de investimento, reporting do portefólio."),
            ("Portefólio", "Em qualquer empresa do portefólio, de qualquer setor: descobrimos o que está a travar o EBITDA e resolvemo-lo, com IA onde ajuda e sem ela onde não ajuda."),
            ("Economia de tokens", "Para onde vai a despesa de compute, o que rende e como a dosear para que o orçamento do ano dure o ano inteiro."),
        ],
        thesis="Ampliação sem atrofia cognitiva.",
        convictions=[
            ("O critério é o produto.", "Numa casa de investimento, o que se entrega é uma decisão defensável; a IA deve tornar esse critério mais apurado, nunca mais superficial."),
            ("A fluência é de toda a casa.", "Do analista mais recente ao managing partner, todos devem saber onde a IA tem lugar no seu próprio trabalho, e onde não tem."),
            ("É no portefólio que compensa.", "Seja qual for o setor, cada empresa do portefólio tem uma parte do negócio que a está a travar. Partimos desse problema, não da tecnologia, e por vezes a resposta certa nem sequer é IA."),
        ],
        insights_title="Publicações.",
        insights_intro="Notas curtas sobre IA em casas de investimento: o que vemos no trabalho, e o que isso significa para os partners.",
        all_insights="Todas as publicações",
        close=("É na fronteira que está a vantagem.",
               "O que vem a seguir na IA ainda está por escrever. Trabalhamos nessa fronteira todos os meses, para que a vossa casa e o seu portefólio possam pisar terreno novo sem perder o equilíbrio."),
        write_to_us="Enviar-nos um email",
        # Insights and articles
        insights_page_title="Publicações · Notas sobre IA para casas de investimento · Solven Advisory",
        insights_page_description="Notas curtas da Solven Advisory sobre IA em casas de private equity, imobiliário e venture capital: o que vemos no trabalho, e o que isso significa para os partners.",
        blog_name="Publicações da Solven Advisory",
        article_title="{} · Publicações · Solven Advisory", article="Artigo", about_insight="Sobre esta publicação",
        # Book a call
        book_title="Marcar uma chamada · Solven Advisory",
        book_description="Marquem trinta minutos com um cofundador da Solven Advisory, por vídeo ou telefone.",
        book_h1="Marcar uma chamada.", calendar="Calendário",
        cal_note="Se o calendário não carregar, <a href=\"https://cal.eu/miguelmonteirosolven/30min\" target=\"_blank\" rel=\"noopener\">abram-no num novo separador</a>. Preferem escrever? ",
    ),
}


def email_icon(t):
    """An envelope that opens the visitor's mail app; the address itself is not printed on the page."""
    return (f'<a class="icon-link" href="mailto:{MAIL}" aria-label="{t["email"]}" title="{t["email"]}">'
            '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">'
            '<rect x="3" y="5.5" width="18" height="13" rx="1"/><path d="M3.5 6.5 12 13l8.5-6.5"/></svg></a>')


def linkedin_icon(t):
    """LinkedIn as the same kind of line icon, beside the envelope."""
    return (f'<a class="icon-link" href="https://www.linkedin.com/company/solven-advisory" aria-label="{t["linkedin"]}" title="{t["linkedin"]}">'
            '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">'
            '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 10.5V17M11.5 17v-6.5M11.5 13.3c0-1.7 1.1-2.8 2.6-2.8s2.4 1.1 2.4 2.8V17"/>'
            '<circle cx="8" cy="7.4" r=".4" fill="currentColor"/></svg></a>')


# ---------------------------------------------------------------- header and footer: three pages

def url(path):
    return "/" + path if path else "/"


def toggle(block, lang, path, alt):
    """The EN/PT switch: each side goes to this page's counterpart, the current language is marked."""
    en, pt = (url(path), url(alt)) if lang == "en" else (url(alt), url(path))
    cur = ' aria-current="true"'
    return rep(block, '<a href="/" lang="en" hreflang="en" aria-current="true">EN</a><a href="/pt" lang="pt-PT" hreflang="pt-PT">PT</a>',
               f'<a href="{en}" lang="en" hreflang="en"{cur if lang == "en" else ""}>EN</a>'
               f'<a href="{pt}" lang="pt-PT" hreflang="pt-PT"{cur if lang == "pt" else ""}>PT</a>')


def furniture(block, t):
    """The labels the header and footer share."""
    block = block.replace('href="/" aria-label="Solven Advisory, home"', f'href="{t["home"]}" aria-label="{t["logo"]}"')
    return block.replace('role="group" aria-label="Language"', f'role="group" aria-label="{t["language"]}"')


def header(t, lang, path, alt, current):
    h = v4.HEADER
    h = re.sub(r'<ul class="nav">.*?</ul>',
               f'<ul class="nav">\n          <li><a href="{t["insights"]}"' + (' aria-current="page"' if current == "insights" else "")
               + f'>{t["nav_insights"]}</a></li>\n        </ul>',
               h, flags=re.S)
    h = rep(h, 'href="/contact#calendar">Book a call</a>', f'href="{t["book"]}"' + (' aria-current="page"' if current == "book" else "") + f'>{t["nav_book"]}</a>')
    h = rep(h, '<span class="menu__open">Menu</span><span class="menu__close">Close</span>',
            f'<span class="menu__open">{t["menu"]}</span><span class="menu__close">{t["close_menu"]}</span>')
    h = rep(h, '<nav aria-label="Main">', f'<nav aria-label="{t["nav"]}">')
    return toggle(furniture(h, t), lang, path, alt)


def footer(t, lang, path, alt):
    f = v4.FOOTER
    f = re.sub(r'<ul>\s*<li><a href="/approach">.*?</ul>', f"""<ul>
          <li><a href="{t["home"]}">{t["nav_home"]}</a></li>
          <li><a href="{t["insights"]}">{t["nav_insights"]}</a></li>
          <li><a href="{t["book"]}">{t["nav_book"]}</a></li>
        </ul>""", f, flags=re.S)
    f = re.sub(r'<ul class="footer__contact">.*?</ul>', f"""<ul class="footer__contact">
        <li>{t["lisbon"]}</li>
        <li><a href="tel:+351967130877">+351 967 130 877</a></li>
        <li class="footer__icons">{linkedin_icon(t)}{email_icon(t)}</li>
      </ul>""", f, flags=re.S)
    f = rep(f, '<nav class="footer__nav" aria-label="Footer">', f'<nav class="footer__nav" aria-label="{t["footer_nav"]}">')
    f = rep(f, '<a href="/privacy">Privacy</a><span aria-hidden="true"> · </span><a href="/privacy#cookies">Cookie settings</a>',
            f'<a href="{t["privacy"]}">{t["privacy_link"]}</a><span aria-hidden="true"> · </span><a href="{t["privacy"]}#cookies">{t["cookies_link"]}</a>')
    return toggle(furniture(f, t), lang, path, alt)


def head(p, t):
    h = v4.head(p).replace(f'<link rel="stylesheet" href="{PREVIEW}/site.css?v=1">',
                           f'<link rel="stylesheet" href="{PREVIEW}/site.css?v=1">\n<link rel="stylesheet" href="{PREVIEW}/site-v5.css?v=8">')
    h = rep(h, '<html lang="en">', f'<html lang="{t["html"]}">')
    other = "pt_PT" if p["lang"] == "en" else "en_GB"
    h = rep(h, '<meta property="og:locale" content="en_GB">',
            f'<meta property="og:locale" content="{t["locale"]}">\n<meta property="og:locale:alternate" content="{other}">')
    if p["path"] not in ("404", "pt/404"):
        # The pair in both directions, English as the default (404 pages are never annotated)
        en, pt = (p["path"], p["alt"]) if p["lang"] == "en" else (p["alt"], p["path"])
        full = lambda x: v4.ORIGIN + ("/" + x if x else "/")
        h = re.sub(r'(<link rel="canonical" href="[^"]*">)',
                   lambda m: m.group(1) + f'\n<link rel="alternate" hreflang="en" href="{full(en)}">'
                                          f'\n<link rel="alternate" hreflang="pt-PT" href="{full(pt)}">'
                                          f'\n<link rel="alternate" hreflang="x-default" href="{full(en)}">', h)
    return h


def page(p):
    t = COPY[p["lang"]]
    body = f"""<body>

<a class="skip" href="#content">{t["skip"]}</a>

{header(t, p["lang"], p["path"], p["alt"], p.get("nav"))}

<main id="content">
{p["main"]}
</main>

{footer(t, p["lang"], p["path"], p["alt"])}

<script src="{PREVIEW}/site.js?v=1"></script>
{p.get("scripts", "")}</body>
</html>
"""
    text = head(p, t) + "\n" + body
    # The placeholder markers say what they are in the page's language
    return text.replace('title="Dummy text: replace before launch"', f'title="{t["dummy_text"]}"') \
               .replace('title="Dummy date: replace before launch"', f'title="{t["dummy_date"]}"')


def links(s):
    """Production paths to the preview, as in v4. The Portuguese pages live inside the preview too."""
    s = s.replace('href="/contact#calendar"', 'href="/book"')
    def fix(m):
        path = m.group(1)
        if re.match(r"/(assets|explorations)(/|$|#|\?)", path):
            return m.group(0)
        return f'href="{PREVIEW}{"" if path == "/" else path}"'
    s = re.sub(r'href="(/[^"]*)"', fix, s)
    return s.replace("/explorations/site/img/", f"{PREVIEW}/img/")


def close(t, art=None):
    c = v4.close(*t["close"], art=art)
    c = rep(c, f"\n      <p class=\"close__note\">{v4.PARTNER}</p>", "")
    c = rep(c, '<a class="btn btn--primary" href="/contact#calendar">Book a call</a>', f'<a class="btn btn--primary" href="{t["book"]}">{t["nav_book"]}</a>')
    return rep(c, '<a class="text-link" href="/contact">Write to us</a>', f'<a class="text-link" href="mailto:{MAIL}">{t["write_to_us"]}</a>')


PAGES = []


def add(lang, path, alt, title, description, main, **kw):
    PAGES.append(dict(lang=lang, path=path, alt=alt, title=title, description=description, main=main, **kw))


def both(path, build, **kw):
    """One page in both languages: build(t, lang) gives the title, description, main and any extras."""
    for lang in ("en", "pt"):
        own, alt = (path, PT_PATH[path]) if lang == "en" else (PT_PATH[path], path)
        title, description, main, extra = build(COPY[lang], lang)
        add(lang, own, alt, title, description, main, **kw, **extra)


# ---------------------------------------------------------------- Insights, read from Markdown

INSIGHTS = ROOT / "content/insights"
REQUIRED = ("title", "subtitle", "summary", "description", "topic", "date")
WORDS_PER_MINUTE = 220


def body_image(src, alt):
    return f'<figure class="prose__image"><img src="{PREVIEW}/img/insights/{esc(src)}" alt="{esc(alt)}"></figure>'


def load_insights(folder, lang):
    """Every <slug>.md in the folder, newest first. The file name is the address: /insights/<slug>
    (/pt/publicacoes/<slug> for the Portuguese ones, which name their English original under en:)."""
    t = COPY[lang]
    out = []
    for f in sorted(folder.glob("*.md")):
        if f.name == "README.md":
            continue
        meta, body = md.front_matter(f.read_text())
        missing = [k for k in REQUIRED + (("en",) if lang == "pt" else ()) if not meta.get(k)]
        if missing:
            raise SystemExit(f"{f.relative_to(ROOT)}: the header block is missing {', '.join(missing)}")
        if meta.get("image") and not meta.get("image_alt"):
            raise SystemExit(f"{f.relative_to(ROOT)}: the image needs a description (image_alt)")
        d = date.fromisoformat(meta["date"])
        label = f"{d.day} {t['months'][d.month - 1]} {d.year}" if t["months"] else f"{d.day} {d:%b %Y}"
        out.append(dict(meta, slug=f.stem, body=md.to_html(body, image=body_image), label=label,
                        placeholder=meta.get("date_is_placeholder", "no") == "yes",
                        minutes=int(meta.get("minutes") or max(1, round(md.words(body) / WORDS_PER_MINUTE)))))
    return sorted(out, key=lambda a: a["date"], reverse=True)


ARTICLES = {"en": load_insights(INSIGHTS, "en"), "pt": load_insights(INSIGHTS / "pt", "pt")}
for a in ARTICLES["pt"]:
    if a["en"] not in {e["slug"] for e in ARTICLES["en"]}:
        raise SystemExit(f"content/insights/pt/{a['slug']}.md: en: {a['en']} names no English insight")
for a in ARTICLES["en"]:
    # An English insight without a translation yet toggles to the Portuguese index
    a["pt"] = next((f"pt/publicacoes/{p['slug']}" for p in ARTICLES["pt"] if p["en"] == a["slug"]), "pt/publicacoes")


def when(a):
    return v4.date_html(a["date"], a["label"], a["placeholder"])


def icard(a, t, topic=False):
    meta = (f"{esc(a['topic'])} · " if topic else "") + f"{when(a)} · {t['min_read'].format(a['minutes'])}"
    return f"""        <article class="icard">
          <h3 class="icard__title"><a href="{t['insights']}/{a['slug']}">{md.inline(a['title'])}</a></h3>
          <p class="icard__sum">{md.inline(a['summary'])}</p>
          <p class="icard__meta">{meta}</p>
        </article>"""


def article_image(a, t):
    """The insight's photograph, chosen for each article. Until one is chosen, a marked placeholder."""
    if not a.get("image"):
        print(f"  note: {a['slug']} has no image yet; the page shows a placeholder")
        return f"""      <figure class="article__image article__image--empty">
        {dummy(*t["image_tbc"])}
      </figure>"""
    return f"""      <figure class="article__image">
        <img src="{PREVIEW}/img/insights/{esc(a['image'])}" alt="{esc(a['image_alt'])}">
      </figure>"""


# ---------------------------------------------------------------- Home

def home(t, lang):
    cards = v4.cards([(n, x, "", None) for n, x in t["services"]]).replace("service service--static", "service service--quiet")
    convictions = "\n".join(f"""        <li class="conviction">
          <h3 class="h3">{h}</h3>
          <p>{x}</p>
        </li>""" for h, x in t["convictions"])
    main = f"""  <section class="hero" aria-labelledby="hero-title">
    <div class="hero__calcada" aria-hidden="true"><i></i><i></i></div>
    <div class="wrap grid">
      <h1 class="h1 hero__title" id="hero-title">{t["hero_title"]}</h1>
      <div class="hero__side">
        <p class="lead hero__lead">{t["hero_lead"]}</p>
        <p class="hero__cta"><a class="btn btn--primary" href="{t["book"]}">{t["nav_book"]}</a></p>
      </div>
    </div>
  </section>

  <section class="section services" id="services" aria-labelledby="services-title">
    <div class="wrap">
      <h2 class="h2" id="services-title">{t["services_title"]}</h2>
{cards}
    </div>
  </section>

  <section class="section why" id="approach" aria-labelledby="why-title">
    <div class="wrap">
      <h2 class="h2" id="why-title">{t["thesis"]}</h2>
      <ul class="convictions">
{convictions}
      </ul>
    </div>
  </section>

  <section class="section insights" aria-labelledby="insights-title">
    <div class="wrap insights__split">
      <div class="insights__intro">
        <h2 class="h2" id="insights-title">{t["insights_title"]}</h2>
        <p>{t["insights_intro"]}</p>
        <a class="btn" href="{t["insights"]}">{t["all_insights"]}</a>
      </div>
      <div class="insights__cards">
{chr(10).join(icard(a, t) for a in ARTICLES[lang][:3])}
      </div>
    </div>
  </section>

""" + close(t, art="maat")
    ld = json.loads(json.dumps(v4.homepage()[1]["ld"]))
    ld[0].update(description=t["ld_description"], knowsAbout=t["knows_about"])
    return t["title"], t["description"], main, dict(ld=ld)


both("", home)

# ---------------------------------------------------------------- Insights and articles

def title_hero(title):
    """Insights and Book a call: the homepage's hero, at its height and title size, with the title only."""
    return f"""  <section class="hero hero--page hero--title" aria-labelledby="hero-title">
    <div class="hero__calcada" aria-hidden="true"><i></i><i></i></div>
    <div class="wrap grid">
      <h1 class="h1 hero__title" id="hero-title">{title}</h1>
    </div>
  </section>
"""


def insights_index(t, lang):
    main = title_hero(t["insights_title"]) + f"""  <section class="section" aria-label="{t["all_insights"]}">
    <div class="wrap">
      <div class="insights__cards icards--wide">
{chr(10).join(icard(a, t, topic=True) for a in ARTICLES[lang])}
      </div>
    </div>
  </section>
""" + close(t, art="maat")
    blog = {"@context": "https://schema.org", "@type": "Blog", "name": t["blog_name"], "url": f"{v4.ORIGIN}{t['insights']}", "publisher": v4.ORG,
            "blogPost": [{"@type": "BlogPosting", "headline": a["title"], "url": f"{v4.ORIGIN}{t['insights']}/{a['slug']}"} for a in ARTICLES[lang]]}
    if lang == "pt":
        blog["inLanguage"] = t["ld_lang"]
    return t["insights_page_title"], t["insights_page_description"], main, dict(ld=[blog])


both("insights", insights_index, nav="insights")


def article(a, lang, alt):
    """Each insight: title and subtitle on top, then the image, the tags, and the text across the page."""
    t = COPY[lang]
    own = f"{t['insights']}/{a['slug']}"
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["title"], "description": a["description"],
          "datePublished": a["date"], "author": v4.ORG, "publisher": v4.ORG, "inLanguage": t["ld_lang"],
          "mainEntityOfPage": f"{v4.ORIGIN}{own}", "url": f"{v4.ORIGIN}{own}", "image": f"{v4.ORIGIN}/assets/og.png"}
    if lang == "pt":
        ld["translationOfWork"] = {"@id": f"{v4.ORIGIN}/insights/{a['en']}"}
    add(lang, own[1:], alt, t["article_title"].format(a["title"]), a["description"],
        v4.hero(md.inline(a["title"]), md.inline(a["subtitle"]), cta=False, calcada=False)
        + f"""  <section class="section article" aria-label="{t["article"]}">
{article_image(a, t)}
    <div class="wrap">
      <ul class="article__tags" aria-label="{t["about_insight"]}">
        <li>{t["min_read"].format(a['minutes'])}</li>
        <li>{esc(a['topic'])}</li>
        <li>{when(a)}</li>
      </ul>
      <article class="prose prose--wide">
{a['body']}
      </article>
      <p class="article__foot"><a class="btn btn--primary" href="{t["book"]}">{t["nav_book"]}</a><a class="text-link" href="{t["insights"]}">{t["all_insights"]}</a></p>
    </div>
  </section>
""",
        nav="insights", og="article", published=a["date"], ld=[ld])


for a in ARTICLES["en"]:
    article(a, "en", a["pt"])
for a in ARTICLES["pt"]:
    article(a, "pt", f"insights/{a['en']}")

# ---------------------------------------------------------------- Book a call

# Straight to the 30-minute event's date picker: one step fewer than the event list
CAL_SCRIPT = (re.search(r'<script>\n  /\* Inline booking calendar.*?</script>\n', [p for p in v4.PAGES if p["path"] == "contact"][0]["scripts"], re.S).group(0)
              .replace('calLink: "miguelmonteirosolven"', 'calLink: "miguelmonteirosolven/30min"'))


def book(t, lang):
    main = title_hero(t["book_h1"]) + f"""  <section class="section book" id="calendar" aria-label="{t["calendar"]}">
    <div class="wrap">
      <div class="cal" id="cal-inline"></div>
      <p class="cal__note">{t["cal_note"]}{email_icon(t)}</p>
    </div>
  </section>
"""
    return t["book_title"], t["book_description"], main, dict(scripts=CAL_SCRIPT)


both("book", book, nav="book")

# ---------------------------------------------------------------- Privacy and 404

priv = [p for p in v4.PAGES if p["path"] == "privacy"][0]
pm = priv["main"]
# No contact form any more: its sentences go; booking and email stay
pm = re.sub(r"If you use the contact form, we receive the details you type: name, firm, email address, and your message\. "
            r"The form is delivered to our inbox by FormSubmit, a form-forwarding service; we use the details only to reply to you\. ", "", pm)
pm = pm.replace("We process contact and booking details", "We process booking details and correspondence")
pm = pm.replace(" Form delivery passes through FormSubmit.", "")
# A legal notice prints the address itself, so here it is text, not the envelope
pm = pm.replace('<a href="mailto:hello@example.com"><span class="dummy" title="Dummy text: replace before launch">hello@example.com</span></a>',
                f'<a href="mailto:{MAIL}">{MAIL}</a>')
assert "example.com" not in pm
assert "FormSubmit" not in pm and "contact form" not in pm

MAIL_LINK = f'<a href="mailto:{MAIL}">{MAIL}</a>'
# The same notice in European Portuguese, in the terms of the Portuguese text of the GDPR (RGPD)
PRIVACY_PT = [
    ("Quem somos", [
        f"A Solven Advisory é uma consultora de formação e implementação de IA sediada em Lisboa, Portugal. Para tudo o que consta deste aviso, o responsável pelo tratamento é a Solven Advisory, e a forma mais rápida de nos contactar é {MAIL_LINK}."]),
    ("O que recolhemos, e porquê", [
        "Se marcar uma chamada, o agendamento corre na infraestrutura da Cal.com alojada na UE, que recolhe o nome, o endereço de email e o horário que indicar, para colocar a reunião em ambos os calendários. Se apenas nos enviar um email ou telefonar, guardamos a correspondência como qualquer empresa guarda o seu correio.",
        "Usamos a análise de audiências sem cookies da Vercel, que conta as visitas de forma agregada, não guarda nada no seu dispositivo e não identifica ninguém. Funciona independentemente do que aceitar ou recusar.",
        "Gostaríamos também de perceber como o site é realmente lido: que páginas prendem a atenção, onde as pessoas param e que percursos levam a uma conversa. Isso exige cookies, por isso pedimos autorização antes de instalar qualquer um. Nenhum destes cookies é ativado antes de aceitar, recusar exige um único clique, e qualquer das escolhas fica guardada. Não há publicidade, nem definição de perfis para segmentação de anúncios, nem dados vendidos ou cedidos a corretores de dados. Não há newsletter nem lista de marketing; quando dizemos que respondemos a pessoas, e não a leads, este aviso é o que isso significa na prática."]),
    ("O fundamento jurídico", [
        "Tratamos os dados de marcação e a correspondência porque nos pediu que o fizéssemos: diligências pré-contratuais a seu pedido (artigo 6.º, n.º 1, alínea b), do RGPD). Conservamos a correspondência comercial corrente com base no interesse legítimo (artigo 6.º, n.º 1, alínea f)). Os cookies de análise assentam apenas no consentimento (artigo 6.º, n.º 1, alínea a), em conjugação com o artigo 5.º, n.º 3, da Diretiva 2002/58/CE, relativa à privacidade nas comunicações eletrónicas, transposta em Portugal pela Lei n.º 41/2004). Nesse caso, o consentimento é o único fundamento: se o retirar, o tratamento cessa."]),
    ("Onde ficam os dados", [
        "O site está alojado na Vercel. O agendamento corre na Cal.com (infraestrutura na UE). O nosso email corre no Microsoft 365. Se aceitar a análise, a PostHog trata esses dados na sua cloud europeia, em Frankfurt, e o Microsoft Clarity trata-os nos termos da Microsoft, que permitem transferências para fora da UE ao abrigo das cláusulas contratuais-tipo. Cada um destes prestadores atua como subcontratante para os dados acima descritos; a nenhum deles são cedidos os seus dados para qualquer finalidade além da prestação do serviço."]),
    ("Durante quanto tempo os guardamos", [
        "A correspondência é conservada enquanto existir uma relação de trabalho, ou uma perspetiva razoável de a vir a ter, e depois apenas durante o tempo que a conservação normal de registos comerciais exigir. Se preferir que algo seja apagado mais cedo, basta pedir."]),
    ("Os seus direitos", [
        f"Pode pedir o acesso aos dados que temos sobre si, a sua retificação ou apagamento, a limitação do tratamento ou opor-se a ele, e receber uma cópia num formato portável. Escreva para {MAIL_LINK} e tratamos do assunto diretamente. Tem também o direito de apresentar reclamação à autoridade de controlo portuguesa, a CNPD (Comissão Nacional de Proteção de Dados), em <a href=\"https://www.cnpd.pt\" rel=\"noopener\">cnpd.pt</a>."]),
]


def privacy(t, lang):
    if lang == "en":
        return priv["title"], priv["description"], pm, {}
    rows = "\n".join(f"""        <li class="row"{' id="cookies"' if i == 1 else ""}>
          <h2 class="h2 h2--sm row__h">{h}</h2>
          <div class="row__p">{"".join(f"<p>{x}</p>" for x in ps)}</div>
        </li>""" for i, (h, ps) in enumerate(PRIVACY_PT))
    main = v4.hero("Termos claros sobre dados pessoais.",
                   "Sem lista de marketing, sem publicidade e sem nenhum cookie antes de dizer que sim. Esta página diz o que guardamos, porquê e durante quanto tempo.",
                   cta=False, calcada=False,
                   extra='\n        <p class="hero__meta">Este aviso abrange os dados pessoais de quem visita este site, nos escreve ou marca uma chamada. Última atualização: <time datetime="2026-07-29">29 de julho de 2026</time>.</p>') + f"""  <section class="section" aria-label="Aviso de privacidade">
    <div class="wrap">
      <ul class="rows rows--wide">
{rows}
      </ul>
    </div>
  </section>
"""
    return ("Privacidade · Solven Advisory",
            "Como a Solven Advisory trata os dados pessoais de quem nos escreve ou marca uma chamada, e que cookies só funcionam depois de os aceitar.",
            main, {})


both("privacy", privacy)

nf = [p for p in v4.PAGES if p["path"] == "404"][0]


def not_found(t, lang):
    if lang == "en":
        m = rep(nf["main"], '<a class="text-link" href="/services">Services</a>', '<a class="text-link" href="/insights">Insights</a>')
        m = rep(m, '\n          <a class="text-link" href="/contact#calendar">Book a call</a>', '\n          <a class="text-link" href="/book">Book a call</a>')
        return nf["title"], nf["description"], m, {}
    main = v4.hero("Não há nada neste endereço.",
                   "A página pode ter mudado de sítio quando o site mudou, ou o endereço pode ter uma gralha. Seja como for, o trabalho continua nas páginas abaixo.",
                   cta=False, fill=True, extra=f"""
        <p class="nf__links">
          <a class="btn btn--primary" href="{t["home"]}">Voltar ao início</a>
          <a class="text-link" href="{t["insights"]}">{t["nav_insights"]}</a>
          <a class="text-link" href="{t["book"]}">{t["nav_book"]}</a>
        </p>""")
    return "Página não encontrada · Solven Advisory", "Não há nada neste endereço.", main, {}


both("404", not_found)

# ---------------------------------------------------------------- checks

# Brazilian forms that must never reach the Portuguese pages (European Portuguese, as written in Portugal)
BRAZILIAN = [r"equipes?", r"você", r"contato", r"usuári\w*", r"registro", r"perspectiva", r"aspecto", r"detect\w*",
             r"fato", r"econôm\w*", r"\w*ônic\w*", r"\w*êmi\w*", r"gerenciar", r"planilha", r"tela", r"celular", r"arquivo",
             r"time", r"treinamento", r"capacitação", r"a gente", r"aba", r"baixar", r"governança",
             r"estou \w+ndo", r"estamos \w+ndo", r"está \w+ndo", r"estão \w+ndo"]
# The furniture of the English pages, which must not survive into the Portuguese ones
ENGLISH = ["Skip to content", ">Insights<", ">Book a call<", "min read", ">Privacy<", "Cookie settings", "Lisbon,",
           'aria-label="Main"', 'aria-label="Footer"', 'aria-label="Language"', "Write to us", "All insights", "Dummy",
           '<html lang="en">', "Solven Advisory, home"]


def check_pt(text, where):
    visible = re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|svg)\b.*?</\1>", "", text, flags=re.S))
    for w in BRAZILIAN:
        m = re.search(rf"(?<![\w-]){w}(?![\w-])", visible, re.I)
        if m:
            raise SystemExit(f"{where}: Brazilian form {m.group(0)!r} in the Portuguese page")
    for w in ENGLISH:
        assert w not in text, (where, w)


if __name__ == "__main__":
    SITE.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "explorations/site/img", SITE / "img", dirs_exist_ok=True)
    if (INSIGHTS / "images").is_dir():
        shutil.copytree(INSIGHTS / "images", SITE / "img/insights", dirs_exist_ok=True)
    shutil.copyfile(ROOT / "explorations/site/site.css", SITE / "site.css")
    shutil.copyfile(ROOT / "explorations/site/site.js", SITE / "site.js")
    for p in PAGES:
        out = SITE / p["path"] / "index.html"
        text = links(page(p))
        v4.check(text, out)
        if p["lang"] == "pt":
            check_pt(text, out)
        assert "/explorations/site/" not in text.replace(PREVIEW + "/", ""), out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
        print(out.relative_to(ROOT), len(text.encode()), "bytes")
