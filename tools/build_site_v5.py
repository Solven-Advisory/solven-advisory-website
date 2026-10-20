"""Site v5 preview: the site cut to three pages, at the owner's request (2026-10-18), in English and
European Portuguese (2026-10-19).

    python3 tools/build_site_v5.py           the preview, in explorations/site-v5/ (noindex)
    python3 tools/build_site_v5.py --prod    the production site, in public/ (what Vercel serves)

  Home          /               /pt                       the hint of everything: services, convictions, insights
  Insights      /insights       /pt/insights              the index and the articles under it, written in Markdown
                                                          in content/insights/ (PT in content/insights/pt/)
  Book a call   /book           /pt/marcar                one line and the calendar
  plus Privacy (/privacy, /pt/privacidade) and 404 (/404, /pt/404), linked from the footer only.

Every page is built from the same template in both languages. All their text, English beside
Portuguese, lives in content/site-copy.md and nowhere else (the articles are in content/insights/);
this script only places it. The EN/PT toggle in the header and footer goes to the page's own counterpart.
The Portuguese is European Portuguese (pt-PT, the 1990 spelling agreement as used in Portugal);
check_pt() fails the build on Brazilian forms and on English left in the page furniture.

The services, approach, about and contact pages are gone; their substance is a small section on
the homepage, and the contact details sit in every footer. Reuses site v4's parts
(tools/build_site_v4.py: head, hero, cards, closing, articles); writes explorations/site-v5/,
with its own copy of site v4's stylesheet plus a few rules (site-v5.css). Site v4 is unchanged.
"""
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_site_v4 as v4  # noqa: E402
import markdown_lite as md  # noqa: E402
import svg_paths  # noqa: E402

ROOT = v4.ROOT
PROD = "--prod" in sys.argv[1:]
PREVIEW = "/explorations/site-v5"
# The preview lives inside the repo at PREVIEW and is never indexed. The production build writes public/,
# Vercel's output directory: pages at their real addresses, the stylesheets, script and drawings under /assets/site.
# It is built in STAGE first and moved to public/ only once every check has passed, so a build that stops
# half way leaves the last good public/ in place (on 20 October one shipped without its drawings, sitemap and llms files).
PUBLIC = ROOT / "public"
STAGE = ROOT / ".public-build"
SITE = STAGE if PROD else ROOT / "explorations/site-v5"
ASSETS = "/assets/site" if PROD else PREVIEW   # where the stylesheets, script and drawings are served
v4.PREVIEW = ASSETS             # head() and page() take the stylesheet and script from here
rep, dummy, esc = v4.rep, v4.dummy, v4.esc

MAIL = "miguelmonteiro@solvenadvisory.ai"     # the address the live site uses
# No partner line: Solven is Registered in the Claude Partner Network (Anthropic: "Partnership begins at Select")
# and enrolled without a tier in the OpenAI Partner Network, so no page names either programme until a tier or
# written approval from the lab allows it (docs/partner-section-research.md).

# Page addresses in each language: the key is the English path, the value the Portuguese one
PT_PATH = {"": "pt", "insights": "pt/insights", "book": "pt/marcar", "privacy": "pt/privacidade", "404": "pt/404"}

# ---------------------------------------------------------------- the copy, read from content/site-copy.md

COPY_FILE = ROOT / "content/site-copy.md"

# What is not copy: the language code, the date format and the page addresses in each language
SETTINGS = {
    "en": dict(html="en", locale="en_GB", ld_lang="en-GB", months=None,
               home="/", insights="/insights", book="/book", privacy="/privacy"),
    "pt": dict(html="pt-PT", locale="pt_PT", ld_lang="pt-PT",
               months=["jan.", "fev.", "mar.", "abr.", "mai.", "jun.", "jul.", "ago.", "set.", "out.", "nov.", "dez."],
               home="/pt", insights="/pt/insights", book="/pt/marcar", privacy="/pt/privacidade"),
}


def reviewed_date(text, where):
    try:
        return date.fromisoformat(text).isoformat()
    except ValueError:
        raise SystemExit(f"{where}: the review date must be written YYYY-MM-DD, not {text!r}")


def read_copy(path):
    """content/site-copy.md: every text of the pages as "### name", then "EN: ..." and "PT: ...".
    Lines under EN: or PT: continue the text until a blank line; # headings and > notes are ignored.
    "PT reviewed: <date>" under an entry records the owner's review of its Portuguese (pt_reviewed)."""
    entries, key, lang = {}, None, None
    for n, line in enumerate(path.read_text().splitlines(), 1):
        s = line.strip()
        if s.startswith("### "):
            key, lang = s[4:].strip(), None
            if key in entries:
                raise SystemExit(f"{path.name} line {n}: {key} appears twice")
            entries[key] = {}
        elif not s or s.startswith("#") or s.startswith(">"):
            lang = None
        elif key and s.startswith("PT reviewed:"):
            entries[key]["pt_reviewed"] = reviewed_date(s[len("PT reviewed:"):].strip(), f"{path.name} line {n}")
            lang = None
        elif key and s[:3] in ("EN:", "PT:"):
            lang = s[:2].lower()
            entries[key][lang] = s[3:].strip()
        elif key and lang:
            entries[key][lang] += " " + s
    for key, v in entries.items():
        for lang in ("en", "pt"):
            if not v.get(lang):
                raise SystemExit(f"{path.name}: {key} has no {lang.upper()}: line")
    return entries


class Copy:
    """One language's copy. t["name"] is the text ready for the page (escaped, with its links),
    t.raw("name") the text as written (for titles and structured data), t.attr("name") for an attribute."""

    def __init__(self, entries, lang):
        self.entries, self.lang, self.used = entries, lang, set()
        self.__dict__.update(SETTINGS[lang])

    def raw(self, key):
        if key not in self.entries:
            raise SystemExit(f"{COPY_FILE.name}: no entry named {key}")
        self.used.add(key)
        return self.entries[key][self.lang]

    def attr(self, key):
        return esc(self.raw(key))

    def __getitem__(self, key):
        h = md.inline(self.raw(key))
        h = h.replace(MAIL, f'<a href="mailto:{MAIL}">{MAIL}</a>')
        h = re.sub(r"\[\[(.+?)\]\]", lambda m: dummy(m.group(1)), h)    # a fact still to come (site-copy.md, Rules)
        return re.sub(r'<a href="(https://[^"]+)">', r'<a href="\1" rel="noopener">', h)

    def items(self, prefix, *fields):
        """Numbered entries: home.service1.name, home.service2.name, ... as tuples of their fields."""
        out, i = [], 1
        while f"{prefix}{i}.{fields[0]}" in self.entries:
            out.append(tuple(self[f"{prefix}{i}.{f}"] for f in fields))
            i += 1
        return out


ENTRIES = read_copy(COPY_FILE)
COPY = {lang: Copy(ENTRIES, lang) for lang in ("en", "pt")}


def email_icon(t):
    """An envelope that opens the visitor's mail app; the address itself is not printed on the page."""
    return (f'<a class="icon-link" href="mailto:{MAIL}" aria-label="{t.attr("label.email")}" title="{t.attr("label.email")}">'
            '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">'
            '<rect x="3" y="5.5" width="18" height="13" rx="1"/><path d="M3.5 6.5 12 13l8.5-6.5"/></svg></a>')


def linkedin_icon(t):
    """LinkedIn as the same kind of line icon, beside the envelope."""
    return (f'<a class="icon-link" href="https://www.linkedin.com/company/solven-advisory" aria-label="{t.attr("label.linkedin")}" title="{t.attr("label.linkedin")}">'
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
    block = block.replace('href="/" aria-label="Solven Advisory, home"', f'href="{t.home}" aria-label="{t.attr("label.logo")}"')
    return block.replace('role="group" aria-label="Language"', f'role="group" aria-label="{t.attr("label.language")}"')


def header(t, lang, path, alt, current):
    h = v4.HEADER
    h = re.sub(r'<ul class="nav">.*?</ul>',
               f'<ul class="nav">\n          <li><a href="{t.insights}"' + (' aria-current="page"' if current == "insights" else "")
               + f'>{t["nav.insights"]}</a></li>\n        </ul>',
               h, flags=re.S)
    h = rep(h, 'href="/contact#calendar">Book a call</a>', f'href="{t.book}"' + (' aria-current="page"' if current == "book" else "") + f'>{t["nav.book"]}</a>')
    h = rep(h, '<span class="menu__open">Menu</span><span class="menu__close">Close</span>',
            f'<span class="menu__open">{t["label.menu"]}</span><span class="menu__close">{t["label.menu_close"]}</span>')
    h = rep(h, '<nav aria-label="Main">', f'<nav aria-label="{t.attr("label.nav")}">')
    return toggle(furniture(h, t), lang, path, alt)


def footer(t, lang, path, alt):
    f = v4.FOOTER
    f = re.sub(r'<ul>\s*<li><a href="/approach">.*?</ul>', f"""<ul>
          <li><a href="{t.home}">{t["nav.home"]}</a></li>
          <li><a href="{t.insights}">{t["nav.insights"]}</a></li>
          <li><a href="{t.book}">{t["nav.book"]}</a></li>
        </ul>""", f, flags=re.S)
    f = re.sub(r'<ul class="footer__contact">.*?</ul>', f"""<ul class="footer__contact">
        <li>{t["footer.city"]}</li>
        <li><a href="tel:+351967130877">+351 967 130 877</a></li>
        <li class="footer__icons">{linkedin_icon(t)}{email_icon(t)}</li>
      </ul>""", f, flags=re.S)
    f = rep(f, '<nav class="footer__nav" aria-label="Footer">', f'<nav class="footer__nav" aria-label="{t.attr("label.footer_nav")}">')
    # No cookie settings: the site sets no cookies of its own (privacy notice, section 2)
    f = rep(f, '<a href="/privacy">Privacy</a><span aria-hidden="true"> · </span><a href="/privacy#cookies">Cookie settings</a>',
            f'<a href="{t.privacy}">{t["footer.privacy"]}</a>')
    return toggle(furniture(f, t), lang, path, alt)


def head(p, t):
    h = v4.head(p).replace(f'<link rel="stylesheet" href="{ASSETS}/site.css?v=1">',
                           f'<link rel="stylesheet" href="{ASSETS}/site.css?v=1">\n<link rel="stylesheet" href="{ASSETS}/site-v5.css?v=9">')
    if p["path"] in ("404", "pt/404"):
        # A missing page has no address of its own to declare
        h = re.sub(r'\n<link rel="canonical" href="[^"]*">', "", h)
        h = re.sub(r'\n<meta property="og:url" content="[^"]*">', "", h)
        h = rep(h, '<meta name="robots" content="noindex, nofollow">', '<meta name="robots" content="noindex">')
    elif PROD:
        h = rep(h, '\n<meta name="robots" content="noindex, nofollow">', "")
    h = rep(h, '<html lang="en">', f'<html lang="{t.html}">')
    # The typefaces are self-hosted (site-v5.css): no Google Fonts, the two latin files preloaded
    h = rep(h, """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,300..700&family=Source+Sans+3:wght@400;500&display=swap">""",
            "\n".join(f'<link rel="preload" href="/assets/fonts/{f}-latin.woff2" as="font" type="font/woff2" crossorigin>'
                      for f in ("source-sans-3-v20", "source-serif-4-v15")))
    other = "pt_PT" if p["lang"] == "en" else "en_GB"
    h = rep(h, '<meta property="og:locale" content="en_GB">',
            f'<meta property="og:locale" content="{t.locale}">\n<meta property="og:locale:alternate" content="{other}">')
    if p["path"] not in ("404", "pt/404") and not p.get("unpaired"):
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
    path, alt = p["path"], p["alt"]
    if path in ("404", "pt/404"):
        # A missing page has no counterpart: the language switch goes to each language's home
        path, alt = ("", "pt") if p["lang"] == "en" else ("pt", "")
    body = f"""<body>

<a class="skip" href="#content">{t["label.skip"]}</a>

{header(t, p["lang"], path, alt, p.get("nav"))}

<main id="content">
{p["main"]}
</main>

{footer(t, p["lang"], path, alt)}

<script src="{ASSETS}/site.js?v=1"></script>
<script defer src="/_vercel/insights/script.js"></script>
{p.get("scripts", "")}</body>
</html>
"""
    text = head(p, t) + "\n" + body
    # The share image: the insight's own card, else the language's home card (tools/build_og_images.py)
    text = text.replace(f"{v4.ORIGIN}/assets/og.png", f"{v4.ORIGIN}/assets/og/{p.get('og_image', p['lang'])}.png")
    # The placeholder markers say what they are in the page's language
    return text.replace('title="Dummy text: replace before launch"', f'title="{t.attr("label.dummy_text")}"') \
               .replace('title="Dummy date: replace before launch"', f'title="{t.attr("label.dummy_date")}"')


def links(s):
    """Production paths to the preview, as in v4. The Portuguese pages live inside the preview too.
    The production build keeps the paths and only moves the drawings to ASSETS."""
    s = s.replace('href="/contact#calendar"', 'href="/book"')
    if PROD:
        return s.replace("/explorations/site/img/", f"{ASSETS}/img/")
    def fix(m):
        path = m.group(1)
        if re.match(r"/(assets|explorations)(/|$|#|\?)", path):
            return m.group(0)
        return f'href="{PREVIEW}{"" if path == "/" else path}"'
    s = re.sub(r'href="(/[^"]*)"', fix, s)
    return s.replace("/explorations/site/img/", f"{PREVIEW}/img/")


def close(t, art=None):
    c = v4.close(t["close.title"], t["close.text"], art=art)
    c = rep(c, f"\n      <p class=\"close__note\">{v4.PARTNER}</p>", "")
    c = rep(c, '<a class="btn btn--primary" href="/contact#calendar">Book a call</a>', f'<a class="btn btn--primary" href="{t.book}">{t["nav.book"]}</a>')
    return rep(c, '<a class="text-link" href="/contact">Write to us</a>', f'<a class="text-link" href="mailto:{MAIL}">{t["close.write"]}</a>')


PAGES = []
ORG = dict(v4.ORG, logo=f"{v4.ORIGIN}/assets/apple-touch-icon.png")     # the publisher of every page and insight


def crumbs(t, *trail):
    """BreadcrumbList from the language's home down to this page: trail is (name, path) pairs."""
    steps = [(t.raw("nav.home"), t.home)] + list(trail)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "inLanguage": t.ld_lang,
            "itemListElement": [{"@type": "ListItem", "position": i, "name": name, "item": v4.ORIGIN + (path if path != "/" else "/")}
                                for i, (name, path) in enumerate(steps, 1)]}


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
    return f'<figure class="prose__image"><img src="{ASSETS}/img/insights/{esc(src)}" alt="{esc(alt)}"></figure>'


def day_label(iso, t):
    """2026-07-28 as the page shows it: 28 Jul 2026, or 28 jul. 2026 in Portuguese."""
    d = date.fromisoformat(iso)
    return f"{d.day} {t.months[d.month - 1]} {d.year}" if t.months else f"{d.day} {d:%b %Y}"


def load_insights(folder, lang):
    """Every <slug>.md in the folder, newest first. The file name is the address: /insights/<slug>
    (/pt/insights/<slug> for the Portuguese ones, which name their English original under en:)."""
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
        if meta.get("reviewed"):
            meta["reviewed"] = reviewed_date(meta["reviewed"], str(f.relative_to(ROOT)))
        label = day_label(meta["date"], t)
        out.append(dict(meta, slug=f.stem, body=md.to_html(body, image=body_image), label=label,
                        placeholder=meta.get("date_is_placeholder", "no") == "yes",
                        minutes=int(meta.get("minutes") or max(1, round(md.words(body) / WORDS_PER_MINUTE)))))
    return sorted(out, key=lambda a: a["date"], reverse=True)


ARTICLES = {"en": load_insights(INSIGHTS, "en"), "pt": load_insights(INSIGHTS / "pt", "pt")}
for a in ARTICLES["pt"]:
    if a["en"] not in {e["slug"] for e in ARTICLES["en"]}:
        raise SystemExit(f"content/insights/pt/{a['slug']}.md: en: {a['en']} names no English insight")
# The service an insight belongs to: service: in the English header block names a service on the homepage
# (home.service1.name, ...); the Portuguese translation takes its original's.
SERVICES = [n for n, in COPY["en"].items("home.service", "name")]


def service_id(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


for a in ARTICLES["en"]:
    if a.get("service") and a["service"] not in SERVICES:
        raise SystemExit(f"content/insights/{a['slug']}.md: service: {a['service']} is not one of {', '.join(SERVICES)}")
for a in ARTICLES["pt"]:
    a["service"] = next(e.get("service") for e in ARTICLES["en"] if e["slug"] == a["en"])
for a in ARTICLES["en"]:
    # An English insight without a translation yet toggles to the Portuguese index
    a["pt"] = next((f"pt/insights/{p['slug']}" for p in ARTICLES["pt"] if p["en"] == a["slug"]), None)


def when(a):
    return v4.date_html(a["date"], a["label"], a["placeholder"])


def icard(a, t, topic=False, h=3):
    meta = (f"{esc(a['topic'])} · " if topic else "") + f"{when(a)} · {t['article.minutes'].replace('{n}', str(a['minutes']))}"
    return f"""        <article class="icard">
          <h{h} class="icard__title"><a href="{t.insights}/{a['slug']}">{md.inline(a['title'])}</a></h{h}>
          <p class="icard__sum">{md.inline(a['summary'])}</p>
          <p class="icard__meta">{meta}</p>
        </article>"""


def article_image(a, t):
    """The insight's photograph, chosen for each article. Until one is chosen, a marked placeholder."""
    # Read every time, so the copy check counts the placeholder's text as used while every insight has its photograph
    missing = dummy(t["article.image_missing"], t.attr("article.image_missing_note"))
    if not a.get("image"):
        print(f"  note: {a['slug']} has no image yet; the page shows a placeholder")
        return f"""      <figure class="article__image article__image--empty">
        {missing}
      </figure>"""
    return f"""      <figure class="article__image">
        <img src="{ASSETS}/img/insights/{esc(a['image'])}" alt="{esc(a['image_alt'])}">
      </figure>"""


# ---------------------------------------------------------------- Home

def home(t, lang):
    cards = v4.cards([(n, x, "", None) for n, x in t.items("home.service", "name", "text")]).replace("service service--static", "service service--quiet")
    # Each service card is an anchor the insights link to (/#token-economics)
    ids = iter(service_id(n) for n in SERVICES)
    cards = re.sub(r'<article class="service service--quiet">', lambda m: f'<article class="service service--quiet" id="{next(ids)}">', cards)
    convictions = "\n".join(f"""        <li class="conviction">
          <h3 class="h3">{h}</h3>
          <p>{x}</p>
        </li>""" for h, x in t.items("home.conviction", "title", "text"))
    main = f"""  <section class="hero" aria-labelledby="hero-title">
    <div class="hero__calcada" aria-hidden="true"><i></i><i></i></div>
    <div class="wrap grid">
      <h1 class="h1 hero__title" id="hero-title">{t["home.hero.title"]}</h1>
      <div class="hero__side">
        <p class="lead hero__lead">{t["home.hero.text"]}</p>
        <p class="hero__cta"><a class="btn btn--primary" href="{t.book}">{t["nav.book"]}</a></p>
      </div>
    </div>
  </section>

  <section class="section services" id="services" aria-labelledby="services-title">
    <div class="wrap">
      <h2 class="h2" id="services-title">{t["home.services.title"]}</h2>
{cards}
    </div>
  </section>

  <section class="section why" id="approach" aria-labelledby="why-title">
    <div class="wrap">
      <h2 class="h2" id="why-title">{t["home.thesis"]}</h2>
      <ul class="convictions">
{convictions}
      </ul>
    </div>
  </section>

  <section class="section insights" aria-labelledby="insights-title">
    <div class="wrap insights__split">
      <div class="insights__intro">
        <h2 class="h2" id="insights-title">{t["home.insights.title"]}</h2>
        <p>{t["home.insights.text"]}</p>
        <a class="btn" href="{t.insights}">{t["insights.all"]}</a>
      </div>
      <div class="insights__cards">
{chr(10).join(icard(a, t) for a in ARTICLES[lang][:3])}
      </div>
    </div>
  </section>

""" + close(t, art="maat")
    ld = json.loads(json.dumps(v4.homepage()[1]["ld"]))
    ld[0].update(description=t.raw("home.ld_description"), knowsAbout=t.raw("home.ld_topics").split(", "),
                 legalName="Solven Advisory, Lda", knowsLanguage=["en", "pt-PT"])
    ld.append({"@context": "https://schema.org", "@type": "WebSite", "@id": f"{v4.ORIGIN}/#website", "url": f"{v4.ORIGIN}/",
               "name": "Solven Advisory", "inLanguage": ["en-GB", "pt-PT"], "publisher": {"@id": ORG["@id"]}})
    return t.raw("home.tab_title"), t.raw("home.description"), main, dict(ld=ld)


both("", home)

# ---------------------------------------------------------------- Insights and articles

def title_hero(title, lead=None):
    """Insights and Book a call: the homepage's hero, at its height and title size, with the title and, on Book a call,
    the homepage's lead beside it."""
    side = f'\n      <div class="hero__side">\n        <p class="lead hero__lead">{lead}</p>\n      </div>' if lead else ""
    return f"""  <section class="hero hero--page hero--title" aria-labelledby="hero-title">
    <div class="hero__calcada" aria-hidden="true"><i></i><i></i></div>
    <div class="wrap grid">
      <h1 class="h1 hero__title" id="hero-title">{title}</h1>{side}
    </div>
  </section>
"""


def insights_index(t, lang):
    main = title_hero(t["home.insights.title"]) + f"""  <section class="section" aria-label="{t.attr("insights.all")}">
    <div class="wrap">
      <div class="insights__cards icards--wide">
{chr(10).join(icard(a, t, topic=True, h=2) for a in ARTICLES[lang])}
      </div>
    </div>
  </section>
""" + close(t, art="maat")
    blog = {"@context": "https://schema.org", "@type": "Blog", "name": t.raw("insights.ld_name"), "url": f"{v4.ORIGIN}{t.insights}", "publisher": ORG,
            "inLanguage": t.ld_lang,
            "blogPost": [{"@type": "BlogPosting", "headline": a["title"], "url": f"{v4.ORIGIN}{t.insights}/{a['slug']}"} for a in ARTICLES[lang]]}
    return t.raw("insights.tab_title"), t.raw("insights.description"), main, dict(ld=[blog, crumbs(t, (t.raw("nav.insights"), t.insights))])


both("insights", insights_index, nav="insights")


def related(a, lang, n=2):
    """Two other insights in the same language: the same topic first, then the newest."""
    others = [o for o in ARTICLES[lang] if o["slug"] != a["slug"]]     # already newest first
    return sorted(others, key=lambda o: o["topic"] != a["topic"])[:n]


# The house separator between the details under an article's image: a line breaks only after it, never inside an item
SEP = '</span><span aria-hidden="true">&nbsp;· </span><span>'


def article(a, lang, alt, unpaired=False):
    """Each insight: title and subtitle on top, then the image, one line of details, and the text across the page."""
    t = COPY[lang]
    own = f"{t.insights}/{a['slug']}"
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["title"], "description": a["description"],
          "datePublished": a["date"], "dateModified": a.get("updated") or a["date"], "author": ORG, "publisher": ORG, "inLanguage": t.ld_lang,
          "mainEntityOfPage": f"{v4.ORIGIN}{own}", "url": f"{v4.ORIGIN}{own}", "image": f"{v4.ORIGIN}/assets/og/{lang}/{a['slug']}.png"}
    updated, label = "", t["article.updated"]     # read even when unused: no insight has an updated: date yet
    if a.get("updated"):
        stamp = f'<time datetime="{a["updated"]}">{day_label(a["updated"], t)}</time>'
        updated = f'{SEP}{label.replace("{date}", stamp)}'
    service = ""
    if a.get("service"):
        name = COPY[lang].items("home.service", "name")[SERVICES.index(a["service"])][0]
        link = f'<a href="{t.home}#{service_id(a["service"])}">{name}</a>'
        service = f'\n      <p class="article__service">{t["article.service"].replace("{service}", link)}</p>'
    if lang == "pt":
        ld["translationOfWork"] = {"@id": f"{v4.ORIGIN}/insights/{a['en']}"}
    add(lang, own[1:], alt, t.raw("article.tab_title").replace("{title}", a["title"]), a["description"],
        v4.hero(md.inline(a["title"]), md.inline(a["subtitle"]), cta=False, calcada=False)
        + f"""  <section class="section article" aria-label="{t.attr("article.label")}">
{article_image(a, t)}
    <div class="wrap">
      <p class="article__meta"><span>{t['article.byline']}{SEP}{esc(a['topic'])}{SEP}{when(a)}{SEP}{t['article.minutes'].replace('{n}', str(a['minutes']))}{updated}</span></p>
      <article class="prose prose--wide">
{a['body']}
      </article>
      <p class="article__foot"><a class="btn btn--primary" href="{t.book}">{t["nav.book"]}</a><a class="text-link" href="{t.insights}">{t["insights.all"]}</a></p>{service}
    </div>
  </section>

  <section class="section related" aria-labelledby="related-title">
    <div class="wrap">
{v4.shead(t["article.related"], "related-title")}
      <div class="insights__cards insights__cards--2">
{chr(10).join(icard(o, t, topic=True) for o in related(a, lang))}
      </div>
    </div>
  </section>
""",
        nav="insights", og="article", og_image=f"{lang}/{a['slug']}", published=a["date"], unpaired=unpaired,
        ld=[ld, crumbs(t, (t.raw("nav.insights"), t.insights), (a["title"], own))])


for a in ARTICLES["en"]:
    article(a, "en", a["pt"] or PT_PATH["insights"], unpaired=not a["pt"])
for a in ARTICLES["pt"]:
    article(a, "pt", f"insights/{a['en']}")

# ---------------------------------------------------------------- Book a call

# Straight to the 30-minute event's date picker: one step fewer than the event list
CAL_SCRIPT = (re.search(r'<script>\n  /\* Inline booking calendar.*?</script>\n', [p for p in v4.PAGES if p["path"] == "contact"][0]["scripts"], re.S).group(0)
              .replace('calLink: "miguelmonteirosolven"', 'calLink: "miguelmonteirosolven/30min"'))


def book(t, lang):
    main = title_hero(t["book.title"], t["book.text"]) + f"""  <section class="section book" id="calendar" aria-label="{t.attr("book.calendar_label")}">
    <div class="wrap">
      <div class="cal" id="cal-inline"></div>
      <p class="cal__note">{t["book.fallback"].replace(' rel="noopener">', ' target="_blank" rel="noopener">')} {t["book.write"]} {email_icon(t)}</p>
    </div>
  </section>
""" + faq_section(t)
    contact = {"@context": "https://schema.org", "@type": "ContactPage", "url": f"{v4.ORIGIN}{t.book}", "name": t.raw("book.tab_title"),
               "inLanguage": t.ld_lang, "about": {"@id": ORG["@id"]}}
    for i in faq_numbers(t):
        for k in (f"book.faq{i}.q", f"book.faq{i}.a"):
            # The FAQPage data must say exactly what the page says: plain text only, no links or emphasis
            if html.unescape(re.sub(r"<[^>]+>", "", t[k])) != t.raw(k) or "<" in t[k]:
                raise SystemExit(f"{COPY_FILE.name}: {k} must be plain text (no links, bold or italic)")
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": t.ld_lang,
           "mainEntity": [{"@type": "Question", "name": t.raw(f"book.faq{i}.q"),
                           "acceptedAnswer": {"@type": "Answer", "text": t.raw(f"book.faq{i}.a")}} for i in faq_numbers(t)]}
    return t.raw("book.tab_title"), t.raw("book.description"), main, dict(scripts=CAL_SCRIPT, ld=[contact, faq, crumbs(t, (t.raw("nav.book"), t.book))])


def faq_numbers(t):
    """book.faq1.q, book.faq2.q, ...: as many questions as the copy has."""
    n = 1
    while f"book.faq{n}.q" in t.entries:
        n += 1
    return range(1, n)


def faq_section(t):
    """The questions under the calendar, in the privacy notice's rows: the question on the left, the answer beside it."""
    rows = "\n".join(f"""        <li class="row">
          <h3 class="h3 row__h">{t[f"book.faq{i}.q"]}</h3>
          <div class="row__p"><p>{t[f"book.faq{i}.a"]}</p></div>
        </li>""" for i in faq_numbers(t))
    return f"""  <section class="section" aria-labelledby="faq">
    <div class="wrap">
{v4.shead(t["book.faq.title"], "faq")}
      <ul class="rows rows--wide">
{rows}
      </ul>
    </div>
  </section>
"""


both("book", book, nav="book")

# ---------------------------------------------------------------- Privacy and 404

def privacy(t, lang):
    rows = "\n".join(f"""        <li class="row">
          <h2 class="h2 h2--sm row__h">{h}</h2>
          <div class="row__p">{"".join(f"<p>{x}</p>" for x in ps)}</div>
        </li>""" for i, (h, ps) in enumerate(privacy_sections(t), 1))
    iso = datetime.strptime(COPY["en"].raw("privacy.updated_date"), "%d %B %Y").date().isoformat()
    main = v4.hero(t["privacy.title"], t["privacy.text"], cta=False, calcada=False,
                   extra=f'\n        <p class="hero__meta">{t["privacy.scope"]} {t["privacy.updated"]} <time datetime="{iso}">{t["privacy.updated_date"]}</time>.</p>') + f"""  <section class="section" aria-label="{t.attr("privacy.label")}">
    <div class="wrap">
      <ul class="rows rows--wide">
{rows}
      </ul>
    </div>
  </section>
"""
    return t.raw("privacy.tab_title"), t.raw("privacy.description"), main, dict(ld=[crumbs(t, (t.raw("footer.privacy"), t.privacy))])


def privacy_sections(t):
    """privacy.s1.title with its paragraphs privacy.s1.p1, privacy.s1.p2, ...; then s2, and so on."""
    out, i = [], 1
    while f"privacy.s{i}.title" in t.entries:
        ps, j = [], 1
        while f"privacy.s{i}.p{j}" in t.entries:
            ps.append(t[f"privacy.s{i}.p{j}"])
            j += 1
        out.append((t[f"privacy.s{i}.title"], ps))
        i += 1
    return out


both("privacy", privacy)


def not_found(t, lang):
    # Production serves one 404.html for every missing address, so the English page carries a line in Portuguese
    pt = COPY["pt"]
    other = "" if lang == "pt" else f"""
        <p class="nf__other" lang="pt-PT">{pt["notfound.title"]} <a class="text-link" href="{pt.home}">{pt["notfound.back"]}</a></p>"""
    main = v4.hero(t["notfound.title"], t["notfound.text"], cta=False, fill=True, extra=f"""
        <p class="nf__links">
          <a class="btn btn--primary" href="{t.home}">{t["notfound.back"]}</a>
          <a class="text-link" href="{t.insights}">{t["nav.insights"]}</a>
          <a class="text-link" href="{t.book}">{t["nav.book"]}</a>
        </p>{other}""")
    return t.raw("notfound.tab_title"), t.raw("notfound.description"), main, {}


both("404", not_found)

# ---------------------------------------------------------------- checks

# Brazilian forms that must never reach the Portuguese pages (European Portuguese, as written in Portugal)
BRAZILIAN = [r"equipes?", r"você", r"contato", r"usuári\w*", r"registro", r"perspectiva", r"aspecto", r"detect\w*",
             r"fato", r"econôm\w*", r"\w*ônic\w*", r"\w*êmi\w*", r"gerenciar", r"planilha", r"tela", r"celular", r"arquivo",
             r"time", r"treinamento", r"capacitação", r"a gente", r"aba", r"baixar", r"governança",
             r"estou \w+ndo", r"estamos \w+ndo", r"está \w+ndo", r"estão \w+ndo"]
# The furniture of the English pages, which must not survive into the Portuguese ones
# ("Insights" is the owner's choice for the Portuguese label too, so it is not on the list)
ENGLISH = ["Skip to content", ">Book a call<", "min read", ">Privacy<", "Cookie settings", "Lisbon,",
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


# ---------------------------------------------------------------- production: public/

STATIC = ["robots.txt", "site.webmanifest"]   # served as they are, from the repo root


def shown(f):
    """A file's path as printed: under public/ in production, wherever the staging folder is."""
    return f"public/{f.relative_to(SITE)}" if PROD else f.relative_to(ROOT)


def page_file(path):
    """Where a page is written. Production serves its one 404 page as /404.html."""
    if PROD and path == "404":
        return SITE / "404.html"
    return SITE / path / "index.html"


def stamp(text):
    """Every file under /assets/site gets ?v=<hash of its content>: vercel.json caches /assets for a year."""
    def one(m):
        f = SITE / m.group(1).lstrip("/")
        if not f.is_file():
            raise SystemExit(f"public/ not replaced: {m.group(1)} is referenced but was not built")
        return f"{m.group(1)}?v={hashlib.sha256(f.read_bytes()).hexdigest()[:10]}"
    return re.sub(rf"({ASSETS}/[\w./-]+?\.\w+)(\?v=\w+)?(?=[\"')\s])", one, text)


def resolve(path):
    """The file production serves at an address (clean URLs, no trailing slash), or None."""
    path = re.split(r"[?#]", path)[0]
    if path == "/":
        return SITE / "index.html"
    for f in (SITE / path.lstrip("/"), SITE / path.lstrip("/") / "index.html"):
        if f.is_file():
            return f
    return None


def check_links():
    """Every internal link, asset and declared address in public/ must reach a file there:
    nothing points at a redirect, at a page that is gone, or at the preview."""
    bad = []
    for f in sorted(SITE.rglob("*")):
        if f.suffix not in (".html", ".css", ".xml", ".txt", ".webmanifest"):
            continue
        text = f.read_text()
        assert "/explorations" not in text, f
        if f.suffix == ".html" and f.name != "404.html":
            assert 'name="robots"' not in text, f
        refs = re.findall(r'(?:href|src|content)="(?:https://solvenadvisory\.ai)?(/[^"]*)"', text)
        refs += re.findall(r'url\("?(/[^")]+)"?\)', text)
        refs += re.findall(r"<loc>https://solvenadvisory\.ai(/[^<]*)</loc>", text)
        refs += re.findall(r'href="https://solvenadvisory\.ai(/[^"]*)"', text)
        # /_vercel/insights is served by Vercel itself (Web Analytics), not from public/
        bad += [f"{f.relative_to(SITE)}: {r}" for r in refs if not r.startswith(("//", "/_vercel/")) and not resolve(r)]
    # The old addresses in vercel.json: each must land on a page, and none may hide a live one
    for r in json.loads((ROOT / "vercel.json").read_text())["redirects"]:
        if "has" in r:  # host-only redirects send the vercel.app address to the apex
            continue
        targets = [r["destination"]]
        if ":slug" in r["destination"]:
            targets = [r["destination"].replace(":slug", a["slug"]) for a in ARTICLES["pt" if r["destination"].startswith("/pt/") else "en"]]
        bad += [f"vercel.json redirect {r['source']}: {d}" for d in targets if not resolve(d)]
        if ":" not in r["source"] and resolve(r["source"]):
            bad.append(f"vercel.json redirect {r['source']} hides a page that exists")
    if bad:
        raise SystemExit("Links to nothing in public/:\n  " + "\n  ".join(sorted(set(bad))))


def changed(files):
    """The last day any of these files changed: its last commit, or today if it has changes not yet committed."""
    days = []
    for f in files:
        rel = str(f.relative_to(ROOT))
        dirty = subprocess.run(["git", "status", "--porcelain", "--", rel], cwd=ROOT, capture_output=True, text=True).stdout
        day = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        days.append(date.today().isoformat() if dirty or not day else day)
    return max(days)


def sources(p):
    """The files a page is made from, for its lastmod: the copy, plus the insights it shows."""
    lang, t = p["lang"], COPY[p["lang"]]
    folder = INSIGHTS if lang == "en" else INSIGHTS / "pt"
    md_of = lambda a: folder / f"{a['slug']}.md"
    if p["path"] in ("", "pt"):
        return [COPY_FILE] + [md_of(a) for a in ARTICLES[lang][:3]]
    if p["path"] == t.insights.lstrip("/"):
        return [COPY_FILE] + [md_of(a) for a in ARTICLES[lang]]
    article = next((a for a in ARTICLES[lang] if p["path"] == f"{t.insights.lstrip('/')}/{a['slug']}"), None)
    return [md_of(article)] if article else [COPY_FILE]


def sitemap():
    """Every indexable page, with its counterpart in the other language and the day it last changed."""
    full = lambda path: v4.ORIGIN + ("/" + path if path else "/")
    rows = []
    for p in PAGES:
        if p["path"] in ("404", "pt/404"):
            continue
        en, pt = (p["path"], p["alt"]) if p["lang"] == "en" else (p["alt"], p["path"])
        pair = "" if p.get("unpaired") else f"""
    <xhtml:link rel="alternate" hreflang="en" href="{full(en)}"/>
    <xhtml:link rel="alternate" hreflang="pt-PT" href="{full(pt)}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{full(en)}"/>"""
        rows.append(f"""  <url>
    <loc>{full(p["path"])}</loc>
    <lastmod>{changed(sources(p))}</lastmod>{pair}
  </url>""")
    text = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(rows) + "\n</urlset>\n")
    (SITE / "sitemap.xml").write_text(text)
    print("public/sitemap.xml", len(rows), "pages")


def llms():
    """llms.txt (the index for language models) and llms-full.txt (the same, then every insight in full),
    both from the copy and the insights, so they say what the pages say and nothing else."""
    full = lambda path: v4.ORIGIN + path if path != "/" else v4.ORIGIN + "/"
    en, pt = COPY["en"], COPY["pt"]
    plain = lambda text: re.sub(r"\s+", " ", text).strip()

    def section(t, lang):
        rows = [f"- [{t.raw('nav.home')}]({full(t.home)}): {t.raw('home.description')}",
                f"- [{t.raw('nav.insights')}]({full(t.insights)}): {t.raw('insights.description')}",
                f"- [{t.raw('nav.book')}]({full(t.book)}): {t.raw('book.description')}",
                f"- [{t.raw('footer.privacy')}]({full(t.privacy)}): {t.raw('privacy.description')}"]
        rows += [f"- [{a['title']}]({full(t.insights + '/' + a['slug'])}): {a['description']}" for a in ARTICLES[lang]]
        return "\n".join(rows)

    services = "\n".join(f"- **{en.raw(f'home.service{i}.name')}**: {en.raw(f'home.service{i}.text')}"
                         for i in range(1, 9) if f"home.service{i}.name" in ENTRIES)
    convictions = "\n".join(f"- **{en.raw(f'home.conviction{i}.title')}** {en.raw(f'home.conviction{i}.text')}"
                            for i in range(1, 9) if f"home.conviction{i}.title" in ENTRIES)
    index = f"""# Solven Advisory

> {en.raw("home.description")}

{en.raw("home.hero.text")}

- Based in {en.raw("footer.city")}. Solven Advisory, Lda.
- Book a 30-minute call: {full(en.book)}
- LinkedIn: https://www.linkedin.com/company/solven-advisory
- The site is in English and in European Portuguese ({full(pt.home)}).

## {plain(en.raw("home.services.title")).rstrip(".")}

{services}

## {plain(en.raw("home.thesis")).rstrip(".")}

{convictions}

## Pages and insights

{section(en, "en")}

## Em português

{section(pt, "pt")}
"""
    articles = []
    for lang, folder in (("en", INSIGHTS), ("pt", INSIGHTS / "pt")):
        t = COPY[lang]
        for a in ARTICLES[lang]:
            _, body = md.front_matter((folder / f"{a['slug']}.md").read_text())
            articles.append(f"""## {a["title"]}

{full(t.insights + "/" + a["slug"])} · {a["topic"]} · {a["date"]}

{a["subtitle"]}

{body.strip()}
""")
    full_text = index + "\n# Insights in full\n\n" + "\n".join(articles)
    for name, text in (("llms.txt", index), ("llms-full.txt", full_text)):
        v4.check(text, name)
        assert "Partner Network" not in text and "/explorations" not in text, name
        (SITE / name).write_text(text)
        print(f"public/{name}", len(text.encode()), "bytes")


def pt_unreviewed():
    """The Portuguese the owner has not yet marked as reviewed: copy entries, then whole insights."""
    keys = [k for k, v in ENTRIES.items() if not v.get("pt_reviewed")]
    articles = [a for a in ARTICLES["pt"] if not a.get("reviewed")]
    return keys, articles


def pt_review_note():
    keys, articles = pt_unreviewed()
    if keys or articles:
        groups = {}
        for k in keys:
            groups[k.split(".")[0]] = groups.get(k.split(".")[0], 0) + 1
        print(f"warning: Portuguese not yet reviewed: {len(keys)} of {len(ENTRIES)} copy entries "
              f"({', '.join(f'{g} {n}' for g, n in groups.items())}) and {len(articles)} of {len(ARTICLES['pt'])} insights. "
              "List them with: python3 tools/build_site_v5.py --pt-review")


def pt_review_list():
    """--pt-review: every unreviewed Portuguese text beside its English, as a checklist for the owner."""
    keys, articles = pt_unreviewed()
    for k in keys:
        print(f"### {k}\nEN: {ENTRIES[k]['en']}\nPT: {ENTRIES[k]['pt']}\n")
    for a in articles:
        print(f"content/insights/pt/{a['slug']}.md (translation of content/insights/{a['en']}.md)\n")
    print(f"{len(keys)} copy entries and {len(articles)} insights to review. Mark each one reviewed with a line "
          "'PT reviewed: YYYY-MM-DD' under its PT line, or 'reviewed: YYYY-MM-DD' in the insight's header block.")


def write_pages():
    for p in PAGES:
        if PROD and p["path"] == "pt/404":
            continue    # production has one 404 page, in English with a line in Portuguese
        out = page_file(p["path"])
        text = links(page(p))
        v4.check(text, out)
        if p["lang"] == "pt":
            check_pt(text, out)
        assert "/explorations/site/" not in text.replace(PREVIEW + "/", ""), out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
        print(shown(out), len(text.encode()), "bytes")
    unused = set(ENTRIES) - COPY["en"].used - COPY["pt"].used
    if unused:
        raise SystemExit(f"{COPY_FILE.name}: not used by any page: {', '.join(sorted(unused))}")


def build_preview():
    SITE.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "explorations/site/img", SITE / "img", dirs_exist_ok=True)
    if (INSIGHTS / "images").is_dir():
        shutil.copytree(INSIGHTS / "images", SITE / "img/insights", dirs_exist_ok=True)
    shutil.copyfile(ROOT / "explorations/site/site.css", SITE / "site.css")
    shutil.copyfile(ROOT / "explorations/site/site.js", SITE / "site.js")
    write_pages()


# What a production build must contain besides the pages: if one is missing, the build stops
OUTPUT = ["sitemap.xml", "llms.txt", "llms-full.txt", "robots.txt", "site.webmanifest", "404.html",
          "assets/site/site.css", "assets/site/site-v5.css", "assets/site/site.js"]


def check_output():
    """The last checks before public/ is replaced: every required file is there, every stylesheet, script
    and image under /assets/site carries its content hash, and no placeholder marked dummy is left."""
    bad = [f"missing: {name}" for name in OUTPUT if not (SITE / name).is_file()]
    for f in sorted(SITE.rglob("*")):
        if f.suffix not in (".html", ".css"):
            continue
        text = f.read_text()
        for ref, v in re.findall(rf"({ASSETS}/[\w./-]+?\.\w+)(\?v=\w*)?(?=[\"')\s])", text):
            if not re.fullmatch(r"\?v=[0-9a-f]{10}", v):
                bad.append(f"{f.relative_to(SITE)}: {ref}{v} has no content hash")
        if f.suffix == ".html" and 'class="dummy"' in text:
            left = sorted(set(re.findall(r'class="dummy"[^>]*>([^<]*)<', text)))
            bad.append(f"{f.relative_to(SITE)}: placeholder left: {' · '.join(left) or 'class=dummy'}")
    if bad:
        raise SystemExit("public/ not replaced, the production build is incomplete:\n  " + "\n  ".join(bad))


def build_prod():
    if SITE.exists():
        shutil.rmtree(SITE)     # what a stopped build left behind
    shutil.copytree(ROOT / "assets", SITE / "assets")
    out = SITE / ASSETS.lstrip("/")
    (out / "img").mkdir(parents=True)
    for name, src in (("site.css", "explorations/site/site.css"), ("site-v5.css", "explorations/site-v5/site-v5.css")):
        (out / name).write_text((ROOT / src).read_text().replace("/explorations/site/img/", f"{ASSETS}/img/"))
    shutil.copyfile(ROOT / "explorations/site/site.js", out / "site.js")
    if (INSIGHTS / "images").is_dir():
        shutil.copytree(INSIGHTS / "images", out / "img/insights")
    for name in STATIC:
        shutil.copyfile(ROOT / name, SITE / name)
    write_pages()
    # Only the drawings the pages and stylesheets use, their paths written compactly (tools/svg_paths.py)
    files = [f for f in SITE.rglob("*") if f.suffix in (".html", ".css")]
    for name in sorted({n for f in files for n in re.findall(rf"{ASSETS}/img/([\w.-]+\.svg)", f.read_text())}):
        src = ROOT / "explorations/site/img" / name
        if not src.is_file():
            raise SystemExit(f"public/ not replaced: {ASSETS}/img/{name} is referenced but {src.relative_to(ROOT)} does not exist")
        (out / "img" / name).write_text(svg_paths.minify(src.read_text()))
    for f in sorted(files, key=lambda f: f.suffix != ".css"):    # stylesheets first: the pages stamp their hash
        f.write_text(stamp(f.read_text()))
    sitemap()
    llms()
    check_links()
    check_output()
    # Every check passed: the new build replaces public/ (generated, never edited, so nothing in it is lost)
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    SITE.rename(PUBLIC)
    print("public/ replaced:", sum(1 for f in PUBLIC.rglob("*") if f.is_file()), "files")


if __name__ == "__main__":
    if "--pt-review" in sys.argv[1:]:
        pt_review_list()
    else:
        build_prod() if PROD else build_preview()
        pt_review_note()
