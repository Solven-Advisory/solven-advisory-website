# Going live and console setup: step-by-step guide

Written 2026-10-20. This guide takes site v5 from this branch to the live address `solvenadvisory.ai` and sets up the dashboards around it (Vercel, GoDaddy, Google Search Console, Bing, Ahrefs, Microsoft 365). Follow the parts in order and tick each box as you go. Do not skip a check: each one tells you whether it is safe to continue.

Button and menu names are as they were in October 2026. If a label is slightly different on screen, look for the closest match in the same place.

---

## Who does what

There are two people in this guide.

- **Owner:** the person whose GitHub account is connected to the Vercel account that hosts the site. Today all 51 commits on `main` are theirs. Only the Owner can log in to Vercel and only the Owner's commits can reach `main`.
- **Developer:** the person who built site v5 on the branch `redesign/site-v5-seo`. The Developer must never appear in the history of `main`.

### Why the Developer cannot touch `main`

The site is on Vercel's free plan (Hobby). On Hobby, a project has one account, and Vercel deploys only commits made by that account's GitHub user. A commit made by anyone else is blocked, and community reports suggest that a `Co-Authored-By:` line naming someone else in a commit message can also trigger the block. So:

1. The Developer never merges, never opens a pull request into `main`, and never pushes to `main`.
2. The Developer pushes only the branch `redesign/site-v5-seo`.
3. The Owner copies the finished files from that branch into **one new commit of their own** on `main`, and pushes it. That commit contains the files but none of the Developer's history. This step is called **a release** in this guide (Part 2).
4. Every later change follows the same path: Developer pushes the branch, Owner does a release (Part 9).

| Part | What | Who |
|---|---|---|
| 1 | Prepare and push the branch | Developer |
| 2 | Release site v5 to `main` | Owner |
| 3 | Vercel domains | Owner |
| 4 | GoDaddy DNS for the website | Whoever has the GoDaddy login (probably the Owner) |
| 5 | Send the `vercel.app` address to the real domain (a small edit on `main`) | Owner |
| 6 | Vercel Web Analytics | Owner |
| 7 | Google Search Console, Bing, Ahrefs | Either; whoever does it adds the other as a user |
| 8 | Email records (SPF, DKIM) | Microsoft 365 admin and the GoDaddy login |
| 9 | Every later update | Developer, then Owner |
| 10 | Final checks | Either |
| 11 | If something goes wrong | Owner |

---

## What is already done (no action needed)

- **Vercel Web Analytics script** on every page (`/_vercel/insights/script.js`, cookieless). It returns "404 not found" until the Owner switches Analytics on (Part 6).
- **`vercel.json`:** tells Vercel to serve the `public/` folder, with clean addresses (no `.html`), no trailing slash, 15 permanent redirects from the old site's addresses (`/programmes`, `/contact`, `/blog/...`, `/pt/contacto` and the rest), security headers and long caching for images.
- **For search engines and AI:** `robots.txt`, `sitemap.xml` (14 addresses), `llms.txt`, `llms-full.txt`, canonical addresses on `https://solvenadvisory.ai`, English/Portuguese pairing (hreflang).
- **Google verification record:** a TXT record `google-site-verification=GpoVtoyc...` already exists on `solvenadvisory.ai`.

## Where things stand (checked 2026-10-20)

- `main` on GitHub still holds the old site. Its last commit is `d0bb425` (29 July 2026, by the Owner). The branch `redesign/site-v5-seo` contains that commit, so nothing on `main` is lost by a release.
- The branch `redesign/site-v5-seo` exists only on the Developer's computer. It is **not on GitHub yet**.
- `solvenadvisory.ai` (without `www`) points to GoDaddy's forwarding service, not to Vercel. It answers with an error (405) or sends visitors to `solven-advisory-website.vercel.app`.
- `www.solvenadvisory.ai` points to Vercel and works.
- Email: the SPF record (`v=spf1 include:secureserver.net -all`) does not allow Microsoft 365 to send for the domain, DKIM is not set up, and DMARC is set to quarantine. Emails from Solven addresses can land in spam.

---

## Part 1. Prepare and push the branch

**Who:** Developer, in a terminal, in the folder `solven-advisory-website`.

1. [ ] Check you are on the right branch:
   ```
   git branch --show-current
   ```
   It must print `redesign/site-v5-seo`. If it prints anything else, stop and run `git switch redesign/site-v5-seo`.
2. [ ] Rebuild the site:
   ```
   python3 tools/build_site_v5.py --prod
   ```
   It must end without an error. If it prints an error, stop and fix it first (ask Claude).
3. [ ] Look at the site on your computer:
   ```
   python3 tools/serve.py
   ```
   Open http://127.0.0.1:8000 in a browser. Click through: home, Insights, one article, Book (the calendar must appear), Privacy, then the PT link and the same pages in Portuguese. Stop the server with `Ctrl+C`.
   (Vercel will not build previews of your commits on the free plan, so this local check is the only preview.)
4. [ ] Commit anything that is not committed yet:
   ```
   git status
   ```
   If it lists changed files you want in the release, commit them (`git add <file>` then `git commit -m "<what changed>"`). Files you do not want can stay uncommitted: only committed files go to GitHub.
5. [ ] Push **the branch only**. Type it exactly:
   ```
   git push -u origin redesign/site-v5-seo
   ```
   Never type `git push origin main`, never open a pull request into `main` on GitHub, never press "Merge" on GitHub.
6. [ ] Vercel may now email the Owner that a deployment of this branch was blocked, or show a red "Blocked" status on GitHub. That is expected and harmless: nothing changes on the live site.
7. [ ] Tell the Owner: "The branch `redesign/site-v5-seo` is on GitHub, ready for release. Last commit: `<paste the output of git rev-parse --short HEAD>`."

## Part 2. Release site v5 to `main`

**Who:** Owner, in a terminal (Terminal on Mac, PowerShell or Git Bash on Windows). You need `git` installed and access to the GitHub repository `Solven-Advisory/solven-advisory-website`.

### 2a. First time only: get the repository

1. [ ] If you do not have the repository on your computer yet:
   ```
   git clone https://github.com/Solven-Advisory/solven-advisory-website.git
   ```
2. [ ] Go into the folder:
   ```
   cd solven-advisory-website
   ```
3. [ ] Check that git uses **your** identity:
   ```
   git config user.name
   git config user.email
   ```
   The email must be one of the emails on the GitHub account that is connected to Vercel (GitHub → your photo, top right → **Settings** → **Emails** shows them). If it is wrong, set it:
   ```
   git config user.name "Your Name"
   git config user.email "you@example.com"
   ```

### 2b. Every release

Run these from inside the `solven-advisory-website` folder, one at a time, and compare the output with what is written.

1. [ ] Make sure you have no unsaved local work:
   ```
   git status
   ```
   It must say `nothing to commit, working tree clean`. If not, stop and ask the Developer.
2. [ ] Switch to `main` and update it:
   ```
   git switch main
   git pull
   ```
3. [ ] Download the Developer's branch:
   ```
   git fetch origin redesign/site-v5-seo
   ```
4. [ ] Check that the branch contains everything on `main` (so the release does not throw away anything):
   ```
   git merge-base --is-ancestor main origin/redesign/site-v5-seo && echo SAFE
   ```
   It must print `SAFE`. If it prints nothing, stop: someone added commits to `main` that the branch does not have. Ask the Developer to sync the branch with `main` (Part 9 step 1) and push it again, then start this release over.
5. [ ] Replace the files on `main` with the files from the branch. This changes files only; it does not copy anyone's commits:
   ```
   git read-tree -u --reset origin/redesign/site-v5-seo
   ```
   It prints nothing. That is normal.
6. [ ] Remove the two "do not merge" guard files (they exist only on the branch, to stop accidental merges):
   ```
   git rm -q -f .no-merge-to-main .github/workflows/no-merge-to-main.yml
   ```
7. [ ] Check that the guard files are gone:
   ```
   ls .no-merge-to-main
   git status --short | grep no-merge
   ```
   The first line must print `No such file or directory` (or `cannot access`). The second must print nothing at all.
8. [ ] Make the release commit. Write the message yourself and do **not** add any `Co-Authored-By:` line. If you use Claude Code or another AI tool for this step, tell it explicitly to leave out the Co-Authored-By line.
   ```
   git commit -m "Release site v5"
   ```
9. [ ] Check that the commit is yours and carries no co-author:
   ```
   git log -1 --format='%an <%ae>%n%b'
   ```
   The first line must be your name and email. There must be no `Co-Authored-By` line.
10. [ ] Check that nobody else's commit is about to go to `main`:
    ```
    git log origin/main..main --format='%an <%ae>'
    ```
    It must print exactly **one** line, with your name and email.
11. [ ] Push:
    ```
    git push origin main
    ```
12. [ ] Watch the deployment: go to https://vercel.com → log in → click the project **solven-advisory-website** → tab **Deployments** at the top. The newest row must say **Production** and turn **Ready** (green) within a minute or two. If it says **Error** or **Blocked**, go to Part 11.
13. [ ] Open https://www.solvenadvisory.ai in a private browser window. You must see the new site. Click **Book a call**: the calendar must appear on the page.

## Part 3. Vercel domains

**Who:** Owner. Do this after Part 2.

1. [ ] Go to https://vercel.com → log in → click the project **solven-advisory-website** → tab **Settings** at the top → **Domains** in the left menu.
2. [ ] You see a list of domains. If `solvenadvisory.ai` (without `www`) is **not** in the list: click **Add Domain** (top right), type `solvenadvisory.ai`, click **Add**. If Vercel offers a choice about `www`, pick the option that **redirects `www.solvenadvisory.ai` to `solvenadvisory.ai`**.
3. [ ] Next to `solvenadvisory.ai`, Vercel shows a red **Invalid Configuration** and the DNS record it wants: Type **A**, Name **@**, and a Value (an IP address such as `216.198.79.1` or `76.76.21.21`). **Write down that Value exactly.** You need it in Part 4.
4. [ ] Find the row `www.solvenadvisory.ai` → click **Edit** (or the **⋯** menu, then **Edit**) → under **Redirect to**, choose `solvenadvisory.ai` → status code **308 Permanent Redirect** → **Save**.
5. [ ] Find the row `solvenadvisory.ai` → **Edit** → make sure **Redirect to** is empty ("No redirect") and the environment is **Production** → **Save**.
6. [ ] Leave this tab open. The apex row stays red until Part 4 is done.

## Part 4. GoDaddy DNS for the website

**Who:** whoever has the GoDaddy login for `solvenadvisory.ai`. Do this right after Part 3: for a short while during this part, `solvenadvisory.ai` (without `www`) may not load. `www` keeps working.

1. [ ] Go to https://www.godaddy.com → **Sign In** (top right) → your name (top right) → **My Products**.
2. [ ] In the **Domains** list, find `solvenadvisory.ai` → click **DNS** (or the **⋯** next to it, then **Manage DNS**).
3. [ ] You see tabs: **DNS Records**, **Forwarding**, **Nameservers** and others. Click **Forwarding**.
4. [ ] Under **Domain**, there is a forwarding to `solven-advisory-website.vercel.app` (or similar). Click the **trash icon** (or **⋯** → **Delete**) and confirm. Leave any **Subdomain** forwarding alone unless it is for `www`.
5. [ ] Click the tab **DNS Records**.
6. [ ] Find the rows with **Type A** and **Name @**. Click the **pencil** (Edit) on the first one, set **Value** to the IP you wrote down in Part 3 step 3, leave TTL as it is, click **Save**.
7. [ ] If there are other **A** rows with **Name @**, delete them (trash icon → confirm). There must be exactly one A record on @.
8. [ ] Do **not** touch these rows: the **CNAME `www`** (it already points to Vercel), the **MX** rows, the **TXT** row starting `google-site-verification=`, the **TXT** row `NETORGFT20700852.onmicrosoft.com`, and anything with `autodiscover`, `_domainkey` or `_dmarc` in its name.
9. [ ] Wait 15 minutes. Then check on https://dnschecker.org: type `solvenadvisory.ai`, choose **A**, click **Search**. Most places must show the IP from Part 3. If they still show `15.197.225.128` or `3.33.251.168`, wait longer (up to a few hours) and check again.
10. [ ] Back in Vercel (**Settings** → **Domains**), refresh the page. `solvenadvisory.ai` must show **Valid Configuration** (blue or green). Vercel issues the HTTPS certificate automatically; that can take a few more minutes.
11. [ ] Open https://solvenadvisory.ai in a private window: the new site loads. Then open https://www.solvenadvisory.ai/book: the address bar must end up as `https://solvenadvisory.ai/book`.

## Part 5. Send the `vercel.app` address to the real domain

**Who:** Owner, alone, directly on `main`. Do this only after Part 4 step 11 works; doing it earlier creates a redirect loop.

This is one small edit to one file, `vercel.json`. It needs no rebuild.

1. [ ] In a terminal, inside the `solven-advisory-website` folder, update `main`:
   ```
   git switch main
   git pull
   git status
   ```
   `git status` must say `nothing to commit, working tree clean`.
2. [ ] Open the file `vercel.json` (in the top folder of the repository) in a text editor (VS Code, Notepad, TextEdit in plain-text mode).
3. [ ] Find this line. It is the last line inside `"redirects": [`:
   ```
       { "source": "/pt/publicacoes/:slug", "destination": "/pt/insights/:slug", "permanent": true }
   ```
4. [ ] Put a comma at the very end of that line, then add a new line after it, so the two lines read exactly:
   ```
       { "source": "/pt/publicacoes/:slug", "destination": "/pt/insights/:slug", "permanent": true },
       { "source": "/:path*", "has": [{ "type": "host", "value": "solven-advisory-website.vercel.app" }], "destination": "https://solvenadvisory.ai/:path*", "permanent": true }
   ```
   The next line must still be `  ],`. Change nothing else. Save the file.
5. [ ] Check that only that file changed, and only by those lines:
   ```
   git diff
   ```
   It must show one line removed (the old `/pt/publicacoes/:slug` line without the comma) and two lines added (the same line with the comma, and the new line). If it shows anything else, run `git checkout vercel.json` to undo and start again from step 2.
6. [ ] Commit and push. As in Part 2b, no `Co-Authored-By:` line:
   ```
   git commit -am "Send the vercel.app address to solvenadvisory.ai"
   git log -1 --format='%an <%ae>%n%b'
   git push origin main
   ```
   The `git log` line must show your name and email, with no `Co-Authored-By` line.
7. [ ] Vercel → project **solven-advisory-website** → tab **Deployments**. The newest row must say **Production** and turn **Ready**. If it says **Error**, the file has a typo: open the row to see the message, or use **Instant Rollback** (Part 11), and compare `vercel.json` with step 4 character by character.
8. [ ] Open https://solven-advisory-website.vercel.app/book in a private window. The address bar must end up as `https://solvenadvisory.ai/book`.
9. [ ] Tell the Developer: "I changed `vercel.json` on `main`. Sync the branch (Part 9 step 1) before your next change." If the Developer skips this, the next release would undo your edit; the check in Part 2b step 4 stops that release before it happens.

## Part 6. Vercel Web Analytics

**Who:** Owner.

1. [ ] Vercel → project **solven-advisory-website** → tab **Analytics** at the top.
2. [ ] Click **Enable** (if asked to choose, pick **Web Analytics**, not Speed Insights) → confirm. The free plan is enough.
3. [ ] Tab **Deployments** → newest row marked **Production** → **⋯** at the right end of the row → **Redeploy** → **Redeploy** again in the dialog. Wait for **Ready**.
4. [ ] Open https://solvenadvisory.ai/_vercel/insights/script.js in a browser. You must see a page of code, not "404".
5. [ ] Visit two or three pages of the site. Within a few minutes, the **Analytics** tab shows visitors.
6. [ ] Do not switch on any feature that uses cookies: the privacy notice says the site sets no cookies of its own.

## Part 7. Google Search Console, Bing, Ahrefs

**Who:** either person, with their own Google account. Do this after Part 4, so the search engines see the new site at the right address. Do 7a first: Bing and Ahrefs import from it.

### 7a. Google Search Console

1. [ ] Go to https://search.google.com/search-console and sign in with a Google account.
2. [ ] Top left, click the property menu → **Add property**.
3. [ ] Choose the left box, **Domain** (not "URL prefix"). Type `solvenadvisory.ai` → **Continue**.
4. [ ] If it says **Ownership verified**: go to step 6.
5. [ ] If it shows a TXT record to add instead: copy it (**Copy** button). Then in GoDaddy (Part 4 steps 1 and 2) → **DNS Records** → **Add New Record** → Type **TXT**, Name **@**, Value: paste, TTL: leave → **Save**. Do not delete the old `google-site-verification` row. Wait 10 minutes, go back to Search Console, click **Verify**. If it fails, wait an hour and click **Verify** again.
6. [ ] Left menu → **Indexing** → **Sitemaps**. In **Add a new sitemap**, type `sitemap.xml` after the address shown → **Submit**. Within a day, the status must be **Success** with 14 discovered pages.
7. [ ] At the very top, click the bar **Inspect any URL in "solvenadvisory.ai"**, paste `https://solvenadvisory.ai/`, press Enter, wait, click **Request indexing**. Do the same for `https://solvenadvisory.ai/pt`.
8. [ ] Left menu, bottom → **Settings** → **Users and permissions** → **Add user** → the other person's Google email → Permission **Full** → **Add**.
9. [ ] A week later: left menu → **Indexing** → **Pages**. Old addresses such as `/programmes` listed under **Page with redirect** are expected and fine.

### 7b. Bing Webmaster Tools

Bing results also feed ChatGPT search and Microsoft Copilot.

1. [ ] Go to https://www.bing.com/webmasters → **Sign in** (a Google account works).
2. [ ] On the welcome screen, under **Import your sites from GSC**, click **Import** → **Continue** → choose the same Google account as in 7a → **Allow**.
3. [ ] Tick `solvenadvisory.ai` → **Import**.
4. [ ] Left menu → **Sitemaps**. `https://solvenadvisory.ai/sitemap.xml` must be listed. If not: **Submit sitemap** → paste it → **Submit**.
5. [ ] Left menu → **Settings** → **User management** → **Add user** → the other person's email → role **Administrator** → **Add**.

### 7c. Ahrefs Webmaster Tools (free)

1. [ ] Go to https://ahrefs.com/webmaster-tools → **Sign up for free** → create the account and confirm the email.
2. [ ] When asked how to add a site, choose **Import from Google Search Console** → choose the same Google account as in 7a → **Allow** → tick `solvenadvisory.ai` → **Import**. No code or DNS change is needed.
3. [ ] Open **Site Audit** → the project → **New crawl** (or wait for the first automatic crawl). When it finishes, export or screenshot the overview and send it to the Developer. Expected and fine: a cookie warning on `/book` (it comes from the booking calendar) and redirects from old addresses.
4. [ ] Top menu → **Alerts** → switch on **New backlinks**, **Lost backlinks** and **Site Audit** issues (email).
5. [ ] Account menu (top right) → **Account settings** → **Members** → invite the other person.

## Part 8. Email records (SPF and DKIM)

**Who:** the Microsoft 365 admin for `solvenadvisory.ai`, together with whoever has the GoDaddy login. This does not affect the website; it stops Solven's emails from landing in spam. The Microsoft account was bought through GoDaddy (the `NETORGFT...` record shows it), so if a Microsoft page refuses access, call GoDaddy support and ask them to "enable DKIM for Microsoft 365 on solvenadvisory.ai".

### 8a. SPF

1. [ ] GoDaddy → **My Products** → `solvenadvisory.ai` → **DNS** → tab **DNS Records**.
2. [ ] Find the **TXT** row on **@** whose value starts with `v=spf1`. Click the **pencil**.
3. [ ] Replace the whole value with exactly:
   ```
   v=spf1 include:spf.protection.outlook.com include:secureserver.net -all
   ```
   **Save**. There must be only one TXT row starting with `v=spf1`.

### 8b. DKIM

1. [ ] Go to https://security.microsoft.com and sign in with the Microsoft 365 admin account.
2. [ ] Left menu → **Email & collaboration** → **Policies & rules** → **Threat policies** → under **Rules**, **Email authentication settings** → tab **DKIM**.
3. [ ] Click `solvenadvisory.ai`. If a button says **Create DKIM keys**, click it. The panel then shows two CNAME records, `selector1._domainkey` and `selector2._domainkey`, each with a long value. Keep this panel open.
4. [ ] In GoDaddy → **DNS Records** → **Add New Record** → Type **CNAME**, Name `selector1._domainkey`, Value: copy it from the Microsoft panel → **Save**. Repeat for `selector2._domainkey`.
5. [ ] Wait one hour. Back in the Microsoft panel, switch **Sign messages for this domain with DKIM signatures** to **On**. If it says the records are not found yet, wait longer and try again.
6. [ ] Test: send an email from a Solven address to a Gmail address. In Gmail, open it → **⋮** (top right of the message) → **Show original**. **SPF**, **DKIM** and **DMARC** must all say **PASS**.

## Part 9. Every later update to the site

1. [ ] **Developer:** before starting any change, sync the branch with `main`, so it has the Owner's release commits and any edit the Owner made on `main` (such as Part 5):
   ```
   git switch redesign/site-v5-seo
   git fetch origin main
   git merge origin/main
   ```
   This copies `main` into the branch, never the other way round, and it is the only merge ever allowed. If git opens an editor for the merge message, save and close it. If it reports a conflict, stop and ask Claude. Then check that the guard file is still there: `ls .no-merge-to-main` must print `.no-merge-to-main`.
2. [ ] **Developer:** make the change on `redesign/site-v5-seo`, run `python3 tools/build_site_v5.py --prod`, check locally with `python3 tools/serve.py`, commit, then `git push origin redesign/site-v5-seo`. Never push `main`.
3. [ ] **Developer:** tell the Owner the branch is ready and paste the output of `git rev-parse --short HEAD`.
4. [ ] **Owner:** do a release: Part 2b, every step, in order. Step 4 and steps 9 and 10 are the safety checks; never skip them.
5. [ ] **Developer:** right after each release, do step 1 again, so the branch stays in step with `main`.

## Part 10. Final checks

**Who:** either, after Parts 1 to 8.

- [ ] Each of these, opened in a private window, ends at `https://solvenadvisory.ai` (look at the address bar):
  - `http://solvenadvisory.ai`
  - `https://www.solvenadvisory.ai`
  - `https://solven-advisory-website.vercel.app`
- [ ] These load and show text: `https://solvenadvisory.ai/robots.txt`, `https://solvenadvisory.ai/sitemap.xml`, `https://solvenadvisory.ai/llms.txt`.
- [ ] `https://solvenadvisory.ai/contact` ends at `/book`, and `https://solvenadvisory.ai/pt/contacto` ends at `/pt/marcar`.
- [ ] Vercel **Analytics** shows visits.
- [ ] Search Console **Sitemaps** shows **Success**.
- [ ] The Gmail test in Part 8b step 6 shows three PASS.

## Part 11. If something goes wrong

**Who:** Owner.

- **The new site looks broken after a release:** Vercel → project → **Deployments** → find the previous row marked **Production** that worked → **⋯** → **Instant Rollback** (or **Promote to Production**) → confirm. The old version is live again in seconds. Then tell the Developer what was wrong.
- **The deployment says Blocked:** the commit was not recognised as yours. Run `git log -1 --format='%an <%ae>%n%b'`: the email must be on your GitHub account and there must be no `Co-Authored-By` line. To fix, run `git commit --amend --reset-author -m "Release site v5"` and then `git push --force-with-lease origin main`. Use the force push only for this case, right after your own release commit.
- **`solvenadvisory.ai` does not load after Part 4:** check dnschecker.org again (Part 4 step 9). DNS changes can take a few hours. `www.solvenadvisory.ai` keeps working meanwhile. If after 24 hours Vercel still says **Invalid Configuration**, compare the A record in GoDaddy with the Value Vercel shows, character by character.
- **A step in this guide does not match the screen:** stop and ask the Developer, with a screenshot.
