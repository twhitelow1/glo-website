"""Regenerate sitemap.xml and llms.txt from the pages' canonical URLs, titles and descriptions.

Run from the repo root after adding or editing a page:  python3 scripts/build_seo_files.py
"""
import glob, html, re, subprocess
from datetime import date

SITE = 'https://gloocala.com'
BOOK = 'https://gloocala.janeapp.com/'


def meta(s, pat):
    m = re.search(pat, s, re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''


def lastmod(path):
    out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', path], capture_output=True, text=True).stdout.strip()
    return out or date.today().isoformat()


pages = []
for f in sorted(glob.glob('*.html') + glob.glob('*/*.html')):
    s = open(f).read()
    if 'noindex' in meta(s, r'<meta name="robots" content="([^"]*)"'):
        continue
    url = meta(s, r'<link rel="canonical" href="([^"]*)"')
    pages.append({
        'file': f, 'url': url, 'path': url[len(SITE):] or '/',
        'title': meta(s, r'<title>(.*?)</title>'),
        'desc': meta(s, r'<meta name="description" content="([^"]*)"'),
        'h1': re.sub(r'\s+', ' ', meta(s, r'<h1[^>]*>(.*?)</h1>')),
        'lastmod': lastmod(f),
    })

order = lambda p: (p['path'] != '/', p['path'].count('/'), p['path'])
pages.sort(key=order)

with open('sitemap.xml', 'w') as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p in pages:
        fh.write(f'  <url><loc>{p["url"]}</loc><lastmod>{p["lastmod"]}</lastmod></url>\n')
    fh.write('</urlset>\n')

def section(prefix_test):
    return [p for p in pages if prefix_test(p['path'])]

groups = [
    ('Treatment categories', section(lambda x: x in ('/treatments', '/injectables', '/skin-services', '/wellness'))),
    ('Treatments', section(lambda x: x.startswith('/treatments/'))),
    ('About', section(lambda x: x == '/about')),
    ('Locations', section(lambda x: x.startswith('/locations'))),
    ('Pricing and payment', section(lambda x: x in ('/membership-programs', '/financing'))),
]

lines = [
    '# GLO Aesthetics + Wellness Lounge',
    '',
    '> Medical spa in Ocala and Palatka, Florida offering injectables (Xeomin, Daxxify, dermal filler), '
    'laser and radiofrequency skin treatments (Tetra CO2, Motus, Everesse), facials, chemical peels, microneedling, '
    'laser hair removal and medical wellness (hormone replacement, peptide therapy, medical weight loss, IV hydration). '
    'Treatments are performed by licensed providers under the direction of a Florida-licensed Medical Director.',
    '',
    '- Ocala: 1925 SW 18th Ct, Unit 109, Ocala, FL 34471',
    '- Palatka: 210 St Johns Ave, Palatka, FL 32177',
    '- Phone: 352-559-8034 · Email: info@gloocala.com',
    f'- Book online: {BOOK}',
    f'- Home: {SITE}/',
    '',
]
for name, items in groups:
    if not items:
        continue
    lines += [f'## {name}', '']
    lines += [f'- [{p["h1"] or p["title"]}]({p["url"]}): {p["desc"]}' for p in items]
    lines.append('')
open('llms.txt', 'w').write('\n'.join(lines))
print(f'{len(pages)} pages in sitemap.xml and llms.txt')
