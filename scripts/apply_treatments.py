"""Apply content/treatments/<slug>.json to treatments/<slug>.html.

Brings every treatment page to the site SEO/AEO standard: keyword H1, 40-60 word direct answer, "Updated" line,
question-led H2s with a direct answer under each, "How it works" and "Is it right for me?" sections,
6+ FAQs as H3s with matching FAQPage schema, related links, and a MedicalWebPage + MedicalProcedure/Therapy graph.
Idempotent: pages carry a marker after the first run and are skipped unless --force is given on a fresh checkout.
Run from the repo root:  python3 scripts/apply_treatments.py
"""
import glob, html, json, re, sys
sys.path.insert(0, 'scripts')
from glo_page import SITE, UPDATED, BUSINESS_ID, esc, plain, updated_line, ld  # noqa

MARK = '<!-- glo-seo-v1 -->'
CAT = {'/injectables': 'Injectables', '/skin-services': 'Skin Services', '/wellness': 'Wellness'}


def sub1(pattern, repl, s, flags=re.S):
    new, n = re.subn(pattern, repl, s, count=1, flags=flags)
    assert n == 1, pattern[:80]
    return new


def fill_seq(s, pattern, values, render):
    """Replace successive matches of pattern with render(match, value), in order."""
    out, pos = [], 0
    for m, v in zip(re.finditer(pattern, s), values):
        out += [s[pos:m.start()], render(m, v)]
        pos = m.end()
    return ''.join(out) + s[pos:]


def build_iv(d):
    """IV Hydration used an older layout; rebuild it on the standard treatment template (Xeomin)."""
    iv = open('treatments/iv-hydration.html').read()
    s = open('treatments/xeomin.html').read()
    assert MARK not in s, 'build IV from the pre-migration Xeomin page'
    old_faqs = re.findall(r'<div><h3[^>]*>(.*?)</h3><p[^>]*>(.*?)</p></div>', iv.split('<!-- ===================== FAQ', 1)[1])
    img = re.search(r"background-image:url\('([^']+)'\)", iv.split('glo-split-media', 1)[1]).group(1)
    s = s.replace('Xeomin', '§X§')
    # hero
    s = sub1(r'<nav class="glo-hero-crumbs".*?</nav>', '<nav class="glo-hero-crumbs" aria-label="Breadcrumb"><a href="/">Home</a> &nbsp;/&nbsp;\n    <a href="/treatments">Treatments</a> &nbsp;/&nbsp;\n    <a href="/wellness">Wellness</a> &nbsp;/&nbsp;\n    <span aria-current="page">IV Hydration Therapy</span></nav>', s)
    s = sub1(r'(letter-spacing:0.28em;color:#B8894F;font-weight:600;">)INJECTIONS(</span>)', r'\1IV THERAPY\2', s)
    s = re.sub(r'https://gloocala\.janeapp\.com/[^"]*', '/#book', s)
    s = s.replace('target="_blank" rel="noopener" ', '')
    s = sub1(r'(<div class="glo-split-media" role="img" aria-label=")[^"]*(" style="background-image:url\(\')[^\']+', r'\1IV hydration therapy lounge at GLO Aesthetics + Wellness Lounge\2' + img, s)
    # stats
    s = fill_seq(s, r'(<span style="font-family:\'Playfair Display\',Georgia,serif;font-size:28px;color:#B8894F;">)[^<]*(</span>\s*<span[^>]*>)[^<]*(</span>)',
                 d['stats'], lambda m, v: m.group(1) + esc(v[0]) + m.group(2) + esc(v[1]) + m.group(3))
    # drop the opt-in offer and pricing blocks
    s = sub1(r'  <!-- ===================== OPT-IN OFFER.*?(?=  <!-- ===================== WHAT IT TREATS)', '', s)
    s = sub1(r'  <!-- ===================== PRICING.*?(?=  <!-- ===================== FAQ)', '', s)
    s = s.replace('Book an Aesthetics Consultation', 'Book Your IV Hydration Session')
    # what it treats cards
    cards = re.findall(r'<h3 style="font-size:18px;color:#221F1B;margin-bottom:8px;">.*?</h3>\s*<p[^>]*>.*?</p>', s, re.S)
    for old, (t, desc) in zip(cards, d['treats']):
        new = re.sub(r'(<h3[^>]*>).*?(</h3>\s*<p[^>]*>).*?(</p>)', lambda m: m.group(1) + esc(t) + m.group(2) + esc(desc) + m.group(3), old, flags=re.S)
        s = s.replace(old, new, 1)
    # expect steps
    s = fill_seq(s, r'(<div style="font-size:16.5px;font-weight:500;color:#221F1B;margin-bottom:6px;">)[^<]*(</div>\s*<div[^>]*>)[^<]*(</div>)',
                 d['expect_steps'], lambda m, v: m.group(1) + esc(v[0]) + m.group(2) + esc(v[1]) + m.group(3))
    # FAQ rows from the old page
    rows = ''.join(f'''
      <div class="faq-row" style="padding:22px 0;">
        <div style="font-size:18px;font-weight:500;color:#221F1B;margin-bottom:8px;">{q}</div>
        <div style="font-size:16px;line-height:1.7;color:#5C574E;font-weight:300;">{a}</div>
      </div>''' for q, a in old_faqs)
    s = sub1(r'(Common Questions</h2>).*?(\n    </div>\n  </div>\n\n  <!-- ===================== RELATED)', lambda m: m.group(1) + rows + m.group(2), s)
    # related links
    links = []
    for slug in d['related']:
        name = json.load(open(f'content/treatments/{slug}.json'))['keyword']
        links.append(f'<a href="/treatments/{slug}" class="btn-outline" style="background:transparent;border:1px solid #6B5435;color:#221F1B;padding:13px 28px;border-radius:2px;font-size:15px;letter-spacing:0.03em;">{esc(name)}</a>')
    s = sub1(r'(<div class="glo-related-links"[^>]*>).*?(\n      </div>)', lambda m: m.group(1) + '\n        ' + '\n        '.join(links) + m.group(2), s)
    # head: breadcrumbs, schema (rebuilt in apply), titles replaced in apply
    s = s.replace('§X§', 'IV Hydration Therapy')
    s = s.replace('/treatments/xeomin', '/treatments/iv-hydration').replace('"/injectables"', '"/wellness"')
    s = re.sub(r'"name": "Injectables",\s*"item": "https://gloocala.com/injectables"', '"name": "Wellness",\n      "item": "https://gloocala.com/wellness"', s)
    s = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "MedicalProcedure".*?</script>\n',
               ld({'@context': 'https://schema.org', '@type': 'MedicalTherapy', 'name': 'IV Hydration Therapy',
                   'description': 'Customized intravenous hydration with vitamins, minerals and electrolytes to support energy, recovery and wellness, offered in Ocala, FL.'}), s, count=1, flags=re.S)
    s = re.sub(r'og:image" content="[^"]*"', f'og:image" content="{img}"', s)
    s = re.sub(r'twitter:image" content="[^"]*"', f'twitter:image" content="{img}"', s)
    open('treatments/iv-hydration.html', 'w').write(s)


def faq_row(q, a, last=False):
    border = 'padding:22px 0;border-bottom:1px solid #E6E1D6;' if last else 'padding:22px 0;'
    return (f'\n      <div class="faq-row" style="{border}">\n'
            f'        <h3 style="font-size:20px;font-weight:500;color:#221F1B;margin:0 0 8px;line-height:1.35;">{q}</h3>\n'
            f'        <p style="font-size:16px;line-height:1.7;color:#5C574E;font-weight:300;margin:0;">{a}</p>\n      </div>')


def fit_section(d):
    li = lambda items, mark: ''.join(
        f'<li style="display:flex;gap:12px;align-items:flex-start;padding:10px 0;border-top:1px solid #E6E1D6;font-size:16px;line-height:1.6;color:#3F3A33;">'
        f'<span aria-hidden="true" style="flex:none;color:#B8894F;font-weight:600;">{mark}</span><span>{esc(t)}</span></li>' for t in items)
    return f'''
  <!-- ===================== HOW IT WORKS + IS IT RIGHT FOR ME ===================== -->
  <div id="how-it-works" style="width:100%;background:#FAF9F6;">
    <div class="glo-container" style="max-width:1140px;margin:0 auto;padding:90px 48px 40px;">
      <div style="max-width:760px;">
        <h2 class="glo-h2" style="font-size:38px;line-height:1.2;color:#221F1B;margin-bottom:16px;">{esc(d["how_h2"])}</h2>
        <p style="font-size:17px;line-height:1.8;color:#5C574E;margin:0;">{esc(d["how"])}</p>
      </div>
    </div>
    <div id="right-for-me" class="glo-container" style="max-width:1140px;margin:0 auto;padding:40px 48px 90px;">
      <h2 class="glo-h2" style="font-size:38px;line-height:1.2;color:#221F1B;margin-bottom:28px;">{esc(d["fit_h2"])}</h2>
      <div class="glo-row" style="display:flex;gap:28px;align-items:stretch;">
        <div class="glo-flex-half" style="flex:1 1 50%;background:#FFFFFF;border:1px solid #E6E1D6;border-radius:8px;padding:28px 28px 18px;">
          <h3 style="font-size:21px;color:#221F1B;margin:0 0 12px;">A good fit if&hellip;</h3>
          <ul style="list-style:none;margin:0;padding:0;">{li(d["good_fit"], "&#10003;")}</ul>
        </div>
        <div class="glo-flex-half" style="flex:1 1 50%;background:#F3F0EA;border:1px solid #E6E1D6;border-radius:8px;padding:28px 28px 18px;">
          <h3 style="font-size:21px;color:#221F1B;margin:0 0 12px;">Talk to us first if&hellip;</h3>
          <ul style="list-style:none;margin:0;padding:0;">{li(d["not_fit"], "&ndash;")}</ul>
        </div>
      </div>
    </div>
  </div>
'''


def apply(path, d):
    s = open(path).read()
    if MARK in s:
        print('skip (already applied)', path)
        return
    slug = d['slug']
    url = f'{SITE}/treatments/{slug}'
    title, meta = d['title'], d['meta']
    assert len(title) <= 60 and 120 <= len(meta) <= 160, (slug, len(title), len(meta))

    # ---- head: title, description, OG/Twitter
    s = sub1(r'<title>.*?</title>', f'<title>{esc(title)}</title>', s)
    s = sub1(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(meta)}">', s)
    s = sub1(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="index, follow, max-image-preview:large">', s)
    for k in ('og:title', 'twitter:title'):
        s = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % k, lambda m: m.group(1) + esc(title), s)
    for k in ('og:description', 'twitter:description'):
        s = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % k, lambda m: m.group(1) + esc(meta), s)
    hero_img = re.search(r"glo-split-media[^>]*background-image:url\('([^']+)'\)", s).group(1)
    s = re.sub(r'(<meta (?:property|name)="(?:og|twitter):image" content=")[^"]*', lambda m: m.group(1) + hero_img, s)

    # ---- breadcrumb: parent category
    parent = re.search(r'<a href="(/injectables|/skin-services|/wellness)">', s.split('glo-hero-crumbs', 2)[2]).group(1)

    # ---- hero: H1, direct answer, updated line, secondary button to parent category
    kw = esc(d['keyword'])
    s = sub1(r'<h1 class="[^"]*" style="[^"]*">.*?</h1>',
             f'<h1 class="glo-hero-h1" style="font-size:54px;line-height:1.12;font-weight:400;color:#221F1B;">{kw} in <span style="font-style:italic;color:#B8894F;">Ocala</span>, FL</h1>', s)
    s = sub1(r'(</h1>\s*<p) style="[^"]*">.*?</p>', lambda m: m.group(1) + f' class="glo-answer" style="margin:24px 0 0;font-size:18px;line-height:1.8;color:#5C574E;font-weight:400;max-width:560px;">\n          {esc(d["answer"])}\n      </p>', s)
    s = re.sub(r'href="/#tx-[a-z]+"', f'href="{parent}"', s)
    s = s.replace('>See Related Treatments</a>', f'>All {CAT[parent]}</a>')
    s = sub1(r'(<div class="glo-hero-cta".*?</div>)', lambda m: m.group(1) + '\n      ' + updated_line(), s)

    # ---- what it treats
    s = sub1(r'(<h2 class="glo-h2"[^>]*>)What [^<]* Treats(</h2>\s*<p[^>]*>).*?(</p>)', lambda m: m.group(1) + esc(d['treats_h2']) + m.group(2) + esc(d['treats_intro']) + m.group(3), s)

    # ---- how it works + right for me, before "what to expect"
    s = sub1(r'(  <!-- ===================== WHAT TO EXPECT)', lambda m: fit_section(d) + '\n' + m.group(1), s)
    s = sub1(r'(<h2 class="glo-h2"[^>]*>)What to Expect(</h2>)', lambda m: m.group(1) + esc(d['expect_h2']) + m.group(2)
             + f'\n        <p style="margin-top:14px;font-size:17px;line-height:1.7;color:#5C574E;font-weight:300;">{esc(d["expect_intro"])}</p>', s)

    # ---- pricing H2 + offer facts
    price = None
    if d.get('cost_h2'):
        s = sub1(r'(INVESTMENT</span>\s*<div[^>]*></div>\s*</div>)', lambda m: m.group(1) + f'\n      <h2 class="glo-h2" style="font-size:34px;line-height:1.2;color:#FAF9F6;margin-bottom:18px;">{esc(d["cost_h2"])}</h2>', s)
        m = re.search(r'Starting at \$([\d,]+)<span[^>]*>\s*/\s*([^<]+)</span>', s)
        price = (m.group(1).replace(',', ''), m.group(2).strip())

    # ---- FAQ: rename, add, convert to H3, rebuild schema
    faq_block = re.search(r'(<h2 class="glo-h2"[^>]*>)(Common Questions)(</h2>)(.*?)(\n    </div>\n  </div>\n\n  <!-- ===================== RELATED)', s, re.S)
    pairs = re.findall(r'<div class="faq-row"[^>]*>\s*<div[^>]*>(.*?)</div>\s*<div[^>]*>(.*?)</div>\s*</div>', faq_block.group(4), re.S)
    rename = {html.unescape(k).replace('’', "'"): v for k, v in d['faq_rename'].items()}
    faqs = []
    for q, a in pairs:
        key = html.unescape(q).replace('’', "'")
        faqs.append((esc(rename[key]) if key in rename else q, a))
    missing = set(rename) - {html.unescape(q).replace('’', "'") for q, _ in pairs}
    assert not missing, (slug, missing)
    faqs += [(esc(x['q']), esc(x['a'])) for x in d['faq_add']]
    rows = ''.join(faq_row(q, a, i == len(faqs) - 1) for i, (q, a) in enumerate(faqs))
    s = s[:faq_block.start()] + faq_block.group(1) + esc(d['faq_h2']) + faq_block.group(3) + rows + faq_block.group(5) + s[faq_block.end():]

    # ---- related: heading + de-duplicated links
    s = sub1(r'(<h2 class="glo-h2"[^>]*>)Related (?:Treatments|Injections)(</h2>)', lambda m: m.group(1) + esc(d['related_h2']) + m.group(2), s)
    rel = re.search(r'(<div class="glo-related-links"[^>]*>)(.*?)(\n      </div>)', s, re.S)
    seen, links = set(), []
    for a in re.findall(r'<a href="[^"]*"[^>]*>.*?</a>', rel.group(2), re.S):
        href = re.search(r'href="([^"]*)"', a).group(1)
        if href not in seen and href != f'/treatments/{slug}':
            seen.add(href)
            links.append(a)
    if parent not in seen:
        links.append(f'<a href="{parent}" class="btn-outline" style="background:transparent;border:1px solid #6B5435;color:#221F1B;padding:13px 28px;border-radius:2px;font-size:15px;letter-spacing:0.03em;">All {CAT[parent]}</a>')
    s = s[:rel.start()] + rel.group(1) + '\n        ' + '\n        '.join(links) + rel.group(3) + s[rel.end():]

    # ---- schema: replace the procedure + FAQ blocks with one graph; keep BreadcrumbList
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>\n?', s, re.S)
    proc = None
    for b in blocks:
        j = json.loads(b)
        if j.get('@type') in ('MedicalProcedure', 'MedicalTherapy'):
            proc = j
    sc = d['schema']
    node = {'@type': sc['type'], '@id': url + '#treatment', 'name': d['keyword'] if d['keyword'] != 'Medical Weight Loss' else 'Functional Weight Loss',
            'description': proc.get('description') if proc else plain(d['answer']), 'url': url}
    alt = sorted({proc.get('name', '') if proc else '', d['keyword']} - {node['name'], ''})
    if alt:
        node['alternateName'] = alt
    if sc.get('procedureType'):
        node['procedureType'] = sc['procedureType']
    for k in ('bodyLocation', 'howPerformed', 'preparation', 'followup'):
        if sc.get(k):
            node[k] = sc[k]
    node['provider'] = {'@id': BUSINESS_ID}
    node['areaServed'] = [{'@type': 'City', 'name': 'Ocala'}, {'@type': 'City', 'name': 'Palatka'}]
    if price:
        node['offers'] = {'@type': 'Offer', 'url': url, 'priceCurrency': 'USD', 'price': price[0],
                          'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': price[0], 'priceCurrency': 'USD',
                                                 'unitText': price[1], 'description': f'Starting at ${int(price[0]):,} per {price[1]}'},
                          'availability': 'https://schema.org/InStock', 'seller': {'@id': BUSINESS_ID}}
    page = {'@type': 'MedicalWebPage', '@id': url + '#page', 'url': url, 'name': title, 'description': meta, 'inLanguage': 'en-US',
            'dateModified': UPDATED[0], 'isPartOf': {'@id': SITE + '/#website'}, 'publisher': {'@id': BUSINESS_ID},
            'about': {'@id': url + '#treatment'}, 'mainEntity': {'@id': url + '#treatment'}, 'primaryImageOfPage': hero_img,
            'breadcrumb': {'@id': url + '#breadcrumb'}, 'speakable': {'@type': 'SpeakableSpecification', 'cssSelector': ['h1', '.glo-answer']}}
    faq = {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
        {'@type': 'Question', 'name': plain(q), 'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}} for q, a in faqs]}
    crumbs = None
    for b in blocks:
        j = json.loads(b)
        if j.get('@type') == 'BreadcrumbList':
            crumbs = j
    crumbs.pop('@context', None)
    crumbs['@id'] = url + '#breadcrumb'
    crumbs['itemListElement'] = [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Treatments', 'item': SITE + '/treatments'},
        {'@type': 'ListItem', 'position': 3, 'name': CAT[parent], 'item': SITE + parent},
        {'@type': 'ListItem', 'position': 4, 'name': d['keyword'], 'item': url}]
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', s, flags=re.S)
    graph = ld({'@context': 'https://schema.org', '@graph': [page, node, crumbs, faq]})
    s = s.replace('<link rel="preconnect"', MARK + '\n' + graph + '<link rel="preconnect"', 1)
    # visible breadcrumb label matches the schema
    s = sub1(r'(<span aria-current="page">)[^<]*(</span></nav>)', lambda m: m.group(1) + kw + m.group(2), s)
    open(path, 'w').write(s)
    print('applied', path, len(faqs), 'FAQs', 'price' if price else 'no price')


if __name__ == '__main__':
    data = {json.load(open(f))['slug']: json.load(open(f)) for f in glob.glob('content/treatments/*.json')}
    if MARK not in open('treatments/iv-hydration.html').read() and 'tv-container' in open('treatments/iv-hydration.html').read():
        build_iv(data['iv-hydration'])
    for slug, d in sorted(data.items()):
        apply(f'treatments/{slug}.html', d)
