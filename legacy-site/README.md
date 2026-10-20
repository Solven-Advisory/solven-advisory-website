# Legacy site (reference copy)

The production site as it was on `main` (commit d0bb425) before site v5 replaced it on this
branch. Kept here only to compare against site v5; it is not deployed (Vercel serves `public/`).

The pages, `blog/`, `pt/`, `solven.css`, `solven.js`, `consent.js`, `llms.txt`, `llms-full.txt` and
`sitemap.xml` were moved here unchanged. `assets/`, `robots.txt`, `site.webmanifest` and `vercel.json`
are copies of `main`'s, so the folder runs on its own.

## Open it

From the repo root:

    python3 tools/serve.py 8001 legacy-site    # the old site: http://127.0.0.1:8001
    python3 tools/serve.py                     # site v5, in another terminal: http://127.0.0.1:8000

The links and assets use absolute paths (`/about`, `/assets/...`), so serve this folder as the
site root as above; opening the files directly or from `/legacy-site/...` breaks them. The server
applies this folder's own `vercel.json` (clean URLs, `/blog.html` to `/blog`), not site v5's redirects.
