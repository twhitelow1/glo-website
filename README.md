# GLO Aesthetics + Wellness Lounge — Website

Static export of the site (originally built as a Claude Design canvas artifact) for Ocala, FL medspa client GLO Aesthetics + Wellness Lounge.

## Structure
Plain static HTML/CSS/JS, one file per page. `index.html` is the home page.

## Hosting
Hosted on **Vercel**. The site is static, so no build step is needed. The `glo-website` Vercel project is linked to this repo:

- A push to `main` deploys to production.
- Every branch and PR gets its own preview URL.
- `vercel.json` turns on clean URLs, so `/Memberships` serves `Memberships.html`.

`firebase.json` and `.firebaserc` are left in place in case Firebase Hosting is used later (`firebase deploy --only hosting`).

## Assets
Images from the original Claude Design project live in `assets/` (logo, home hero, Cherry financing images). Other photos load from the Higgsfield CDN.

## Local preview
Any static file server works, e.g.:
    python3 -m http.server 8000
