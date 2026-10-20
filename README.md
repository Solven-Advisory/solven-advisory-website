# Solven Advisory website

> **Never merge this branch into `main`.** It makes site v5 the site and moves the old one to
> `legacy-site/`. Pushing to `main` deploys to production immediately, so a merge would replace
> the live site. The file `.no-merge-to-main` marks the branch; the guards below refuse the merge.

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

## Never merge this branch into main

Guards, all keyed on the file `.no-merge-to-main` at the repo root:

- `tools/git-hooks/pre-merge-commit`: refuses a merge commit into `main`/`master` that brings the file in.
- `tools/git-hooks/pre-push`: refuses a push to `main`/`master` (any remote) of a commit that contains it.
  This also catches a fast-forward, which makes no merge commit.
- `tools/git-hooks/post-merge`: after any merge or fast-forward that leaves `main` carrying the file,
  prints a warning and the undo command (`git reset --hard ORIG_HEAD`). It changes nothing itself.
- `.github/workflows/no-merge-to-main.yml`: fails every pull request into `main`/`master` from a branch
  that has the file. It blocks the merge button only once "No merge to main / guard" is a required
  status check in GitHub (Settings > Branches > protection rule for `main`).

Git hooks are not versioned: install them once per clone with `sh tools/git-hooks/install.sh`
(it copies them into `.git/hooks/`, so they keep working while `main` is checked out).

To remove the guards: revert the commit that added them (or delete `.no-merge-to-main`,
`tools/git-hooks/`, `.github/workflows/no-merge-to-main.yml`, this section and the note at the top),
then `rm .git/hooks/pre-merge-commit .git/hooks/pre-push .git/hooks/post-merge` in each clone.
Deleting the marker disarms the merge hook and the pull-request check, but `pre-push` checks every
commit being pushed, and earlier commits still carry the marker, so the installed hooks must go too.
