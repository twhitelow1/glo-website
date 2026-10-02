"""Move every page to its canonical path and rewrite internal links to root-absolute clean URLs.

Old file -> new file (served by Vercel cleanUrls at the canonical path).
Run once from the repo root; it also writes the 301 redirects for the old names.
"""
import json, os, re, subprocess

PAGES = {}
for f in sorted(os.listdir('.')):
    if not f.endswith('.html'):
        continue
    m = re.search(r'<link rel="canonical" href="https://gloocala\.com([^"]*)"', open(f).read())
    PAGES[f] = m.group(1) or '/'

def target_file(path):
    if path == '/':
        return 'index.html'
    if path in ('/treatments', '/locations'):
        return path.strip('/') + '/index.html'
    return path.strip('/') + '.html'

# old href -> new href
LINKS = {old: new for old, new in PAGES.items()}

def fix_links(html):
    def repl(m):
        attr, url = m.group(1), m.group(2)
        base, frag = (url.split('#', 1) + [None])[:2]
        if base in LINKS:
            new = LINKS[base]
            if frag is not None:
                new = (new if new != '/' else '/') + '#' + frag
            return f'{attr}="{new}"'
        if base.startswith('assets/'):
            return f'{attr}="/{url}"'
        return m.group(0)
    html = re.sub(r'(href|src)="([^"#:][^":]*?)"', repl, html)
    html = html.replace("url('assets/", "url('/assets/")
    return html

for old, path in PAGES.items():
    new = target_file(path)
    html = fix_links(open(old).read())
    if new != old:
        os.makedirs(os.path.dirname(new) or '.', exist_ok=True)
        subprocess.run(['git', 'mv', old, new], check=True)
    open(new, 'w').write(html)
    print(f'{old:45} -> {new:45} {path}')

redirects = []
for old, path in PAGES.items():
    if old == 'index.html':
        continue
    stem = old[:-5]
    for src in (f'/{stem}', f'/{old}'):
        redirects.append({'source': src, 'destination': path, 'permanent': True})
for gone, dest in [('Treatment-EyelashBrowServices', '/treatments'),
                   ('Category-BeautyServices', '/skin-services'),
                   ('Category-Skin', '/skin-services'),
                   ('Category-LaserServices', '/skin-services'),
                   ('Category-NonLaserServices', '/skin-services')]:
    for src in (f'/{gone}', f'/{gone}.html'):
        redirects.append({'source': src, 'destination': dest, 'permanent': True})
print(json.dumps(redirects, indent=2))  # pasted into vercel.json
