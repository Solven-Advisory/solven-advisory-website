"""Site v5 preview: the site cut to three pages, at the owner's request (2026-10-18), in English and
European Portuguese (2026-10-19).

    python3 tools/build_site_v5.py

  Home          /               /pt                       the hint of everything: services, convictions, insights
  Insights      /insights       /pt/publicacoes           the index and the articles under it, written in Markdown
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
import json
import re
import shutil
import sys
from datetime import date, datetime
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

# ---------------------------------------------------------------- the copy, read from content/site-copy.md

COPY_FILE = ROOT / "content/site-copy.md"

# What is not copy: the language code, the date format and the page addresses in each language
SETTINGS = {
    "en": dict(html="en", locale="en_GB", ld_lang="en-GB", months=None,
               home="/", insights="/insights", book="/book", privacy="/privacy"),
    "pt": dict(html="pt-PT", locale="pt_PT", ld_lang="pt-PT",
               months=["jan.", "fev.", "mar.", "abr.", "mai.", "jun.", "jul.", "ago.", "set.", "out.", "nov.", "dez."],
               home="/pt", insights="/pt/publicacoes", book="/pt/marcar", privacy="/pt/privacidade"),
}


def read_copy(path):
    """content/site-copy.md: every text of the pages as "### name", then "EN: ..." and "PT: ...".
    Lines under EN: or PT: continue the text until a blank line; # headings and > notes are ignored."""
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
    f = rep(f, '<a href="/privacy">Privacy</a><span aria-hidden="true"> · </span><a href="/privacy#cookies">Cookie settings</a>',
            f'<a href="{t.privacy}">{t["footer.privacy"]}</a><span aria-hidden="true"> · </span><a href="{t.privacy}#cookies">{t["footer.cookies"]}</a>')
    return toggle(furniture(f, t), lang, path, alt)


def head(p, t):
    h = v4.head(p).replace(f'<link rel="stylesheet" href="{PREVIEW}/site.css?v=1">',
                           f'<link rel="stylesheet" href="{PREVIEW}/site.css?v=1">\n<link rel="stylesheet" href="{PREVIEW}/site-v5.css?v=9">')
    h = rep(h, '<html lang="en">', f'<html lang="{t.html}">')
    other = "pt_PT" if p["lang"] == "en" else "en_GB"
    h = rep(h, '<meta property="og:locale" content="en_GB">',
            f'<meta property="og:locale" content="{t.locale}">\n<meta property="og:locale:alternate" content="{other}">')
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

<a class="skip" href="#content">{t["label.skip"]}</a>

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
    return text.replace('title="Dummy text: replace before launch"', f'title="{t.attr("label.dummy_text")}"') \
               .replace('title="Dummy date: replace before launch"', f'title="{t.attr("label.dummy_date")}"')


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
    c = v4.close(t["close.title"], t["close.text"], art=art)
    c = rep(c, f"\n      <p class=\"close__note\">{v4.PARTNER}</p>", "")
    c = rep(c, '<a class="btn btn--primary" href="/contact#calendar">Book a call</a>', f'<a class="btn btn--primary" href="{t.book}">{t["nav.book"]}</a>')
    return rep(c, '<a class="text-link" href="/contact">Write to us</a>', f'<a class="text-link" href="mailto:{MAIL}">{t["close.write"]}</a>')


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
        label = f"{d.day} {t.months[d.month - 1]} {d.year}" if t.months else f"{d.day} {d:%b %Y}"
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
    meta = (f"{esc(a['topic'])} · " if topic else "") + f"{when(a)} · {t['article.minutes'].replace('{n}', str(a['minutes']))}"
    return f"""        <article class="icard">
          <h3 class="icard__title"><a href="{t.insights}/{a['slug']}">{md.inline(a['title'])}</a></h3>
          <p class="icard__sum">{md.inline(a['summary'])}</p>
          <p class="icard__meta">{meta}</p>
        </article>"""


def article_image(a, t):
    """The insight's photograph, chosen for each article. Until one is chosen, a marked placeholder."""
    if not a.get("image"):
        print(f"  note: {a['slug']} has no image yet; the page shows a placeholder")
        return f"""      <figure class="article__image article__image--empty">
        {dummy(t["article.image_missing"], t.attr("article.image_missing_note"))}
      </figure>"""
    return f"""      <figure class="article__image">
        <img src="{PREVIEW}/img/insights/{esc(a['image'])}" alt="{esc(a['image_alt'])}">
      </figure>"""


# ---------------------------------------------------------------- Home

def home(t, lang):
    cards = v4.cards([(n, x, "", None) for n, x in t.items("home.service", "name", "text")]).replace("service service--static", "service service--quiet")
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
    ld[0].update(description=t.raw("home.ld_description"), knowsAbout=t.raw("home.ld_topics").split(", "))
    return t.raw("home.tab_title"), t.raw("home.description"), main, dict(ld=ld)


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
    main = title_hero(t["home.insights.title"]) + f"""  <section class="section" aria-label="{t.attr("insights.all")}">
    <div class="wrap">
      <div class="insights__cards icards--wide">
{chr(10).join(icard(a, t, topic=True) for a in ARTICLES[lang])}
      </div>
    </div>
  </section>
""" + close(t, art="maat")
    blog = {"@context": "https://schema.org", "@type": "Blog", "name": t.raw("insights.ld_name"), "url": f"{v4.ORIGIN}{t.insights}", "publisher": v4.ORG,
            "blogPost": [{"@type": "BlogPosting", "headline": a["title"], "url": f"{v4.ORIGIN}{t.insights}/{a['slug']}"} for a in ARTICLES[lang]]}
    if lang == "pt":
        blog["inLanguage"] = t.ld_lang
    return t.raw("insights.tab_title"), t.raw("insights.description"), main, dict(ld=[blog])


both("insights", insights_index, nav="insights")


def article(a, lang, alt):
    """Each insight: title and subtitle on top, then the image, the tags, and the text across the page."""
    t = COPY[lang]
    own = f"{t.insights}/{a['slug']}"
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["title"], "description": a["description"],
          "datePublished": a["date"], "author": v4.ORG, "publisher": v4.ORG, "inLanguage": t.ld_lang,
          "mainEntityOfPage": f"{v4.ORIGIN}{own}", "url": f"{v4.ORIGIN}{own}", "image": f"{v4.ORIGIN}/assets/og.png"}
    if lang == "pt":
        ld["translationOfWork"] = {"@id": f"{v4.ORIGIN}/insights/{a['en']}"}
    add(lang, own[1:], alt, t.raw("article.tab_title").replace("{title}", a["title"]), a["description"],
        v4.hero(md.inline(a["title"]), md.inline(a["subtitle"]), cta=False, calcada=False)
        + f"""  <section class="section article" aria-label="{t.attr("article.label")}">
{article_image(a, t)}
    <div class="wrap">
      <ul class="article__tags" aria-label="{t.attr("article.tags_label")}">
        <li>{t['article.minutes'].replace('{n}', str(a['minutes']))}</li>
        <li>{esc(a['topic'])}</li>
        <li>{when(a)}</li>
      </ul>
      <article class="prose prose--wide">
{a['body']}
      </article>
      <p class="article__foot"><a class="btn btn--primary" href="{t.book}">{t["nav.book"]}</a><a class="text-link" href="{t.insights}">{t["insights.all"]}</a></p>
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
    main = title_hero(t["book.title"]) + f"""  <section class="section book" id="calendar" aria-label="{t.attr("book.calendar_label")}">
    <div class="wrap">
      <div class="cal" id="cal-inline"></div>
      <p class="cal__note">{t["book.fallback"].replace(' rel="noopener">', ' target="_blank" rel="noopener">')} {t["book.write"]} {email_icon(t)}</p>
    </div>
  </section>
"""
    return t.raw("book.tab_title"), t.raw("book.description"), main, dict(scripts=CAL_SCRIPT)


both("book", book, nav="book")

# ---------------------------------------------------------------- Privacy and 404

def privacy(t, lang):
    rows = "\n".join(f"""        <li class="row"{' id="cookies"' if i == 2 else ""}>
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
    return t.raw("privacy.tab_title"), t.raw("privacy.description"), main, {}


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
    main = v4.hero(t["notfound.title"], t["notfound.text"], cta=False, fill=True, extra=f"""
        <p class="nf__links">
          <a class="btn btn--primary" href="{t.home}">{t["notfound.back"]}</a>
          <a class="text-link" href="{t.insights}">{t["nav.insights"]}</a>
          <a class="text-link" href="{t.book}">{t["nav.book"]}</a>
        </p>""")
    return t.raw("notfound.tab_title"), t.raw("notfound.description"), main, {}


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
    unused = set(ENTRIES) - COPY["en"].used - COPY["pt"].used
    if unused:
        raise SystemExit(f"{COPY_FILE.name}: not used by any page: {', '.join(sorted(unused))}")
