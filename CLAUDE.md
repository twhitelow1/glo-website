# GLO website — rules for every change

Static HTML site for GLO Aesthetics + Wellness Lounge (med spa, Ocala and Palatka, FL), hosted on Vercel.
Built by DubLow Digital. SEO (Google) and AEO/GEO (ChatGPT, Gemini, Perplexity, AI Overviews) are requirements,
not extras: **no page ships unless it meets the page standard below**, and all copy is written for both search and people.

## URLs and files
- A page's file path is its canonical URL: `treatments/xeomin.html` → `https://gloocala.com/treatments/xeomin`
  (Vercel `cleanUrls`). Hubs use `index.html` (`treatments/index.html` → `/treatments`).
- Lowercase, hyphenated slugs. Internal links are root-absolute clean URLs (`/treatments/xeomin`, `/#book`), never `.html`.
- Renaming or removing a page needs a permanent redirect in `vercel.json`.

## Page standard (every indexable page)
- Title ≤ 60 characters: keyword + "Ocala, FL" + GLO. Meta description 140–155 characters: keyword, benefit, call to action.
- Canonical, Open Graph and Twitter tags; `og:image` and `twitter:image` are the page's hero photo.
- One H1: keyword + city ("Xeomin in Ocala, FL").
- A 40–60 word direct answer right under the H1 (`class="glo-answer"`): what it is, who it's for, key facts.
- H2s phrased as the questions people ask, each answered in its first sentence or two.
- Visible breadcrumb in the hero + BreadcrumbList schema (no `#` URLs).
- 4–8 real FAQs as H3s with matching FAQPage schema.
- Schema for the page type, linked to the business by `@id` (`https://gloocala.com/#business`).
- Links up to the parent category or hub, across to 2–4 related pages, and to booking.
- Photos as `<img>` with descriptive alt text (not CSS backgrounds). AI imagery keeps its disclosure.
- One booking call to action above the fold and one at the end. Usable at 390px with no sideways scroll.
- Name, address and phone exactly as on the home page.

Medical pages (treatments, categories) also need: the `Updated` line (`glo-updated`), the device or product named,
who it's for and who should wait, what to expect, time/downtime/results, a "from" price when one exists, the medical
disclaimer, and schema `MedicalWebPage` + `MedicalProcedure`/`MedicalTherapy`.

## Medical and advertising compliance (Florida Board of Medicine, FTC)
- Never invent prices, statistics, provider names, credentials, reviews or ratings. Use facts on the page or from GLO.
- No outcome guarantees, "best in Ocala" claims or "cure". Off-label or compounded therapies are never called FDA-approved.
- Don't claim content was "medically reviewed" until a named GLO provider has reviewed it; then add their name and
  credentials to the Updated line and `reviewedBy`/`lastReviewed` to the schema.
- Placeholder text (`[TBD]`, `[Confirm …]`) is only allowed on `noindex` pages and never inside JSON-LD.

## Tools (run from the repo root before every push)
- `python3 scripts/check_site.py`: links, anchors, JSON-LD, the page standard. Must report 0 errors.
- `python3 scripts/build_seo_files.py`: regenerates `sitemap.xml` and `llms.txt`. Run after adding or editing a page.
- Treatment page content lives in `content/treatments/<slug>.json`; `scripts/apply_treatments.py` applied it.
- Category pages are generated: edit `scripts/build_categories.py`, then run it.
- `scripts/glo_page.py` holds the shared page shell, SEO head and schema helpers for new generated pages.
- `python3 scripts/design_layer.py`: applies the shared design layer (`assets/site.css`, `assets/site.js`, shared footer,
  mobile Book/Call bar, marquee, H2 accent words, card thumbnails, photo bands from `content/bands.json`). Run it after
  adding or regenerating a page; add the new page's H2s to its accent map.

## Brand
Playfair Display headings, Inter body, Montserrat labels and buttons. Cream `#F3F0EA`, page `#FAF9F6`, gold `#B8894F`,
bronze sections `#6B5435` (`glo-dark`). Reuse the brand characters in `docs/brand-characters.md` for imagery.
Every H2 gets one italic gold accent word (`.glo-accent`). Each treatment page has its own photo band; never reuse
one photo set across pages. Copy is warm, inviting and accepting, and uses NEPQ-style questions that help the reader see themselves.
