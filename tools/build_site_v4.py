"""Site v4 preview: every page of the site in the ledger-v4 design language, under explorations/site/.

    python3 tools/build_site_v4.py

The homepage is explorations/ledger-v4/index.html with its stylesheet cascade replaced by
explorations/site/site.css, its inline scripts by explorations/site/site.js, its head by the
production head (title, description, canonical, Open Graph, Twitter) and its internal links pointed
inside the preview. Every other page shares the same head, header, footer and logo, taken from
ledger-v4 by this script. Article bodies and FAQ answers are read verbatim from the live pages
(blog/<slug>.html, programmes.html, contact.html), so they cannot drift.

Internal links are written as production paths (/services/build) and rewritten to the preview
(/explorations/site/services/build) at the end; /pt links stay as they are (no PT build yet).
Canonicals point at the future production URLs on https://solvenadvisory.ai.
Nothing here touches the production pages, ledger-v4 or the other explorations.
"""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEGACY = ROOT / "legacy-site"   # the pre-v5 site, whose content these pages are read from
SITE = ROOT / "explorations/site"
PREVIEW = "/explorations/site"
ORIGIN = "https://solvenadvisory.ai"
V4 = (ROOT / "explorations/ledger-v4/index.html").read_text()
IMAGES = ["calcada-wave.svg", "maat.svg", "padrao.svg", "belem.svg", "ponte-25-de-abril.svg",
          "farol-do-bugio.svg", "skyline.svg"]
EMDASH, ENDASH = chr(0x2014), chr(0x2013)
# Names that must never appear in the preview, spelt in parts so this file stays clean of them too
GONE_PAGE, OLD_BADGE, FOUNDER = "AI " + "Flix", "Phase " + "1", "Miguel " + "Monteiro"


def grab(pattern, text=V4):
    m = re.search(pattern, text, re.S)
    assert m, pattern
    return m.group(0)


def rep(s, a, b, n=1):
    assert s.count(a) == n, (a, s.count(a))
    return s.replace(a, b)


def dummy(text, title="Dummy text: replace before launch"):
    return f'<span class="dummy" title="{title}">{text}</span>'


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- shared parts from ledger-v4

HEADER = grab(r'<header class="header cta-quiet">.*?</header>')
FOOTER = grab(r'<footer class="footer">.*?</footer>')
AZ = re.findall(r'<div class="service__az" aria-hidden="true">.*?</svg></span></div>', V4, re.S)
assert len(AZ) == 4
PARTNER = dummy("Member of the Anthropic Partner Network")

NAV_KEYS = {"approach": "/approach", "services": "/services", "insights": "/insights", "about": "/about", "contact": "/contact"}


def header(nav, here, pt, quiet):
    h = HEADER
    if not quiet:
        h = rep(h, '<header class="header cta-quiet">', '<header class="header">')
    if nav:
        href = NAV_KEYS[nav]
        h = rep(h, f'<li><a href="{href}">', f'<li><a href="{href}" aria-current="page">')
    return lang(h, here, pt)


def lang(block, here, pt):
    block = rep(block, '<a href="/" lang="en" hreflang="en" aria-current="true">EN</a>',
                f'<a href="{here}" lang="en" hreflang="en" aria-current="true">EN</a>')
    return rep(block, '<a href="/pt" lang="pt-PT" hreflang="pt-PT">PT</a>',
               f'<a href="{pt}" lang="pt-PT" hreflang="pt-PT">PT</a>')


def head(p):
    url = ORIGIN + (p["path"] and "/" + p["path"])
    if not p["path"]:
        url = ORIGIN + "/"
    t, d = esc(p["title"]), esc(p["description"])
    ld = "".join(f'\n<script type="application/ld+json">\n{json.dumps(x, indent=2, ensure_ascii=False)}\n</script>' for x in p.get("ld", []))
    extra = ""
    if p.get("published"):
        extra = f'\n<meta property="article:published_time" content="{p["published"]}">'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{p.get('og', 'website')}">
<meta property="og:site_name" content="Solven Advisory">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{ORIGIN}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_GB">{extra}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{ORIGIN}/assets/og.png">
<link rel="icon" type="image/svg+xml" href="/assets/logos/05_solven_favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,300..700&family=Source+Sans+3:wght@400;500&display=swap">
<link rel="stylesheet" href="{PREVIEW}/site.css?v=1">
<script>document.documentElement.classList.add("js")</script>{ld}
</head>"""


def page(p, main):
    here = "/" + p["path"] if p["path"] else "/"
    quiet = 'class="hero' in main
    body = f"""<body>

<a class="skip" href="#content">Skip to content</a>

{header(p.get("nav"), here, p["pt"], quiet)}

<main id="content">
{main}
</main>

{lang(FOOTER, here, p["pt"])}

<script src="{PREVIEW}/site.js?v=1"></script>
{p.get("scripts", "")}</body>
</html>
"""
    return head(p) + "\n" + body


def preview_links(s):
    """Production paths to preview paths, for every internal link that is not PT, an asset or already inside."""
    def fix(m):
        attr, path = m.group(1), m.group(2)
        if re.match(r"/(pt|assets|explorations)(/|$|#|\?)", path):
            return m.group(0)
        return f'{attr}="{PREVIEW}{"" if path == "/" else path}"' if not path.startswith("/#") else f'{attr}="{PREVIEW}{path[1:]}"'
    return re.sub(r'(href)="(/[^"]*)"', fix, s)


# ---------------------------------------------------------------- building blocks

def hero(title, lead, cta=True, calcada=True, extra="", fill=False):
    cal = '    <div class="hero__calcada" aria-hidden="true"><i></i><i></i></div>\n' if calcada else ""
    button = '\n        <p class="hero__cta"><a class="btn btn--primary" href="/contact#calendar">Book a call</a></p>' if cta else ""
    cls = "hero hero--page" + ("" if calcada else " hero--plain") + (" hero--fill" if fill else "")
    return f"""  <section class="{cls}" aria-labelledby="hero-title">
{cal}    <div class="wrap grid">
      <h1 class="h1 hero__title" id="hero-title">{title}</h1>
      <div class="hero__side">
        <p class="lead hero__lead">{lead}</p>{button}{extra}
      </div>
    </div>
  </section>
"""


def shead(h2, sid, lead=None, cls=""):
    l = f'\n        <p class="shead__lead">{lead}</p>' if lead else ""
    return f"""      <div class="shead{cls}">
        <h2 class="h2" id="{sid}">{h2}</h2>{l}
      </div>"""


def cards(items, static=True, three=False, start=0):
    """items: (title, text, extra_html, href or None). Each card is headed by one of the owner's azulejos."""
    out = []
    for i, (title, text, extra, href) in enumerate(items):
        az = AZ[(start + i) % 4]
        t = f'<a href="{href}">{title}</a>' if href else title
        cls = "service" + (" service--static" if not href else "")
        p = f"\n          <p>{text}</p>" if text else ""
        out.append(f"""        <article class="{cls}">
          {az}
          <h3 class="h3">{t}</h3>{p}{extra}
        </article>""")
    grid = "services__grid" + (" services__grid--3" if three else "")
    return f'      <div class="{grid}">\n' + "\n".join(out) + "\n      </div>"


def dark(h2, sid, items, lead=None, link=None, cols=3):
    l = f'\n      <p class="why__lead">{lead}</p>' if lead else ""
    mod = {3: "", 4: " convictions--4", 2: " convictions--2"}[cols]
    lis = "\n".join(f"""        <li class="conviction">
          <h3 class="h3">{h}</h3>
          <p>{t}</p>{x}
        </li>""" for h, t, x in items)
    sl = f'\n      <a class="section-link" href="{link[1]}">{link[0]}</a>' if link else ""
    return f"""  <section class="section why" aria-labelledby="{sid}">
    <div class="wrap">
      <h2 class="h2" id="{sid}">{h2}</h2>{l}
      <ul class="convictions{mod}">
{lis}
      </ul>{sl}
    </div>
  </section>
"""


ART = {
    "maat": '<div class="close__maat" aria-hidden="true"><img src="/explorations/site/img/maat.svg" alt="" width="1505" height="749" loading="lazy"></div>',
    "ponte": '<div class="close__art close__art--ponte close__art--right" aria-hidden="true"><img src="/explorations/site/img/ponte-25-de-abril.svg" alt="" width="4000" height="1238" loading="lazy"></div>',
    "belem": '<div class="close__art close__art--belem close__art--right" aria-hidden="true"><img src="/explorations/site/img/belem.svg" alt="" width="1395" height="1148" loading="lazy"></div>',
    "padrao": '<div class="close__art close__art--padrao close__art--right" aria-hidden="true"><img src="/explorations/site/img/padrao.svg" alt="" width="1500" height="1500" loading="lazy"></div>',
    "farol": '<div class="close__art close__art--farol close__art--left" aria-hidden="true"><img src="/explorations/site/img/farol-do-bugio.svg" alt="" width="3440" height="2205" loading="lazy"></div>',
    "skyline": '<div class="close__art close__art--skyline" aria-hidden="true"></div>',
}

CLOSE_HOME = ("Let's tune a programme to your firm's priorities.",
              "A short conversation is the fastest way to see where Claude belongs in your team's work, and where it shouldn't.")


def close(h2=CLOSE_HOME[0], line=CLOSE_HOME[1], art=None):
    a = f"    {ART[art]}\n" if art else ""
    cls = "section close" + (" close--skyline" if art == "skyline" else "")
    return f"""  <section class="{cls}" aria-labelledby="close-title">
{a}    <div class="wrap grid">
      <div class="close__head">
        <h2 class="h2" id="close-title">{h2}</h2>
      </div>
      <div class="close__body">
        <p class="lead">{line}</p>
        <p class="close__actions">
          <a class="btn btn--primary" href="/contact#calendar">Book a call</a>
          <a class="text-link" href="/contact">Write to us</a>
        </p>
      </div>
      <p class="close__note">{PARTNER}</p>
    </div>
  </section>
"""


# ---------------------------------------------------------------- content read from the live site

def faq_from(path):
    s = (LEGACY / path).read_text()
    items = re.findall(r'<summary>(.*?)</summary>\s*<div class="faq__a"><p>(.*?)</p></div>', s, re.S)
    return [(html.unescape(q.strip()), a.strip()) for q, a in items]


FAQ = faq_from("programmes.html")
assert len(FAQ) == 10, len(FAQ)
FAQ_CONTACT = faq_from("contact.html")
assert len(FAQ_CONTACT) == 3
for q, a in FAQ_CONTACT:   # the three shared answers, word for word
    assert (q, a) in FAQ, q
SHARED = [q for q, _ in FAQ_CONTACT]


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub(r"<[^>]+>", "", a))}} for q, a in items]}


# slug, title, topic, ISO date, shown date, dummy date?, one-line summary (homepage), standfirst (live)
ARTICLES = [
    ("editors-of-drafts-they-cannot-defend", "Editors of drafts they cannot defend", "AI adoption", "2026-10-02", "2 Oct 2026", True,
     "Why the real risk in AI rollouts is cognitive offloading, not adoption failure."),
    ("how-to-tell-whether-the-ai-is-real", "How to tell whether the AI is real", "AI diligence", "2026-09-09", "9 Sep 2026", True,
     "A working method for AI diligence."),
    ("making-every-token-earn-its-place", "Making every token earn its place", "Token economics", "2026-07-28", "28 Jul 2026", False,
     "Why AI spend behaves nothing like software licences."),
]


def article_src(slug):
    s = (LEGACY / f"blog/{slug}.html").read_text()
    body = re.search(r'<article class="prose reveal">\n?(.*?)</article>', s, re.S).group(1).strip()
    body = body.replace('href="/contact#book"', 'href="/contact#calendar"')
    lead = re.search(r'<p class="lead[^"]*"[^>]*>(.*?)</p>', s, re.S).group(1)
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    return body, lead, desc


def date_html(iso, label, is_dummy):
    shown = dummy(label, "Dummy date: replace before launch") if is_dummy else label
    return f'<time datetime="{iso}">{shown}</time>'


def icard(a, topic=False, long=False):
    slug, title, top, iso, label, dum, short = a
    summ = article_src(slug)[1] if long else short
    meta = (f"{top} · " if topic else "") + date_html(iso, label, dum) + " · 4 min read"
    return f"""        <article class="icard">
          <h3 class="icard__title"><a href="/insights/{slug}">{title}</a></h3>
          <p class="icard__sum">{summ}</p>
          <p class="icard__meta">{meta}</p>
        </article>"""


ORG = {"@type": "Organization", "@id": f"{ORIGIN}/#organization", "name": "Solven Advisory", "url": f"{ORIGIN}/"}

# ---------------------------------------------------------------- pages

PAGES = []


def add(path, title, description, main, pt, nav=None, **kw):
    PAGES.append(dict(path=path, title=title, description=description, main=main, pt=pt, nav=nav, **kw))


# -------- Services hub
SERVICES = [
    ("Enablement", "Learn the tools, at every level of the firm. Hands-on Claude sessions for the whole team, from the newest analyst to the managing partner, in a four-session arc from first principles to building with the most advanced tools in the suite.", "/services/enablement"),
    ("Build", "Then build AI systems on your workflows. Agents, automation and workflow systems applied to the real work: contract redlining, IC memo interrogation, portfolio reporting. Build hours pair with the training, so confidence becomes real systems.", "/services/build"),
    ("AI Diligence", "And tell real AI from marketing jargon. We pressure-test whether a target or a pitching founder is genuinely AI-native, or simply fluent in the vocabulary, before the term sheet is signed.", "/services/ai-diligence"),
    ("Token Economics", "And make every token earn its place. Where your compute spend actually goes, what it returns, and how to pace it, so the firm's token budget lasts the full year, not the first quarter.", "/services/token-economics"),
]
PRACTICES = [
    ("Diligence and deal flow", "First-pass diligence, question banks, comparables, data room synthesis and sourcing screens, all defensible at investment committee.", "Deal team"),
    ("Portfolio operations", "Board packs, quarterly reports, KPI monitoring and variance flagging that scale with the portfolio, not the headcount.", "Portfolio team"),
    ("Investor relations and compliance", "LP letters, capital call narratives, and SFDR, CSRD and ESG workflows, at the cadence investors expect and with the audit trail intact.", "CFO and IR"),
    ("Knowledge and methodology", "Institutional memory, workflow playbooks, and analyst training in the AI-as-adversary method that holds under pressure.", "Managing partner"),
]
rows = "\n".join(f"""        <li class="row">
          <h3 class="h3 row__h">{h}</h3>
          <p class="row__p">{t}</p>
          <p class="row__aside">{a}</p>
        </li>""" for h, t, a in PRACTICES)
add("services", "Services · Solven Advisory",
    "Four ways Solven Advisory works with investment firms: Claude enablement programmes, build work on real workflows, AI diligence on targets, and token economics.",
    hero("Four ways we work with a firm.", "We train entire investment teams on AI, then build AI systems on the workflows that matter. Each engagement is scoped to the firm, and each is designed to sharpen judgment rather than substitute for it.")
    + f"""  <section class="section services" aria-labelledby="svc-title">
    <div class="wrap">
      <h2 class="sr" id="svc-title">Services</h2>
{cards([(n, t, "", h) for n, t, h in SERVICES])}
    </div>
  </section>
  <section class="section" aria-labelledby="practices-title">
    <div class="wrap">
{shead("Four practices, four entry points into the firm.", "practices-title", "Each maps to a different seat at the table.")}
      <ul class="rows">
{rows}
      </ul>
    </div>
  </section>
""" + dark("Built to flex around the firm.", "flex-title", [
        ("Month to month.", "Programmes run monthly with no minimum commitment. Stay as long as the frontier keeps moving, which is to say, as long as it is useful.", ""),
        ("Sessions plus build hours.", "Training pairs with optional build and consulting hours, so confidence from the room turns into real systems on real workflows.", ""),
        ("On site or remote.", "Delivered at your office in Lisbon, remotely, or a mix. The format follows the team, not the other way round.", ""),
        ("Open to the whole firm.", "Analyst to managing partner. Fluency is a firm-wide capability, not a specialism held by a few.", ""),
    ], lead="Each engagement is scoped and priced individually.", cols=4) + close(),
    "/pt/servicos", nav="services",
    ld=[{"@context": "https://schema.org", "@type": "ItemList", "name": "Services",
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": f"{ORIGIN}{h}"} for i, (n, _, h) in enumerate(SERVICES)]}])

# -------- Enablement
SESSIONS = [
    ("Session one · Foundations", "How AI thinks: understand what a model is doing well enough to know when to trust it, and when to push back.",
     ["The history of AI through the transformer breakthrough", "Tokens, embeddings, vectors and attention", "How generation works: probability, sampling, run-to-run variance", "Where Claude is sharpest, where it fails, and why hallucinations happen", "The analyst-first principle and the habit of verification"]),
    ("Session two · Conversation", "Claude.ai: the prompting craft that separates competent output from compelling, and the devil's advocate pattern at its core.",
     ["The interface: chat, Projects, Memory, files, web search, Artifacts", "Structured prompting: XML tagging, role framing, output specs", "Few-shot prompting, chain-of-thought and metaprompting", "The devil's advocate pattern: Claude as critic, not author", "Context-window management, token economics, knowing when to stop"]),
    ("Session three · Production", "Claude in the tools you already use: where the team's deliverables actually live, in the workbook, the deck and across the desktop.",
     ["Claude for Excel: formula generation, audit trails, financial models, cross-sheet reasoning", "Claude for PowerPoint: decks from outlines, brand-aligning, IC-ready memos", "Claude Cowork: desktop automation and multi-app workflows", "The bigger idea: tools and function calling"]),
    ("Session four · Construction", "Building with Claude Code: the most capable tool in the suite, far beyond a developer tool, where AI-native workflows compound month over month.",
     ["The agentic loop, version-controlled prompts and markdown fluency", "Skills and SKILL.md: packaging team expertise as deployable capability", "MCP: connecting Claude to databases, APIs and internal systems", "Automation patterns: structured extraction, batch processing, report generation"]),
]
SESSION_CARDS = [(h, t, '\n          <ul class="service__list">' + "".join(f"<li>{x}</li>" for x in topics) + "</ul>", None) for h, t, topics in SESSIONS]
faq_items = "\n".join(f"""        <details class="faq__item">
          <summary>{esc(q)}</summary>
          <p class="faq__a">{a}</p>
        </details>""" for q, a in FAQ)
add("services/enablement", "Enablement · Claude training for investment firms · Solven Advisory",
    "Solven's enablement programmes bring genuine AI fluency to every level of an investment firm, analyst to partner: a four-session arc from first principles to building with Claude Code, monthly because the frontier is weekly.",
    hero("Genuine AI fluency at every level of the firm, from analyst to partner.",
         "Hands-on Claude sessions that take an entire firm from first principles to building with the most advanced tools in the suite. Our programmes are monthly because the technology is weekly.")
    + f"""  <section class="section services" aria-labelledby="arc-title">
    <div class="wrap">
{shead("The four-session arc.", "arc-title", "Every session carries the analyst-first principle: analysts produce the formative work first, then bring Claude in as a critic, a red-teamer and a verifier.")}
{cards(SESSION_CARDS)}
    </div>
  </section>
""" + dark("The frontier moves weekly. We keep your team on it.", "frontier-title", [
        ("Hands-on, on the real work.", "Sessions run on the firm's actual deals, models, memos and reports, so each person leaves knowing where Claude fits their day.", ""),
        ("Month one is breadth.", "Orientation across the full Claude suite, from first principles to building, so the whole team shares a map of what is possible.", ""),
        ("From month two, we go deep.", "Later sessions concentrate on the areas the team finds most valuable. The arc stays; the path adapts.", ""),
        ("Trainers read the room.", "The topics are guidance, not a script. Pace and emphasis follow the people in the room, analyst to partner.", ""),
    ], lead="A team trained once is a team falling behind. A firm that trained six months ago is already operating on stale knowledge.", link=("Our approach", "/approach"), cols=4)
    + f"""  <section class="section" aria-labelledby="faq-title">
    <div class="wrap faq">
      <div class="faq__head">
        <h2 class="h2" id="faq-title">Questions firms ask before they book.</h2>
        <p class="shead__lead">Straight answers to the questions that usually precede the first call. Anything unanswered here is a good opening for the call itself.</p>
      </div>
      <div class="faq__list">
{faq_items}
      </div>
    </div>
  </section>
""" + close("A conversation to tune the programme to your firm's priorities.",
            "Tell us where your team is today and what the next quarter looks like. We will shape the arc around it.", art="padrao"),
    "/pt/servicos/enablement", nav="services",
    ld=[{"@context": "https://schema.org", "@type": "Service", "name": "Claude enablement programmes", "serviceType": "AI enablement",
         "provider": ORG, "areaServed": ["Portugal", "Spain", "United Kingdom"],
         "audience": {"@type": "BusinessAudience", "audienceType": "Private equity, real estate and venture firms"},
         "url": f"{ORIGIN}/services/enablement"}, faq_ld(FAQ)])

# -------- Build
BUILDS = [
    ("Contract redlining", "An agent that extracts and compares lease and financing terms across documents, surfacing deviations for a human reviewer to rule on."),
    ("IC memo interrogation", "An agent that stress-tests investment-committee papers before presentation: the devil's advocate pattern, operationalised."),
    ("Portfolio reporting", "An ingestion, normalisation and verification layer that meets founders in email, WhatsApp, Notion, Excel or PowerPoint, and reconciles everything into one portfolio view, with the source for every figure preserved."),
    ("Discovery and scoping", "Before any build, a map of where AI belongs across deal evaluation and memo workflows, the judgment that must stay human, and the enablement the team needs."),
]
add("services/build", "Build · AI systems for investment firms · Solven Advisory",
    "Solven builds agents and workflow systems on the real work of investment firms: contract redlining, IC memo interrogation and portfolio reporting, paired with firm-wide Claude training.",
    hero("Agents and workflow systems on the real work.",
         "Build hours pair with the training, so confidence from the room turns into real systems on the diligence, financing, committee and reporting workflows that fill an investment team's week.")
    + f"""  <section class="section services" aria-labelledby="build-title">
    <div class="wrap">
{shead("What we build.", "build-title", "Described by the work itself, by workflow and structure, with no metrics we cannot stand behind.")}
{cards([(h, t, "", None) for h, t in BUILDS])}
    </div>
  </section>
""" + dark("Enablement and build, on real workflows.", "both-title", [
        ("How we train.", "A monthly enablement programme across the whole firm, analyst to partner, designed the adversary-first way, so the team builds verification habits as it builds fluency.", '\n          <a class="text-link" href="/services/enablement">Enablement</a>'),
        ("What we build.", "A build track alongside it that turns the most repetitive, judgment-heavy reviews into supervised agents, designed to challenge and verify human reasoning, never to quietly replace it.", '\n          <a class="text-link" href="/approach">Our approach</a>'),
    ], lead="How the two sides of the work fit together on the workflows that fill an investment team's week.", cols=2)
    + close("There is probably a workflow on your desk that fits.",
            "If a recurring, judgment-heavy process comes to mind, that is usually the right place to start.", art="ponte"),
    "/pt/servicos/build", nav="services",
    ld=[{"@context": "https://schema.org", "@type": "Service", "name": "AI build work for investment firms", "serviceType": "AI implementation",
         "provider": ORG, "url": f"{ORIGIN}/services/build"}])

# -------- AI Diligence
PITCH = ["“Proprietary AI engine.”", "“AI-native from day one.”", "“Our models are the moat.”", "“The workflow is fully automated.”"]
SURFACE = ["The stack behind the story: built in-house, or a thin wrapper on a model anyone can rent.",
           "Whether the data and models are genuinely defensible, or commodity dressed up as a moat.",
           "Whether the team can ship what they claim, at the velocity they claim.",
           "Where AI actually touches the P&amp;L, and where it is theatre for the raise."]
add("services/ai-diligence", "AI Diligence · Solven Advisory",
    "Independent AI diligence for funds: a defensible read on whether a target's AI is genuine capability or marketing, before the term sheet is signed.",
    hero("Find out whether the AI is real.",
         "When a target or a founder claims to be “AI-powered,” we give the fund a defensible read on what is genuine capability and what is marketing jargon, before the term sheet.")
    + f"""  <section class="section" aria-labelledby="surface-title">
    <div class="wrap">
{shead("The pitch, and what we surface.", "surface-title")}
      <div class="lists">
        <div>
          <p class="list__label">The pitch</p>
          <ul class="list list--quotes">{''.join(f'<li>{x}</li>' for x in PITCH)}</ul>
        </div>
        <div>
          <p class="list__label">What we surface</p>
          <ul class="list">{''.join(f'<li>{x}</li>' for x in SURFACE)}</ul>
        </div>
      </div>
    </div>
  </section>
""" + f"""  <section class="section why" aria-labelledby="deliv-title">
    <div class="wrap">
      <h2 class="h2" id="deliv-title">A clear read for the investment committee.</h2>
      <p class="why__lead">The deliverable covers what is real, what is veneer, and what it changes about the price.</p>
      <a class="section-link" href="/insights/how-to-tell-whether-the-ai-is-real">How to tell whether the AI is real</a>
    </div>
  </section>
""" + close(art="belem"),
    "/pt/servicos/ai-diligence", nav="services",
    ld=[{"@context": "https://schema.org", "@type": "Service", "name": "AI due diligence", "serviceType": "AI due diligence",
         "provider": ORG, "url": f"{ORIGIN}/services/ai-diligence"}])

# -------- Token Economics
TOKENS = [
    ("Usage analytics", "A clear read on where tokens go, by team, workflow, model and prompt, so the spend that was invisible becomes legible."),
    ("ROI analytics", "What each token actually returns. Cost measured per outcome, not per call, so you can see which workflows earn their keep and which don't."),
    ("Efficiency", "Right-sized models, prompt caching and tighter context: the same output for a fraction of the spend, without dropping quality."),
    ("Budget pacing", "Forecasts and guardrails that keep consumption tracking the year, so there are no surprises and no scramble in the fourth quarter."),
]
add("services/token-economics", "Token Economics · Solven Advisory",
    "Where an investment firm's AI compute spend goes, what it returns, and how to pace it so the year's budget lasts the year: a token P&L the partners can read.",
    hero("Make every token earn its place.",
         "An unmanaged compute budget has a way of being gone by March. We show you where the tokens went, what they returned, and how to make the year's budget last the year.")
    + f"""  <section class="section services" aria-labelledby="te-title">
    <div class="wrap">
{shead("Where the tokens go, and what they return.", "te-title")}
{cards([(h, t, "", None) for h, t in TOKENS])}
    </div>
  </section>
  <section class="section why" aria-labelledby="pnl-title">
    <div class="wrap">
      <h2 class="h2" id="pnl-title">A token P&amp;L the partners can read.</h2>
      <p class="why__lead">The deliverable shows what each workflow costs, what it earns, and the changes that stretch the same budget across the whole year.</p>
      <a class="section-link" href="/insights/making-every-token-earn-its-place">Making every token earn its place</a>
    </div>
  </section>
""" + close(),
    "/pt/servicos/token-economics", nav="services",
    ld=[{"@context": "https://schema.org", "@type": "Service", "name": "Token economics", "serviceType": "AI cost management",
         "provider": ORG, "url": f"{ORIGIN}/services/token-economics"}])

# -------- Approach
PRACTICE = [
    ("Analyst-first", "The analyst produces a defensible first pass before engaging the model."),
    ("Show your work", "Appendices make the human contribution legible to senior reviewers."),
    ("Verification", "The devil's advocate pattern is built into the workflow, not bolted on."),
    ("Calibration", "Senior-led reviews surface drift before it compounds across the team."),
]
add("approach", "Our approach · Augmentation without cognitive atrophy · Solven Advisory",
    "The thesis behind Solven Advisory: augmentation without cognitive atrophy. AI as a critic, red-teamer and verifier of the analyst's reasoning, not a generator of it.",
    hero("Augmentation without cognitive atrophy.",
         "The risk in enterprise AI is not adoption failure. It is what happens to analytical judgment when adoption succeeds.", cta=False)
    + """  <section class="section" aria-label="The risk and the principle">
    <div class="wrap pair">
      <div class="pair__item">
        <h2 class="h2">Cognitive offloading.</h2>
        <p>When an analyst can produce a polished draft in a single prompt, the formative work quietly stops happening: sitting with the data, building a position from first principles, defending a number under pressure.</p>
        <p>The analyst becomes a passive editor of model output. Quality looks the same on the page; the underlying judgment thins out.</p>
      </div>
      <div class="pair__item">
        <h2 class="h2">AI as adversary, not author.</h2>
        <p>We treat the model as a stress-tester of the analyst's reasoning, not a generator of it. The analyst forms a position first; the model challenges it.</p>
        <p>Used this way, AI sharpens the very skills that unconstrained use erodes. The output is better and the judgment behind it is stronger.</p>
      </div>
    </div>
  </section>
""" + f"""  <section class="section services" aria-labelledby="practice-title">
    <div class="wrap">
{shead("Constraints that hold under pressure.", "practice-title", "The principle becomes real through how the work is sequenced and reviewed. The shape varies by firm; the discipline does not.")}
{cards([(h, t, "", None) for h, t in PRACTICE])}
    </div>
  </section>
""" + dark("Three convictions that shape the work.", "why-title", [
        ("Judgment is the product.", "In an investment firm the deliverable is a defensible decision; AI should make that judgment sharper, never thinner.", ""),
        ("Fluency is firm-wide.", "From the newest analyst to the managing partner, everyone should know where Claude belongs in their own work.", ""),
        ("The frontier is the job.", "Staying current is a standing discipline, not a one-off project, which is why our work is monthly.", ""),
    ]) + """  <section class="section" aria-labelledby="both-title">
    <div class="wrap">
""" + shead("One thesis, both sides of the work.", "both-title", "It is not a slide at the front of a deck. It is the operating principle behind every session we teach and every system we ship.") + """
      <div class="pair">
        <div class="pair__item">
          <h3 class="h3">How we train</h3>
          <p>Every session is designed the adversary-first way, so the team builds verification habits as it builds fluency.</p>
          <a class="text-link" href="/services/enablement">Enablement</a>
        </div>
        <div class="pair__item">
          <h3 class="h3">What we build</h3>
          <p>Agents and workflows are designed to challenge and verify human reasoning, never to quietly replace it.</p>
          <a class="text-link" href="/services/build">Build</a>
        </div>
      </div>
    </div>
  </section>
""" + close(),
    "/pt/abordagem", nav="approach")

# -------- About us
PEDIGREE = [
    ("Trading", "Non-linear and ETF trading desks at a global investment bank."),
    ("M&amp;A", "Mergers and acquisitions at corporate and investment banks."),
    ("Investing", "Search-fund analysis and venture-capital investing."),
    ("AI research", "Applied AI research at national research institutes."),
    ("AI delivery", "Agent development and AI strategy consulting."),
    ("Teaching", "Award-recognised teaching in programming and computer science."),
]
add("about", "About us · A finance-native and AI-native firm · Solven Advisory",
    "Solven Advisory is a boutique AI enablement and implementation consultancy founded in Lisbon in 2025, working with private equity, real estate and venture firms across Iberia and Europe.",
    hero("Finance-native and AI-native, in equal measure.",
         "Solven Advisory is a boutique AI enablement and implementation consultancy, founded in Lisbon in 2025, working with private equity, real estate and venture firms across Iberia and, increasingly, Europe.", cta=False)
    + """  <section class="section" aria-labelledby="founders-title">
    <div class="wrap grid split">
      <div class="split__head">
        <h2 class="h2" id="founders-title">Three co-founders, both sides of the work.</h2>
      </div>
      <div class="split__body">
        <p>Solven has three co-founders. Two bring backgrounds in finance and in AI engineering; the third, a senior co-founder, brings the experience of having built and run a business through to exit.</p>
        <p>That combination is deliberate. The people who decide where AI belongs in an investment firm should understand both the investment work and the technology underneath it.</p>
        <p>We are thesis-driven. Everything we teach and build runs through a single idea, <a class="text-link" href="/approach">augmentation without cognitive atrophy</a>, and a refusal to let capable people become editors of drafts they cannot defend.</p>
      </div>
    </div>
  </section>
""" + dark("The credibility is in the pedigree, not the pitch.", "pedigree-title", [(h, t, "") for h, t in PEDIGREE],
           lead="The team's backgrounds span institutional finance and applied AI. We let the experience speak plainly.")
    + close("We would rather have a conversation than send a brochure.",
            "Tell us about your firm and where your team is today. We will be straight about whether we can help.", art="skyline"),
    "/pt/sobre", nav="about",
    ld=[{"@context": "https://schema.org", "@type": "AboutPage", "url": f"{ORIGIN}/about", "about": ORG}])

# -------- Contact
CAL_LOADER = re.search(r"\(function \(C, A, L\).*?\)\(window, \"https://app\.cal\.eu/embed/embed\.js\", \"init\"\);",
                       (LEGACY / "contact.html").read_text(), re.S).group(0)
faq_open = "\n".join(f"""        <div class="faq__item">
          <h3 class="h3">{esc(q)}</h3>
          <p class="faq__a">{a}</p>
        </div>""" for q, a in FAQ_CONTACT)
add("contact", "Contact · Solven Advisory",
    "Book a thirty-minute call with Solven Advisory, or send a note. Based in Lisbon, working with investment firms from Lisbon to London.",
    hero("Let's start a conversation.",
         "Tell us where your team is today and what the next quarter looks like. We will be straight about whether we can help.", cta=False)
    + f"""  <section class="section" id="calendar" aria-labelledby="book-title">
    <div class="wrap contact__grid">
      <div class="contact__side">
        <h2 class="h2" id="book-title">Run your diligence on us.</h2>
        <p class="shead__lead">Every firm we work with is in the business of scrutiny, so we will not ask you to take a pitch on faith.</p>
        <ul class="terms">
          <li><strong>Thirty minutes with a co-founder.</strong> Video or phone, Lisbon time. No deck, no warm-up act.</li>
          <li><strong>Bring the workflow that fills your team's week:</strong> the memo, the model, the reporting cycle. We will tell you where AI sharpens it, and where it should not be let near it.</li>
          <li><strong>A straight answer,</strong> including “we are not the right firm for this.” Ask the questions you would ask any target.</li>
          <li><strong>No further obligations.</strong> No follow-up sequence, no list, no retainer implied.</li>
        </ul>
      </div>
      <div class="contact__main">
        <div class="cal" id="cal-inline"></div>
        <p class="cal__note">Booking runs on Cal.com's EU infrastructure. If the calendar does not load, <a href="https://cal.eu/miguelmonteirosolven" target="_blank" rel="noopener">open it in a new tab</a>.</p>
      </div>
    </div>
  </section>
  <section class="section band" id="write" aria-labelledby="write-title">
    <div class="wrap contact__grid">
      <div class="contact__side">
        <h2 class="h2" id="write-title">Send a note.</h2>
        <p class="shead__lead">Sent directly from the page. Prefer email, a phone call or LinkedIn? The details are below.</p>
        <dl class="details">
          <div><dt>Email</dt><dd><a href="mailto:hello@example.com">{dummy("hello@example.com")}</a></dd></div>
          <div><dt>Phone</dt><dd><a href="tel:+351967130877">+351 967 130 877</a></dd></div>
          <div><dt>LinkedIn</dt><dd><a href="https://www.linkedin.com/company/solven-advisory">solven-advisory</a></dd></div>
          <div><dt>Based in</dt><dd>Lisbon, Portugal</dd></div>
          <div><dt>Working</dt><dd>From Lisbon to London</dd></div>
        </dl>
      </div>
      <div class="contact__main">
        <div class="form" id="form">
          <form action="https://formsubmit.co/miguelmonteiro@solvenadvisory.ai" method="POST">
            <input type="hidden" name="_subject" value="Website enquiry · solvenadvisory.ai">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="_next" value="https://solvenadvisory.ai/contact?sent=1#form">
            <div class="honey" aria-hidden="true"><input type="text" name="_honey" tabindex="-1" autocomplete="off"></div>
            <div class="form__row">
              <div class="field"><label for="name">Name</label><input type="text" id="name" name="Name" autocomplete="name" required></div>
              <div class="field"><label for="firm">Firm</label><input type="text" id="firm" name="Firm" autocomplete="organization" required></div>
            </div>
            <div class="field"><label for="email">Email</label><input type="email" id="email" name="Email" autocomplete="email" required></div>
            <div class="field"><label for="interest">Interested in</label>
              <select id="interest" name="Interested in">
                <option>Enablement programme</option>
                <option>A specific build</option>
                <option>AI diligence</option>
                <option>Token economics</option>
                <option>Not sure yet</option>
              </select>
            </div>
            <div class="field"><label for="message">Message</label><textarea id="message" name="Message" placeholder="A line on your firm and where your team is today."></textarea></div>
            <div class="form__foot">
              <button class="btn btn--primary" type="submit">Send</button>
              <p class="form__note">We reply to people, not leads. There is no marketing list.</p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
  <section class="section" aria-labelledby="faq-title">
    <div class="wrap faq">
      <div class="faq__head">
        <h2 class="h2" id="faq-title">Three answers worth having first.</h2>
        <p class="shead__lead">These are the three that usually come up before a first call. The full set is on the <a href="/services/enablement#faq-title">enablement page</a>.</p>
      </div>
      <div class="faq__list">
{faq_open}
      </div>
    </div>
  </section>
""",
    "/pt/contacto", nav="contact",
    ld=[{"@context": "https://schema.org", "@type": "ContactPage", "url": f"{ORIGIN}/contact", "about": ORG}],
    scripts=f"""<script>
  /* Inline booking calendar: Cal.com (EU-hosted), official embed loader. */
  {CAL_LOADER}
  Cal("init", {{ origin: "https://app.cal.eu" }});
  Cal("inline", {{ elementOrSelector: "#cal-inline", calLink: "miguelmonteirosolven", config: {{ layout: "month_view", theme: "light" }} }});
  Cal("ui", {{ cssVarsPerTheme: {{ light: {{ "cal-brand": "#2A2A28" }} }}, hideEventTypeDetails: false, layout: "month_view" }});
</script>
<script>
  /* Form success state: FormSubmit redirects back with ?sent=1. */
  (function () {{
    if (new URLSearchParams(window.location.search).get("sent") !== "1") return;
    var card = document.querySelector(".form");
    if (!card) return;
    card.innerHTML = '<h3 class="h3">Received.</h3><p>Your note is with us. We reply to people, not leads: expect a personal answer, not a sequence.</p>';
  }})();
</script>
""")

# -------- Insights
add("insights", "Insights · Notes on AI for investment firms · Solven Advisory",
    "Plain-spoken writing from Solven Advisory on the AI developments that matter to private equity, real estate and venture firms: new models, new tooling, and what is signal versus noise.",
    hero("Notes from the frontier, as it moves.",
         "Short, practical writing on what is actually changing in AI: new models, new tooling, and what it means for firms where judgment is the product.", cta=False)
    + f"""  <section class="section" aria-labelledby="all-title">
    <div class="wrap">
      <h2 class="sr" id="all-title">All insights</h2>
      <div class="insights__cards icards--wide">
{chr(10).join(icard(a, topic=True, long=True) for a in ARTICLES)}
      </div>
    </div>
  </section>
""" + close(art="farol"),
    "/pt/publicacoes", nav="insights",
    ld=[{"@context": "https://schema.org", "@type": "Blog", "name": "Solven Advisory insights", "url": f"{ORIGIN}/insights", "publisher": ORG,
         "blogPost": [{"@type": "BlogPosting", "headline": a[1], "url": f"{ORIGIN}/insights/{a[0]}"} for a in ARTICLES]}])

# -------- Articles
for a in ARTICLES:
    slug, title, topic, iso, label, dum, short = a
    body, lead, desc = article_src(slug)
    others = [x for x in ARTICLES if x[0] != slug]
    meta = f"{topic} · {date_html(iso, label, dum)} · 4 min read"
    add(f"insights/{slug}", f"{title} · Insights · Solven Advisory", desc,
        hero(title, lead, cta=False, calcada=False, extra=f'\n        <p class="hero__meta">{meta}</p>')
        + f"""  <section class="section" aria-label="Article">
    <div class="wrap">
      <article class="prose">
{body}
      </article>
      <p class="article__foot"><a class="btn btn--primary" href="/contact#calendar">Book a call</a><a class="text-link" href="/insights">All insights</a></p>
    </div>
  </section>
  <section class="section band" aria-labelledby="more-title">
    <div class="wrap insights__split">
      <div class="insights__intro">
        <h2 class="h2" id="more-title">More insights.</h2>
        <p>Short notes on AI in investment firms: what we see in the work, and what it means for partners.</p>
        <a class="btn" href="/insights">All insights</a>
      </div>
      <div class="insights__cards insights__cards--2">
{chr(10).join(icard(x, topic=True) for x in others)}
      </div>
    </div>
  </section>
""",
        "/pt/publicacoes", nav="insights", og="article", published=iso,
        ld=[{"@context": "https://schema.org", "@type": "BlogPosting", "headline": title, "description": desc,
             "datePublished": iso, "author": ORG, "publisher": ORG, "inLanguage": "en-GB",
             "mainEntityOfPage": f"{ORIGIN}/insights/{slug}", "url": f"{ORIGIN}/insights/{slug}", "image": f"{ORIGIN}/assets/og.png"}])

# -------- Privacy
PRIV = re.search(r"<main.*?</main>", (LEGACY / "privacy.html").read_text(), re.S).group(0)


def priv_section(heading):
    m = re.search(rf"<h2[^>]*>{re.escape(heading)}</h2>(.*?)(?=<h2|</section>|</article>|</div>\s*</div>\s*</main>)", PRIV, re.S)
    assert m, heading
    ps = re.findall(r"<p[^>]*>(.*?)</p>", m.group(1), re.S)
    return [re.sub(r"\s+", " ", p).strip() for p in ps]


EMAIL_DUMMY = f'<a href="mailto:hello@example.com">{dummy("hello@example.com")}</a>'
priv_rows = []
for h in ["Who we are", "What we collect, and why", "The legal basis", "Where the data sits", "How long we keep it", "Your rights"]:
    ps = priv_section(h)
    ps = [re.sub(r'<a href="mailto:miguelmonteiro@solvenadvisory\.ai">miguelmonteiro@solvenadvisory\.ai</a>', EMAIL_DUMMY, p) for p in ps]
    # The removed video page is gone: its sentence goes with it
    ps = [re.sub(r"\s*Video on the " + GONE_PAGE + r" page[^.]*\.", "", p) for p in ps]
    rid = ' id="cookies"' if h == "What we collect, and why" else ""
    priv_rows.append(f"""        <li class="row"{rid}>
          <h2 class="h2 h2--sm row__h">{h}</h2>
          <div class="row__p">{"".join(f"<p>{p}</p>" for p in ps)}</div>
        </li>""")
add("privacy", "Privacy · Solven Advisory",
    "How Solven Advisory handles the personal data of the people who write to us or book a call, and which cookies run only after you accept them.",
    hero("Plain terms for personal data.",
         "No marketing list, no advertising, and no cookie before you say yes. This page says what we do hold, why, and for how long.",
         cta=False, calcada=False,
         extra='\n        <p class="hero__meta">This notice covers the personal data of people who visit this site, write to us, or book a call. Last updated <time datetime="2026-07-29">29 July 2026</time>.</p>')
    + f"""  <section class="section" aria-label="Privacy notice">
    <div class="wrap">
      <ul class="rows rows--wide">
{chr(10).join(priv_rows)}
      </ul>
    </div>
  </section>
""", "/pt")

# -------- 404
add("404", "Page not found · Solven Advisory", "There is nothing at this address.",
    hero("There is nothing at this address.",
         "The page may have moved when the site did, or the address may have a typo in it. Either way, the work continues at the pages below.", cta=False,
         extra="""
        <p class="nf__links">
          <a class="btn btn--primary" href="/">Back to the start</a>
          <a class="text-link" href="/services">Services</a>
          <a class="text-link" href="/contact#calendar">Book a call</a>
        </p>""", fill=True), "/pt")


# ---------------------------------------------------------------- homepage: ledger-v4 with links pointed inside the preview

def homepage():
    p = dict(path="", title="Solven Advisory · AI enablement and implementation for investment firms",
             description="Solven Advisory trains private equity teams on AI and builds it into their workflows, so the people making the call still own the reasoning behind it. Augmentation without cognitive atrophy.",
             pt="/pt",
             ld=[{"@context": "https://schema.org", "@type": "ProfessionalService", "@id": f"{ORIGIN}/#organization",
                  "name": "Solven Advisory", "url": f"{ORIGIN}/", "logo": f"{ORIGIN}/assets/apple-touch-icon.png", "image": f"{ORIGIN}/assets/og.png",
                  "description": "Solven Advisory trains investment teams on AI and builds AI systems on their workflows: enablement programmes, AI due diligence, and token economics for private equity, real estate, and venture firms.",
                  "telephone": "+351967130877", "foundingDate": "2025",
                  "address": {"@type": "PostalAddress", "addressLocality": "Lisbon", "addressCountry": "PT"},
                  "areaServed": ["Portugal", "Spain", "United Kingdom"],
                  "knowsAbout": ["AI enablement", "AI due diligence", "Private equity workflows", "Token economics", "Claude"],
                  "sameAs": ["https://www.linkedin.com/company/solven-advisory"]}])
    body = grab(r"<body .*?</html>")
    body = rep(body, '<body class="cards-tile cards-stretch cta-promote" style="--h1-weight: 400">', "<body>")
    body = re.sub(r"\n<script>\n  /\* Promote:.*?</script>\n<script>\n  /\* Calçada:.*?</script>\n",
                  f'\n<script src="{PREVIEW}/site.js?v=1"></script>\n', body, flags=re.S)
    assert "Promote:" not in body and "site.js" in body
    body = body.replace('src="/explorations/wow/maat.svg"', 'src="/explorations/site/img/maat.svg"')
    return head(p) + "\n" + body, p


def check(text, where):
    assert EMDASH not in text and ENDASH not in text, where
    assert GONE_PAGE not in text and OLD_BADGE not in text, where
    assert FOUNDER not in text, where


if __name__ == "__main__":
    (SITE / "img").mkdir(parents=True, exist_ok=True)
    for name in IMAGES:
        shutil.copyfile(ROOT / "explorations/wow" / name, SITE / "img" / name)
    home, _ = homepage()
    out = {SITE / "index.html": preview_links(home)}
    for p in PAGES:
        out[SITE / p["path"] / "index.html"] = preview_links(page(p, p["main"]))
    for path, text in out.items():
        check(text, path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        print(path.relative_to(ROOT), len(text.encode()), "bytes")
