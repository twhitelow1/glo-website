"""Build the three category pages (/injectables, /skin-services, /wellness) from content below.

Treatment cards are copied from the Treatments pillar so both pages always show the same facts.
Run from the repo root:  python3 scripts/build_categories.py
"""
import re, sys
sys.path.insert(0, 'scripts')
from glo_page import *  # noqa

PILLAR = open('treatments/index.html').read()


def card(slug):
    m = re.search(r'(        <a href="/treatments/%s" class="card-hover".*?\n        </a>)' % re.escape(slug), PILLAR, re.S)
    return m.group(1)


def card_name(slug):
    return plain(re.search(r'<h3[^>]*>(.*?)</h3>', card(slug)).group(1))


def group(gid, h2, intro, slugs, bg):
    cards = '\n'.join(card(s) for s in slugs)
    return f'''
  <!-- ===================== {gid.upper()} ===================== -->
  <div id="{gid}" style="width:100%;background:{bg};scroll-margin-top:130px;">
    <div class="glo-container" style="max-width:1320px;margin:0 auto;padding:90px 48px;">
      <div style="max-width:760px;margin-bottom:36px;">
        <h2 class="glo-h2" style="font-size:40px;line-height:1.2;color:#221F1B;margin-bottom:12px;">{h2}</h2>
        <p style="font-size:17px;line-height:1.7;color:#5C574E;margin:0;">{intro}</p>
      </div>
      <div class="tx-grid" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;">
{cards}
      </div>
    </div>
  </div>
'''


def compare(h2, intro, cols, rows, caption, bg='#F3F0EA'):
    th = 'style="text-align:left;padding:16px 18px;font-size:12px;letter-spacing:0.16em;text-transform:uppercase;color:#8A8377;font-weight:600;"'
    head = ''.join(f'<th scope="col" {th}>{c}</th>' for c in [''] + cols)
    body = ''.join('<tr><th scope="row" style="text-align:left;padding:16px 18px;font-weight:600;color:#221F1B;border-top:1px solid #E6E1D6;white-space:nowrap;">'
                   + r[0] + '</th>' + ''.join(f'<td data-label="{plain(col)}" style="padding:16px 18px;border-top:1px solid #E6E1D6;color:#5C574E;">{c}</td>' for col, c in zip(cols, r[1:])) + '</tr>'
                   for r in rows)
    return f'''
  <!-- ===================== COMPARE ===================== -->
  <div id="compare" style="width:100%;background:{bg};">
    <div class="glo-container" style="max-width:1100px;margin:0 auto;padding:90px 48px;">
      <div style="max-width:720px;margin:0 auto 36px;text-align:center;">
        <h2 class="glo-h2" style="font-size:38px;line-height:1.2;color:#221F1B;margin-bottom:14px;">{h2}</h2>
        <p style="font-size:17px;line-height:1.7;color:#5C574E;margin:0;">{intro}</p>
      </div>
      <div class="glo-table-wrap" style="overflow-x:auto;background:#FFFFFF;border:1px solid #E6E1D6;border-radius:8px;">
        <table class="glo-stack" style="width:100%;border-collapse:collapse;font-size:15.5px;line-height:1.5;min-width:640px;">
          <caption style="position:absolute;left:-9999px;">{caption}</caption>
          <thead><tr>{head}</tr></thead>
          <tbody>{body}</tbody>
        </table>
      </div>
    </div>
  </div>
'''


def related(h2, links):
    a = ''.join(f'<a href="{p}" class="btn-outline" style="background:transparent;border:1px solid #6B5435;color:#221F1B;padding:13px 28px;border-radius:2px;font-size:15px;letter-spacing:0.03em;">{n}</a>' for n, p in links)
    return f'''
  <!-- ===================== RELATED ===================== -->
  <div style="width:100%;background:#F3F0EA;">
    <div class="glo-container" style="max-width:1100px;margin:0 auto;padding:70px 48px 80px;text-align:center;">
      <h2 class="glo-h2" style="font-size:30px;color:#221F1B;margin-bottom:28px;">{h2}</h2>
      <div class="glo-related-links" style="display:flex;justify-content:center;gap:16px;flex-wrap:wrap;">{a}</div>
    </div>
  </div>
'''


CATS = [
 dict(
  file='injectables.html', path='/injectables', name='Injectables', img=IMG.format('0f788a80-530e-483a-ba1b-60820956532a'),
  alt='Woman in her forties with smooth, relaxed skin and natural expression',
  title='Injectables in Ocala, FL | Xeomin, Daxxify & Filler | GLO',
  meta='Injectables in Ocala, FL: Xeomin and Daxxify for frown lines and crow’s feet, plus lip and dermal filler and liquid rhinoplasty. Book a consultation.',
  eyebrow='INJECTABLES',
  h1='Injectables in <span style="font-style:italic;color:#B8894F;">Ocala</span>, FL',
  answer='Injectables are quick, in-office treatments that soften expression lines or restore lost volume without surgery. At GLO, a licensed provider uses Xeomin or Daxxify for frown lines and crow&rsquo;s feet, and hyaluronic acid filler for lips, cheeks and profile balancing. Most visits take under an hour, with little to no downtime.',
  buttons=f'<a href="https://gloocala.janeapp.com/locations/ocala-location-glo-aesthetics-wellness-lounge/book#/discipline/14/treatment/114" target="_blank" rel="noopener" {BTN}>Book an Aesthetics Consultation</a><a href="#compare" {BTN_OUT}>Tox vs. Filler</a>',
  groups=[
   ('wrinkle-relaxers', 'Which injectable smooths wrinkles?',
    'Wrinkle relaxers (neuromodulators) such as Xeomin and Daxxify soften lines that form when you move &mdash; the &ldquo;11s&rdquo; between your brows, forehead lines and crow&rsquo;s feet. You still look like you, just more rested.',
    ['xeomin', 'daxxify']),
   ('filler', 'Which injectable restores volume or reshapes my features?',
    'Hyaluronic acid filler adds back volume and shape where it has faded &mdash; lips, cheeks, smile lines &mdash; and can smooth a nasal bump without surgery. Because it&rsquo;s hyaluronic acid, it can also be dissolved if it ever needs correcting.',
    ['dermal-filler', 'liquid-rhinoplasty', 'dissolve-ha-dermal-filler']),
  ],
  compare=('Wrinkle relaxer or filler: what&rsquo;s the difference?',
   'Wrinkle relaxers calm the muscles that crease your skin; filler adds volume under it. Many people use both. Here&rsquo;s how they compare.',
   ['Xeomin', 'Daxxify', 'Dermal filler'],
   [['What it does', 'Relaxes the muscles behind expression lines', 'Relaxes the muscles behind expression lines', 'Adds volume and shape with hyaluronic acid'],
    ['Best for', 'Frown lines, forehead lines, crow&rsquo;s feet', 'Expression lines, longer between visits', 'Lips, cheeks, smile lines, under-eye hollows'],
    ['Visit length', '10&ndash;15 min', '10&ndash;15 min', '30&ndash;45 min'],
    ['Results last', 'Up to 3 months', 'Up to 6&ndash;9 months', '6&ndash;18 months'],
    ['Downtime', 'Minimal', 'Minimal', 'Minimal; possible swelling or bruising']],
   'Comparison of Xeomin, Daxxify and dermal filler'),
  faqs=[
   ('What&rsquo;s the difference between tox and filler?', 'Tox (a neuromodulator such as Xeomin or Daxxify) relaxes the muscles that cause lines when you move. Filler is hyaluronic acid that adds volume and shape, for example to lips or cheeks. Tox softens movement lines; filler restores what time has taken away. Many plans use both.'),
   ('What&rsquo;s the difference between Xeomin and Daxxify?', 'Both soften expression lines. Xeomin contains only the active ingredient and typically lasts up to 3 months. Daxxify is peptide-formulated and can last 6&ndash;9 months for many people, so you visit less often. Your provider will help you choose based on your goals and budget.'),
   ('How long do injectables last?', 'It depends on the product: Xeomin up to about 3 months, Daxxify up to 6&ndash;9 months, and hyaluronic acid filler about 6&ndash;18 months depending on the area. Results vary from person to person.'),
   ('Do injections hurt?', 'Most people feel a quick pinch. The needles are very fine, wrinkle-relaxer visits take about 15 minutes, and most fillers contain lidocaine to keep you comfortable. Topical numbing is available if you&rsquo;d like it.'),
   ('Is there downtime after injectables?', 'Usually very little. You can return to work the same day. Mild swelling or bruising at injection sites can happen, especially with filler, and typically fades within a few days.'),
   ('Can filler be reversed?', 'Yes. Hyaluronic acid filler can be dissolved with hyaluronidase if you&rsquo;re unhappy with the result or it needs correcting. GLO offers filler dissolving, including for filler placed elsewhere.'),
  ],
  related_h2='Explore more at GLO',
  related=[('All Treatments', '/treatments'), ('Skin Services', '/skin-services'), ('Wellness', '/wellness'), ('Memberships', '/membership-programs')],
  cta=('Not sure which injectable is right for you?', 'Tell us what you&rsquo;d like to soften or restore. We&rsquo;ll look at your features, explain your options and costs, and you decide &mdash; no pressure.'),
 ),
 dict(
  file='skin-services.html', path='/skin-services', name='Skin Services', img=IMG.format('175e4678-0ae9-4464-8168-4d4a5e763ed7'),
  alt='Woman in her sixties with radiant skin and silver hair smiling in morning light',
  title='Skin Services in Ocala, FL | Laser, RF & Facials | GLO',
  meta='Skin services in Ocala, FL: CO2 laser resurfacing, RF skin tightening, laser hair removal, facials, chemical peels and microneedling. Book a consultation.',
  eyebrow='SKIN SERVICES',
  h1='Skin Services in <span style="font-style:italic;color:#B8894F;">Ocala</span>, FL',
  answer='GLO&rsquo;s skin services treat sun spots, fine lines, acne scars, loose skin, dullness and unwanted hair. A licensed provider matches you to the right technology &mdash; Tetra CO2 or Motus laser, Everesse radiofrequency, SkinPen microneedling, custom facials or chemical peels &mdash; based on your skin, your goals and how much downtime you can take.',
  buttons=f'<a href="/#book" {BTN}>Book a Skin Consultation</a><a href="#compare" {BTN_OUT}>Compare Treatments</a>',
  groups=[
   ('laser', 'Which laser treatment is right for my skin?',
    'Lasers use light energy to resurface or refresh skin and to remove hair. Tetra CO2 resurfacing treats deeper lines, scars and sun damage; CoolPeel and the Motus laser facial refresh tone and texture with far less downtime.',
    ['laser-skin-revitalization', 'coolpeel', 'motus-laser-facial', 'laser-hair-removal']),
   ('radiofrequency', 'What does radiofrequency skin tightening do?',
    'Radiofrequency (RF) gently heats the deeper layers of skin to prompt new collagen, so loose or crepey skin looks firmer over the following months. Everesse on its own isn&rsquo;t a laser and has no downtime; Radiant Lift adds a CoolPeel CO2 laser to refresh tone and texture too.',
    ['skin-tightening', 'radiant-lift']),
   ('facials', 'Which facial, peel or microneedling treatment should I choose?',
    'Custom facials and chemical peels clear congestion, even tone and restore glow; SkinPen microneedling builds collagen to improve texture, pores and acne scars. Mini Facials are a quick monthly refresh.',
    ['custom-facials-peels', 'mini-facials', 'microneedling', 'daxxify-facial-microneedling']),
  ],
  compare=('Laser, radiofrequency or microneedling: how do they compare?',
   'All three build healthier, firmer-looking skin; they differ in how they work and how much downtime they need.',
   ['CO2 laser (Tetra CO2)', 'Radiofrequency (Everesse)', 'SkinPen microneedling'],
   [['How it works', 'Laser energy resurfaces the outer layers and triggers collagen', 'Heat in the deeper layers tightens and builds collagen', 'Fine needles create micro-channels that trigger collagen'],
    ['Best for', 'Deeper lines, acne scars, sun damage', 'Loose or crepey skin on the face, jaw and neck', 'Texture, pores and acne scars, all skin tones'],
    ['Downtime', 'About 5&ndash;7 days', 'None', 'About 24&ndash;72 hours of redness'],
    ['Typical plan', '1&ndash;3 sessions, 4&ndash;6 weeks apart', 'Often 2 sessions about 6 months apart', '3 or more sessions about 4 weeks apart'],
    ['Starting price', 'From $800 per session', 'From $700 per session', 'From $250 per session']],
   'Comparison of CO2 laser, radiofrequency and microneedling'),
  faqs=[
   ('Which skin treatment has the least downtime?', 'Mini Facials, custom facials, the Motus laser facial, Everesse radiofrequency and laser hair removal typically have little to no downtime. CoolPeel and Radiant Lift (Everesse + CoolPeel) usually mean 24&ndash;72 hours of redness; Tetra CO2 resurfacing needs the most recovery, about 5&ndash;7 days.'),
   ('Is Everesse a laser?', 'No. Everesse uses radiofrequency energy, not laser light. It heats the deeper layers of skin to tighten and build collagen, with no downtime, which makes it a good option for loose or crepey skin.'),
   ('What&rsquo;s the difference between Tetra CO2 and CoolPeel?', 'Both use CO2 laser technology on the same platform. Tetra CO2 resurfacing goes deeper for lines, scars and sun damage, with about a week of downtime. CoolPeel is a lighter, faster treatment with 24&ndash;72 hours of redness, usually done as a series.'),
   ('Are laser treatments safe for darker skin?', 'Many are, with the right technology and settings. Your provider assesses your skin type at your consultation and adjusts settings or recommends an alternative. Microneedling works without heat or light, so it suits most skin types and tones.'),
   ('How many sessions will I need?', 'It depends on the treatment and your goals. Microneedling and CoolPeel are usually done as a series of 3 or more, laser hair removal as 6&ndash;8 sessions, and Everesse often as 2 sessions about 6 months apart. Your provider will build your plan with you.'),
   ('Can I combine skin treatments?', 'Often, yes. Many clients pair a resurfacing or microneedling series with monthly facials, or add radiofrequency tightening. Your provider will space treatments safely and tell you what works well together for your skin.'),
  ],
  related_h2='Explore more at GLO',
  related=[('All Treatments', '/treatments'), ('Injectables', '/injectables'), ('Wellness', '/wellness'), ('Memberships', '/membership-programs')],
  cta=('Not sure which skin treatment fits?', 'Tell us what you&rsquo;d like to change about your skin. We&rsquo;ll look closely, explain your options and downtime, and help you choose &mdash; no pressure.'),
 ),
 dict(
  file='wellness.html', path='/wellness', name='Wellness', img=IMG.format('f2efb89a-4a81-4e8a-ac4e-4c29d2e70aba'),
  alt='Man in his late forties looking energized and healthy outdoors',
  title='Medical Wellness in Ocala, FL | Weight Loss & HRT | GLO',
  meta='Medical wellness in Ocala, FL: medical weight loss with GLP-1 options, hormone replacement therapy, IV hydration and peptide therapy. Book a consultation.',
  eyebrow='MEDICAL WELLNESS',
  h1='Medical Wellness in <span style="font-style:italic;color:#B8894F;">Ocala</span>, FL',
  answer='GLO&rsquo;s medical wellness programs help with stubborn weight, hormone changes, low energy and slow recovery. Each starts with a clinical evaluation and, where needed, lab work; then a licensed provider builds a plan &mdash; medical weight loss, hormone replacement therapy, IV hydration or peptide therapy &mdash; and adjusts it with you over time.',
  buttons=f'<a href="/#book" {BTN}>Book a Wellness Consultation</a><a href="#compare" {BTN_OUT}>Compare Programs</a>',
  groups=[
   ('weight-hormones', 'Can a medical program help with weight or hormones?',
    'Yes &mdash; when there&rsquo;s a medical reason behind it. Medical weight loss and hormone replacement therapy start with labs, so your plan treats what&rsquo;s actually going on, with monitoring and adjustments along the way.',
    ['functional-weight-loss', 'hormone-replacement-therapy']),
   ('recovery', 'What helps with energy and recovery?',
    'IV hydration replenishes fluids, vitamins and minerals in a single visit. Peptide therapy is an ongoing, provider-directed protocol to support recovery, sleep and vitality.',
    ['iv-hydration', 'peptide-therapy']),
  ],
  compare=('Which wellness program fits my goals?',
   'Each program serves a different goal. Your provider will confirm what&rsquo;s right for you after your evaluation.',
   ['Medical weight loss', 'Hormone therapy', 'IV hydration', 'Peptide therapy'],
   [['Best for', 'Weight that won&rsquo;t budge with diet and exercise alone', 'Hot flashes, low energy, mood or libido changes', 'Feeling run-down, dehydrated or depleted', 'Recovery, sleep and vitality'],
    ['Starts with', 'Metabolic labs and evaluation', 'Lab work and symptom review', 'Health screening', 'Goals and relevant labs'],
    ['How it&rsquo;s given', 'Nutrition plan, monitoring and, when appropriate, GLP-1 medication', 'Injectable, topical or pellet protocol', 'A customized IV drip', 'A personalized protocol'],
    ['Timeline', 'Ongoing program', 'Full effects over 3&ndash;6 months', '30&ndash;60 minute visit', 'Typically weeks; ongoing']],
   'Comparison of GLO wellness programs'),
  faqs=[
   ('Do I need lab work before starting a wellness program?', 'For medical weight loss, hormone therapy and peptide therapy, yes. Labs show what&rsquo;s actually happening so your provider can prescribe only what&rsquo;s appropriate and monitor you safely. IV hydration starts with a health screening.'),
   ('Does GLO prescribe GLP-1 medications like semaglutide or tirzepatide?', 'When appropriate, yes. GLO&rsquo;s medical weight loss program can include GLP-1 medications alongside metabolic labs, personalized nutrition and ongoing monitoring. Your provider decides whether medication fits after your evaluation.'),
   ('Is hormone replacement therapy for men and women?', 'Yes. GLO offers testosterone replacement for men, bioidentical hormone therapy for women and thyroid support, each built around your labs and symptoms, with follow-up labs to adjust your plan.'),
   ('Are compounded or peptide therapies FDA-approved?', 'Not all are. Some compounded and peptide therapies haven&rsquo;t been evaluated by the FDA for every use. Your provider will explain what&rsquo;s known about any therapy they recommend and prescribe it only when it&rsquo;s appropriate for you.'),
   ('How long does an IV hydration session take?', 'Most IV hydration sessions take 30 to 60 minutes, depending on the blend and infusion rate. You can relax in the lounge and return to your day afterward.'),
   ('Do I need a consultation first?', 'Yes. Every wellness program begins with a clinical evaluation so your plan is safe and personal. Hormone therapy is coming soon; call us to join the list.'),
  ],
  related_h2='Explore more at GLO',
  related=[('All Treatments', '/treatments'), ('Injectables', '/injectables'), ('Skin Services', '/skin-services'), ('Memberships', '/membership-programs')],
  cta=('Ready to feel like yourself again?', 'Tell us what&rsquo;s been off &mdash; energy, weight, sleep or mood. We&rsquo;ll listen, check what&rsquo;s going on and build a plan with you.'),
 ),
]

for c in CATS:
    crumbs = [('Home', '/'), ('Treatments', '/treatments'), (c['name'], c['path'])]
    body = split_hero(crumbs, c['eyebrow'], c['h1'], c['answer'], c['buttons'], c['img'], c['alt'])
    bgs = ['#FAF9F6', '#F3F0EA', '#FAF9F6']
    for i, (gid, h2, intro, slugs) in enumerate(c['groups']):
        body += group(gid, h2, intro, slugs, bgs[i % 2])
    body += compare(*c['compare'], bg='#F3F0EA' if len(c['groups']) % 2 == 0 else '#FAF9F6')
    body += faq_html(f'{c["name"]} FAQs', c['faqs'])
    body += related(c['related_h2'], c['related'])
    body += cta(*c['cta']) + '\n'
    slugs = [s for g in c['groups'] for s in g[3]]
    url = SITE + c['path']
    graph = [
        {'@type': ['CollectionPage', 'MedicalWebPage'], '@id': url + '#page', 'url': url, 'name': plain(c['title']),
         'description': c['meta'], 'inLanguage': 'en-US', 'dateModified': UPDATED[0],
         'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': BUSINESS_ID}, 'publisher': {'@id': BUSINESS_ID},
         'primaryImageOfPage': c['img'], 'mainEntity': {'@id': url + '#list'}, 'breadcrumb': {'@id': url + '#breadcrumb'}},
        {'@type': 'ItemList', '@id': url + '#list', 'name': f'{c["name"]} at GLO Aesthetics + Wellness Lounge',
         'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': card_name(s), 'url': f'{SITE}/treatments/{s}'} for i, s in enumerate(slugs)]},
        dict(breadcrumbs(crumbs), **{'@id': url + '#breadcrumb'}),
        faq_schema(c['faqs']),
    ]
    write_page(c['file'], c['title'], plain(c['meta']), c['path'], c['img'], graph, body)
    print('built', c['file'], len(plain(c['title'])), len(plain(c['meta'])), len(plain(c['answer']).split()))
