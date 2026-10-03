"""Site checks run before every push: internal links, anchors, JSON-LD, one H1, title/meta length, div balance."""
import glob, html, json, os, re, sys

def resolve(path):
    path = path.rstrip('/') or '/'
    if path == '/':
        return 'index.html'
    p = path.lstrip('/')
    for cand in (p, p + '.html', p + '/index.html'):
        if os.path.isfile(cand):
            return cand
    return None

errors, warnings = [], []
files = sorted(glob.glob('*.html') + glob.glob('*/*.html'))
ids = {f: set(re.findall(r'\sid="([^"]+)"', open(f).read())) for f in files}
for f in files:
    s = open(f).read()
    noindex = 'content="noindex' in s
    for url in re.findall(r'(?:href|src)="(/[^"]*)"', s):
        base, _, frag = url.partition('#')
        target = resolve(base) if base else f
        if not target:
            errors.append(f'{f}: broken link {url}')
        elif frag and frag not in ids.get(target, ()):
            errors.append(f'{f}: missing anchor {url}')
    for frag in re.findall(r'href="#([^"]+)"', s):
        if frag not in ids[f]:
            errors.append(f'{f}: missing anchor #{frag}')
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(block)
        except Exception as e:
            errors.append(f'{f}: bad JSON-LD {e}')
    h1s = len(re.findall(r'<h1[\s>]', s))
    if h1s != 1:
        errors.append(f'{f}: {h1s} H1s')
    if s.count('<div') != s.count('</div>'):
        errors.append(f'{f}: unbalanced divs')
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        if re.search(r'\[(TBD|Confirm)', block):
            errors.append(f'{f}: placeholder text in JSON-LD')
    if noindex:
        continue
    if re.search(r'\[(TBD|Confirm)', s):
        errors.append(f'{f}: placeholder text on an indexable page (set noindex until confirmed)')
    h1 = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1)))
    if not re.search(r'Ocala|Palatka', h1):
        warnings.append(f'{f}: H1 has no city ({h1.strip()})')
    if f.startswith('treatments/') or f in ('injectables.html', 'skin-services.html', 'wellness.html'):
        for need, label in (('glo-answer', 'direct-answer paragraph'), ('glo-updated', 'Updated line'), ('FAQPage', 'FAQPage schema'), ('BreadcrumbList', 'BreadcrumbList schema')):
            if need not in s:
                errors.append(f'{f}: missing {label}')
    og = re.search(r'og:image" content="([^"]*)"', s)
    tw = re.search(r'twitter:image" content="([^"]*)"', s)
    if og and tw and og.group(1) != tw.group(1):
        warnings.append(f'{f}: og:image and twitter:image differ')
    title = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    if len(title) > 60:
        warnings.append(f'{f}: title {len(title)} chars')
    if not 120 <= len(desc) <= 160:
        warnings.append(f'{f}: meta description {len(desc)} chars')
    for need in ('rel="canonical"', 'og:image', 'application/ld+json'):
        if need not in s:
            warnings.append(f'{f}: missing {need}')
# AI imagery (hosted on the Higgsfield CDN) has no per-photo caption, so the page must carry the fine-print photography line.
for f in files:
    s = open(f).read()
    if 'cloudfront.net' in s and 'Photography on this site is representative' not in s:
        errors.append(f'{f}: AI imagery without the fine-print photography line')

# Compliance guards: Florida s. 456.062 notice on every page (free consults, offers, member discounts), no AI image labelled
# as a client or a result, no "FDA-approved" next to GLP-1 brands.
for f in files:
    s = open(f).read()
    if 'class="glo-footer"' in s and 'glo-footer-legal' not in s:
        errors.append(f'{f}: missing the Florida 456.062 free/discount notice in the footer')
    for alt in re.findall(r'<img src="https://d8j0ntlcm91z4[^"]*" alt="([^"]*)"', s):
        if re.search(r'\bclients?\b|\bafter\b|\bresults?\b', alt, re.I):
            errors.append(f'{f}: AI image labelled as a client or result: "{alt}"')
    if re.search(r'FDA-approved GLP|Wegovy|Ozempic|Mounjaro|Zepbound', re.sub(r'<!--.*?-->', '', s, flags=re.S)):
        errors.append(f'{f}: GLP-1 brand or "FDA-approved GLP-1" claim (confirm with GLO first)')

# The main nav must be identical on every page (a stray find-and-replace once scrambled one page's menu).
navs = {}
for f in files:
    s = open(f).read()
    a = s.find('<!-- ===================== MAIN NAV BAR')
    if a >= 0:
        navs[f] = s[a:s.find('<!-- =====', a + 10)]
if navs:
    common = max(set(navs.values()), key=list(navs.values()).count)
    errors += [f'{f}: main nav differs from the other pages' for f, n in navs.items() if n != common]
print('\n'.join(['ERROR ' + e for e in errors] + ['WARN  ' + w for w in warnings]) or 'all clear')
print(f'{len(files)} files, {len(errors)} errors, {len(warnings)} warnings')
sys.exit(1 if errors else 0)
