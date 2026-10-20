# Solven Advisory website

Marketing site for Solven Advisory (solvenadvisory.ai). Plain HTML, CSS and JS; no framework.

## Layout on this branch

| Path | What it is |
|---|---|
| `public/` | **The site (site v5).** Generated; Vercel serves this folder (`vercel.json`: `outputDirectory`). Never hand-edit. |
| `content/site-copy.md`, `content/insights/` | All page copy (EN and PT) and the articles, in Markdown. |
| `tools/build_site_v5.py` | Builds the site: `--prod` writes `public/`; without it, the preview in `explorations/site-v5/`. |
| `legacy-site/` | The pre-v5 site, exactly as on `main`, kept only for comparison. Not deployed. See `legacy-site/README.md`. |
| `explorations/`, `docs/` | Design explorations and working notes. Not deployed. |

## Build and run

    python3 tools/build_site_v5.py --prod      # rebuild public/ after any copy change
    python3 tools/serve.py                     # site v5 on http://127.0.0.1:8000

Compare with the old site side by side, in a second terminal:

    python3 tools/serve.py 8001 legacy-site    # the pre-v5 site on http://127.0.0.1:8001

`tools/serve.py` mirrors Vercel: clean URLs, no trailing slash, the redirects in `vercel.json`
(the old site's addresses go to their place in v5), and `404.html` on a miss.
