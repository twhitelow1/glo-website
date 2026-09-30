# GLO Aesthetics + Wellness Lounge — Website

Static export of the site (originally built as a Claude Design canvas artifact) for Ocala, FL medspa client GLO Aesthetics + Wellness Lounge.

## Structure
Plain static HTML/CSS/JS, one file per page. `index.html` is the home page.

## Hosting
The site is static, so no build step is needed. Both hosts serve the repo root with clean URLs (`/Memberships` serves `Memberships.html`).

- **Vercel**: the `glo-website` project is linked to this repo. Every push to `main` deploys to production, and each PR gets a preview URL. Config: `vercel.json`, `.vercelignore`.
- **Firebase Hosting** (project `glo-aesthetics-wellness-lounge`): GitHub Actions in `.github/workflows/` deploy `main` to the live channel and each PR to a preview channel. This needs the repo secret `FIREBASE_SERVICE_ACCOUNT_GLO_AESTHETICS_WELLNESS_LOUNGE`, which you can create by running `firebase init hosting:github` or by adding a service-account JSON key by hand.

## Local preview
Any static file server works, e.g.:
    python3 -m http.server 8000
