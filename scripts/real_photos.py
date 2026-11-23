"""Place GLO's real Ocala photos (assets/ocala/) on the Ocala page, the About page and matching treatment pages.
Idempotent. Run from the repo root after design_layer.py:  python3 scripts/real_photos.py
"""
import glob, json, re, sys
sys.path.insert(0, 'scripts')
from design_layer import balanced_div_end

SITE = 'https://gloocala.com'
P = {
    'lounge': ('/assets/ocala/lounge.webp', 'Client lounge at GLO Aesthetics + Wellness Lounge in Ocala with ivory chairs and a gold table', 'The client lounge'),
    'hallway': ('/assets/ocala/hallway.webp', 'Hallway with gold starburst chandeliers leading to private treatment rooms at GLO Ocala', 'Private treatment rooms'),
    'laser-room': ('/assets/ocala/laser-room.webp', 'Tetra Pro CO2 laser beside a white treatment chair at GLO Ocala', 'Our Tetra Pro CO2 laser'),
    'motus-room': ('/assets/ocala/motus-room.webp', 'DEKA Motus AY laser beside a white treatment chair at GLO Ocala', 'Our DEKA Motus AY laser'),
    'facial-room': ('/assets/ocala/facial-room.webp', 'Softly lit facial room with a heated treatment bed at GLO Ocala', 'A calm facial suite'),
    'everesse-treatment': ('/assets/ocala/everesse-treatment.webp', 'A GLO provider in pink gloves gliding the Everesse radiofrequency handpiece across a relaxed client\'s forehead in Ocala', 'Everesse in progress'),
    'everesse-device': ('/assets/ocala/everesse-device.webp', 'The Everesse monopolar radiofrequency system by Classys in a GLO treatment room in Ocala', 'Our Everesse system'),
    'laser-treatment': ('/assets/ocala/laser-treatment.webp', 'A laser handpiece with its red aiming beam on a client\'s forearm during a treatment at GLO Ocala', 'A laser treatment in progress'),
    'front-desk': ('/assets/ocala/glo-ocala-med-spa-front-desk.webp', 'Baily Bellamy at the front desk of GLO Aesthetics + Wellness Lounge in Ocala, FL, beside the skincare case and gold mirror', 'Our Ocala front desk'),
    'reception-desk': ('/assets/ocala/glo-ocala-med-spa-reception-desk.webp', 'Baily Bellamy checking in a client at the reception desk of GLO Aesthetics + Wellness Lounge in Ocala, FL', 'Checking in at GLO Ocala'),
    'weight-loss-labs': ('/assets/ocala/medical-weight-loss-lab-draw-ocala-fl.webp', 'A GLO provider drawing blood for metabolic lab work before a medical weight loss plan at GLO Aesthetics + Wellness Lounge in Ocala, FL', 'Lab work at GLO Ocala'),
    'peptide-labs': ('/assets/ocala/peptide-therapy-lab-work-ocala-fl.webp', 'A GLO provider collecting a blood sample for lab work before peptide therapy at GLO Aesthetics + Wellness Lounge in Ocala, FL', 'Lab work before peptide therapy'),
    'lounge-retail': ('/assets/ocala/lounge-retail.webp', 'Lounge seating, coffee bar and medical-grade skincare shelves at GLO Ocala', 'Coffee, Wi-Fi &amp; medical-grade skincare'),
}
ORDER = ['lounge', 'hallway', 'laser-room', 'facial-room', 'lounge-retail']


def gallery(h2, intro, bg='#F3F0EA'):
    figs = ''.join(f'<figure><img src="{P[k][0]}" alt="{P[k][1]}" width="900" height="1599" loading="lazy" decoding="async"><figcaption>{P[k][2]}</figcaption></figure>' for k in ORDER)
    return (f'  <!-- ===================== OCALA PHOTOS ===================== -->\n'
            f'  <section id="inside" style="width:100%;background:{bg};">\n'
            f'    <div class="glo-container" style="max-width:1240px;margin:0 auto;padding:90px 48px;">\n'
            f'      <div style="max-width:760px;margin-bottom:34px;">\n'
            f'        <h2 class="glo-h2" style="font-size:40px;line-height:1.2;color:#221F1B;margin-bottom:12px;">{h2}</h2>\n'
            f'        <p style="font-size:17px;line-height:1.7;color:#5C574E;margin:0;">{intro}</p>\n'
            f'      </div>\n      <div class="glo-gallery">{figs}</div>\n    </div>\n  </section>\n\n')


def ocala(s):
    if '/assets/ocala/glo-ocala-med-spa-front-desk.webp" alt' in s.split('glo-split-media', 2)[-1][:300]:
        return s
    src, alt, _ = P['front-desk']
    s = re.sub(r'<div class="glo-split-media"><img [^>]*>',
               f'<div class="glo-split-media"><img src="{src}" alt="{alt}" width="1600" height="1069" fetchpriority="high" decoding="async" style="object-position:center 40%;">',
               s, count=1)
    for prop in ('og:image', 'twitter:image'):
        s = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % prop, lambda m: m.group(1) + SITE + '/assets/ocala/glo-ocala-med-spa-front-desk.jpg', s)
    if 'id="inside"' in s:
        return s
    m = re.search(r'  <!-- ===================== PHOTO BAND[^\n]*-->\n', s)
    if not m:
        return s
    start = s.index('<section', m.end())
    end = s.index('</section>', start) + len('</section>')
    g = gallery('What does our Ocala med spa <span class="glo-accent">look like</span>?',
                'Bright, calm and private. Settle into the lounge with a coffee, then head down the hall to your own treatment room &mdash; these are real photos of our Ocala space.')
    s = s[:m.start()] + g + s[end:].lstrip('\n')
    # location schema: real photos
    def fix(mm):
        j = json.loads(mm.group(1))
        if isinstance(j.get('@type'), list) and 'MedicalBusiness' in j['@type']:
            j['image'] = [SITE + '/assets/ocala/glo-ocala-med-spa-front-desk.jpg'] + [SITE + P[k][0] for k in ORDER]
            return '<script type="application/ld+json">\n' + json.dumps(j, indent=1, ensure_ascii=False) + '\n</script>'
        return mm.group(0)
    return re.sub(r'<script type="application/ld\+json">\n(.*?)\n</script>', fix, s, flags=re.S)


def figure(s, key, caption):
    if 'class="hiw-figure"' in s:
        return s
    src, alt, _ = P[key]
    m = re.search(r'(<div id="how-it-works"[^>]*>\s*<div class="glo-container"[^>]*>\s*)(<div style="max-width:760px;">.*?</div>)', s, re.S)
    if not m:
        return s
    text = m.group(2).replace('<div style="max-width:760px;">', '<div>', 1)
    block = (f'<div class="hiw-flex">{text}'
             f'<figure class="hiw-figure"><img src="{src}" alt="{alt}" width="900" height="1599" loading="lazy" decoding="async"><figcaption>{caption}</figcaption></figure></div>')
    return s[:m.start(2)] + block + s[m.end(2):]


def locations_team(s):
    if 'id="meet-team"' in s:
        return s
    g = json.load(open('content/team.json'))['group_photo']
    sec = f'''  <!-- ===================== MEET THE TEAM ===================== -->
  <section id="meet-team" style="width:100%;background:#FAF9F6;">
    <div class="glo-container glo-teamshot" style="max-width:1140px;margin:0 auto;padding:90px 48px;">
      <figure><img src="{g['src']}" alt="{g['alt']}" width="{g['width']}" height="{g['height']}" loading="lazy" decoding="async"></figure>
      <div>
        <h2 class="glo-h2" style="font-size:40px;line-height:1.2;color:#221F1B;margin-bottom:16px;">Who will I <span class="glo-accent">meet</span> at GLO?</h2>
        <p style="font-size:17.5px;line-height:1.8;color:#5C574E;margin:0 0 16px;">Founded by Renee Porter, GLO has two homes. In Ocala, you can book with McKenzie McCalla, Sundee Bass, Baily Bellamy and Mariah Young. In Palatka, Sundee Bass and Baily Bellamy see clients too.</p>
        <p style="font-size:17.5px;line-height:1.8;color:#5C574E;margin:0 0 26px;">Every visit starts with listening. Book with the provider whose focus fits your goals, or let us match you at your consultation.</p>
        <a href="/about#team" class="btn-outline" style="display:inline-block;border:1px solid #221F1B;color:#221F1B;padding:15px 30px;border-radius:2px;font-size:13px;letter-spacing:0.1em;font-weight:500;text-transform:uppercase;">Meet Our Team</a>
      </div>
    </div>
  </section>

'''
    return s.replace('  <!-- ===================== FAQ', sec + '  <!-- ===================== FAQ', 1)


def hero(slug, key, pos='center 45%'):
    """Swap a treatment page's hero photo (and og/twitter image) for a real GLO photo; card thumbnails follow."""
    p = f'treatments/{slug}.html'
    s = open(p).read()
    m = re.search(r'<div class="glo-split-media"><img src="([^"]+)" alt="([^"]*)"[^>]*>', s)
    src, alt, _ = P[key]
    if m.group(1) == src:
        return
    old_src, old_alt = m.group(1), m.group(2)
    s = s.replace(m.group(0), f'<div class="glo-split-media"><img src="{src}" alt="{alt}" width="1600" height="1069" fetchpriority="high" decoding="async" style="object-position:{pos};">', 1)
    jpg = SITE + src.replace('.webp', '.jpg')
    for prop in ('og:image', 'twitter:image'):
        s = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % prop, lambda mm: mm.group(1) + jpg, s)
    s = s.replace(f'"image": "{old_src}"', f'"image": "{jpg}"').replace(f'"primaryImageOfPage": "{old_src}"', f'"primaryImageOfPage": "{jpg}"')
    open(p, 'w').write(s)
    for f in glob.glob('*.html') + glob.glob('*/*.html'):
        t = open(f).read()
        n = re.sub(r'(<a href="/treatments/%s" class="card-hover"[^>]*>\s*<span class="tx-thumb"><img src=")[^"]*(" alt=")[^"]*' % slug,
                   lambda mm: mm.group(1) + src + mm.group(2) + alt, t)
        if n != t:
            open(f, 'w').write(n)


def home_why(s):
    src, alt, _ = P['reception-desk']
    return re.sub(r'(<div id="about".*?<img src=")[^"]*(" alt=")[^"]*(" style="width:100%;height:100%;object-fit:cover;)(display:block;)',
                  lambda m: m.group(1) + src + m.group(2) + alt + m.group(3) + 'object-position:72% center;' + m.group(4), s, count=1, flags=re.S) \
        if src not in s else s


if __name__ == '__main__':
    f = 'locations/index.html'
    s = locations_team(open(f).read())
    open(f, 'w').write(s)
    f = 'locations/ocala.html'
    s = ocala(open(f).read())
    open(f, 'w').write(s)
    for slug, key, cap in [('laser-skin-revitalization', 'laser-room', 'The Tetra Pro CO2 laser in our Ocala treatment room.'),
                           ('coolpeel', 'laser-room', 'CoolPeel is performed on the Tetra Pro CO2 laser in our Ocala treatment room.'),
                           ('motus-laser-facial', 'motus-room', 'The DEKA Motus AY laser in our Ocala treatment room.'),
                           ('custom-facials-peels', 'facial-room', 'One of our private facial suites in Ocala.'),
                           ('mini-facials', 'facial-room', 'One of our private facial suites in Ocala.'),
                           ('skin-tightening', 'everesse-treatment', 'A real Everesse treatment at our Ocala med spa: the cooled handpiece glides over the skin.'),
                           ('radiant-lift', 'everesse-device', 'Radiant Lift starts on our Everesse system; the CoolPeel follows on the Tetra Pro CO2 laser.'),
                           ('laser-hair-removal', 'laser-treatment', 'A laser treatment in progress at our Ocala med spa; the red light is the aiming beam.')]:
        p = f'treatments/{slug}.html'
        s = figure(open(p).read(), key, cap)
        open(p, 'w').write(s)
    hero('functional-weight-loss', 'weight-loss-labs', 'center 45%')
    hero('peptide-therapy', 'peptide-labs', '40% 45%')
    s = home_why(open('index.html').read())
    open('index.html', 'w').write(s)
    print('done')
