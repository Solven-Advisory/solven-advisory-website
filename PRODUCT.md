# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
- **Primary:** partners, associates and analysts at private equity firms, then real estate and venture firms, across Iberia and Europe. Most arrive already aware of Solven, through a referral, LinkedIn or direct outreach, and use the site to check the firm before or after a conversation. They skim, and they judge credibility quickly.
- **Secondary:** executives at portfolio companies, who are often sent the link by their sponsor.
- **Tertiary:** future hires, who check whether the firm is serious.
- Partners often forward the link internally. The site has to hold up when someone reads it cold, with no introduction.

## Product Purpose
The site presents Solven Advisory, Lda, a boutique AI enablement and implementation consultancy in Lisbon and a member of the Anthropic Partner Network. It explains what Solven believes, what it does, and how to engage, in the time a busy investment professional will give it.

Success means a booked 30-minute call (Cal.com, on `/contact`), or a partner confident enough to forward the link to colleagues. Every page reads like an elevator pitch: the key ideas only, with depth one link away.

## Positioning
Two parts carry the position, with equal weight:
1. **The thesis:** "Augmentation without cognitive atrophy." The real risk in an AI rollout is analysts becoming editors of drafts they cannot defend. So the analyst produces the formative work first, and the model comes in as critic, red-teamer and verifier, never as author.
2. **Finance insiders who build:** the team comes from finance and AI engineering, and every engagement runs on the firm's own deals, models and memos.

The Anthropic Partner Network membership and the private equity focus support the position. Neither is the position on its own.

## Operating Context
- Visitors check the firm around a meeting: on a laptop at the office, or on a phone between calls. They often open the link from an email or a LinkedIn message.
- The engagement path is a 30-minute call booked inline on `/contact`, with a contact form as the alternative. "Book a call" sits in every header and closes every page.
- Delivery is in Portuguese or English, on site in Lisbon, remotely, or a mix.

## Capabilities and Constraints
- **Four services:** Enablement (monthly Claude programmes built around a four-session arc), Build (agents on real workflows), AI Diligence (independent assessment of targets), and Token Economics (workflow-level AI costing). Programmes run monthly because the frontier moves weekly. There is no minimum commitment, and each engagement is scoped and priced individually.
- **Three convictions:** Judgment is the product · Fluency is firm-wide · The frontier is the job.
- **Content rule:** copy can be condensed or moved, not reinvented.
- **Languages:** English first, with a hand-maintained European Portuguese mirror of every paired page.
- **Stack:** plain HTML, CSS and JS with no framework, build step or npm, deployed on Vercel with clean URLs. Pages must be static and fast, and run smoothly on an ordinary laptop.
- **Planned information architecture** (redesign, see `docs/redesign-log.md`): Approach · Services (one page per service) · Insights · About us · Contact. The PT equivalents are Abordagem · Serviços · Publicações · Sobre nós · Contacto. Old URLs get 301 redirects at build time.
- **SEO** must be kept: per-page titles and descriptions, canonicals on solvenadvisory.ai, EN/PT hreflang, ProfessionalService structured data, OG images, exactly one H1 per page.
- **Privacy promise:** "No cookies, no list." Cookieless analytics only.
- **Removed:** AI Flix is gone entirely and gets a redirect. Never reference it.

## Brand Commitments
- **Name:** Solven Advisory. The logo is fixed: the "Solven" wordmark with a custom V notch, and "ADVISORY" below it (`assets/logos/`). Only its two colour slots may change.
- **Voice:** considered, not corporate. Complete sentences, specific over generic, fewer words when in doubt, British spelling, and European Portuguese for PT.
- **Banned words:** synergy, leverage (verb), value-add, robust, holistic, leading, cutting-edge, unlock, ecosystem, journey, delight.
- **No em dashes anywhere.** The middot (·) is the house separator.
- **Character:** prestigious, formal and polished, "good old-fashioned finance", with freshness that comes from precision and plain language, never from effects.
- **People:** three co-founders (two younger ones, with finance and AI/engineering backgrounds, and one senior former business owner). No names or photos on the site for now, and no headshot grids.
- **Visual system:** `docs/design-brief.md` is the source of truth. The hard limits in `CLAUDE.md` override everything.

## Evidence on Hand
- **Real:** the thesis and methods; three published articles (on cognitive offloading, AI diligence and token economics, in `blog/`); the team's background (trading, M&A, search-fund and venture analysis, applied AI research, award-recognised teaching); and the firm facts (Lisbon; Iberia & Europe; private equity focus; Anthropic Partner Network).
- **Absent, and must not be invented:** client names or logos, case studies, testimonials, engagement numbers, statistics and pricing. Sections that will need proof later use clearly marked placeholders.
- **Partner wording:** only what the Anthropic agreement permits. Do not use "Phase 1". The verification link has to come from the owner.
- **Photography:** captioned placeholders during explorations, curated real stock before launch, and the owner's own Lisbon photography over time.

## Product Principles
1. **Credibility before persuasion.** Visitors arrive already checking Solven, so the site proves seriousness through clarity and true facts, not claims.
2. **One idea per section, with depth one link away.** Skimmers get the point in seconds, and anyone who wants detail can find it.
3. **The thesis shows in how Solven works.** Judgment stays with the professional, and the site's own restraint should reflect that.
4. **Truth only.** Unknown proof stays a visible placeholder and is never invented.
5. **Forwardable.** Every page has to make sense to a colleague who received only the link.

## Accessibility & Inclusion
- WCAG 2.1 AA contrast on all text.
- `prefers-reduced-motion` is respected, and the site has no motion as a feature anyway.
- Full parity between English and European Portuguese on paired pages.
