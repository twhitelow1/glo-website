"""Build /about (about.html): who GLO is, the team (from content/team.json), values, locations and FAQs.
Run from the repo root, then run scripts/design_layer.py:  python3 scripts/build_about.py
"""
import json, sys
sys.path.insert(0, 'scripts')
from glo_page import *  # noqa

_t = json.load(open('content/team.json'))
team, founder, group = _t['team'], _t['founder'], _t['group_photo']
PATH, URL = '/about', SITE + '/about'
IMG_HERO = json.load(open('content/team.json'))['group_photo']['src']
HERO_SRC = '/assets/ocala/lounge.webp'
TITLE = 'About GLO Med Spa in Ocala, FL | Meet Our Team | GLO'
META = 'Meet the licensed team at GLO Aesthetics + Wellness Lounge in Ocala and Palatka, FL: nurse practitioners, medical estheticians and aestheticians.'

answer = ('GLO Aesthetics + Wellness Lounge is a medical aesthetics and wellness med spa in Ocala and Palatka, FL. '
          'Our team of nurse practitioners, medical estheticians and aestheticians works under the direction of a Florida-licensed '
          'Medical Director, and every plan starts with a no-pressure consultation where we listen first.')

crumbs = [('Home', '/'), ('About', '/about')]
body = split_hero(crumbs, 'ABOUT GLO', 'About GLO in <span style="font-style:italic;color:#B8894F;">Ocala</span>, FL', answer,
                  f'<a href="#team" {BTN}>Meet Our Team</a><a href="/#book" {BTN_OUT}>Book a Consultation</a>',
                  group['src'], group['alt'], 'center 30%', note='AI-generated composite of the GLO team', size=(group['width'], group['height']))
body = body.replace('<div class="glo-split-hero">', '<div class="glo-split-hero glo-split-hero--group">', 1)


def member(m):
    creds = f', {m["credentials"]}' if m['credentials'] else ''
    focus = ''.join(f'<li>{f}</li>' for f in m['focus'])
    bio = ''.join(f'<p>{p}</p>' for p in m['bio']) or f'<p>{m["name"].split()[0]} sees clients at our {" and ".join(m["locations"])} location{"s" if len(m["locations"]) > 1 else ""}. Book a consultation to meet her and talk through your goals.</p>'
    first = m["name"].split()[0]
    locs = ''.join(f'<li><a href="/locations/{l.lower()}">{l}, FL</a></li>' for l in m['locations'])
    books = ''.join(f'<a href="{url}" target="_blank" rel="noopener" class="tm-book">Book with {first} in {l} &rarr;</a>'
                    for l, url in m['book'].items())
    return f'''
        <article class="tm-card" id="{m["name"].lower().replace(" ", "-")}">
          <div class="tm-photo"><img src="{m["photo"]}" alt="{m["name"]}{creds}, {m["title"]} at GLO Aesthetics + Wellness Lounge" width="160" height="190" loading="lazy" decoding="async"></div>
          <div class="tm-body">
            <h3>{m["name"]}<span class="tm-creds">{creds}</span></h3>
            <div class="tm-title">{m["title"]}</div>
            <ul class="tm-loc" aria-label="Locations">{locs}</ul>
            {bio}
            <ul class="tm-focus" aria-label="Focus areas">{focus}</ul>
            <div class="tm-books">{books}</div>
          </div>
        </article>'''


body += f'''
<style id="glo-team-css">
  .tm-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:26px;}}
  .tm-card{{display:flex;gap:26px;background:#FFFFFF;border:1px solid #E6E1D6;border-radius:10px;padding:28px;}}
  .tm-photo{{flex:none;width:160px;height:190px;border-radius:8px;overflow:hidden;background:#EFE9E1;}}
  .tm-photo img{{width:100%;height:100%;object-fit:cover;display:block;}}
  .tm-body h3{{font-size:26px;color:#221F1B;margin:0;}}
  .tm-creds{{font-family:'Montserrat',sans-serif;font-size:14px;letter-spacing:.06em;color:#B8894F;font-weight:600;}}
  .tm-title{{font-size:15px;color:#221F1B;font-weight:500;margin-top:6px;}}
  .tm-loc{{display:flex;flex-wrap:wrap;gap:8px;list-style:none;margin:10px 0 14px;padding:0;}}
  .tm-loc a{{display:inline-flex;align-items:center;gap:6px;font-family:'Montserrat',sans-serif;font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:#FAF9F6;background:#6B5435;border-radius:999px;padding:5px 12px;}}
  .tm-loc a::before{{content:'';width:6px;height:6px;border-radius:50%;background:#E3C79B;}}
  .tm-books{{display:flex;flex-direction:column;gap:6px;}}
  .tm-body p{{font-size:15px;line-height:1.7;color:#5C574E;margin:0 0 10px;}}
  .tm-focus{{display:flex;flex-wrap:wrap;gap:8px;list-style:none;margin:12px 0 16px;padding:0;}}
  .tm-focus li{{font-size:12.5px;color:#6B5435;background:#F3F0EA;border:1px solid #E6E1D6;border-radius:999px;padding:5px 12px;}}
  .tm-book{{font-size:14.5px;color:#B8894F;font-weight:600;}}
  .gv-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;}}
  .gv-grid > div{{background:#FAF9F6;border:1px solid #E6E1D6;border-radius:8px;padding:28px 26px;}}
  .gv-grid h3{{font-size:21px;color:#221F1B;margin:0 0 8px;}}
  .gv-grid p{{font-size:15px;line-height:1.7;color:#5C574E;margin:0;}}
  .fd-wrap{{display:flex;gap:64px;align-items:center;}}
  .fd-photo{{flex:0 0 400px;margin:0;}}
  .fd-photo img{{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;object-position:center 20%;border-radius:10px;display:block;box-shadow:0 24px 48px rgba(34,31,27,.12);}}
  .fd-name{{display:block;font-family:'Playfair Display',Georgia,serif;font-style:italic;font-size:28px;color:#221F1B;}}
  .fd-role{{display:block;font-family:'Montserrat',sans-serif;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:#B8894F;font-weight:600;margin-top:4px;}}
  @media (max-width:900px){{.fd-wrap{{flex-direction:column;align-items:stretch;gap:32px;}}.fd-photo{{flex:none;max-width:420px;}}}}
  @media (max-width:1000px){{.tm-grid,.gv-grid{{grid-template-columns:1fr;}}}}
  @media (max-width:600px){{.tm-card{{flex-direction:column;align-items:flex-start;padding:22px;}}}}
</style>

  <!-- ===================== FOUNDER ===================== -->
  <div id="founder" style="width:100%;background:#F3F0EA;">
    <div class="glo-container fd-wrap" style="max-width:1140px;margin:0 auto;padding:90px 48px;">
      <figure class="fd-photo"><img src="{founder['photo']}" alt="Renee Porter, founder of GLO Aesthetics + Wellness Lounge, seated in the Ocala lounge" width="{founder['width']}" height="{founder['height']}" loading="lazy" decoding="async"></figure>
      <div class="fd-copy">
        {eyebrow('OUR FOUNDER')}
        <h2 class="glo-h2" style="font-size:40px;line-height:1.2;color:#221F1B;margin-bottom:16px;">Who <span class="glo-accent">founded</span> GLO?</h2>
        <p style="font-size:17.5px;line-height:1.8;color:#5C574E;margin:0 0 16px;">GLO Aesthetics + Wellness Lounge was founded by Renee Porter. Her vision shapes everything you&rsquo;ll find here: a calm, beautiful space in Ocala, a licensed team that listens first, and care that never feels rushed or pressured.</p>
        <p style="font-size:17.5px;line-height:1.8;color:#5C574E;margin:0 0 24px;">From the lounge to the treatment rooms, GLO was designed to feel less like a clinic and more like a place you look forward to coming back to.</p>
        <div class="fd-sign"><span class="fd-name">Renee Porter</span><span class="fd-role">Founder</span></div>
      </div>
    </div>
  </div>

  <!-- ===================== TEAM ===================== -->
  <div id="team" style="width:100%;background:#FAF9F6;scroll-margin-top:130px;">
    <div class="glo-container" style="max-width:1240px;margin:0 auto;padding:90px 48px;">
      <div style="max-width:760px;margin-bottom:40px;">
        {eyebrow('OUR TEAM')}
        <h2 class="glo-h2" style="font-size:40px;line-height:1.2;color:#221F1B;margin-bottom:12px;">Who will I see at GLO?</h2>
        <p style="font-size:17px;line-height:1.7;color:#5C574E;margin:0;">You&rsquo;ll be cared for by licensed providers who take time to listen. Each has her own focus, so you can book with the person whose expertise fits your goals &mdash; or let us match you at your consultation. McKenzie, Sundee, Baily and Mariah all see clients in <a href="/locations/ocala" style="color:#B8894F;">Ocala</a>; Sundee and Baily also see clients in <a href="/locations/palatka" style="color:#B8894F;">Palatka</a>.</p>
      </div>
      <div class="tm-grid">{''.join(member(m) for m in team)}
      </div>
    </div>
  </div>

'''
from real_photos import gallery
body += gallery('Where will I be <span class="glo-accent">treated</span>?',
                'In a bright, calm space designed to feel like a retreat. These are real photos of our Ocala med spa &mdash; the lounge, our private treatment rooms and the Tetra Pro laser.', '#FFFFFF')
body += f'''
  <!-- ===================== VALUES ===================== -->
  <div style="width:100%;background:#F3F0EA;">
    <div class="glo-container" style="max-width:1240px;margin:0 auto;padding:90px 48px;">
      <div style="max-width:760px;margin-bottom:36px;">
        <h2 class="glo-h2" style="font-size:40px;line-height:1.2;color:#221F1B;margin-bottom:12px;">What makes GLO different?</h2>
        <p style="font-size:17px;line-height:1.7;color:#5C574E;margin:0;">We listen before we recommend anything. Most people arrive with a feeling, not a treatment name &mdash; and that&rsquo;s exactly where we like to start.</p>
      </div>
      <div class="gv-grid">
        <div><h3>Listening first</h3><p>Every new client starts with a consultation about your goals, health history and budget. You never have to decide anything on the spot.</p></div>
        <div><h3>Medical oversight</h3><p>Injectable, laser, energy-based and wellness treatments are performed by licensed providers under the direction of our Florida-licensed Medical Director.</p></div>
        <div><h3>Results that look like you</h3><p>Our goal is a rested, refreshed version of you &mdash; never an overdone look. Results vary, and we&rsquo;ll be honest about what to expect.</p></div>
      </div>
    </div>
  </div>
'''

body += reviews_section('What do clients <span class="glo-accent">say</span> about GLO?',
                        'Here&rsquo;s how our clients describe their visits, in their own words. These reviews come straight from Google and update as new ones arrive.',
                        bg='#FAF9F6')

FAQ = [
    ('Who founded GLO Aesthetics + Wellness Lounge?', 'GLO Aesthetics + Wellness Lounge was founded by Renee Porter. GLO has two Florida locations, in Ocala and Palatka, with a licensed team working under the direction of a Florida-licensed Medical Director.'),
    ('Who performs treatments at GLO?', 'Treatments are performed by GLO&rsquo;s licensed team &mdash; including a board-certified family nurse practitioner, medical estheticians and aestheticians &mdash; under the direction of our Florida-licensed Medical Director.'),
    ('Which providers work at each GLO location?', 'McKenzie McCalla, Sundee Bass, Baily Bellamy and Mariah Young all see clients at our Ocala location. Sundee Bass and Baily Bellamy also see clients at our Palatka location. You can book any of them online for the location that suits you.'),
    ('Can I choose my provider?', 'Yes. You can book with a specific team member through our online booking, or book a consultation and we&rsquo;ll match you with the provider whose focus fits your goals.'),
    ('Do you have a Medical Director?', 'Yes. All aesthetic, injectable, laser, energy-based and medical wellness services at GLO are performed under the direction of a Florida-licensed Medical Director, in line with Florida Board of Medicine requirements for medical spas.'),
    ('Where are GLO&rsquo;s locations?', 'GLO has two Florida locations: 1925 SW 18th Ct, Unit 109, Ocala, FL 34471, and 210 St Johns Ave, Palatka, FL 32177. Call 352-559-8034 for either.'),
    ('Is the first consultation free?', 'Aesthetic and skincare consultations are free to book online. Some wellness visits, such as weight loss appointments, carry a fee that&rsquo;s shown when you book.'),
]
body += faq_html('About GLO FAQs', FAQ)
body += cta('Ready to meet us?', 'Tell us what you&rsquo;d like to feel again. We&rsquo;ll listen first, then walk you through your options &mdash; no pressure.') + '\n'

people = [{'@type': 'Person', '@id': f'{URL}#{m["name"].lower().replace(" ", "-")}', 'name': m.get('full_name', m['name']),
           'alternateName': m['name'], 'jobTitle': plain(m['title']), 'image': m['photo'],
           'worksFor': {'@id': BUSINESS_ID}, 'workLocation': [{'@id': f'{SITE}/locations/{l.lower()}#location'} for l in m['locations']],
           **({'honorificSuffix': m['credentials']} if m['credentials'] else {}),
           'knowsAbout': [plain(f) for f in m['focus']]} for m in team]
graph = [
    {'@type': 'AboutPage', '@id': URL + '#page', 'url': URL, 'name': TITLE, 'description': META, 'inLanguage': 'en-US',
     'dateModified': UPDATED[0], 'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': BUSINESS_ID},
     'mainEntity': {'@id': BUSINESS_ID}, 'primaryImageOfPage': IMG_HERO, 'breadcrumb': {'@id': URL + '#breadcrumb'}},
    {'@type': ['MedicalBusiness', 'HealthAndBeautyBusiness'], '@id': BUSINESS_ID, 'name': 'GLO Aesthetics + Wellness Lounge',
     'url': SITE + '/', 'employee': [{'@id': p['@id']} for p in people], 'founder': {'@id': URL + '#renee-porter'}},
    {'@type': 'Person', '@id': URL + '#renee-porter', 'name': founder['name'], 'jobTitle': 'Founder',
     'image': SITE + founder['photo_jpg'], 'worksFor': {'@id': BUSINESS_ID}},
    *people,
    dict(breadcrumbs(crumbs), **{'@id': URL + '#breadcrumb'}),
    faq_schema(FAQ),
]
write_page('about.html', TITLE, META, PATH, IMG_HERO, graph, body)
print('built about.html', len(TITLE), len(META), len(plain(answer).split()))
