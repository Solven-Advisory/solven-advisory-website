# Writing an insight

Each insight is one Markdown file in this folder. The file name is its address:
`making-every-token-earn-its-place.md` becomes `/insights/making-every-token-earn-its-place`.
After adding or editing a file, rebuild the site:

    python3 tools/build_site_v5.py

## The header block

Every file starts with this block. All lines are required except the last three.

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
    ---

- **image**: a real photograph, chosen for each insight. Put the file in `content/insights/images/`
  and write its file name here. Until one is chosen, leave it empty and the page shows a marked
  placeholder.
- **image_alt**: required once there is an image.
- **date_is_placeholder**: `yes` marks the date as a dummy on the page, until the real one is known.
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
`/pt/publicacoes/fazer-cada-token-valer-o-que-custa`), and its header block has one extra line, `en:`,
naming the English file it translates:

    en: making-every-token-earn-its-place

The PT toggle on the English article goes to its translation; an English insight without one
toggles to the Portuguese index. Write in European Portuguese, never Brazilian: equipa, utilizador,
registo, perceber, «guillemets», "a fazer" rather than "fazendo". The build stops if it finds a
common Brazilian form.
