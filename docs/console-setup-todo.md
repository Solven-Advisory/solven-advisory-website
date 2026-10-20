# Console setup: manual to-do list

Written 2026-10-20. These steps are done by hand in the providers' dashboards (Vercel, GoDaddy, Google, Bing, Ahrefs). Nothing here needs a code change unless a step says so. Do them in order: each part depends on the one before.

## What is already done in the code

- **Vercel Web Analytics (cookieless):** the script `/_vercel/insights/script.js` is on every page (commit 00f3bf7). It returns 404 until Web Analytics is switched on in the Vercel dashboard (part 3).
- **`vercel.json`:** serves `public/`, clean URLs, no trailing slash, 15 permanent redirects from the old site's addresses (`/programmes`, `/contact`, `/blog/:slug`, `/pt/contacto` and the rest), security headers, and long caching for `/assets/`.
- **For search engines:** `robots.txt`, `sitemap.xml` (14 URLs), `llms.txt`, `llms-full.txt`, canonicals on `https://solvenadvisory.ai`, EN/PT hreflang.
- **Google verification:** the TXT record `google-site-verification=GpoVtoyc...` already exists on `solvenadvisory.ai`.

## Current state of the live domain (checked 2026-10-20)

- `solvenadvisory.ai` (apex) points to GoDaddy forwarding (`15.197.225.128`, `3.33.251.168`). It answers `405` or redirects to `solven-advisory-website.vercel.app`. **It is not served by Vercel.**
- `www.solvenadvisory.ai` points to Vercel and serves the site.
- SPF is `v=spf1 include:secureserver.net -all` (GoDaddy only), but mail runs on Microsoft 365.
- Production deploys from `main`, which still holds the old site. Site v5 lives on `redesign/site-v5-seo`, which must never be merged into `main`.

---

## Part 0. Decide how site v5 goes live

Every later step assumes the live site is v5. Today it is not.

- [ ] Decide how v5 becomes production. One option, with no merge into `main`: Vercel, Project, **Settings, Git, Production Branch**, set it to the v5 branch. Discuss this before doing it: it changes what the live site serves.
- [ ] Before switching, open a Vercel **preview deployment** of the v5 branch and check that every page returns 200 and that `/book` shows the calendar.

## Part 1. DNS at GoDaddy (the domain registrar)

- [ ] In GoDaddy, **Domain, Forwarding**: delete the forwarding on `solvenadvisory.ai`.
- [ ] In GoDaddy, **DNS records**: set the apex `A` record (`@`) to `76.76.21.21` and remove any other `A` records on `@`. Confirm the value in Vercel, **Settings, Domains**, which shows the record it expects.
- [ ] Keep the `www` CNAME pointing to Vercel as it is now.
- [ ] Do not delete the `google-site-verification` TXT record or the Microsoft TXT record (`NETORGFT20700852.onmicrosoft.com`).
- [ ] While in DNS, fix email (it affects deliverability of replies to clients):
  - [ ] SPF: replace it with `v=spf1 include:spf.protection.outlook.com -all`. If GoDaddy still sends mail for you, keep `include:secureserver.net` as well.
  - [ ] DKIM: in the Microsoft 365 Defender portal (**Email & collaboration, Policies, DKIM**), enable DKIM for `solvenadvisory.ai` and add the two `selector1` and `selector2` CNAME records it shows.
- [ ] Wait for propagation (minutes to a few hours). Check with `dig +short solvenadvisory.ai`: it should return `76.76.21.21`.

## Part 2. Vercel: domains

Vercel dashboard, Project, **Settings, Domains**.

- [ ] Make `solvenadvisory.ai` (apex) the primary domain, with status "Valid Configuration".
- [ ] Set `www.solvenadvisory.ai` to **Redirect to** `solvenadvisory.ai` (308 permanent).
- [ ] Check in a browser: `https://solvenadvisory.ai` loads, and `https://www.solvenadvisory.ai/book` ends at `https://solvenadvisory.ai/book` in one hop.
- [ ] **Code step, after this works:** ask Claude to add the redirect from `solven-advisory-website.vercel.app` to the apex in `vercel.json` (plan item 1.2). Do not add it before the apex serves from Vercel, or it loops.

## Part 3. Vercel: Web Analytics

- [ ] Vercel dashboard, Project, **Analytics** tab, **Enable** Web Analytics (the free Hobby tier is enough).
- [ ] Redeploy production once (Deployments, latest, Redeploy) so the script is served.
- [ ] Check: `https://solvenadvisory.ai/_vercel/insights/script.js` returns 200, and visits appear in the Analytics tab within a few minutes.
- [ ] Do not enable anything cookie-based: the privacy notice says the site sets no cookies of its own.

## Part 4. Google Search Console

Do this after parts 1 and 2, so Google crawls v5 on the right address.

- [ ] Go to https://search.google.com/search-console and add a **Domain** property for `solvenadvisory.ai` (not a URL-prefix property). It should verify at once with the existing TXT record.
- [ ] **Sitemaps**: submit `https://solvenadvisory.ai/sitemap.xml`. Status should become "Success" with 14 URLs discovered.
- [ ] **URL Inspection**: inspect `https://solvenadvisory.ai/` and `https://solvenadvisory.ai/pt`, then click **Request indexing** for each.
- [ ] After a few days, check **Pages** (indexing): old addresses like `/programmes` should show as "Page with redirect", which is expected.
- [ ] Optional: add your co-founders as users (**Settings, Users and permissions**).

## Part 5. Bing Webmaster Tools

Bing also feeds ChatGPT search and Copilot, so it matters for visibility in LLMs.

- [ ] Go to https://www.bing.com/webmasters and sign in.
- [ ] Choose **Import from Google Search Console**. It copies the site and the sitemap, with no extra verification.
- [ ] Check that the sitemap shows under **Sitemaps**. If not, submit `https://solvenadvisory.ai/sitemap.xml`.

## Part 6. Ahrefs Webmaster Tools (free)

- [ ] Go to https://ahrefs.com/webmaster-tools and create a free account.
- [ ] Add the project and choose **Import from Google Search Console**. This verifies the site without any code or DNS change.
- [ ] Run the first **Site Audit** and keep the report. Expected noise: the Cal.com cookie on `/book`, and the redirects from old addresses.
- [ ] Turn on email alerts for new and lost backlinks and for new audit issues.

## Part 7. Checks after everything is done

- [ ] `http://solvenadvisory.ai`, `https://www.solvenadvisory.ai` and `https://solven-advisory-website.vercel.app` all reach `https://solvenadvisory.ai` in one redirect.
- [ ] `https://solvenadvisory.ai/robots.txt`, `/sitemap.xml` and `/llms.txt` load.
- [ ] Vercel Analytics shows visits; Search Console shows the sitemap read.
- [ ] Send a test email from the Solven mailbox to a Gmail address and check "Show original": SPF, DKIM and DMARC should all say PASS.
