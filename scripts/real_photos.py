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
    'xeomin': ('/assets/ai/glo-0d65b188-75d3-41df-9f9d-6be56dcab860.webp', AI + 'Baily Bellamy giving a Xeomin injection between a client\'s brows', 'center 25%', 1600, 2000),
    'microneedling': ('/assets/team/sundee-bass-microneedling-pen-ocala-fl.webp', 'Sundee Bass, GLO medical esthetician and microneedling specialist, holding her microneedling pen in Ocala, FL', 'center 20%', 1200, 1500),
    'coolpeel': ('/assets/ai/glo-bd33ca89-99f6-44bb-929a-085ac3af08ea.webp', AI + 'McKenzie McCalla, APRN, performing CoolPeel with the Tetra Pro CO2 laser', 'center 25%', 1600, 2000),
    'laser-skin-revitalization': ('/assets/ai/glo-a8535d18-fd0d-4bae-be2c-1336b2597f96.webp', AI + 'McKenzie McCalla, APRN, performing CO2 laser resurfacing on the Tetra Pro laser', 'center 25%', 1600, 2000),
    'motus-laser-facial': ('/assets/ai/glo-48fd7c71-78b2-4087-8a43-de70bc178e63.webp', AI + 'Sundee Bass performing a Motus AY laser facial', 'center 25%', 1600, 2000),
    'laser-hair-removal': ('/assets/ai/glo-8f0ddcbd-999c-49dc-b58b-5ae715e28e09.webp', AI + 'a laser hair removal handpiece gliding along a lower leg', 'center 40%', 1600, 2000),
    'skin-tightening': ('/assets/ai/glo-54cf79e1-d826-497d-8bc7-857cd8fb2300.webp', AI + 'McKenzie McCalla, APRN, gliding the Everesse handpiece along a client\'s jawline', 'center 25%', 1600, 2000),
    'radiant-lift': ('/assets/ai/glo-a05f2566-5295-4f03-98ab-8fcfdae61641.webp', AI + 'McKenzie McCalla, APRN, beside the Everesse system with a Radiant Lift client', 'center 25%', 1600, 2000),
    'custom-facials-peels': ('/assets/ai/glo-bb2e7956-fe2e-4aaf-82cf-9f7df265e26e.webp', AI + 'Sundee Bass brushing a chemical peel onto a client\'s cheek', 'center 25%', 1600, 2000),
    'mini-facials': ('/assets/ai/glo-ec78ddd6-8dc0-4003-b08c-765b5db5e25d.webp', AI + 'Sundee Bass applying serum during a mini facial', 'center 25%', 1600, 2000),
    'daxxify-facial-microneedling': ('/assets/ai/glo-29520b2c-26e3-4df1-8e47-452d3b80e276.webp', AI + 'Sundee Bass microneedling a client\'s cheek during a Daxxify facial', 'center 25%', 1600, 2000),
    'daxxify': ('/assets/ai/glo-9e8b55f1-f5e7-4b87-94fb-2aabd3ceb8f0.webp', AI + 'McKenzie McCalla, APRN, giving a Daxxify injection at the crow\'s feet', 'center 25%', 1600, 2000),
    'dermal-filler': ('/assets/ai/glo-23dd3f42-a777-4f76-ac98-fb7fb4182a98.webp', AI + 'Baily Bellamy placing lip filler with a fine syringe', 'center 25%', 1600, 2000),
    'liquid-rhinoplasty': ('/assets/ai/glo-8ea145b7-9823-4267-905e-a13bcd4eb224.webp', AI + 'Baily Bellamy placing filler at the bridge of a client\'s nose', 'center 25%', 1600, 2000),
    'dissolve-ha-dermal-filler': ('/assets/ai/glo-d4429368-9e19-446d-b8a4-08c27b3cd623.webp', AI + 'McKenzie McCalla, APRN, assessing a client\'s lips before dissolving earlier filler', 'center 25%', 1600, 2000),
    'hormone-replacement-therapy': ('/assets/ai/glo-c83b37a7-97cf-4960-b81f-45dd7374aafb.webp', AI + 'McKenzie McCalla, APRN, listening to a client describe her symptoms', 'center 25%', 1600, 2000),
    'iv-hydration': ('/assets/ai/glo-f1458133-9d82-48fa-b2d6-061d87dbb739.webp', AI + 'a man relaxing in a lounge chair with an IV drip, reading a book', 'center 30%', 1600, 2000),
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


# Images that must match the words beside them (Nov 2026 audit): real staff doing what the section describes.
# (file, src of the image to replace, nth match, new src, alt, object-position, width, height, is_hero)
SWAPS = [
    ('index.html', '/assets/ocala/facial-room.webp', 0, '/assets/ai/glo-ca456cf2-393d-4434-87e6-4ce74fc951a1.webp', AI + 'McKenzie McCalla, APRN, listening to a client during her consultation', 'center 30%', 1600, 2000, False),
    ('index.html', '/assets/ocala/hallway.webp', 0, '/assets/team/mckenzie-mccalla-treatment-plan-ocala-fl.webp', 'McKenzie McCalla, APRN, with her laptop, ready to walk you through your options and pricing', 'center 25%', 1200, 1500, False),
    ('index.html', '/assets/ocala/laser-room.webp', 0, '/assets/ai/glo-1891efea-b54a-4bf1-bb8d-31cc993f5b4d.webp', AI + 'Baily Bellamy performing an Everesse treatment in a private room', 'center 30%', 1600, 2000, False),
    ('financing.html', '/assets/ocala/facial-room.webp', 0, '/assets/ai/glo-872b5a58-7e3d-423d-91ca-b6e05bae034a.webp', AI + 'Baily Bellamy walking a client through monthly payment options on a tablet', 'center 25%', 1600, 2000, True),
    ('reviews.html', '/assets/ocala/lounge.webp', 0, '/assets/ai/glo-ee0111c8-4adc-4430-8583-629ceef7f1f6.webp', AI + 'Sundee Bass laughing with a happy client after her appointment', 'center 25%', 1600, 2000, True),
    ('locations/palatka.html', '/assets/ai/glo-d9e4d660-1b3a-42f6-9dc6-df4028ebe8bf.webp', 0, '/assets/ai/glo-b644410c-5ac9-4a5c-a2c3-0e61a6b7ff0c.webp', AI + 'Baily Bellamy and Sundee Bass, who see clients at GLO in Palatka', 'center 20%', 1600, 2000, True),
    ('membership-programs.html', '/assets/ocala/facial-room.webp', 0, '/assets/ai/glo-52879d92-ee42-4642-9cb3-dd92c132cb5b.webp', AI + 'Sundee Bass beginning a client\'s monthly Signature Facial', 'center 25%', 1600, 2000, True),
    ('membership-programs.html', '/assets/ocala/lounge-retail.webp', 0, '/assets/ai/glo-18aaa743-7f4e-4649-a4c1-ee8b9c4e4fa4.webp', AI + 'Sundee Bass performing gua sha sculpting massage during a Signature Facial', 'center 30%', 1600, 2000, False),
    ('skin-services.html', '/assets/ai/glo-175e4678-0ae9-4464-8168-4d4a5e763ed7.webp', 0, '/assets/ai/glo-1f9b1f1d-d855-48ea-b9b0-17f8fb938f89.webp', AI + 'McKenzie McCalla and Sundee Bass with the Tetra Pro CO2 laser and Everesse system', 'center 25%', 1600, 2000, True),
    ('wellness.html', '/assets/ai/glo-f2efb89a-4a81-4e8a-ac4e-4c29d2e70aba.webp', 0, '/assets/ai/glo-e9e0bfd9-305f-4cca-9144-b6d1a5f416a0.webp', AI + 'McKenzie McCalla, APRN, reviewing a client\'s lab results with him', 'center 25%', 1600, 2000, True),
    ('treatments/index.html', '/assets/ai/glo-a0a683a6-c3f0-4e84-b5d5-d3d138eabaee.webp', 0, '/assets/ai/glo-59b1e871-1e92-4e71-851e-0b3a30a84ff6.webp', AI + 'GLO providers Baily Bellamy, Sundee Bass and McKenzie McCalla in a treatment room', 'center 20%', 1600, 2000, True),
    ('treatments/custom-facials-peels.html', '/assets/ocala/facial-room.webp', 0, '/assets/ai/glo-c53b7bad-65d9-4d91-84a6-ba421af71a82.webp', AI + 'Sundee Bass examining a client\'s skin under a magnifying lamp before her facial', 'center 30%', 1600, 2000, False),
    ('treatments/mini-facials.html', '/assets/ocala/facial-room.webp', 0, '/assets/ai/glo-0ba60a43-1e9e-484e-b405-aef2af4422bf.webp', AI + 'Sundee Bass brushing on a hydrating mask during a mini facial', 'center 30%', 1600, 2000, False),
]
CAPTIONS = {  # new figure captions where the old one described a room
    ('treatments/custom-facials-peels.html', 'One of our private facial suites in Ocala.'): 'Every facial starts with a close look at your skin.',
    ('treatments/mini-facials.html', 'One of our private facial suites in Ocala.'): 'A quick, hydrating refresh in a private suite.',
    ('membership-programs.html', 'Our Ocala lounge, with the medical-grade skincare members save on.'): 'Gua sha and sculpting massage are two of the techniques your facial may include.',
}


def swap_images():
    for f, old, nth, src, alt, pos, w, h, hero in SWAPS:
        s = open(f).read()
        tags = [m for m in re.finditer(r'<img [^>]*src="%s"[^>]*>' % re.escape(old), s)]
        if len(tags) <= nth:
            continue
        m = tags[nth]
        tag = m.group(0)
        new = re.sub(r'src="[^"]*"', f'src="{src}"', tag, 1)
        new = re.sub(r'alt="[^"]*"', 'alt="%s"' % alt.replace('"', '&quot;'), new, 1)
        new = re.sub(r'width="\d+"', f'width="{w}"', new, 1)
        new = re.sub(r'height="\d+"', f'height="{h}"', new, 1)
        new = re.sub(r'object-position:[^;"]*', f'object-position:{pos}', new, 1) if 'object-position' in new else new
        s = s[:m.start()] + new + s[m.end():]
        if hero:
            jpg = SITE + src.replace('.webp', '.jpg')
            old_jpg = SITE + old.replace('.webp', '.jpg')
            for prop in ('og:image', 'twitter:image'):
                s = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % prop, lambda mm: mm.group(1) + jpg, s)
            s = s.replace(f'"{old_jpg}"', f'"{jpg}"').replace(f'"{SITE}{old}"', f'"{jpg}"')
        for (cf, a), b in CAPTIONS.items():
            if cf == f:
                s = s.replace(a, b)
        open(f, 'w').write(s)


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
    swap_images()
    print('done')
