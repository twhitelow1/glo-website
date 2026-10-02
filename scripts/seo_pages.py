"""One-off SEO/AEO pass for home, locations, memberships, financing and the Treatments pillar, plus sitewide
hero photos as <img>. Safe to re-run: each step checks whether it has already been applied."""
import json, re, sys
sys.path.insert(0, 'scripts')
from glo_page import SITE, UPDATED, BUSINESS_ID, IMG, esc, plain, updated_line, faq_html  # noqa

GBP_OCALA = 'https://maps.google.com/?cid=11063403909156873399'
GEO_OCALA = {'@type': 'GeoCoordinates', 'latitude': 29.1688429, 'longitude': -82.1558657}
HOURS_OCALA = [
    {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Thursday', 'Friday'], 'opens': '09:00', 'closes': '17:00'},
    {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Wednesday', 'opens': '09:00', 'closes': '18:00'}]
ADDR = {
    'ocala': {'@type': 'PostalAddress', 'streetAddress': '1925 SW 18th Ct, Unit 109', 'addressLocality': 'Ocala', 'addressRegion': 'FL', 'postalCode': '34471', 'addressCountry': 'US'},
    'palatka': {'@type': 'PostalAddress', 'streetAddress': '210 St Johns Ave', 'addressLocality': 'Palatka', 'addressRegion': 'FL', 'postalCode': '32177', 'addressCountry': 'US'}}
LOGO = SITE + '/assets/glo-logo.png'


def rd(p):
    return open(p).read()


def wr(p, s):
    open(p, 'w').write(s)


def set_head(s, title=None, desc=None, image=None, robots=None):
    if title:
        s = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', s, count=1)
        s = re.sub(r'(<meta (?:property|name)="(?:og|twitter):title" content=")[^"]*', lambda m: m.group(1) + esc(title), s)
    if desc:
        s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">', s, count=1)
        s = re.sub(r'(<meta (?:property|name)="(?:og|twitter):description" content=")[^"]*', lambda m: m.group(1) + esc(desc), s)
    if image:
        for prop, tag in (('og:image', 'property'), ('twitter:image', 'name')):
            if f'"{prop}"' in s:
                s = re.sub(r'(<meta %s="%s" content=")[^"]*' % (tag, prop), lambda m: m.group(1) + image, s)
            else:
                anchor = '<meta property="og:locale"' if prop == 'og:image' and '<meta property="og:locale"' in s else '</head>'
                if prop == 'twitter:image':
                    anchor = '<script type="application/ld+json">' if '<script type="application/ld+json">' in s else '</head>'
                s = s.replace(anchor, f'<meta {tag}="{prop}" content="{image}">\n' + anchor, 1)
    if robots:
        s = re.sub(r'<meta name="robots" content="[^"]*">', f'<meta name="robots" content="{robots}">', s, count=1)
    return s


def add_ld(s, obj, marker):
    if marker in s:
        s = re.sub(r'<!-- %s -->\n<script type="application/ld\+json">.*?</script>\n' % re.escape(marker), '', s, flags=re.S)
    block = f'<!-- {marker} -->\n<script type="application/ld+json">\n' + json.dumps(obj, indent=1, ensure_ascii=False) + '\n</script>\n'
    return s.replace('<link rel="preconnect"', block + '<link rel="preconnect"', 1)


def faq_pairs(s, start_marker, end_marker):
    sec = s.split(start_marker, 1)[1].split(end_marker, 1)[0]
    return re.findall(r'<div class="faq-row"[^>]*>\s*<(?:div|h3)[^>]*>(.*?)</(?:div|h3)>\s*<(?:div|p)[^>]*>(.*?)</(?:div|p)>\s*</div>', sec, re.S)


def faq_ld(pairs, url):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
        {'@type': 'Question', 'name': plain(q), 'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}} for q, a in pairs]}


def rows_to_h3(s, start_marker, end_marker, extra=()):
    head, rest = s.split(start_marker, 1)
    sec, tail = rest.split(end_marker, 1)
    sec = re.sub(r'(<div class="faq-row"[^>]*>\s*)<div style="[^"]*">(.*?)</div>(\s*)<div style="[^"]*">(.*?)</div>',
                 r'\1<h3 style="font-size:20px;font-weight:500;color:#221F1B;margin:0 0 8px;line-height:1.35;">\2</h3>\3<p style="font-size:16px;line-height:1.7;color:#5C574E;font-weight:300;margin:0;">\4</p>', sec, flags=re.S)
    if extra and extra[0][0] not in sec:
        add = ''.join(f'''
      <div class="faq-row" style="padding:22px 0;">
        <h3 style="font-size:20px;font-weight:500;color:#221F1B;margin:0 0 8px;line-height:1.35;">{q}</h3>
        <p style="font-size:16px;line-height:1.7;color:#5C574E;font-weight:300;margin:0;">{a}</p>
      </div>''' for q, a in extra)
        sec = re.sub(r'(\n    </div>\n  </div>\n\s*)$', lambda m: add + m.group(1), sec, count=1)
    return head + start_marker + sec + end_marker + tail


# ------------------------------------------------------------------ hero photos as <img>, sitewide
def hero_img(s):
    def repl(m):
        alt, url, pos = m.group(1), m.group(2), m.group(3) or 'center'
        return (f'<div class="glo-split-media"><img src="{url}" alt="{alt}" width="1024" height="1365" fetchpriority="high" '
                f'decoding="async" style="object-position:{pos};"></div>')
    return re.sub(r'<div class="glo-split-media" role="img" aria-label="([^"]*)" style="background-image:url\(\'([^\']+)\'\);(?:background-position:([^;"]+);)?[^"]*"></div>', repl, s)


def lifestyle_imgs(s):
    if 'lc-shade' in s:
        return s
    def repl(m):
        alt, grad, url, pos, rest = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        return (f'<div class="lifestyle-card" style="border-radius:8px;overflow:hidden;background:#B8894F;{rest}">'
                f'<img src="{url}" alt="{alt}" width="768" height="1024" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos};">'
                f'<span class="lc-shade" aria-hidden="true" style="position:absolute;inset:0;background:{grad};"></span>')
    s = re.sub(r'<div class="lifestyle-card" role="img" aria-label="([^"]*)" style="border-radius:8px;overflow:hidden;background:(linear-gradient\([^)]*\)[^)]*\)),url\(\'([^\']+)\'\) ([^/]+)/cover no-repeat,#B8894F;([^"]*)">', repl, s)
    return s.replace('.lifestyle-card:hover{', '.lifestyle-card > :not(img):not(.lc-shade){position:relative;z-index:1;}\n  .lifestyle-card:hover{', 1)


import glob
for f in sorted(glob.glob('*.html') + glob.glob('*/*.html')):
    s = rd(f)
    n = hero_img(s)
    if f == 'index.html':
        n = lifestyle_imgs(n)
    # og:image / twitter:image always match the hero photo where there is one
    m = re.search(r'<div class="glo-split-media"><img src="([^"]+)"', n)
    if m and 'cloudfront' in m.group(1):
        n = set_head(n, image=m.group(1))
    if n != s:
        wr(f, n)
        print('images', f)

# ------------------------------------------------------------------ home
s = rd('index.html')
s = set_head(s, 'Medical Aesthetics & Wellness in Ocala, FL | GLO MedSpa',
             'GLO is a medical aesthetics and wellness med spa in Ocala and Palatka, FL: injectables, laser, skin care and medical weight loss. Book a consultation.')
s = s.replace('Medical Aesthetics &amp; Wellness Lounge in <span style="font-style:italic;font-weight:600;color:#B8894F;">Ocala</span></h1>',
              'Medical Aesthetics &amp; Wellness Lounge in <span style="font-style:italic;font-weight:600;color:#B8894F;">Ocala</span>, FL</h1>')
HOME_FAQ = [
    ('What is a med spa?', 'A med spa (medical spa) pairs a calm spa setting with medical treatments &mdash; injectables, lasers, medical-grade skin care and wellness therapies &mdash; performed by licensed providers under a physician&rsquo;s direction. GLO Aesthetics + Wellness Lounge is a med spa in Ocala and Palatka, FL.'),
    ('Where is GLO Aesthetics + Wellness Lounge?', 'GLO has two Florida locations: 1925 SW 18th Ct, Unit 109, Ocala, FL 34471, and 210 St Johns Ave, Palatka, FL 32177. Call 352-559-8034 or <a href="/locations" style="color:#B8894F;font-weight:500;">see both locations</a>.'),
    ('What treatments does GLO offer?', 'Injectables (Xeomin, Daxxify, dermal and lip filler, liquid rhinoplasty), skin services (Tetra CO2 and Motus laser, CoolPeel, laser hair removal, Everesse and Radiant Lift radiofrequency, facials, chemical peels and SkinPen microneedling) and medical wellness (weight loss, hormone therapy, IV hydration and peptides). <a href="/treatments" style="color:#B8894F;font-weight:500;">Compare all treatments</a>.'),
    ('Do I need a consultation before my first treatment?', 'Yes. Every new client starts with a consultation, so a licensed provider can review your goals and health history and recommend a plan. There&rsquo;s never pressure to book anything during the visit.'),
    ('What are GLO&rsquo;s hours?', 'The Ocala location is open Monday, Tuesday, Thursday and Friday 9am&ndash;5pm, Wednesday 9am&ndash;6pm, and weekends by appointment. Palatka hours vary; see real-time availability on our online booking calendar or call 352-559-8034.'),
    ('Do you offer memberships or financing?', 'Yes. GLO memberships include a monthly treatment and member pricing, and financing through Cherry lets you pay over time. <a href="/financing" style="color:#B8894F;font-weight:500;">Learn about financing</a>.'),
]
if 'id="faq"' not in s:
    s = s.replace('  <!-- ===================== VISIT US ===================== -->',
                  faq_html('GLO Med Spa FAQs', HOME_FAQ, 'faq', '#FAF9F6').lstrip('\n') + '\n  <!-- ===================== VISIT US ===================== -->', 1)
s = s.replace('<a href="#" class="footer-link">FAQs</a>', '<a href="/#faq" class="footer-link">FAQs</a>')
# business schema: complete it and fix the catalog grouping (Everesse is radiofrequency, not laser)
m = re.search(r'<script type="application/ld\+json">\n(\{\n  "@context": "https://schema.org",\n  "@type": \["MedicalBusiness".*?)\n</script>', s, re.S)
biz = json.loads(m.group(1))
pillar = rd('treatments/index.html')
def section_items(sec):
    block = re.search(r'<div id="%s".*?<div class="tx-grid"[^>]*>(.*?)\n      </div>\n    </div>\n  </div>' % sec, pillar, re.S).group(1)
    return [{'@type': 'Offer', 'itemOffered': {'@type': 'MedicalTherapy' if sec == 'wellness' else 'MedicalProcedure', 'name': plain(n), 'url': SITE + u}}
            for u, n in re.findall(r'<a href="(/treatments/[^"]+)" class="card-hover".*?<h3[^>]*>(.*?)</h3>', block, re.S)]
biz.update({
    'legalName': 'GLO Aesthetics + Wellness Lounge', 'alternateName': ['GLO MedSpa', 'GLO Ocala'],
    'logo': LOGO, 'geo': GEO_OCALA, 'hasMap': GBP_OCALA, 'sameAs': [GBP_OCALA],
    'openingHoursSpecification': HOURS_OCALA,
    'areaServed': [{'@type': 'City', 'name': c} for c in ('Ocala', 'Belleview', 'Silver Springs Shores', 'Palatka', 'Gainesville')] + [{'@type': 'AdministrativeArea', 'name': 'Marion County, Florida'}, {'@type': 'AdministrativeArea', 'name': 'Putnam County, Florida'}],
    'department': [{'@id': SITE + '/locations/ocala#location'}, {'@id': SITE + '/locations/palatka#location'}],
    'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Treatments at GLO Aesthetics + Wellness Lounge', 'url': SITE + '/treatments', 'itemListElement': [
        {'@type': 'OfferCatalog', 'name': 'Injectables', 'url': SITE + '/injectables', 'itemListElement': section_items('injectables')},
        {'@type': 'OfferCatalog', 'name': 'Skin Services', 'url': SITE + '/skin-services', 'itemListElement': section_items('skin')},
        {'@type': 'OfferCatalog', 'name': 'Medical Wellness', 'url': SITE + '/wellness', 'itemListElement': section_items('wellness')}]},
})
biz['areaServed'] = [a for a in biz['areaServed'] if a['name'] != 'Gainesville']
s = s[:m.start(1)] + json.dumps(biz, indent=1, ensure_ascii=False) + s[m.end(1):]
s = add_ld(s, {'@context': 'https://schema.org', '@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/',
               'name': 'GLO Aesthetics + Wellness Lounge', 'inLanguage': 'en-US', 'publisher': {'@id': BUSINESS_ID}}, 'glo-website-ld')
s = add_ld(s, faq_ld(HOME_FAQ, SITE + '/'), 'glo-faq-ld')
wr('index.html', s)


# ------------------------------------------------------------------ location pages
LOC = {
 'ocala': dict(
   title='Med Spa in Ocala, FL | GLO Aesthetics + Wellness Lounge',
   h1_old='Our Ocala, FL Location', city='Ocala',
   answer='GLO Aesthetics + Wellness Lounge in Ocala is our flagship med spa at 1925 SW 18th Ct, Unit 109, Ocala, FL 34471. Licensed providers offer injectables, laser and radiofrequency skin treatments, facials and medical wellness. We&rsquo;re open weekdays, with weekends by appointment &mdash; call 352-559-8034 or book online.',
   extra=[('Where is GLO&rsquo;s Ocala location?', 'GLO&rsquo;s Ocala med spa is at 1925 SW 18th Ct, Unit 109, Ocala, FL 34471. Tap &ldquo;Get Directions&rdquo; above for turn-by-turn directions from Google Maps.'),
          ('What are the Ocala location&rsquo;s hours?', 'Monday, Tuesday, Thursday and Friday 9am&ndash;5pm, Wednesday 9am&ndash;6pm, and Saturday and Sunday by appointment. Call 352-559-8034 for same-week availability.')],
   ld=dict(geo=GEO_OCALA, hasMap=GBP_OCALA, sameAs=[GBP_OCALA], openingHoursSpecification=HOURS_OCALA)),
 'palatka': dict(
   title='Med Spa in Palatka, FL | GLO Aesthetics + Wellness Lounge',
   h1_old='Our Palatka, FL Location', city='Palatka',
   answer='GLO Aesthetics + Wellness Lounge in Palatka brings the same licensed aesthetics and wellness care as our Ocala flagship to 210 St Johns Ave, Palatka, FL 32177 &mdash; injectables, laser and radiofrequency skin treatments, facials and medical wellness, closer to home for Putnam County. Book online or call 352-559-8034.',
   extra=[('Where is GLO&rsquo;s Palatka location?', 'GLO&rsquo;s Palatka med spa is at 210 St Johns Ave, Palatka, FL 32177. Tap &ldquo;Get Directions&rdquo; above for directions from Google Maps.'),
          ('What are the Palatka location&rsquo;s hours?', 'Palatka appointment times vary with our providers&rsquo; schedules. See real-time availability on our online booking calendar, or call 352-559-8034 and we&rsquo;ll find a time that works.')],
   ld={}),
}
for slug, c in LOC.items():
    f = f'locations/{slug}.html'
    s = rd(f)
    url = f'{SITE}/locations/{slug}'
    s = set_head(s, c['title'])
    s = re.sub(r'(<h1 class="glo-hero-h1" style=")[^"]*(">)' + re.escape(c['h1_old']) + '</h1>',
               lambda m: m.group(1) + 'font-size:54px;line-height:1.12;color:#221F1B;max-width:560px;' + m.group(2)
               + f'Med Spa in <span style="font-style:italic;color:#B8894F;">{c["city"]}</span>, FL</h1>', s)
    s = re.sub(r'(</h1>\s*<p) style="([^"]*)">.*?</p>', lambda m: m.group(1) + f' class="glo-answer" style="{m.group(2)}">\n          {c["answer"]}\n        </p>', s, count=1, flags=re.S)
    s = rows_to_h3(s, '<!-- ===================== FAQ', '<!-- ===================== OTHER LOCATION', c['extra'])
    pairs = faq_pairs(s, '<!-- ===================== FAQ', '<!-- ===================== OTHER LOCATION')
    m = re.search(r'<script type="application/ld\+json">\n(\{\n  "@context": "https://schema.org",\n  "@type": \[\n    "MedicalBusiness".*?)\n</script>', s, re.S)
    loc = json.loads(m.group(1))
    loc.update({'@id': url + '#location', 'parentOrganization': {'@id': BUSINESS_ID}, 'image': re.search(r'og:image" content="([^"]+)"', s).group(1),
                'logo': LOGO, 'email': 'info@gloocala.com', 'priceRange': '$$-$$$', 'address': ADDR[slug],
                'areaServed': [{'@type': 'City', 'name': c['city']}, {'@type': 'AdministrativeArea', 'name': 'Marion County, Florida' if slug == 'ocala' else 'Putnam County, Florida'}]})
    loc.update(c['ld'])
    s = s[:m.start(1)] + json.dumps(loc, indent=1, ensure_ascii=False) + s[m.end(1):]
    s = add_ld(s, faq_ld(pairs, url), 'glo-faq-ld')
    wr(f, s)
    print('location', f, len(pairs), 'FAQs')

# ------------------------------------------------------------------ locations hub
f = 'locations/index.html'
s = rd(f)
url = SITE + '/locations'
s = set_head(s, 'Med Spa Locations in Ocala & Palatka, FL | GLO',
             'Visit GLO Aesthetics + Wellness Lounge in Ocala or Palatka, FL. Addresses, hours, maps and online booking for both med spa locations. Book today.')
HUB_FAQ = [
    ('Where are GLO&rsquo;s locations?', 'GLO Aesthetics + Wellness Lounge has two Florida med spas: 1925 SW 18th Ct, Unit 109, Ocala, FL 34471 (our flagship), and 210 St Johns Ave, Palatka, FL 32177.'),
    ('Do both locations offer the same treatments?', 'Both locations offer the full GLO treatment menu. Availability of specific devices may vary by location, so ask when you book if you have a particular technology in mind.'),
    ('How do I book at a specific location?', 'Use the &ldquo;Book in Ocala&rdquo; or &ldquo;Book in Palatka&rdquo; button above to see that location&rsquo;s real-time availability, or call 352-559-8034.'),
    ('Is there one phone number for both locations?', 'Yes. Call 352-559-8034 for either location, or email info@gloocala.com.'),
]
if 'id="faq"' not in s:
    s = s.replace('  <!-- ===================== MEDICAL / COMPLIANCE DISCLAIMER', faq_html('Location FAQs', HUB_FAQ, 'faq', '#F3F0EA').lstrip('\n') + '\n  <!-- ===================== MEDICAL / COMPLIANCE DISCLAIMER', 1)
s = add_ld(s, {'@context': 'https://schema.org', '@graph': [
    {'@type': 'CollectionPage', '@id': url + '#page', 'url': url, 'name': 'Med Spa Locations in Ocala & Palatka, FL', 'isPartOf': {'@id': SITE + '/#website'},
     'about': {'@id': BUSINESS_ID}, 'mainEntity': {'@id': url + '#list'}},
    {'@type': 'ItemList', '@id': url + '#list', 'name': 'GLO Aesthetics + Wellness Lounge locations', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'item': {'@type': ['MedicalBusiness', 'HealthAndBeautyBusiness'], '@id': SITE + '/locations/ocala#location', 'name': 'GLO Aesthetics + Wellness Lounge — Ocala', 'url': SITE + '/locations/ocala', 'telephone': '+13525598034', 'address': ADDR['ocala'], 'geo': GEO_OCALA, 'hasMap': GBP_OCALA}},
        {'@type': 'ListItem', 'position': 2, 'item': {'@type': ['MedicalBusiness', 'HealthAndBeautyBusiness'], '@id': SITE + '/locations/palatka#location', 'name': 'GLO Aesthetics + Wellness Lounge — Palatka', 'url': SITE + '/locations/palatka', 'telephone': '+13525598034', 'address': ADDR['palatka']}}]},
    {k: v for k, v in faq_ld(HUB_FAQ, url).items() if k != '@context'}]}, 'glo-hub-ld')
wr(f, s)

# ------------------------------------------------------------------ memberships + financing (drafts: noindex until GLO confirms terms)
DRAFT = 'noindex, follow'
s = rd('membership-programs.html')
s = set_head(s, 'Med Spa Memberships in Ocala, FL | GLO Aesthetics',
             'Med spa memberships in Ocala and Palatka, FL: a monthly skin or wellness treatment, member pricing and priority booking at GLO. Compare plans today.',
             IMG.format('2940c9f3-89bf-4257-a861-f02aa9a1279d'), DRAFT if '[TBD' in s else 'index, follow, max-image-preview:large')
s = re.sub(r'(<h1 class="mem-h1" style="[^"]*">)Aesthetic care, on your terms\.(</h1>)',
           r'\1Med Spa Memberships in <span style="font-style:italic;color:#B8894F;">Ocala</span>, FL\2', s)
wr('membership-programs.html', s)

s = rd('financing.html')
s = set_head(s, 'Med Spa Financing in Ocala, FL | Cherry | GLO Aesthetics',
             'Pay over time for treatments at GLO Aesthetics in Ocala and Palatka, FL with Cherry financing. Check eligibility in minutes, no hit to your credit.',
             SITE + '/assets/financing-cherry-tablet.png', DRAFT if '[TBD' in s else 'index, follow, max-image-preview:large')
s = re.sub(r'(<h1 class="fin-h1" style=")([^"]*)(">)Beautiful results, made more accessible\.(</h1>)',
           lambda m: m.group(1) + m.group(2).replace('font-style:italic;', '') + m.group(3) + 'Med Spa Financing in <span style="font-style:italic;color:#B8894F;">Ocala</span>, FL' + m.group(4), s)
wr('financing.html', s)

# ------------------------------------------------------------------ Treatments pillar: Updated line
s = rd('treatments/index.html')
if 'glo-updated' not in s:
    s = re.sub(r'(<a href="#wellness" class="btn-outline"[^>]*>Wellness</a>\n      </div>)', lambda m: m.group(1) + '\n      ' + updated_line(), s, count=1)
    s = re.sub(r'(</h1>\s*<p) style=', r'\1 class="glo-answer" style=', s, count=1)
    wr('treatments/index.html', s)
print('done')
