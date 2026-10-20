# Writing an insight

Each insight is one Markdown file in this folder. The file name is its address:
`making-every-token-earn-its-place.md` becomes `/insights/making-every-token-earn-its-place`.
After adding an insight or changing its title or topic, make its share image (the card LinkedIn and
others show), then rebuild the site:

    python3 tools/build_og_images.py
    python3 tools/build_site_v5.py --prod

The production build stops if an insight has no share image. For any other edit, the rebuild alone is enough.

## The header block

Every file starts with this block. All lines are required except the last five.

    ---
    title: How to tell whether the AI is real
    subtitle: One or two sentences under the title, at the top of the page.
    summary: One short line for the cards on the homepage and the Insights page.
    description: The sentence search engines and link previews show (about 150 characters).
    topic: AI diligence
    date: 2026-09-09
    image: ai-diligence.jpg
    image_alt: What the photograph shows, for readers who cannot see it.
    date_is_placeholder: no
    updated: 2026-11-04
    service: Token Economics
    ---

- **image**: a real photograph, chosen for each insight. Put the file in `content/insights/images/`
  and write its file name here. Until one is chosen, leave it empty and the page shows a marked
  placeholder.
- **image_alt**: required once there is an image.
- **date_is_placeholder**: `yes` marks the date as a dummy on the page, until the real one is known.
- **updated**: the day of the last material revision. The page shows it as a tag ("Updated 4 Nov 2026") and search
  engines read it (`dateModified`). Leave it out until there is one.
- **service**: the service on the homepage this insight belongs to, exactly as named there (Enablement, Build,
  Portfolio, Token Economics). The article ends with a line linking to it. Leave it out for no link. The
  Portuguese translation takes its original's; do not repeat it there.
- The reading time is counted from the text. To set it by hand, add `minutes: 6`.

## The text

    A paragraph is lines of text; a blank line starts the next one.

    ## A section heading

    ### A smaller heading, if a section needs one

    > A pull quote.

    - A bulleted item
    - Another

    1. A numbered item
    2. Another

    **Bold**, *italic*, and [a link](/book).

    ![What the photograph shows](another-photo.jpg)

The title comes from the header block, so the text never starts with a single `#`.
House rules still apply: no em dashes, British spelling.

## The Portuguese version

Each insight can have a European Portuguese translation in `content/insights/pt/`. Its file name is
its Portuguese address (`pt/fazer-cada-token-valer-o-que-custa.md` becomes
`/pt/insights/fazer-cada-token-valer-o-que-custa`), and its header block has one extra line, `en:`,
naming the English file it translates:

    en: making-every-token-earn-its-place

The PT toggle on the English article goes to its translation; an English insight without one
toggles to the Portuguese index, and declares no Portuguese counterpart (no hreflang pair). Write in European Portuguese, never Brazilian: equipa, utilizador,
registo, perceber, «guillemets», "a fazer" rather than "fazendo". The build stops if it finds a
common Brazilian form.

Once the owner has read and approved a translation, add `reviewed: YYYY-MM-DD` to its header block.
The build warns about every translation without one (and every unreviewed entry in
`content/site-copy.md`); `python3 tools/build_site_v5.py --pt-review` lists them.

## Photo sources

Every photograph in `images/` must be free to use without a licence or credit. The current ones are
CC0 (public domain dedication), from the Unsplash archive on Wikimedia Commons:

- `editors-of-drafts.jpg`: "Sign here" by Helloquence, https://commons.wikimedia.org/wiki/File:Sign_here_(Unsplash).jpg
- `ai-diligence.jpg`: "Minimalist meeting room" by Breather, https://commons.wikimedia.org/wiki/File:Minimalist_meeting_room_(Unsplash).jpg
- `token-economics.jpg`: "Desktop with laptop and calculator", https://commons.wikimedia.org/wiki/File:Desktop_with_laptop_and_calculator_(Unsplash).jpg

Saved at 2000px wide, JPEG quality 78. The page crops them to 16:7 (4:3 on phones).
