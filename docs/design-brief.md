# Design brief · solvenadvisory.ai redesign

Status: Phase 3, written 2026-10-14. This file is the single source of truth for typography, colour, spacing, grid and components. If it conflicts with anything except the hard limits in `CLAUDE.md`, this brief wins. Where it is silent, ask; do not improvise.

Sources: `CLAUDE.md`, `docs/redesign-log.md`, `docs/references/` (current-site, hark, subduxion, actionist, institutional, synthesis, client screenshots in `screens/`), and the copy in `index.html` and `about.html`. All reference measurements are at 1440px wide in Chromium, 2026-10-14.

How to read the rules: "must" and "never" are binding. A value followed by "Reason:" was chosen here; the reason ties it to a reference or a client note.

---

## 1. Intent

Solven Advisory is a boutique AI enablement and implementation consultancy in Lisbon, working first for private equity. The site should feel prestigious, formal and polished: good old-fashioned finance. Its freshness comes from precision, clarity and plain language, never from effects.

- The old-money character comes from **type and colour**: a light, upright serif for the top headings and a formal, warm-neutral palette with one deep anchor.
- The calm structure comes from **Hark, Subduxion and Actionist**: flat surfaces, one job per section, real photographs, short pages, depth one click away.
- Readers (PE partners, associates, analysts, portfolio executives, future hires) skim. Every section does one job: a heading, at most three lines of text, one component, one link.
- The page is fully present on load. Nothing moves on its own.

---

## 2. Typography

### 2.1 Roles

| Role | Family | Rules |
|---|---|---|
| H1, H2 | The direction's serif | Upright only. Weight 300 (H1) or 400 (H2). Never italic, never bold. Never below 28px. |
| H3 and everything else | The direction's sans | H3, body, lead, nav, buttons, labels, captions, footer, form fields. |
| Small figures | IBM Plex Mono (Direction 2 only) | Dates and small figures on insights only, 14px, sentence case or digits. Never a label above a heading. |
| Logo | Fixed SVG | Georgia appears only inside the logo. Never set any other text in Georgia. |

Reason: Lazard and Goldman use a light upright serif for one or two levels only and a sans for all reading text (`institutional.md`, synthesis 4b); the old site's serif-everywhere is on the reject list (synthesis 4c, item 6).

### 2.2 Scale

| Token | Desktop (≥960px) | Mobile (<640px) | Line-height | Tracking | Weight | Family |
|---|---|---|---|---|---|---|
| `--fs-h1` | 56px | 36px | 1.08 | -0.015em | 300 | Serif |
| `--fs-h2` | 36px | 28px | 1.15 | -0.01em | 400 | Serif |
| `--fs-h3` | 21px | 20px | 1.3 | 0 | 500 | Sans |
| `--fs-lead` | 20px | 18px | 1.5 | 0 | 400 | Sans |
| `--fs-body` | 18px | 17px | 1.6 | 0 | 400 | Sans |
| `--fs-small` | 14px | 14px | 1.5 | 0 | 400 | Sans (or Plex Mono in D2) |
| `--fs-nav` | 16px | 18px (menu panel) | 1.4 | 0 | 400 (500 for current page) | Sans |
| `--fs-button` | 16px | 16px | 1 | 0 | 500 | Sans |

- Between 640px and 960px, H1 and H2 scale linearly: `--fs-h1: clamp(36px, 2.2rem + 2.2vw, 56px)`, `--fs-h2: clamp(28px, 1.5rem + 0.9vw, 36px)`. Body steps at 640px only.
- Body measure: 60-72 characters. Set `max-width: 34em` on body paragraphs and leads (about 66 characters at 18px). H1 `max-width: 18em`, H2 `max-width: 22em`.
- Sentence case everywhere: headings, buttons, nav, labels. No `text-transform: uppercase` on any text except what lives inside the logo.
- Numerals: lining, proportional by default; `font-variant-numeric: tabular-nums` on dates and the facts strip.
- Paragraph spacing: 1em between paragraphs; heading to following text 16px (H3), 24px (H2), 24px (H1).

Reason: H1 56px is smaller than every reference (60-112px) on purpose: the client found Direction B's type too big (`redesign-log.md`) and the homepage must shrink to a third. Weight 300 at display size is the institutional pattern (Lazard, Goldman, J.P. Morgan, Evercore). Body 18px matches Goldman, Evercore and Hark.

### 2.3 Font loading

- Load from Google Fonts with only the weights used, `display=swap`, and two preconnects in `<head>`:
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  ```
- Directions 1 and 3:
  `https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,300;8..60,400&family=Source+Sans+3:wght@400;500&display=swap`
  Set `font-optical-sizing: auto` on headings so 36-56px use the display end of the optical-size axis (this is "Source Serif 4 Display"). Reason: the matched pair recommended first in synthesis 4d; the display optical size gives the tight, light Lazard treatment.
- Direction 2:
  `https://fonts.googleapis.com/css2?family=Spectral:wght@300;400&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400&display=swap`
  Reason: synthesis 4d pairing 2; Plex Sans is Evercore's body face.
- Maximum five font files per page (D2), four for D1 and D3. No italic files are loaded, so an italic cannot appear by accident.
- Fallback stacks: serif `Georgia` is **not** allowed as a fallback (it is logo-only); use `"Source Serif 4", "Iowan Old Style", "Times New Roman", serif` and `"Spectral", "Iowan Old Style", "Times New Roman", serif`. Sans: `"Source Sans 3", system-ui, -apple-system, "Segoe UI", sans-serif` and `"IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif`.
- Portuguese: all five families cover Latin-1 (ã, õ, ç, á, à, é, ê, í, ó, ô, ú, «, ») in Google's `latin` subset. Before approving any direction, render this test line in every face and weight used and check it visually: `Formação, gestão, decisões, análise, equipas, «sócios», você, três, à, ô, ú.`

Note: synthesis 4d suggested self-hosting woff2. The owner chose Google Fonts for Phase 4; self-hosting can be revisited at build (see Open questions).

### 2.4 Forbidden

- Italic words or phrases in any heading, lead or quote. Emphasis by italics, colour or weight inside a headline (J.P. Morgan's coloured last word is the same device).
- Uppercase, letter-spaced labels above or below headings ("eyebrows"), including Subduxion's mono tags.
- Georgia anywhere outside the logo.
- Inter, Playfair Display, Cormorant (any cut), Fraunces, Instrument Serif. Also no Calibri or bare system stack as the body face.
- Serif text below 28px, serif in buttons, nav, labels, numerals or body.
- Weights below 300 for any text; weight 300 only on H1.

---

## 3. Colour

### 3.1 Shared rules

- Every palette has exactly these roles, as CSS custom properties with these names:
  `--c-ground` (page), `--c-band` (one light alternate band), `--c-anchor` (deep colour: H1/H2 colour, one dark band, footer, solid buttons, logo wordmark), `--c-text` (body), `--c-muted` (secondary text), `--c-rule` (1px rules on light), `--c-accent` (optional), `--c-link`, `--c-focus`, and the on-anchor set `--c-on-anchor`, `--c-on-anchor-muted`, `--c-rule-on-anchor`, plus the logo slots `--c-logo-word`, `--c-logo-mark` and their reversed pair `--c-logo-word-rev`, `--c-logo-mark-rev`.
- Pure white `#FFFFFF` and pure black `#000000` are never used. Text greys are fixed hex values, never opacity.
- The anchor fills at most **one** full-width band plus the footer per page.
- The accent covers under 2% of any screen and is never a background fill. Use it for links and focus, or one small detail, never both a link colour and a decorative detail in the same palette.
- H1 and H2 are set in `--c-anchor`; H3 and body in `--c-text`.
- Contrast: all text must pass WCAG 2.1 AA (4.5:1 body, 3:1 for text ≥24px or ≥19px at 500). Every pairing below was computed with the WCAG formula and passes AA at body size; most pass AAA.
- Reason for the grounds: all three are paper whites within 3% of white, cooler than the old bone `#F4F2EB`, matching Hark `#F3F3F3` and the institutions (synthesis 4a, 5).

### 3.2 P1 · Ink and oxblood (Direction 1)

| Token | Hex | Contrast | Note |
|---|---|---|---|
| `--c-ground` | `#FAF9F6` | | Paper white |
| `--c-band` | `#EFEDE9` | | Light warm grey |
| `--c-anchor` | `#1B2433` | 14.8:1 on ground, 13.3:1 on band | Ink navy. Reason: navy anchors at Lazard `#23283C`, Evercore `#002037`. |
| `--c-text` | `#1C1D20` | 16.0:1 ground, 14.4:1 band | |
| `--c-muted` | `#5E6066` | 6.0:1 ground, 5.4:1 band | |
| `--c-rule` | `#D9D6D0` | (non-text) | 1px |
| `--c-accent` | `#7A2E2E` | 8.8:1 ground, 8.0:1 band | Oxblood: link underline colour, link hover text, logo mark. Never a fill. |
| `--c-link` | `--c-text` text, `--c-accent` underline | | |
| `--c-focus` | `#1B2433` | 14.8:1 | |
| `--c-on-anchor` | `#FAF9F6` | 14.8:1 on anchor | |
| `--c-on-anchor-muted` | `#B4B9C2` | 7.9:1 on anchor | Derived here. |
| `--c-rule-on-anchor` | `#3A4354` | (non-text) | Derived here. |
| `--c-logo-word` / `--c-logo-mark` | `#1B2433` / `#7A2E2E` | 14.8:1 / 8.8:1 | |
| `--c-logo-word-rev` / `--c-logo-mark-rev` | `#FAF9F6` / `#D7A9A3` | 14.8:1 / 7.5:1 on anchor | Oxblood on ink fails, so the reversed mark is a light oxblood tint. Derived here. |

### 3.3 P2 · Oxblood (Direction 3)

| Token | Hex | Contrast | Note |
|---|---|---|---|
| `--c-ground` | `#F8F7F4` | | Paper white, slightly warm |
| `--c-band` | `#ECEAE6` | | |
| `--c-anchor` | `#5B1F24` | 11.8:1 ground, 10.5:1 band | Oxblood. Reason: the formal warm register the owner wants, without cream or sage. |
| `--c-text` | `#23201E` | 15.1:1 ground, 13.5:1 band | |
| `--c-muted` | `#68625C` | 5.6:1 ground, 5.0:1 band | |
| `--c-rule` | `#D6D2CB` | (non-text) | |
| `--c-accent` | `#2E4A62` | 8.6:1 ground, 7.7:1 band | Ink blue, **text links only**. |
| `--c-link` | `#2E4A62`, underlined | 8.6:1 | |
| `--c-focus` | `#2E4A62` | 8.6:1 | |
| `--c-on-anchor` | `#F8F7F4` | 11.8:1 on anchor | |
| `--c-on-anchor-muted` | `#E0CFCC` | 8.4:1 on anchor | Derived here. |
| `--c-rule-on-anchor` | `#7A3F44` | (non-text) | Derived here. |
| `--c-logo-word` / `--c-logo-mark` | `#5B1F24` / `#68625C` | 11.8:1 / 5.6:1 | The accent is links-only, so the mark takes the muted grey. |
| `--c-logo-word-rev` / `--c-logo-mark-rev` | `#F8F7F4` / `#E0CFCC` | 11.8:1 / 8.4:1 on anchor | |

### 3.4 P3 · Bottle green, no accent (Direction 2)

| Token | Hex | Contrast | Note |
|---|---|---|---|
| `--c-ground` | `#F7F7F5` | | Neutral paper white |
| `--c-band` | `#ECEDE9` | | |
| `--c-anchor` | `#1F3A2E` | 11.5:1 ground, 10.5:1 band | Bottle green. Must read as near-black green, never sage. |
| `--c-text` | `#1C1E1C` | 15.6:1 ground, 14.3:1 band | |
| `--c-muted` | `#5F635F` | 5.7:1 ground, 5.2:1 band | |
| `--c-rule` | `#D5D6D0` | (non-text) | |
| `--c-accent` | none | | Reason: Subduxion has no accent; emphasis from the anchor alone (`subduxion.md`). If one is ever needed, `#2E4A62`, never brass or gold. |
| `--c-link` | `#1F3A2E`, underlined | 11.5:1 | |
| `--c-focus` | `#1F3A2E` | 11.5:1 | |
| `--c-on-anchor` | `#F7F7F5` | 11.5:1 on anchor | |
| `--c-on-anchor-muted` | `#C2C7C3` | 7.2:1 on anchor | Neutral grey, not a sage tint. Derived here. |
| `--c-rule-on-anchor` | `#3B5347` | (non-text) | Derived here. |
| `--c-logo-word` / `--c-logo-mark` | `#1F3A2E` / `#5F635F` | 11.5:1 / 5.7:1 | |
| `--c-logo-word-rev` / `--c-logo-mark-rev` | `#F7F7F5` / `#C2C7C3` | 11.5:1 / 7.2:1 on anchor | |

### 3.5 Logo

- Source files: `assets/logos/01_solven_primary_lockup.svg`, `02_solven_reversed_lockup.svg`, `03_solven_horizontal_lockup.svg`. Use them inline so the two fills can take `var(--c-logo-word)` and `var(--c-logo-mark)`.
- Only these may change: the wordmark fill (slot 1) and the V notch plus "ADVISORY" fill (slot 2). Never change paths, letterforms, font attributes, letter-spacing, positions or proportions. Cropping the `viewBox` to the artwork is allowed (it removes empty margin; the geometry is untouched). The reversed file's background `rect` is dropped; the band behind it provides the colour.
- Header: `03` horizontal lockup, 40px tall desktop, 32px mobile. Footer: `01` primary lockup, 88px tall, reversed slots.
- Clear space: at least the height of the "S" on all sides.

---

## 4. Spacing, grid and layout

### 4.1 Spacing scale

`--s-1: 4px; --s-2: 8px; --s-3: 12px; --s-4: 16px; --s-5: 24px; --s-6: 32px; --s-7: 48px; --s-8: 64px; --s-9: 96px; --s-10: 128px.` No other spacing values.

- Section padding (top and bottom): 80px desktop (≥960), 64px tablet, 48px mobile. Only the hero may use 96px top. Reason: Hark about 52px, Actionist 60px, Subduxion 96px; 80px sits between and keeps the 3,000px budget.
- Heading block to component: 48px desktop, 32px mobile.
- Component to section link: 32px.

### 4.2 Grid

- 12 columns, `max-width: 1200px` content, 24px gutters, centred. Side margins: `max(24px, (100vw - 1200px) / 2)`; at 1440px that is 120px. Reason: Subduxion 1088-1280px, Actionist about 1210px.
- Breakpoints: `640px` (mobile to tablet), `960px` (tablet to desktop), `1280px` (wide; only the margins grow). Mobile: 4 columns, 16px gutters, 24px side margins. Tablet: 8 columns, 24px gutters, 32px margins.
- Text never runs the full 12 columns: body and leads span at most 7 columns (about 680px).
- Full-bleed is allowed only for the band background colour and for one photo panel per page (Direction 3 hero). Content inside bands stays on the grid.

### 4.3 Surfaces

- Radius: `--r: 3px` on buttons, inputs and boxes; `0` on photos and bands. Nothing above 4px. Reason: Hark 3-5px, institutions 0, CLAUDE.md 3-5px.
- Rules: 1px solid `--c-rule` (or `--c-rule-on-anchor`). No 0.5px hairlines (they render unevenly on ordinary laptop screens).
- No `box-shadow`, no `filter`, no `backdrop-filter`, no gradients, no textures or grain.
- Header is static (scrolls away). If it is ever made sticky, it gets a solid `--c-ground` background and a 1px bottom rule, never transparency or blur.

### 4.4 Homepage height budget

Target: about 3,000px at 1440px wide (current homepage 7,661px measured, about 9,400px per CLAUDE.md's earlier figure). Each direction in section 9 gives per-section budgets summing to 2,850-3,050px. A section that exceeds its budget by more than 15% must be cut down, not allowed to grow. Mobile (390px) target: under 6,000px.

---

## 5. Homepage content structure

Copy below is condensed from `index.html` (services) and `about.html` (convictions). It is not final; it is the substance to work with. All copy must follow CLAUDE.md writing rules: no em dashes, British spelling, banned word list.

### 5.1 Sections, in order

**(1) Header.** Logo left. Nav right: Approach · Services · Insights · Firm · Contact (rendered as five links; the middots here are only notation). "Book a call" primary button. EN/PT switch at the far right. PT labels: see Open questions.

**(2) Hero.** H1 (thesis), one supporting line, one primary action ("Book a call", to `/contact#calendar`). No second button.
- H1 placeholder options:
  - "Sharper judgment for the age of AI."
  - "AI that strengthens the analyst."
  - "The thinking stays human. The rest moves faster."
- Supporting line: "Solven trains private equity teams on AI and builds it into their workflows, so the people making the call still own the reasoning behind it."
- The thesis phrase "Augmentation without cognitive atrophy" is kept as the H2 of section 4 (see below).

**(3) Services.** H2: "Four ways we work with a firm." Four items, each an H3, at most two lines of text (about 110 characters), and one link.

| Service | Two-line text | Link |
|---|---|---|
| Enablement | Hands-on Claude sessions for the whole firm, analyst to managing partner, run monthly because the frontier moves weekly. | The programmes → `/programmes` |
| Build | Agents and workflow systems on the real work: contract redlining, IC memo interrogation, portfolio reporting. | Selected work → `/work` |
| AI Diligence | An independent read on whether a target's AI is genuine capability or marketing, before the term sheet is signed. | How it works → `[detail page TBD]` |
| Token Economics | Where the compute spend goes, what it returns, and how to pace it so the year's budget lasts the year. | How it works → `[detail page TBD]` |

**(4) Why Solven.** H2: "Augmentation without cognitive atrophy." Three convictions, H3 plus one sentence each:
- Judgment is the product. "In an investment firm the deliverable is a defensible decision; AI should make that judgment sharper, never thinner."
- Fluency is firm-wide. "From the newest analyst to the managing partner, everyone should know where Claude belongs in their own work."
- The frontier is the job. "Staying current is a standing discipline, not a one-off project, which is why our work is monthly."
Section link: "Our approach" → `/approach`.

**(5) Latest insights.** H2: "Insights." Up to three entries from `blog/` (title, date, one-line summary or photo per direction). Section link: "All insights" → `/blog`. Placeholders allowed: `[Insight title]`, `[Month 2026]`.

**(6) Closing call to action.** H2: "Let's tune a programme to your firm's priorities." One line: "A short conversation is the fastest way to see where Claude belongs in your team's work, and where it shouldn't." Primary button "Book a call". Secondary text link "Write to us" → `/contact`. The line "Member of the Anthropic Partner Network" may sit here in `--fs-small`, plain text.

**(7) Footer.** Anchor colour. Reversed logo; "Lisbon, Portugal"; email; nav repeat (Approach, Services, Insights, Firm, Contact); EN/PT switch; legal row: "© 2026 Solven Advisory, Lda · Privacy · Cookie settings". LinkedIn as a text link, no icon.

### 5.2 Reserved slots (describe, do not build)

- **Clients**, between (4) and (5): heading, a two-line intro, one static horizontal row of up to six marked placeholders `[Client logo · pending permission]`, 160px each, greyscale, no motion. Budget when built: 280px. Reason: the Actionist clients section the client liked, as a static row (screenshot name: "horizontal flow, not scroll").
- **Careers**, between (5) and (6): one photo panel (3:2) left, H2, two-line paragraph and a text link right. Budget when built: 420px. Reason: the Actionist careers section the client liked.
- Neither slot appears in Phase 4 mockups except as a 1px dashed outline with its name, if the owner asks to see placement.

### 5.3 Exclusions

No founder names or photos, no team grid, no client logos (until permitted), no case numbers or statistics, no testimonial quotes, nothing about AI Flix, no FAQ on the homepage, no Token Economics chart, no cadence timeline. The practices grid and the AI Diligence pitch/surface comparison move off the homepage to their detail pages.

---

## 6. Components

All interactive states change **colour, background-colour, border-colour, text-decoration or opacity only**, with `transition: <property> 120ms linear`. Never transform, size, position or blur. Under `@media (prefers-reduced-motion: reduce)` set `transition: none` on everything. Focus: `outline: 2px solid var(--c-focus); outline-offset: 3px` on `:focus-visible` for every link, button and input (on anchor bands, `--c-on-anchor`). Never remove an outline without replacing it.

### 6.1 Header and nav

- Desktop (≥960px): height 80px, 1px bottom rule, `--c-ground`. Logo left on column 1. Nav links 16px sans 400, `--c-text`, 32px apart; current page weight 500 with a 1px underline 6px below. Then "Book a call" primary button (small size, 40px tall), then the EN/PT switch 24px to its right.
- Hover on nav: underline appears (1px, `--c-text`), no colour shift.
- Tablet and mobile (<960px): height 64px. Logo left; "Menu" text button right (16px, 500, 44px tap target). It opens a full-width panel below the header on `--c-ground` (no animation, instant): links 18px stacked with 1px rules, 56px rows, then "Book a call" full width, then the EN/PT switch. "Close" replaces "Menu". `aria-expanded` and `aria-controls` set; Escape closes.
- Skip link "Skip to content" is the first element, visible on focus.

### 6.2 Buttons

| | Primary | Secondary |
|---|---|---|
| Fill | `--c-anchor` | transparent |
| Text | `--c-on-anchor`, 16px sans 500 | `--c-anchor`, 16px sans 500 |
| Border | 1px `--c-anchor` | 1px `--c-anchor` |
| Size | 48px tall, padding 0 24px (header: 40px, 0 16px) | same |
| Radius | 3px | 3px |
| Hover | fill `--c-text` (P1: `--c-accent`) | fill `--c-band` |
| Focus | outline as above | outline as above |
| Disabled | not used | not used |

- Label then a 16px right arrow "→" set in the sans, 8px gap. The arrow does not move on hover.
- On an anchor band: primary becomes `--c-on-anchor` fill with `--c-anchor` text; hover fill `--c-on-anchor-muted`.
- One primary button per section at most. Mobile: buttons are full width only inside the menu panel; elsewhere they keep natural width.

### 6.3 Text link

- Body links: `--c-link` text, `text-decoration: underline`, `text-decoration-thickness: 1px`, `text-underline-offset: 3px`, underline colour per palette (P1 `--c-accent`).
- Hover: thickness 2px and (P1, P2) text in `--c-accent`; (P3) underline in `--c-text`.
- Section links ("All insights →", "Read more →"): 16px sans 500, underlined, trailing arrow. One per section.

### 6.4 Facts strip (Direction 1)

- Four equal cells on the grid (3 columns each), 1px rules top and bottom and between cells, height 112px, cell padding 24px.
- Each cell: one fact in 18px sans 500 `--c-text`, one 14px `--c-muted` caption line.
- Content (no numbers until the owner supplies verified ones): "Lisbon" / "Based in Portugal"; "Iberia and Europe" / "Where we work"; "Anthropic Partner Network" / "Member"; "Private equity" / "Our first focus". Any future figure stays `[Figure]` until verified.
- Mobile: 2 × 2, height 2 × 96px.

### 6.5 Service item

- **Box variant (D1):** 6 columns wide, min-height 216px, padding 32px, 1px `--c-rule` border, 3px radius, `--c-ground` on a `--c-band` section (or the reverse). H3, 12px gap, two-line body (16px allowed here for fit, `--c-text`), then link at the bottom-left. Whole box is not a link; only the text link is. Hover on box: none.
- **Row variant (D2, D3):** full content width, 1px rule above each row and below the last. Row padding 32px top and bottom. Columns: H3 (cols 1-3), text (cols 4-9), link right-aligned (cols 10-12). Row height about 120px. Mobile: stacked, 24px padding, link below text.

### 6.6 Conviction item

- H3 (sans 500, 21px) and one sentence (18px). Three items in a row, 4 columns each, separated by 24px gutters; a 1px rule above each item. No numbers, no icons.
- On an anchor band (D1): H3 `--c-on-anchor`, sentence `--c-on-anchor-muted`, rules `--c-rule-on-anchor`.
- Mobile: stacked, 32px apart.

### 6.7 Photo panel

- Allowed aspect ratios only: **3:2** (in-section photo with text beside it), **4:5** (portrait panel, insight images in D3), **1:1** (D2 hero), **16:9** (insight images in D2 if 3:2 does not fit), **3:1** (D3 full-width hero strip). Reason: Actionist 3:2 and 0.82; institutions 16:9 and 3:4; J.P. Morgan's Lisbon strip about 3.1:1.
- `object-fit: cover`, radius 0, no border, no overlay, no tint, no colour layer, no caption over the image.
- Every photo has `width`/`height` attributes (no layout shift), `loading="lazy"` below the fold, `decoding="async"`, real `alt` text. Formats AVIF or WebP with JPEG fallback; hero image under 180KB at 1440px.
- Exploration placeholder: a block in `--c-band` with a 1px `--c-rule` border at the final aspect ratio, and a 14px `--c-muted` caption centred inside: "Photo: [subject]", e.g. "Photo: Lisbon office interior, morning light, empty desk with printed memo".

### 6.8 Insight card

- D1 (list row): 1px rule above; date left (14px `--c-muted`, tabular), title (18px sans 500, `--c-text`) and one-line summary (16px `--c-muted`); row 88px. Whole row is the link; hover underlines the title.
- D2 (card): photo 3:2 on top, then 16px gap, date in 14px Plex Mono `--c-muted` ("14 Oct 2026"), 8px gap, title 20px sans 500 (two lines max), no category label. 4 columns wide. Whole card is one link; hover underlines the title. No border.
- D3 (feature plus list): one feature (photo 4:5 at 4 columns, title and one-line summary beside it) and two list rows as in D1.
- No uppercase category labels (unlike the client's dark "Latest news" screenshot), no open line frames.

### 6.9 CTA band

- Full-width band (colour per direction), content on the grid: H2 (cols 1-7), one supporting line (`--fs-lead`), primary button, optional secondary text link 24px to its right. Padding 80px top and bottom. Left-aligned, never centred.

### 6.10 Footer

- `--c-anchor` background, `--c-on-anchor` text, 64px top padding, 32px bottom.
- Top row: reversed lockup (cols 1-3); nav column (cols 5-6); contact column with "Lisbon, Portugal", email, LinkedIn (cols 7-9); EN/PT switch (cols 10-12, right).
- 1px `--c-rule-on-anchor` rule, then the legal row in 14px `--c-on-anchor-muted`, separated by middots.
- Links: `--c-on-anchor`, underline on hover. Footer column headings, if any, in 16px sans 500 sentence case; preferably none.
- Mobile: stacked, 32px between groups.

### 6.11 EN/PT switch

- Two text links "EN" and "PT" separated by a 1px vertical rule 14px tall, 14px sans 500. The current language is `--c-text` with `aria-current="true"`; the other is `--c-muted`, underlined on hover. Tap target 44 × 44px each.
- Each link targets the page's own counterpart (`/programmes` ↔ `/pt/programas`, etc.); on unpaired pages PT targets `/pt`. `lang` and `hreflang` attributes on each link.

---

## 7. Imagery

- Real, contextual, calm photography in natural colour: architecture (Lisbon stone, arcades, stairwells), workspaces (empty desks, meeting rooms in daylight), documents (printed memos, annotated pages, a pen on a term sheet), Lisbon light on façades and floors, hands at work (writing, turning a page, at a keyboard; faces out of frame).
- People only as hands, backs, or small figures in a space; nobody looks at the camera. No headshots, no portraits, no team photos.
- Never: gradients, 3D renders, abstract glass, ASCII or halftone treatments, AI-generated or AI-looking illustrations, icon-per-feature graphics, glows, colour overlays or tints, stock handshakes, screens showing chat interfaces.
- One photo per section at most; at most four photos on the homepage (insight images count).
- During Phase 4 explorations every photo is a placeholder block (section 6.7) with its intended subject. Sourcing is an open question.

---

## 8. Avoid list (consolidated)

From CLAUDE.md hard limits:
1. Any motion as a feature: scroll-triggered reveals, fade-ins, text that bolds or assembles on scroll, split letters, animated shapes, intro loaders, parallax, smooth-scroll hijacking, WebGL, animated or video backgrounds, autoplay carousels, marquees.
2. GSAP, Framer Motion, Lenis, any animation library, any framework, bundler or npm dependency. Do not extend `solven.js`.
3. Team headshot grids, founder names or photos.
4. Client logos, case numbers, invented statistics.
5. Anything about AI Flix.
6. Radius above 4px, pills, drop shadows, heavy rules.
7. Abstract gradients, 3D renders, non-photographic imagery.

From the old site (`current-site.md`):
8. Warm cream ground (`#F4F2EB`-like) and its bands `#EDEADF`, `#E7ECE3`.
9. Sage green as a brand colour (`#6B8068`, `#8FA68A`, `#C8D4C2`), and green-cast charcoal `#1F2420`.
10. Georgia outside the logo; Calibri or system stacks as the chosen body face.
11. Italicised single words in headlines; italic grey serif leads; italic quotes.
12. Small uppercase tracked labels (12px, 700, 0.22em) above headings and in footers.
13. 01/02/03 or i/ii/iii numbering on cards, practices, sessions or clauses.
14. Faded giant V watermark anywhere; the V lives only in the logo.
15. A 112px headline; serif at every level.
16. Two-CTA heroes, "wry lines", magnetic buttons, scroll-progress bars, film grain, header blur.

Generic AI-startup aesthetics:
17. Black or near-black page backgrounds with glows; blurred colour spheres.
18. Purple, blue or multicolour gradients.
19. Inter-on-black slogan heroes; giant centred one-liners.
20. Bento grids; 2 × 2 dark image cards with large radii.
21. Emoji or icon-per-feature cards; checkmark lists.

From synthesis section 5 (reference traits not to carry over):
22. Hark: abstract glass renders, hero video, pinned stats, giant serif numerals, translucent blue panels, people section.
23. Subduxion: 8-24px radii, ASCII canvas images, uppercase mono tags under titles, carousels.
24. Actionist: logo marquee, clip-path mask reveals, header reacting to scroll direction, orange glow sphere, 30px pills, 100px rounded photo corner, weight 200 body text.
25. Institutions: uppercase labels above headings (Goldman, Evercore, Morgan Stanley, Lazard); J.P. Morgan's coloured last word; carousels with counters ("01 / 06"); background video (Evercore).
26. From the owner's rejected sketches (`redesign-log.md`): dark green with brass and a classic serif, centred ("Private Bank"); oversized grotesk on white with cobalt ("Swiss Ledger"); ticker bands and orange ("Tear Sheet").

---

## 9. The three directions for Phase 4

All three follow sections 1-8 exactly. They differ only in layout, type pairing and palette. Each is a homepage mockup at 1440px and 390px, built as static HTML on its own child branch of `redesign/base`, and logged in `docs/redesign-log.md`.

### 9.1 Direction 1 · "Ledger" (Hark-like)

Type: Source Serif 4 (H1 300, H2 400) + Source Sans 3 (400, 500). Palette: P1 Ink and oxblood.

| # | Section | Layout | Surface | Budget |
|---|---|---|---|---|
| 1 | Header | Standard (6.1) | Ground | 80 |
| 2 | Hero | Type only. H1 left on cols 1-8, supporting line cols 1-7, primary button. 96px top, 64px bottom. | Ground | 440 |
| 3 | Facts strip | Four cells (6.4), full content width | Ground, ruled | 112 |
| 4 | Services | H2 left, then 2 × 2 boxes (6.5 box), 24px gaps | Band | 720 |
| 5 | Why Solven | H2 cols 1-7, three convictions in a row, link | **Anchor (the one dark band)** | 480 |
| 6 | Insights | H2 left and "All insights" right on one line; three list rows (6.8 D1) | Ground | 400 |
| 7 | Closing CTA | 6.9 | Band | 320 |
| 8 | Footer | 6.10 | Anchor | 360 |
| | **Total** | | | **2,912** |

Photos: none on the homepage. Distinct because: it is the only type-led direction (no photograph above the fold), the only one with a facts strip and boxed services, and the only one that puts the convictions on the dark band. It reads like the first page of an annual report.

### 9.2 Direction 2 · "Register" (Subduxion-like)

Type: Spectral (H1 300, H2 400) + IBM Plex Sans (400, 500); IBM Plex Mono 400 only for insight dates. Palette: P3 Bottle green, no accent.

| # | Section | Layout | Surface | Budget |
|---|---|---|---|---|
| 1 | Header | Standard | Ground | 80 |
| 2 | Hero | H1, line and button on cols 1-6, vertically centred; photo panel 1:1 on cols 8-12 (about 486 × 486). Photo: "Lisbon office interior, morning light, papers on a desk". | Ground | 620 |
| 3 | Services | H2 and a one-line lead, then four ruled rows (6.5 row) | Ground | 700 |
| 4 | Why Solven | H2 left, three convictions in a quiet three-column row, rules above each, link | Band | 400 |
| 5 | Insights | H2 left and "All insights" right; three cards with 3:2 photos and Plex Mono dates (6.8 D2) | Ground | 600 |
| 6 | Closing CTA | 6.9, separated from Insights by a 1px rule | Ground | 280 |
| 7 | Footer | 6.10 | Anchor (the only dark surface) | 360 |
| | **Total** | | | **3,040** |

Photos: hero plus three insight images (four). Distinct because: it is the quietest direction, with no full dark band at all (the anchor appears only in the footer, in buttons and headings), services as a ruled register of rows rather than boxes, a split hero with one square photograph, and the only use of a monospace.

### 9.3 Direction 3 · "Chapters" (Actionist-like)

Type: Source Serif 4 (H1 300, H2 400) + Source Sans 3 (400, 500). Palette: P2 Oxblood.

| # | Section | Layout | Surface | Budget |
|---|---|---|---|---|
| 1 | Header | Standard | Ground | 80 |
| 2 | Hero chapter | H1 cols 1-8 and line cols 1-7, primary button; 48px below, a full-bleed 3:1 photo strip (1440 × 480). Photo: "Lisbon arcade or stone stairwell in raking light". | Ground | 800 |
| 3 | Services chapter | Photo panel 3:2 on cols 1-6 (588 × 392). Right, cols 7-12: H2, then four compact rows (6.5 row, stacked: H3 above text, link inline) | Ground | 640 |
| 4 | Why Solven chapter | Mirror: cols 1-6 H2 and three convictions stacked (rule above each), cols 8-12 photo panel 4:5. Photo: "Hands annotating a printed memo". | Band | 600 |
| 5 | Insights | H2 left, "All insights" right; one feature (photo 4:5 cols 1-4, title and summary cols 5-8) and two list rows on cols 9-12 | Ground | 460 |
| 6 | Closing CTA | 6.9 on oxblood | **Anchor (the one dark band)** | 300 |
| 7 | Footer | 6.10, separated from the CTA by a 1px `--c-rule-on-anchor` rule | Anchor | 320 |
| | **Total** | | | **3,200** |

Photos: hero strip, services, convictions, one insight (four). Distinct because: it is the only direction built from alternating photo and text panels (left, then right), the only full-bleed photograph, and the only one where the dark band is the closing call to action, flowing into the footer. It reads like chapters of a printed brochure. The total runs about 7% over 3,000px; if it must come down, shorten the hero strip to 4:1 (1440 × 360, saving 120px).

### 9.4 Common acceptance checks for every direction

- Height at 1440px within 2,850-3,200px; no horizontal scroll at 390px; one H1.
- No text fails the contrast table; every focus state visible; keyboard path header → hero CTA → services links → footer works.
- No em dash in any file; no italic, uppercase label, numbering or watermark anywhere.
- Lighthouse performance ≥ 95 on desktop with placeholders; total font payload under 150KB.
- PT test line renders in every face used.

---

## 10. Open questions

1. **Headline.** Which of the three H1 options (or another)? Copy is placeholder until chosen.
2. **Navigation and URLs.** The new nav is Approach · Services · Insights · Firm · Contact, but current URLs are `/programmes`, `/blog`, `/about`. Rename the pages (with 301s, sitemap, hreflang and canonical updates) or keep URLs and change only labels?
3. **PT nav labels.** Proposed: Abordagem · Serviços · Publicações · Sobre nós · Contacto. "Firma" is excluded by the European Portuguese rules; "Firm" needs an approved PT equivalent. Insights are EN-only today: does the PT nav link to the EN journal as "Publicações · EN"?
4. **Detail pages for AI Diligence and Token Economics.** Their homepage sections are removed; where do the "How it works" links go (sections of `/programmes`, or new pages)?
5. **Logo legibility.** At header size, "ADVISORY" renders at about 6px in every supplied lockup. Is that acceptable as a mark, or should the header use the wordmark-only file `04`? Also, the logo's text is live `<text>` in Georgia and Calibri, which renders differently on devices without those fonts; may it be converted to outlined paths (same geometry) for consistency?
6. **Logo mark colour in P2 and P3.** The brief puts the V and "ADVISORY" in the muted grey because P2's accent is links-only and P3 has none. Confirm, or prefer the anchor for both slots.
7. **Photography source.** Commissioned Lisbon shoot, licensed stock, or the owner's own photos? Placeholders until decided.
8. **Facts strip content (D1).** Are the four placeholder facts acceptable, and is "Anthropic Partner Network" to be shown with "Phase 1" and a verification link?
9. **Fonts at build.** Keep Google Fonts in production (third-party request, but cookieless) or self-host the woff2 files as synthesis 4d suggested?
10. **Founder count.** The contact signature says "Co-founder" and about says "the team". The homepage avoids the question, but the Firm page will need an answer.
11. **Insights on the homepage.** Should they always show the three newest journal posts, or a hand-picked set? Do insight images exist for the current three articles?
12. **D3 budget.** Accept about 3,200px, or enforce 3,000px by shortening the hero strip?
