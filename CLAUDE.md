# Solven Advisory Website

## Project
Website for Solven Advisory, Lda (solvenadvisory.ai): a boutique AI enablement and implementation consultancy in Lisbon, member of the Anthropic Partner Network. Clients: private equity firms first, also real estate and venture firms, across Iberia and Europe. Readers are PE partners, associates and analysts, portfolio-company executives, and future hires. They skim, so pages read like an elevator pitch: key ideas only, then links to depth.

## Stack
- Plain HTML, CSS and JS. No framework, no build step, no package.json. Deployed on Vercel (clean URLs).
- Local dev server: `python3 tools/serve.py` (default http://127.0.0.1:8000). Pass a port number as an argument to run a second instance, e.g. `python3 tools/serve.py 8001`.
- Pages: `.html` files at the repo root (index, programmes, approach, work, about, contact, privacy, 404) and articles in `blog/`.
- Global styles: `solven.css`. The current motion layer lives in `solven.js` and will be removed in the redesign; do not extend it.
- Portuguese: a hand-maintained copy of each page in `pt/` (index, programas, abordagem, trabalho, sobre, contacto), linked with hreflang tags and an EN/PT toggle. Any page change must be mirrored in its PT counterpart once a design is approved (not during explorations).
- Do not introduce a framework, bundler, npm dependencies or an animation library without explicit approval.

## Status
A full visual redesign is in progress on branch redesign/base and its child branches. The design source of truth will be docs/design-brief.md and DESIGN.md once they exist. Read them before any UI work. Log every design attempt and every rejection in docs/redesign-log.md.
Phase 3: docs/design-brief.md is the source of truth for typography, colour, spacing, grid and components. If it conflicts with anything else except the hard limits, the brief wins.

## Feeling
Prestigious, formal, polished: "good old-fashioned finance", with a quiet freshness that comes from precision, clarity and plain confident language, never from effects.

## Hard limits (never violate, even if a skill suggests otherwise)
- Zero motion as a feature: no scroll-triggered reveals, fade-ins, text that bolds or assembles on scroll, split-letter effects, animated shapes, intro loaders, parallax, smooth-scroll hijacking, WebGL or animated backgrounds. Do not add GSAP, Framer Motion, Lenis or any animation library. Allowed: simple hover states and instant UI feedback. Always respect prefers-reduced-motion.
- Must run smoothly on an ordinary laptop. Static, fast pages.
- No team headshot grids. No founder names or photos.
- No client logos, case numbers or invented statistics. Use clearly marked placeholders where a future section needs them.
- Remove "AI Flix" entirely.
- Do not reproduce the old site's patterns: warm cream background (#F3EEE4-like), sage green (#6B8068) as a brand colour, Georgia anywhere outside the logo, italicised single words inside headlines, small uppercase tracked 'eyebrow' labels above headings, 01/02/03 or i/ii/iii numbering, faded giant logo watermark, scroll fade-ins. A serif headline typeface IS allowed, used upright, at one or two heading levels only, as defined in docs/design-brief.md.
- Avoid generic AI-startup aesthetics: black backgrounds with glows, purple/blue gradients, Inter-on-black slogan heroes, bento grids, emoji or icon-per-feature cards.
- Flat surfaces: small radii (about 3 to 5px), no drop shadows, thin rules.
- Photography must be real and contextual, not abstract gradients or 3D renders.
- Homepage target height: roughly one third of the current one (about 3,000px on desktop).

## Logo (fixed)
Wordmark "Solven" in Georgia with a custom V notch, "ADVISORY" in spaced capitals below. Source: assets/logos/01_solven_primary_lockup.svg (reversed: 02_solven_reversed_lockup.svg). Only the two colour slots may change (wordmark fill; V notch + ADVISORY fill). Never change letterforms, fonts, the V shape or proportions. Georgia appears only in the logo.

## Content
The substance of the current copy stays: the thesis "Augmentation without cognitive atrophy", the three convictions (Judgment is the product, Fluency is firm-wide, The frontier is the job), and four services (Enablement, Build, AI Diligence, Token Economics). Copy can be condensed or moved, not reinvented. Languages: EN and PT, with a PT mirror of every page.
AI Flix is being removed from the site entirely (page /ai-flix and any links or mentions). Do not reference it in new work; it will get a 301 redirect at build time.

## SEO (must be preserved in any rebuild)
Per-page titles and meta descriptions, canonical URLs on solvenadvisory.ai, EN/PT hreflang, ProfessionalService structured data, Open Graph images, one H1 per page.

## Working rules
- Change only what the current prompt asks for. Do not "improve" untouched sections.
- Commit after each completed step with a descriptive message.
- Only use design skills that the prompt names explicitly. If a design skill activates without being named, say so and stop.
- docs/, CLAUDE.md, tools/, .claude/ and .impeccable/ are excluded from deployment via .vercelignore; keep it that way.

## Figma
- Figma access is a Starter plan with a View seat: read tools (get_design_context, get_screenshot, get_metadata, get_variable_defs, etc.) are limited to about 20 calls per month. Never call Figma read tools unless the prompt explicitly asks for it.
- Write tools are allowed: use generate_figma_design (code to canvas) to capture pages into a file in my Figma drafts when asked.

## Current site reference (pre-redesign)

This section describes the site as built before the redesign. The build,
deployment, SEO and writing mechanics still apply. Where anything below
conflicts with the sections above (the motion layer, AI Flix, the founder
name, the old palette and type), the sections above win.

Marketing site for Solven Advisory: a one-founder AI enablement and
implementation consultancy in Lisbon (founder: Miguel Monteiro), selling to
private equity, real estate, and venture firms. Core thesis: "augmentation
without cognitive atrophy". The analyst produces the work first; the model
enters as critic, red-teamer, and verifier, never as author. Offer: monthly
Claude enablement programmes (four-session arc), build work (agents on real
workflows), AI due diligence on targets, and token economics. Solven is a
member of the Anthropic Partner Network.

### Stack and deployment

- Plain HTML/CSS/JS. No framework, no build step, no webfonts.
- Deployed on Vercel from GitHub `miguel9monteiro/solven-advisory-website`;
  **pushing to `main` deploys to production immediately.**
- `vercel.json`: `cleanUrls` on, `trailingSlash` off, `/blog.html` redirect,
  security and asset-cache headers. Internal links are extensionless
  (`/about`, `/contact#book`); assets use absolute paths (`/assets/...`).
- `.vercelignore` keeps `BRAND.md` and `tools/` out of production (they were
  once publicly served; keep it that way). The old Astro site (`legacy/`) was
  deleted from the tree in July 2026; it survives in git history if ever
  needed.
- Canonical origin: `https://solvenadvisory.ai` (apex, no www, no trailing
  slash; the PT page is `/pt`). Every page carries canonical + OG + Twitter
  meta and shares `assets/og.png` (1200x630, generated from brand SVGs).

### Layout

- Pages: `index`, `programmes`, `approach`, `work`, `about`, `contact`,
  `privacy`, `404`, `blog/index` + three articles (`blog/<slug>.html`,
  July 2026, author Miguel Monteiro).
- Portuguese mirror under `pt/`: `pt/index` plus full pt-PT versions of the
  five core pages. The pairs (keep in sync when EN copy changes):
  `/` ↔ `/pt`, `/programmes` ↔ `/pt/programas`, `/approach` ↔ `/pt/abordagem`,
  `/work` ↔ `/pt/trabalho`, `/about` ↔ `/pt/sobre`,
  `/contact` ↔ `/pt/contacto`. PT pages use the standard header with PT
  labels (Blog links to the EN journal as "Blog · EN") and the compact
  `.ptfooter`. The journal, privacy, and 404 are EN-only (their PT toggle
  goes to `/pt`).
- Shared: `solven.css` (design system + motion), `solven.js` (motion/interaction
  layer), `BRAND.md` (brand reference: palette, type, voice; not deployed).
- Discovery: `robots.txt` (deliberately liberal; all crawlers and AI bots
  explicitly welcomed), `sitemap.xml` (12 URLs, hreflang on the `/` and `/pt`
  pair only), `llms.txt` (hand-written index), `llms-full.txt` (**generated**:
  run `python3 tools/build_llms_full.py` after any copy change, never hand-edit),
  `site.webmanifest`.
- Structured data: ProfessionalService on `/`, Service + FAQPage on
  `/programmes`, Blog/BlogPosting on the journal, WebPage on `/pt`.

### Conversion stack

- Booking: Cal.com EU embedded inline on `/contact#calendar`
  (`cal.eu/miguelmonteirosolven`, loader from `app.cal.eu/embed/embed.js`);
  the "countersign" signature block links to it on-page. A "Book a call"
  `.nav-cta` button sits in every header; booking is the primary CTA in the
  hero and all closers.
- Contact form posts to FormSubmit (`formsubmit.co/miguelmonteiro@solvenadvisory.ai`)
  with honeypot and `?sent=1` success state.
- Header also carries a `.nav-lang` language toggle: PT on English pages, EN
  on `/pt`.
- Analytics: Vercel Web Analytics snippet on every page (cookieless; the site
  promises "No cookies, no list", so never add cookie-based tracking).

### Writing rules

- **Em dashes are a big no. Never use an em dash (—) anywhere**: not in copy,
  titles, meta, JSON-LD, code comments, or generated files. Rewrite with a
  comma, colon, full stop, or restructure. En dashes and spaced hyphens as
  dashes are not acceptable substitutes. The middot (·) is the house separator
  for labels ("Lisbon · 2026", "Contact · Solven Advisory"). This extends to
  visual elements: a decorative hairline that reads as a dash was removed too.
- Voice (BRAND.md): considered, not corporate; complete sentences, no
  fragments for emphasis; specific over generic; fewer words when in doubt.
  Banned words: synergy, leverage (verb), value-add, robust, holistic,
  leading, cutting-edge, unlock, ecosystem, journey, delight.
- British spelling (programmes, analyse, organisation).
- Portuguese content is **European Portuguese**: formação (not capacitação),
  casas/sociedades de investimento (not firmas), equipas, vossos, «guillemets»,
  "marcar uma chamada". Finance anglicisms (private equity, term sheet, deck)
  are deliberate.

### Invariants

- The three FAQ answers shared between `programmes.html` and `contact.html`
  must stay word-for-word identical, and the FAQPage JSON-LD in
  `programmes.html` must exactly match the visible answer text.
- title = og:title = twitter:title, and description = og:description =
  twitter:description, per page.
- hreflang (en / pt-PT / x-default) lives only on paired pages, reciprocally
  on both sides of each EN ↔ PT pair (and in the sitemap); annotating
  unpaired pages (journal, privacy, 404) is invalid.
- The `.nav-lang` toggle always targets the page's own counterpart, never
  the other language's home (except on unpaired pages, where PT → `/pt`).
- The three shared FAQ answers exist in BOTH languages: EN on
  `programmes`/`contact`, PT on `pt/programas`/`pt/contacto`; each language
  pair must stay word-for-word identical internally.
- Exactly one h1 per page; no internal link may end in `.html`.
- Motion: content visible by default. Hidden states exist only behind
  JS-applied classes (`.pending`, `body.intro-armed`, `html.anim`) with timed
  rescue paths; `prefers-reduced-motion: reduce` is a hard stop for every
  effect. See the headers in `solven.js` and the cinematic sections of
  `solven.css` (view-transition continuity, blur focus-pull reveals, dark-band
  light drift, breathing chevrons, the self-drawing contract signature on
  contact, `data-stagger` cascades).
- Never pure black, no greens beyond the two brand sages, no third typeface,
  bone background not white (BRAND.md).

### Known issues and owner to-dos (verify before assuming fixed)

- **Apex misrouted**: `solvenadvisory.ai` 301s to
  `solven-advisory-website.vercel.app`; only `www` serves correctly. Fix is in
  Vercel domain settings (apex primary, www redirects to it). Canonicals
  already point at the apex.
- **Email deliverability**: MX is Microsoft 365 but SPF is GoDaddy-only
  (`include:secureserver.net -all`) and M365 DKIM is off; DMARC quarantines.
  Owner must fix DNS + M365 admin.
- FormSubmit needs a one-time activation click (first live form submission
  emails the owner a confirmation link).
- Vercel Web Analytics needs its dashboard toggle (until then the snippet
  404s harmlessly).
- Sitemap not yet submitted in Google Search Console (domain verification
  TXT already exists on solvenadvisory.ai).
- `solvenadvisory.com` belongs to an unrelated ERP advisory (name collision on
  branded search). `solvenadvisory.pt` and `solven.pt` were unregistered as of
  2026-07-28; owner intends to register.
- The contact signature says "Co-founder" while about says "the team"; whether
  Solven is one founder or two is unresolved. Do not "fix" without asking.
- The "Anthropic Partner Network · Phase 1" badge is plain text; it needs a
  verification link only the owner can supply.
