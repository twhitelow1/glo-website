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
    'everesse-device': ('/assets/ocala/everesse-device.webp', 'The Everesse monopolar radiofrequency system by Classys in a GLO treatment room in Ocala', 'Our Everesse system'),
    'laser-treatment': ('/assets/ocala/laser-treatment.webp', 'A laser handpiece with its red aiming beam on a client\'s forearm during a treatment at GLO Ocala', 'A laser treatment in progress'),
    'front-desk': ('/assets/ocala/glo-ocala-med-spa-front-desk.webp', 'Baily Bellamy at the front desk of GLO Aesthetics + Wellness Lounge in Ocala, FL, beside the skincare case and gold mirror', 'Our Ocala front desk'),
    'reception-desk': ('/assets/ocala/glo-ocala-med-spa-reception-desk.webp', 'Baily Bellamy checking in a client at the reception desk of GLO Aesthetics + Wellness Lounge in Ocala, FL', 'Checking in at GLO Ocala'),
    'weight-loss-labs': ('/assets/ocala/medical-weight-loss-lab-draw-ocala-fl.webp', 'A GLO provider drawing blood for metabolic lab work before a medical weight loss plan at GLO Aesthetics + Wellness Lounge in Ocala, FL', 'Lab work at GLO Ocala'),
    'peptide-vials': ('/assets/ocala/peptide-therapy-vials-ocala-fl.webp', 'Vials and syringes on a gold tray in the treatment room at GLO Aesthetics + Wellness Lounge in Ocala, FL', 'Peptide therapy at GLO'),
    'peptide-labs': ('/assets/ocala/peptide-therapy-lab-work-ocala-fl.webp', 'A GLO provider collecting a blood sample for lab work before peptide therapy at GLO Aesthetics + Wellness Lounge in Ocala, FL', 'Lab work before peptide therapy'),
    'lounge-retail': ('/assets/ocala/lounge-retail.webp', 'Lounge seating, coffee bar and medical-grade skincare shelves at GLO Ocala', 'Coffee bar &amp; skincare'),
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
            f'      </div>\n      <div class="glo-gallery">{figs}</div>\n      <p class="glo-gallery-hint" aria-hidden="true">Swipe to see more &rarr;</p>\n    </div>\n  </section>\n\n')


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
        <p style="font-size:17.5px;line-height:1.8;color:#5C574E;margin:0 0 16px;">Founded by Renee Porter, GLO has two homes. In Ocala, you can book with McKenzie McCalla, Sundee Bass and Baily Bellamy. In Palatka, Sundee Bass and Baily Bellamy see clients too.</p>
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


def injectors():
    """GLO's two injectors (real photo) on the /injectables hero and the home Injectables tile."""
    ph = json.load(open('content/team.json'))['injectors_photo']
    src, alt, jpg = ph['src'], ph['alt'], SITE + ph['src'].replace('.webp', '.jpg')
    s = open('injectables.html').read()
    m = re.search(r'<div class="glo-split-media"><img src="([^"]+)"[^>]*>', s)
    if m.group(1) != src:
        old = m.group(1)
        s = s.replace(m.group(0), f'<div class="glo-split-media"><img src="{src}" alt="{alt}" width="{ph["width"]}" height="{ph["height"]}" fetchpriority="high" decoding="async" style="object-position:center 8%;">', 1)
        for prop in ('og:image', 'twitter:image'):
            s = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % prop, lambda mm: mm.group(1) + jpg, s)
        s = s.replace(f'"{old}"', f'"{jpg}"')
        open('injectables.html', 'w').write(s)
    s = open('index.html').read()
    n = re.sub(r'(<a href="/injectables" class="txs-photo"><img src=")[^"]*(" alt=")[^"]*("[^>]*style="object-position:)[^;"]*',
               lambda mm: mm.group(1) + src + mm.group(2) + alt + mm.group(3) + 'center 8%', s)
    if n != s:
        open('index.html', 'w').write(n)


# Service-page heroes (Nov 2026): one image per page, never reused as another page's hero.
# Real GLO photos where one fits; otherwise AI images generated from GLO's own device photos (Tetra Pro, Motus AY,
# Everesse, microneedling pen) with the brand characters in docs/brand-characters.md as clients.
CF = 'https://d8j0ntlcm91z4.cloudfront.net/user_3JRDtqjRvBX48mQoPYnwuq2wzO6/'
AI = 'Representative image, AI-generated: '
HEROES = {
    'xeomin': ('/assets/team/baily-bellamy-xeomin-injector-ocala-fl.webp', 'Baily Bellamy, a GLO injector, holding a syringe in Ocala, FL', 'center 20%', 1200, 1500),
    'microneedling': ('/assets/team/sundee-bass-microneedling-pen-ocala-fl.webp', 'Sundee Bass, GLO medical esthetician and microneedling specialist, holding her microneedling pen in Ocala, FL', 'center 20%', 1200, 1500),
    'coolpeel': (CF + 'hf_20261123_174932_df54e212-dd3c-43ef-9b53-f2547bdbac44.png', AI + 'a woman in laser goggles during a CoolPeel treatment with a Tetra Pro CO2 laser handpiece', 'center 30%', 1792, 2240),
    'laser-skin-revitalization': (CF + 'hf_20261123_174930_2e395884-e877-4aa2-8b87-6386b7726da1.png', AI + 'a woman in laser goggles during CO2 laser resurfacing on a Tetra Pro laser', 'center 30%', 1792, 2240),
    'motus-laser-facial': (CF + 'hf_20261123_174832_1e4c7598-67bc-4bcf-a542-2fa93d94f02e.png', AI + 'a woman in laser goggles during a Motus AY laser facial', 'center 30%', 1792, 2240),
    'laser-hair-removal': (CF + 'hf_20261123_174831_8f0ddcbd-999c-49dc-b58b-5ae715e28e09.png', AI + 'a laser hair removal handpiece gliding along a lower leg', 'center 40%', 1792, 2240),
    'skin-tightening': (CF + 'hf_20261123_174831_4d5111a7-e8a6-4f63-abd9-b0eca4af07c7.png', AI + 'an Everesse radiofrequency handpiece gliding along a woman\'s jawline', 'center 35%', 1792, 2240),
    'radiant-lift': (CF + 'hf_20261123_174932_92c52bab-50d3-4c21-827f-b5f7c0fc93bf.png', AI + 'a woman relaxing in a treatment chair beside the Everesse radiofrequency system', 'center 30%', 1792, 2240),
    'custom-facials-peels': (CF + 'hf_20261123_174830_9cdf821c-9dbb-4a37-8aeb-89dbd87ca592.png', AI + 'an esthetician brushing a chemical peel onto a woman\'s cheek', 'center 30%', 1792, 2240),
    'mini-facials': (CF + 'hf_20261123_174832_fa32a497-2b7f-4289-8a86-d143a23b148a.png', AI + 'an esthetician applying serum during a mini facial', 'center 30%', 1792, 2240),
    'daxxify-facial-microneedling': (CF + 'hf_20261123_174830_31aabe3b-97a6-43b5-b4ba-ea871445284f.png', AI + 'a microneedling pen gliding across a woman\'s cheek during a Daxxify facial', 'center 30%', 1792, 2240),
    'daxxify': (CF + 'hf_20261123_174833_f793b6bf-5151-4c8b-9df7-99592297dc89.png', AI + 'a provider giving a small neuromodulator injection near a woman\'s brow', 'center 30%', 1792, 2240),
    'dermal-filler': (CF + 'hf_20261123_174832_f99a448f-b9a3-4fed-a4aa-b2d9a5bfa265.png', AI + 'a provider placing lip filler with a fine syringe', 'center 30%', 1792, 2240),
    'liquid-rhinoplasty': (CF + 'hf_20261123_174931_6087343e-e4b2-4fef-8b9e-9322fe51a2df.png', AI + 'a provider placing filler at the bridge of a man\'s nose', 'center 30%', 1792, 2240),
    'dissolve-ha-dermal-filler': (CF + 'hf_20261123_174930_0f62e75d-5c5b-4147-ade2-ab46eed370e1.png', AI + 'a woman with a hand mirror talking with her provider about adjusting earlier lip filler', 'center 25%', 1792, 2240),
    'iv-hydration': (CF + 'hf_20261123_174930_f1458133-9d82-48fa-b2d6-061d87dbb739.png', AI + 'a man relaxing in a lounge chair with an IV drip, reading a book', 'center 30%', 1792, 2240),
}


def set_hero(slug, src, alt, pos, w, h):
    """Swap a treatment page's hero (img, og/twitter image, schema image) and its card thumbnails. Idempotent."""
    p = f'treatments/{slug}.html'
    s = open(p).read()
    m = re.search(r'<div class="glo-split-media"><img src="([^"]+)"[^>]*>', s)
    old = m.group(1)
    if old == src:
        return
    s = s.replace(m.group(0), f'<div class="glo-split-media"><img src="{src}" alt="{alt}" width="{w}" height="{h}" fetchpriority="high" decoding="async" style="object-position:{pos};">', 1)
    share = src if src.startswith('http') else SITE + src.replace('.webp', '.jpg')
    for prop in ('og:image', 'twitter:image'):
        s = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % prop, lambda mm: mm.group(1) + share, s)
    old_abs = old if old.startswith('http') else SITE + old.replace('.webp', '.jpg')
    s = s.replace(f'"{old}"', f'"{share}"').replace(f'"{old_abs}"', f'"{share}"')
    open(p, 'w').write(s)
    for f in glob.glob('*.html') + glob.glob('*/*.html'):
        t = open(f).read()
        n = re.sub(r'(<a href="/treatments/%s" class="card-hover"[^>]*>\s*<span class="tx-thumb"><img src=")[^"]*(" alt=")[^"]*' % slug,
                   lambda mm: mm.group(1) + src + mm.group(2) + alt, t)
        if n != t:
            open(f, 'w').write(n)


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
                           ('skin-tightening', 'everesse-device', 'Our Everesse system in an Ocala treatment room.'),
                           ('radiant-lift', 'everesse-device', 'Radiant Lift starts on our Everesse system; the CoolPeel follows on the Tetra Pro CO2 laser.'),
                           ('laser-hair-removal', 'laser-treatment', 'A laser treatment in progress at our Ocala med spa; the red light is the aiming beam.')]:
        p = f'treatments/{slug}.html'
        s = figure(open(p).read(), key, cap)
        open(p, 'w').write(s)
    hero('functional-weight-loss', 'weight-loss-labs', 'center 45%')
    hero('peptide-therapy', 'peptide-vials', '40% 70%')
    injectors()
    for slug, h in HEROES.items():
        set_hero(slug, *h)
    print('done')
