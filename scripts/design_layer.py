"""Apply the shared design layer to every page (idempotent):
site.css/site.js, the shared footer, the mobile Book/Call bar, a benefit marquee on hub pages,
italic accent words in H2s, long-H1 sizing and photo thumbnails on treatment cards.
Run from the repo root:  python3 scripts/design_layer.py
"""
import glob, html, json, re

ACCENTS = {
    'What would my monthly payment be?': 'monthly',
    # home
    'What happens at your first visit?': 'first',
    'Injectables, Laser &amp; Skin Treatments in Ocala': 'Ocala',
    'Personalized Skincare, Every Session': 'Every Session',
    'Every Journey Starts With a Conversation': 'Conversation',
    'GLO Med Spa FAQs': 'FAQs',
    'Find Your Sanctuary in Ocala': 'Sanctuary',
    # pillar
    'Which treatment is right for me?': 'right for me',
    'Injectables in Ocala, FL': 'Injectables',
    'Skin Services in Ocala, FL': 'Skin Services',
    'Wellness in Ocala, FL': 'Wellness',
    'Treatment Questions, Answered': 'Answered',
    'Not sure where to start?': 'start',
    # locations
    'Ocala, FL': 'Ocala', 'Palatka, FL': 'Palatka', 'Location FAQs': 'FAQs',
    'Visit Us in Ocala': 'Ocala', 'Visit Us in Palatka': 'Palatka',
    'Treatments at Our Ocala Location': 'Ocala', 'Treatments at Our Palatka Location': 'Palatka',
    'Beautiful Skin Looks Different on Everyone': 'Everyone',
    "Visiting Ocala? Here's What to Know": 'What to Know', "Visiting Palatka? Here's What to Know": 'What to Know',
    'Our Palatka, FL Location': 'Palatka', 'Our Ocala, FL Location': 'Ocala',
    # memberships, financing
    'Skin &amp; Skin Health Membership': 'Skin Health', 'Weight Loss &amp; Metabolic Membership': 'Metabolic',
    'Membership FAQ': 'FAQ', 'Ready to join?': 'join',
    '3 Reasons Why Patients Love Cherry': 'Love', 'How Does It Work?': 'Work', 'Patient Requirements': 'Requirements',
    'Talk to Us Before You Apply': 'Before You Apply', 'Financing FAQ': 'FAQ',
    # about
    'Who will I see at GLO?': 'see', 'What makes GLO different?': 'different', 'About GLO FAQs': 'FAQs', 'Ready to meet us?': 'meet us',
    # categories
    'Which injectable smooths wrinkles?': 'smooths wrinkles',
    'Which injectable restores volume or reshapes my features?': 'restores volume',
    'Wrinkle relaxer or filler: what&rsquo;s the difference?': 'the difference',
    'Injectables FAQs': 'FAQs', 'Skin Services FAQs': 'FAQs', 'Wellness FAQs': 'FAQs',
    'Explore more at GLO': 'GLO',
    'Not sure which injectable is right for you?': 'right for you',
    'Which laser treatment is right for my skin?': 'right for my skin',
    'What does radiofrequency skin tightening do?': 'radiofrequency',
    'Which facial, peel or microneedling treatment should I choose?': 'should I choose',
    'Laser, radiofrequency or microneedling: how do they compare?': 'how do they compare',
    'Not sure which skin treatment fits?': 'fits',
    'Can a medical program help with weight or hormones?': 'weight or hormones',
    'What helps with energy and recovery?': 'energy and recovery',
    'Which wellness program fits my goals?': 'my goals',
    'Ready to feel like yourself again?': 'yourself again',
}

MARQUEE_ITEMS = ['Licensed providers', 'Plans built around you', 'Injectables', 'Laser &amp; RF skin care',
                 'Facials &amp; peels', 'Medical wellness', 'Judgment-free care', 'Ocala &amp; Palatka, FL']

FOOTER = '''  <!-- ===================== FOOTER ===================== -->
  <footer id="contact" class="glo-footer">
    <div class="glo-footer-top">
      <div class="glo-footer-brand">
        <a href="/" aria-label="GLO Aesthetics + Wellness Lounge home"><img src="/assets/glo-logo.png" alt="GLO Aesthetics + Wellness Lounge" width="160" height="72" style="height:72px;width:auto;display:block;" loading="lazy"></a>
        <p>A medical aesthetics &amp; wellness med spa in Ocala and Palatka, FL &mdash; where every plan starts with listening to you.</p>
        <a href="/#book" class="glo-footer-book">Book a Consultation</a>
      </div>
      <nav aria-label="Treatments">
        <h3>Treatments</h3>
        <ul>
          <li><a href="/injectables">Injectables</a></li>
          <li><a href="/skin-services">Skin Services</a></li>
          <li><a href="/wellness">Medical Wellness</a></li>
          <li><a href="/treatments">All Treatments</a></li>
          <li><a href="/membership-programs">Memberships</a></li>
          <li><a href="/financing">Financing</a></li>
        </ul>
      </nav>
      <nav aria-label="Popular treatments">
        <h3>Popular</h3>
        <ul>
          <li><a href="/treatments/xeomin">Xeomin</a></li>
          <li><a href="/treatments/dermal-filler">Dermal &amp; Lip Filler</a></li>
          <li><a href="/treatments/laser-skin-revitalization">CO2 Laser Resurfacing</a></li>
          <li><a href="/treatments/microneedling">Microneedling</a></li>
          <li><a href="/treatments/laser-hair-removal">Laser Hair Removal</a></li>
          <li><a href="/treatments/functional-weight-loss">Medical Weight Loss</a></li>
        </ul>
      </nav>
      <div>
        <h3>Visit Us</h3>
        <div class="glo-footer-loc"><strong><a href="/locations/ocala">Ocala</a></strong><p>1925 SW 18th Ct, Unit 109<br>Ocala, FL 34471<br>Mon, Tue, Thu, Fri 9am&ndash;5pm &middot; Wed 9am&ndash;6pm<br>Sat &amp; Sun by appointment</p></div>
        <div class="glo-footer-loc"><strong><a href="/locations/palatka">Palatka</a></strong><p>210 St Johns Ave<br>Palatka, FL 32177</p></div>
        <p style="margin-top:18px;"><a href="tel:+13525598034">352-559-8034</a><br><a href="mailto:info@gloocala.com">info@gloocala.com</a></p>
      </div>
    </div>
    <div class="glo-footer-bottom">
      <span>&copy; 2026 GLO Aesthetics + Wellness Lounge. All rights reserved.</span>
      <span><a href="/about">About &amp; Team</a> &nbsp;&middot;&nbsp; <a href="/reviews">Reviews</a> &nbsp;&middot;&nbsp; <a href="/locations">Locations</a> &nbsp;&middot;&nbsp; <a href="/#faq">FAQs</a> &nbsp;&middot;&nbsp; <a href="/#book">Book Online</a></span>
    </div>
  </footer>
'''


def balanced_div_end(s, start):
    """Index just past the </div> that closes the <div ...> opening at `start`."""
    depth, i = 0, start
    for m in re.finditer(r'<div\b|</div>', s[start:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return start + m.end()
    raise ValueError('unbalanced')


def replace_footer(s):
    if 'class="glo-footer"' in s:
        return s
    m = re.search(r'  <!-- ===================== FOOTER[^\n]*-->\n', s)
    start = s.index('<div', m.end())
    end = balanced_div_end(s, start)
    old = s[start:end]
    disclaimer = ''
    d = re.search(r'\n\s*<div class="glo-container" style="max-width:1000px;margin:0 auto;padding:0 48px 28px;text-align:center;">\s*<p[^>]*>\s*(Individual results vary.*?)</p>\s*</div>', old, re.S)
    if d:  # home: the disclaimer lived inside the footer; give it its own band like the other pages
        disclaimer = ('  <!-- ===================== MEDICAL / COMPLIANCE DISCLAIMER ===================== -->\n'
                      '  <div style="width:100%;background:#F3F0EA;border-top:1px solid #E6E1D6;">\n'
                      '    <div class="glo-container" style="max-width:1000px;margin:0 auto;padding:28px 48px;text-align:center;">\n'
                      f'      <p style="font-size:13px;line-height:1.7;color:#8A8377;font-weight:400;">{d.group(1).strip()}</p>\n    </div>\n  </div>\n\n')
    return s[:m.start()] + disclaimer + FOOTER + s[end:].lstrip(' ')


def add_assets(s):
    if '/assets/site.css' not in s:
        s = s.replace('</head>', '<link rel="stylesheet" href="/assets/site.css">\n</head>', 1)
    if '/assets/site.js' not in s:
        s = s.replace('</body>', '<script src="/assets/site.js" defer></script>\n</body>', 1)
    return s


def add_mbar(s):
    if 'class="glo-mbar"' in s:
        return s
    hero = s.split('<!-- ===================== HERO', 1)[-1][:6000]
    m = re.search(r'<a href="(https://gloocala\.janeapp\.com[^"]*)"', hero)
    book = f'<a href="{m.group(1)}" target="_blank" rel="noopener" class="glo-mbar-book">Book Now</a>' if m else '<a href="/#book" class="glo-mbar-book">Book Now</a>'
    bar = ('<nav class="glo-mbar" aria-label="Quick actions">' + book +
           '<a href="tel:+13525598034" class="glo-mbar-call"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>Call</a></nav>\n')
    return s.replace('<script src="/assets/site.js"', bar + '<script src="/assets/site.js"', 1)


def marquee():
    items = ''.join(f'<li>{t}</li>' for t in MARQUEE_ITEMS)
    return ('  <!-- ===================== BENEFIT MARQUEE ===================== -->\n'
            f'  <div class="glo-marquee" role="presentation"><div class="glo-marquee-track"><ul>{items}</ul><ul aria-hidden="true">{items}</ul></div></div>\n\n')


def add_marquee(f, s):
    if 'glo-marquee' in s and 'class="glo-marquee"' in s:
        return s
    if f == 'index.html':
        marker = '  <!-- ===================== PHILOSOPHY'
    elif f in ('treatments/index.html', 'injectables.html', 'skin-services.html', 'wellness.html', 'locations/index.html'):
        after = s.index('<!-- ===================== HERO')
        nxt = re.compile(r'  <!-- ===================== ').search(s, after + 10)
        marker = s[nxt.start():nxt.start() + 60]
    else:
        return s
    return s.replace(marker, marquee() + marker, 1)


def accent_h2(f, s, keyword=None):
    def repl(m):
        attrs, inner = m.group(1), m.group(2)
        if '<span' in inner or '<em' in inner:
            return m.group(0)
        word = ACCENTS.get(inner.strip())
        if word is None and keyword:
            k = re.search(re.escape(keyword), inner, re.I)
            word = k.group(0) if k else None
        if not word or word not in inner:
            return m.group(0)
        i = inner.rindex(word) if word in ('Ocala', 'Palatka') else inner.index(word)
        return f'<h2{attrs}>{inner[:i]}<span class="glo-accent">{word}</span>{inner[i + len(word):]}</h2>'
    return re.sub(r'<h2([^>]*)>(.*?)</h2>', repl, s, flags=re.S)


def long_h1(s):
    m = re.search(r'<h1 class="glo-hero-h1( is-long)?"', s)
    if not m or m.group(1):
        return s
    text = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1)))
    if len(text) > 30:
        s = s.replace('<h1 class="glo-hero-h1"', '<h1 class="glo-hero-h1 is-long"', 1)
    return s


def card_thumbs(s, heroes):
    def repl(m):
        a, slug = m.group(0), m.group(1)
        if slug not in heroes:
            return a
        src, alt = heroes[slug]
        return a + f'\n          <span class="tx-thumb"><img src="{src}" alt="{alt}" width="400" height="260" loading="lazy" decoding="async"></span>'
    if 'class="tx-thumb"' in s:
        return s
    return re.sub(r'<a href="/treatments/([a-z0-9-]+)" class="card-hover"[^>]*>', repl, s)


if __name__ == '__main__':
    heroes = {}
    for f in glob.glob('treatments/*.html'):
        m = re.search(r'<div class="glo-split-media"><img src="([^"]+)" alt="([^"]*)"', open(f).read())
        if m and not f.endswith('index.html'):
            heroes[f.split('/')[1][:-5]] = (m.group(1), m.group(2))
    keywords = {json.load(open(p))['slug']: json.load(open(p))['keyword'] for p in glob.glob('content/treatments/*.json')}
    for f in sorted(glob.glob('*.html') + glob.glob('*/*.html')):
        s = open(f).read()
        n = add_assets(s)
        n = replace_footer(n)
        n = add_mbar(n)
        n = add_marquee(f, n)
        slug = f.split('/')[1][:-5] if f.startswith('treatments/') else None
        n = accent_h2(f, n, keywords.get(slug))
        n = long_h1(n)
        n = card_thumbs(n, heroes)
        if n != s:
            open(f, 'w').write(n)
            print('updated', f)


def photo_band(f, s, bands):
    """Swap the repeated four-photo strip for a full-bleed photo band unique to the page."""
    key = f[:-5] if f.startswith('locations/') else (f.split('/')[1][:-5] if f.startswith('treatments/') else None)
    if key not in bands or 'class="glo-band"' in s:
        return s
    m = re.search(r'  <!-- ===================== REAL RESULTS[^\n]*-->\n', s)
    if not m:
        return s
    start = s.index('<div', m.end())
    end = balanced_div_end(s, start)
    h2, text, img, alt = bands[key]
    hero = s.split('<!-- ===================== HERO', 1)[-1][:6000]
    jm = re.search(r'<a href="(https://gloocala\.janeapp\.com[^"]*)"', hero)
    book = f'href="{jm.group(1)}" target="_blank" rel="noopener"' if jm else 'href="/#book"'
    pos = 'center 30%' if key.startswith('locations/') else 'left center'
    band = (f'  <!-- ===================== PHOTO BAND ===================== -->\n'
            f'  <section class="glo-band">\n'
            f'    <img src="{img}" alt="{alt}" width="1920" height="1080" loading="lazy" decoding="async" style="object-position:{pos};">\n'
            f'    <div class="glo-band-inner"><div class="glo-band-copy">\n'
            f'      <div class="glo-band-kicker">Real glow, real life</div>\n'
            f'      <h2 class="glo-h2">{h2}</h2>\n'
            f'      <p>{text}</p>\n'
            f'      <a {book} class="glo-band-btn">Book a Consultation</a>\n'
            f'    </div></div>\n'
            f'    <p class="glo-band-note">Representative imagery, AI-generated for illustration.</p>\n'
            f'  </section>')
    return s[:m.start()] + band + s[end:]


if __name__ == '__main__':
    bands = json.load(open('content/bands.json'))
    for f in sorted(glob.glob('treatments/*.html') + glob.glob('locations/*.html')):
        s = open(f).read()
        n = photo_band(f, s, bands)
        if n != s:
            open(f, 'w').write(n)
            print('band', f)
