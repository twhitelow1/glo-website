"""Serve AI images from the site instead of the generator's CDN.

Generated images are 1.5-6 MB PNGs on d8j0ntlcm91z4.cloudfront.net; on cards and photo bands they load slowly or
not at all. This downloads each one once, saves a compressed WebP (for <img>) and a JPG (for og/twitter/schema)
in assets/ai/, and rewrites every page to use them. Idempotent; run it last, after the other build scripts:

    python3 scripts/localize_images.py        (needs Pillow: pip install pillow)
"""
import glob
import io
import os
import re
import urllib.request

from PIL import Image

SITE = 'https://gloocala.com'
CDN = re.compile(r'https://d8j0ntlcm91z4\.cloudfront\.net/[A-Za-z0-9_/.-]+?\.png')
OUT = 'assets/ai'
MAX_W = 1600
# CDN paths that moved (the generator re-issued the file under a new timestamp)
MOVED = {
    'hf_20261001_004311_2940c9f3-89bf-4257-a861-f02aa9a1279d.png': 'hf_20261001_004608_2940c9f3-89bf-4257-a861-f02aa9a1279d.png',
}


def local_name(url):
    job = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', url).group(1)
    return f'glo-{job}'


def fetch(url):
    name = local_name(url)
    webp, jpg = f'{OUT}/{name}.webp', f'{OUT}/{name}.jpg'
    if os.path.exists(webp) and os.path.exists(jpg):
        return name
    base = url.rsplit('/', 1)
    src = base[0] + '/' + MOVED.get(base[1], base[1])
    req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req, timeout=60).read()
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    os.makedirs(OUT, exist_ok=True)
    im.save(webp, quality=80, method=6)
    im.save(jpg, quality=82, optimize=True, progressive=True)
    print('saved', name, im.size)
    return name


def main():
    for f in sorted(glob.glob('*.html') + glob.glob('*/*.html')):
        s = open(f).read()
        urls = set(CDN.findall(s))
        if not urls:
            continue
        for url in urls:
            name = fetch(url)
            # <img src> and <source srcset> get the WebP; everything else (meta, JSON-LD) gets the absolute JPG
            s = re.sub(r'((?:src|srcset)=")' + re.escape(url), lambda m: m.group(1) + f'/{OUT}/{name}.webp', s)
            s = s.replace(url, f'{SITE}/{OUT}/{name}.jpg')
        open(f, 'w').write(s)
        print('localized', f, len(urls))


if __name__ == '__main__':
    main()
