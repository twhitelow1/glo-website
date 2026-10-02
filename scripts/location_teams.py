"""Show who sees clients at each location, from content/team.json (which follows GLO's Jane booking pages).

Adds or refreshes:
  - a "Who will I see at our <city> location?" team section on locations/ocala.html and locations/palatka.html,
  - a matching "Which providers see clients in <city>?" FAQ (HTML + FAQPage schema),
  - `employee` links from each location's schema to the Person entries on /about,
  - the provider-by-location copy in the Locations hub's #meet-team section.

Safe to re-run. Run after real_photos.py and design_layer.py.
"""
import json
import re

SITE = 'https://gloocala.com'
data = json.load(open('content/team.json'))
TEAM = data['team']
WORDS = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six'}
START, END = '  <!-- ===================== LOCATION TEAM ===================== -->', '  <!-- /LOCATION TEAM -->'


def slug(m):
    return m['name'].lower().replace(' ', '-')


def full(m):
    return m['name'] + (f', {m["credentials"]}' if m['credentials'] else '')


def names(ms):
    n = [m["name"] for m in ms]
    return n[0] if len(n) == 1 else ', '.join(n[:-1]) + ' and ' + n[-1]


def at(city):
    return [m for m in TEAM if city in m['locations']]


def card(m, city):
    others = [l for l in m['locations'] if l != city]
    also = f'<span class="lt-also">Also sees clients in <a href="/locations/{others[0].lower()}">{others[0]}</a></span>' if others else ''
    return f'''
        <article class="lt-card">
          <img src="{m['photo']}" alt="{full(m)}, {m['title']} at GLO Aesthetics + Wellness Lounge in {city}, FL" width="160" height="190" loading="lazy" decoding="async">
          <div>
            <h3><a href="/about#{slug(m)}">{m['name']}</a><span class="lt-creds">{', ' + m['credentials'] if m['credentials'] else ''}</span></h3>
            <div class="lt-title">{m['title']}</div>
            {also}
            <a href="{m['book'][city]}" target="_blank" rel="noopener" class="lt-book">Book with {m['name'].split()[0]} in {city} &rarr;</a>
          </div>
        </article>'''


def faq_answer(city):
    ms = at(city)
    a = f'{names(ms)} see{"s" if len(ms) == 1 else ""} clients at our {city} location. '
    other = 'Palatka' if city == 'Ocala' else 'Ocala'
    shared = [m for m in ms if other in m['locations']]
    if shared:
        a += f'{names(shared)} also see{"s" if len(shared) == 1 else ""} clients in {other}. '
    return a + f'You can book any of them online for {city}, or call 352-559-8034 and we&rsquo;ll match you.'


def section(city):
    ms = at(city)
    intro = (f'Every {city} visit is with a licensed GLO provider who takes time to listen. '
             f'{WORDS[len(ms)]} of our team see clients here &mdash; book with the person whose focus fits your goals, '
             f'or let us match you at your consultation.')
    return f'''{START}
  <section id="team" style="width:100%;background:#FFFFFF;scroll-margin-top:130px;">
    <div class="glo-container" style="max-width:1140px;margin:0 auto;padding:90px 48px;">
      <div style="max-width:760px;margin-bottom:36px;">
        <h2 class="glo-h2" style="font-size:40px;line-height:1.2;color:#221F1B;margin-bottom:12px;">Who will I <span class="glo-accent">see</span> at our {city} location?</h2>
        <p style="font-size:17px;line-height:1.7;color:#5C574E;margin:0;">{intro}</p>
      </div>
      <div class="lt-grid">{''.join(card(m, city) for m in ms)}
      </div>
      <p style="font-size:15px;color:#5C574E;margin:28px 0 0;">Want to know more about each provider? <a href="/about#team" style="color:#B8894F;font-weight:600;">Meet the whole GLO team &rarr;</a></p>
    </div>
  </section>
{END}

'''


def faq_row(q, a):
    return f'''      <div class="faq-row" style="padding:22px 0;" data-lt-faq>
        <h3 style="font-size:20px;font-weight:500;color:#221F1B;margin:0 0 8px;line-height:1.35;">{q}</h3>
        <p style="font-size:16px;line-height:1.7;color:#5C574E;font-weight:300;margin:0;">{a}</p>
      </div>
'''


def plain(t):
    return re.sub(r'<[^>]+>', '', t).replace('&rsquo;', '’').replace('&mdash;', '—').replace('&amp;', '&')


def update_ld(s, city, q, a):
    loc_id = f'{SITE}/locations/{city.lower()}#location'

    def fix(m):
        d = json.loads(m.group(1))
        nodes = d.get('@graph', [d])
        for n in nodes:
            if n.get('@id') == loc_id:
                n['employee'] = [{'@id': f'{SITE}/about#{slug(x)}'} for x in at(city)]
            if n.get('@type') == 'FAQPage':
                n['mainEntity'] = [e for e in n['mainEntity'] if e['name'] != q]
                n['mainEntity'].insert(1, {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}})
        return f'<script type="application/ld+json">\n{json.dumps(d, indent=1, ensure_ascii=False)}\n</script>'
    return re.sub(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', fix, s, flags=re.S)


def location_page(city):
    f = f'locations/{city.lower()}.html'
    s = open(f).read()
    s = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n\n', '', s, flags=re.S)
    s = s.replace('  <!-- ===================== FAQ', section(city) + '  <!-- ===================== FAQ', 1)
    q, a = f'Which providers see clients in {city}?', faq_answer(city)
    s = re.sub(r'      <div class="faq-row"[^>]*data-lt-faq>.*?</div>\n', '', s, flags=re.S)
    i = s.index('<div class="faq-row"', s.index('<!-- ===================== FAQ'))
    s = s[:i - 6] + faq_row(q, a) + s[i - 6:]
    s = update_ld(s, city, q, a)
    if 'id="glo-lt-css"' not in s:
        s = s.replace('</head>', CSS + '</head>', 1)
    open(f, 'w').write(s)
    print('updated', f)


CSS = '''<style id="glo-lt-css">
  .lt-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;}
  .lt-card{display:flex;gap:22px;align-items:center;background:#FAF9F6;border:1px solid #E6E1D6;border-radius:10px;padding:22px;}
  .lt-card img{flex:none;width:112px;height:133px;object-fit:cover;border-radius:8px;background:#EFE9E1;}
  .lt-card h3{font-size:23px;color:#221F1B;margin:0;}
  .lt-card h3 a{color:inherit;}
  .lt-creds{font-family:'Montserrat',sans-serif;font-size:13px;letter-spacing:.06em;color:#B8894F;font-weight:600;}
  .lt-title{font-size:14.5px;color:#5C574E;margin-top:4px;}
  .lt-also{display:block;font-size:13.5px;color:#8A8377;margin-top:6px;}
  .lt-also a{color:#6B5435;text-decoration:underline;}
  .lt-book{display:inline-block;margin-top:12px;font-size:14.5px;color:#B8894F;font-weight:600;}
  @media (max-width:900px){.lt-grid{grid-template-columns:1fr;}}
  @media (max-width:480px){.lt-card{gap:16px;padding:16px;}.lt-card img{width:88px;height:105px;}.lt-card h3{font-size:20px;}}
</style>
'''


def hub(s):
    o, p = at('Ocala'), at('Palatka')
    founder = data['founder']['name']
    new = (f'Founded by {founder}, GLO has two homes. In <a href="/locations/ocala" style="color:#B8894F;">Ocala</a>, '
           f'you can book with {names(o)}. In <a href="/locations/palatka" style="color:#B8894F;">Palatka</a>, '
           f'{names(p)} see clients too, so you can choose the location that&rsquo;s easier for you.')
    return re.sub(r'(<section id="meet-team".*?<p[^>]*>).*?(</p>)', lambda m: m.group(1) + new + m.group(2), s, count=1, flags=re.S)


if __name__ == '__main__':
    for city in ('Ocala', 'Palatka'):
        location_page(city)
    f = 'locations/index.html'
    s = hub(open(f).read())
    open(f, 'w').write(s)
    print('updated', f)
