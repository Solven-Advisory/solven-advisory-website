"""Site v5 preview: the site cut to three pages, at the owner's request (2026-10-18).

    python3 tools/build_site_v5.py

  Home          /               the hint of everything: services, convictions, insights
  Insights      /insights       the index and the articles under it, written in Markdown in content/insights/
  Book a call   /book           one line and the calendar
  plus Privacy and 404, which are legal and technical necessities, linked from the footer only.

The services, approach, about and contact pages are gone; their substance is a small section on
the homepage, and the contact details sit in every footer. Reuses site v4's parts
(tools/build_site_v4.py: head, hero, cards, closing, articles); writes explorations/site-v5/,
with its own copy of site v4's stylesheet plus a few rules (site-v5.css). Site v4 is unchanged.
"""
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

EMAIL = f'<a href="mailto:hello@example.com">{dummy("hello@example.com")}</a>'

# ---------------------------------------------------------------- header and footer: three pages

NAV = {"insights": ("/insights", "Insights")}


def header(here, pt, current):
    h = v4.HEADER
    h = re.sub(r'<ul class="nav">.*?</ul>',
               '<ul class="nav">\n          <li><a href="/insights"' + (' aria-current="page"' if current == "insights" else "") + '>Insights</a></li>\n        </ul>',
               h, flags=re.S)
    h = rep(h, 'href="/contact#calendar">Book a call</a>', 'href="/book"' + (' aria-current="page"' if current == "book" else "") + '>Book a call</a>')
    return v4.lang(h, here, pt)


FOOTER = v4.FOOTER
FOOTER = re.sub(r'<ul>\s*<li><a href="/approach">.*?</ul>', """<ul>
          <li><a href="/">Home</a></li>
          <li><a href="/insights">Insights</a></li>
          <li><a href="/book">Book a call</a></li>
        </ul>""", FOOTER, flags=re.S)
FOOTER = re.sub(r'<ul class="footer__contact">.*?</ul>', f"""<ul class="footer__contact">
        <li>Lisbon, Portugal</li>
        <li>{EMAIL}</li>
        <li><a href="tel:+351967130877">+351 967 130 877</a></li>
        <li><a href="https://www.linkedin.com/company/solven-advisory">LinkedIn</a></li>
      </ul>""", FOOTER, flags=re.S)


def page(p, main):
    here = "/" + p["path"] if p["path"] else "/"
    body = f"""<body>

<a class="skip" href="#content">Skip to content</a>

{header(here, p["pt"], p.get("nav"))}

<main id="content">
{main}
</main>

{v4.lang(FOOTER, here, p["pt"])}

<script src="{PREVIEW}/site.js?v=1"></script>
{p.get("scripts", "")}</body>
</html>
"""
    h = v4.head(p).replace(f'<link rel="stylesheet" href="{PREVIEW}/site.css?v=1">',
                           f'<link rel="stylesheet" href="{PREVIEW}/site.css?v=1">\n<link rel="stylesheet" href="{PREVIEW}/site-v5.css?v=3">')
    return h + "\n" + body


def links(s):
    """Production paths to the preview, as in v4."""
    s = s.replace('href="/contact#calendar"', 'href="/book"')
    def fix(m):
        path = m.group(1)
        if re.match(r"/(pt|assets|explorations)(/|$|#|\?)", path):
            return m.group(0)
        return f'href="{PREVIEW}{"" if path == "/" else path}"'
    s = re.sub(r'href="(/[^"]*)"', fix, s)
    return s.replace("/explorations/site/img/", f"{PREVIEW}/img/")


def close(art=None):
    c = v4.close(art=art)
    return rep(c, '<a class="text-link" href="/contact">Write to us</a>', '<a class="text-link" href="mailto:hello@example.com">Write to us</a>')


PAGES = []


def add(path, title, description, main, pt, **kw):
    PAGES.append(dict(path=path, title=title, description=description, main=main, pt=pt, **kw))


# ---------------------------------------------------------------- Insights, read from Markdown

INSIGHTS = ROOT / "content/insights"
REQUIRED = ("title", "subtitle", "summary", "description", "topic", "date")
WORDS_PER_MINUTE = 220


def body_image(src, alt):
    return f'<figure class="prose__image"><img src="{PREVIEW}/img/insights/{esc(src)}" alt="{esc(alt)}"></figure>'


def load_insights():
    """Every content/insights/<slug>.md, newest first. The file name is the address: /insights/<slug>."""
    out = []
    for f in sorted(INSIGHTS.glob("*.md")):
        if f.name == "README.md":
            continue
        meta, body = md.front_matter(f.read_text())
        missing = [k for k in REQUIRED if not meta.get(k)]
        if missing:
            raise SystemExit(f"{f.relative_to(ROOT)}: the header block is missing {', '.join(missing)}")
        if meta.get("image") and not meta.get("image_alt"):
            raise SystemExit(f"{f.relative_to(ROOT)}: the image needs a description (image_alt)")
        d = date.fromisoformat(meta["date"])
        out.append(dict(meta, slug=f.stem, body=md.to_html(body, image=body_image), label=f"{d.day} {d:%b %Y}",
                        placeholder=meta.get("date_is_placeholder", "no") == "yes",
                        minutes=int(meta.get("minutes") or max(1, round(md.words(body) / WORDS_PER_MINUTE)))))
    return sorted(out, key=lambda a: a["date"], reverse=True)


ARTICLES = load_insights()


def when(a):
    return v4.date_html(a["date"], a["label"], a["placeholder"])


def icard(a, topic=False):
    meta = (f"{esc(a['topic'])} · " if topic else "") + f"{when(a)} · {a['minutes']} min read"
    return f"""        <article class="icard">
          <h3 class="icard__title"><a href="/insights/{a['slug']}">{md.inline(a['title'])}</a></h3>
          <p class="icard__sum">{md.inline(a['summary'])}</p>
          <p class="icard__meta">{meta}</p>
        </article>"""


def article_image(a):
    """The insight's photograph, chosen for each article. Until one is chosen, a marked placeholder."""
    if not a.get("image"):
        print(f"  note: content/insights/{a['slug']}.md has no image yet; the page shows a placeholder")
        return f"""      <figure class="article__image article__image--empty">
        {dummy("Image to be chosen", "Placeholder: choose a photograph for this insight")}
      </figure>"""
    return f"""      <figure class="article__image">
        <img src="{PREVIEW}/img/insights/{esc(a['image'])}" alt="{esc(a['image_alt'])}">
      </figure>"""


# ---------------------------------------------------------------- Home

SERVICES = [
    ("Enablement", "Hands-on Claude sessions for the whole firm, analyst to managing partner, run monthly because the frontier moves weekly."),
    ("Build", "Agents and workflow systems on the real work: contract redlining, IC memo interrogation, portfolio reporting."),
    ("AI Diligence", "An independent read on whether a target's AI is genuine capability or marketing, before the term sheet is signed."),
    ("Token Economics", "Where the compute spend goes, what it returns, and how to pace it so the year's budget lasts the year."),
]
cards = v4.cards([(n, t, "", None) for n, t in SERVICES]).replace("service service--static", "service service--quiet")

HOME = f"""  <section class="hero" aria-labelledby="hero-title">
    <div class="hero__calcada" aria-hidden="true"><i></i><i></i></div>
    <div class="wrap grid">
      <h1 class="h1 hero__title" id="hero-title">Sharper judgment for the age of AI.</h1>
      <div class="hero__side">
        <p class="lead hero__lead">Solven trains private equity teams on AI and builds it into their workflows, so the people making the call still own the reasoning behind it.</p>
        <p class="hero__cta"><a class="btn btn--primary" href="/book">Book a call</a></p>
      </div>
    </div>
  </section>

  <section class="section services" id="services" aria-labelledby="services-title">
    <div class="wrap">
      <h2 class="h2" id="services-title">Four ways we work with a firm.</h2>
{cards}
    </div>
  </section>

  <section class="section why" id="approach" aria-labelledby="why-title">
    <div class="wrap">
      <h2 class="h2" id="why-title">Augmentation without cognitive atrophy.</h2>
      <ul class="convictions">
        <li class="conviction">
          <h3 class="h3">Judgment is the product.</h3>
          <p>In an investment firm the deliverable is a defensible decision; AI should make that judgment sharper, never thinner.</p>
        </li>
        <li class="conviction">
          <h3 class="h3">Fluency is firm-wide.</h3>
          <p>From the newest analyst to the managing partner, everyone should know where Claude belongs in their own work.</p>
        </li>
        <li class="conviction">
          <h3 class="h3">The frontier is the job.</h3>
          <p>Staying current is a standing discipline, not a one-off project, which is why our work is monthly.</p>
        </li>
      </ul>
    </div>
  </section>

  <section class="section insights" aria-labelledby="insights-title">
    <div class="wrap insights__split">
      <div class="insights__intro">
        <h2 class="h2" id="insights-title">Insights.</h2>
        <p>Short notes on AI in investment firms: what we see in the work, and what it means for partners.</p>
        <a class="btn" href="/insights">All insights</a>
      </div>
      <div class="insights__cards">
{chr(10).join(icard(a) for a in ARTICLES[:3])}
      </div>
    </div>
  </section>

""" + rep(close(art="maat"), f'      <p class="close__note">{v4.PARTNER}</p>\n', "")

add("", "Solven Advisory · AI enablement and implementation for investment firms",
    "Solven Advisory trains private equity teams on AI and builds it into their workflows, so the people making the call still own the reasoning behind it. Augmentation without cognitive atrophy.",
    HOME, "/pt", ld=v4.homepage()[1]["ld"])

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


add("insights", "Insights · Notes on AI for investment firms · Solven Advisory",
    "Short notes from Solven Advisory on AI in private equity, real estate and venture firms: what we see in the work, and what it means for partners.",
    title_hero("Insights.")
    + f"""  <section class="section" aria-label="All insights">
    <div class="wrap">
      <div class="insights__cards icards--wide">
{chr(10).join(icard(a, topic=True) for a in ARTICLES)}
      </div>
    </div>
  </section>
""" + close(art="maat"),
    "/pt/publicacoes", nav="insights",
    ld=[{"@context": "https://schema.org", "@type": "Blog", "name": "Solven Advisory insights", "url": f"{v4.ORIGIN}/insights", "publisher": v4.ORG,
         "blogPost": [{"@type": "BlogPosting", "headline": a["title"], "url": f"{v4.ORIGIN}/insights/{a['slug']}"} for a in ARTICLES]}])

# Each insight: title and subtitle on top, then the image, the tags, and the text across the page.
for a in ARTICLES:
    slug = a["slug"]
    add(f"insights/{slug}", f"{a['title']} · Insights · Solven Advisory", a["description"],
        v4.hero(md.inline(a["title"]), md.inline(a["subtitle"]), cta=False, calcada=False)
        + f"""  <section class="section article" aria-label="Article">
    <div class="wrap">
{article_image(a)}
      <ul class="article__tags" aria-label="About this insight">
        <li>{a['minutes']} min read</li>
        <li>{esc(a['topic'])}</li>
        <li>{when(a)}</li>
      </ul>
      <article class="prose prose--wide">
{a['body']}
      </article>
      <p class="article__foot"><a class="btn btn--primary" href="/book">Book a call</a><a class="text-link" href="/insights">All insights</a></p>
    </div>
  </section>
""",
        "/pt/publicacoes", nav="insights", og="article", published=a["date"],
        ld=[{"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["title"], "description": a["description"],
             "datePublished": a["date"], "author": v4.ORG, "publisher": v4.ORG, "inLanguage": "en-GB",
             "mainEntityOfPage": f"{v4.ORIGIN}/insights/{slug}", "url": f"{v4.ORIGIN}/insights/{slug}", "image": f"{v4.ORIGIN}/assets/og.png"}])

# ---------------------------------------------------------------- Book a call

add("book", "Book a call · Solven Advisory",
    "Book thirty minutes with a Solven Advisory co-founder, by video or phone.",
    title_hero("Book a call.") + """  <section class="section book" id="calendar" aria-label="Calendar">
    <div class="wrap">
      <div class="cal" id="cal-inline"></div>
      <p class="cal__note">If the calendar does not load, <a href="https://cal.eu/miguelmonteirosolven/30min" target="_blank" rel="noopener">open it in a new tab</a>. Prefer to write? """ + EMAIL + """</p>
    </div>
  </section>
""",
    "/pt", nav="book",
    # Straight to the 30-minute event's date picker: one step fewer than the event list
    scripts=re.search(r'<script>\n  /\* Inline booking calendar.*?</script>\n', [p for p in v4.PAGES if p["path"] == "contact"][0]["scripts"], re.S).group(0)
    .replace('calLink: "miguelmonteirosolven"', 'calLink: "miguelmonteirosolven/30min"'))

# ---------------------------------------------------------------- Privacy and 404

priv = [p for p in v4.PAGES if p["path"] == "privacy"][0]
pm = priv["main"]
# No contact form any more: its sentences go; booking and email stay
pm = re.sub(r"If you use the contact form, we receive the details you type: name, firm, email address, and your message\. "
            r"The form is delivered to our inbox by FormSubmit, a form-forwarding service; we use the details only to reply to you\. ", "", pm)
pm = pm.replace("We process contact and booking details", "We process booking details and correspondence")
pm = pm.replace(" Form delivery passes through FormSubmit.", "")
pm = pm.replace("who visit this site, write to us, or book a call.", "who visit this site, write to us, or book a call.")
assert "FormSubmit" not in pm and "contact form" not in pm
add("privacy", priv["title"], priv["description"], pm, "/pt")

nf = [p for p in v4.PAGES if p["path"] == "404"][0]
nfm = rep(nf["main"], '<a class="text-link" href="/services">Services</a>', '<a class="text-link" href="/insights">Insights</a>')
nfm = rep(nfm, '\n          <a class="text-link" href="/contact#calendar">Book a call</a>', '\n          <a class="text-link" href="/book">Book a call</a>')
add("404", nf["title"], nf["description"], nfm, "/pt")


if __name__ == "__main__":
    SITE.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "explorations/site/img", SITE / "img", dirs_exist_ok=True)
    if (INSIGHTS / "images").is_dir():
        shutil.copytree(INSIGHTS / "images", SITE / "img/insights", dirs_exist_ok=True)
    shutil.copyfile(ROOT / "explorations/site/site.css", SITE / "site.css")
    shutil.copyfile(ROOT / "explorations/site/site.js", SITE / "site.js")
    for p in PAGES:
        out = SITE / p["path"] / "index.html"
        text = links(page(p, p["main"]))
        v4.check(text, out)
        assert "/explorations/site/" not in text.replace(PREVIEW + "/", ""), out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
        print(out.relative_to(ROOT), len(text.encode()), "bytes")
