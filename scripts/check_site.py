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
    if noindex:
        continue
    title = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    if len(title) > 60:
        warnings.append(f'{f}: title {len(title)} chars')
    if not 120 <= len(desc) <= 160:
        warnings.append(f'{f}: meta description {len(desc)} chars')
    for need in ('rel="canonical"', 'og:image', 'application/ld+json'):
        if need not in s:
            warnings.append(f'{f}: missing {need}')
print('\n'.join(['ERROR ' + e for e in errors] + ['WARN  ' + w for w in warnings]) or 'all clear')
print(f'{len(files)} files, {len(errors)} errors, {len(warnings)} warnings')
sys.exit(1 if errors else 0)
