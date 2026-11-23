"""Location-aware booking: every Jane button says which location it books, and Palatka lists only what Palatka offers.

- Home #book: an Ocala | Palatka switch. The Palatka panel keeps only treatments Jane offers in Palatka; buttons read
  "Book for Ocala" / "Book for Palatka". Without JS both panels show, one after the other.
- Treatment pages offered in both towns: the pricing button becomes "Book for Ocala" + "Book for Palatka".
  Ocala-only pages say so under the pricing button.

Palatka-enabled Jane treatment ids come from gloocala.janeapp.com/api/v2/treatments (location_ids contains 2). Re-check
Jane when GLO adds a service to Palatka, update PALATKA_TX / PALATKA_PAGES, and re-run. Idempotent.
"""
import re

OCALA = 'https://gloocala.janeapp.com/locations/ocala-location-glo-aesthetics-wellness-lounge/book'
PALATKA = 'https://gloocala.janeapp.com/locations/palatka-location-glo-aesthetics-wellness-lounge/book'
# Jane treatments bookable in Palatka (Nov 2026): consults, injectables, microneedling, mini facial, weight loss, peptides
PALATKA_TX = {57, 58, 59, 82, 87, 93, 97, 102, 105, 108, 114, 115, 116, 117, 118, 119, 121, 122, 85, 67}
# Treatment pages whose treatment is offered in Palatka (by what Jane offers there, not just the consult id they link)
PALATKA_PAGES = ['xeomin', 'daxxify', 'dermal-filler', 'dissolve-ha-dermal-filler', 'liquid-rhinoplasty', 'microneedling',
                 'daxxify-facial-microneedling', 'mini-facials', 'functional-weight-loss', 'peptide-therapy']
OCALA_ONLY = ['coolpeel', 'custom-facials-peels', 'laser-hair-removal', 'laser-skin-revitalization', 'motus-laser-facial',
              'radiant-lift', 'skin-tightening']

CSS = '''<style id="glo-locbook-css">
  .lb-switch{display:flex;justify-content:center;gap:0;margin:0 auto 34px;width:max-content;border:1px solid #D9CFC0;border-radius:999px;padding:4px;background:#FFFFFF;}
  .lb-switch button{all:unset;cursor:pointer;padding:11px 26px;border-radius:999px;font-family:'Albert Sans',sans-serif;font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:600;color:#6B5435;}
  .lb-switch button[aria-selected="true"]{background:#6B5435;color:#FAF9F6;}
  .lb-switch button:focus-visible{outline:2px solid #B8894F;outline-offset:2px;}
  .lb-panel + .lb-panel{margin-top:56px;}
  .lb-panel-title{font-family:'Newsreader',Georgia,serif;font-size:28px;color:#221F1B;text-align:center;margin:0 0 6px;}
  .lb-panel-addr{text-align:center;font-size:15px;color:#8A8377;margin:0 0 28px;}
  html.glo-lb .lb-panel-title{display:none;}
  html.glo-lb .lb-panel + .lb-panel{margin-top:0;}
  html.glo-lb .lb-panel[hidden]{display:none;}
  .bk-btn{white-space:nowrap;}
  .loc-book{display:flex;flex-wrap:wrap;justify-content:center;gap:14px;margin-top:32px;}
  .loc-book a{margin-top:0 !important;}
  .loc-note{margin:14px 0 0;font-size:14px;color:inherit;opacity:.8;}
</style>
'''

JS = '''<script id="glo-locbook-js">
(function () {
  var sw = document.querySelector('.lb-switch');
  if (!sw) return;
  document.documentElement.classList.add('glo-lb');
  var tabs = sw.querySelectorAll('button');
  function show(loc) {
    Array.prototype.forEach.call(tabs, function (t) {
      var on = t.getAttribute('data-loc') === loc;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
  }
  Array.prototype.forEach.call(tabs, function (t) { t.addEventListener('click', function () { show(t.getAttribute('data-loc')); }); });
  show(location.hash === '#book-palatka' ? 'palatka' : 'ocala');
  window.addEventListener('hashchange', function () { if (location.hash === '#book-palatka') show('palatka'); });
})();
</script>
'''


def home(s):
    if 'class="lb-switch"' in s:
        return s
    m = re.search(r'      <div class="bk-grid">.*?\n      </div>\n(?=    </div>\n  </div>\n)', s, re.S)
    grid = m.group(0)
    oc = grid.replace('class="bk-btn"', 'class="bk-btn"').replace('>Book</a>', '>Book for Ocala</a>')
    oc = re.sub(r'aria-label="Book ([^"]*)"', r'aria-label="Book \1 in Ocala"', oc)
    # Palatka: same cards, only rows Jane offers in Palatka (the hormone "coming soon" row stays)
    pa = grid
    def keep(row):
        r = row.group(0)
        t = re.search(r'/treatment/(\d+)', r)
        return r if (t is None or int(t.group(1)) in PALATKA_TX) else ''
    pa = re.sub(r'\n\s*<li id="[^"]*" class="bk-row">.*?</li>', keep, pa)
    pa = pa.replace(OCALA, PALATKA).replace('>Book</a>', '>Book for Palatka</a>')
    pa = re.sub(r'aria-label="Book ([^"]*)"', r'aria-label="Book \1 in Palatka"', pa)
    pa = re.sub(r'<li id="([^"]+)"', r'<li id="\1-palatka"', pa)
    pa = pa.replace('Laser, radiofrequency, facials, peels &amp; microneedling.', 'Skincare consultations and mini facials.')
    panels = f'''      <div class="lb-switch" role="tablist" aria-label="Choose your GLO location">
        <button type="button" role="tab" id="lb-tab-ocala" data-loc="ocala" aria-controls="book-ocala" aria-selected="true">Ocala</button>
        <button type="button" role="tab" id="lb-tab-palatka" data-loc="palatka" aria-controls="book-palatka" aria-selected="false">Palatka</button>
      </div>
      <div class="lb-panel" id="book-ocala" role="tabpanel" aria-labelledby="lb-tab-ocala">
        <h3 class="lb-panel-title">Book in Ocala</h3>
        <p class="lb-panel-addr">1925 SW 18th Ct, Unit 109, Ocala, FL 34471</p>
{oc}      </div>
      <div class="lb-panel" id="book-palatka" role="tabpanel" aria-labelledby="lb-tab-palatka">
        <h3 class="lb-panel-title">Book in Palatka</h3>
        <p class="lb-panel-addr">210 St Johns Ave, Palatka, FL 32177 &middot; Palatka offers injectables, skincare and wellness. Lasers, Everesse and custom facials are in Ocala.</p>
{pa}      </div>
'''
    s = s[:m.start()] + panels + s[m.end():]
    s = s.replace('</head>', CSS + '</head>', 1)
    s = s.replace('</body>', JS + '</body>', 1)
    return s


def pricing_block(s):
    i = s.find('<!-- ===================== PRICING')
    if i < 0:
        return None
    m = re.compile(r'<a href="(' + re.escape(OCALA) + r'[^"]*)" target="_blank" rel="noopener" class="btn-primary" style="([^"]*)">([^<]*)</a>').search(s, i)
    return m


def treatment(slug):
    p = f'treatments/{slug}.html'
    s = open(p).read()
    if 'class="loc-book"' in s or 'class="loc-note"' in s:
        return
    m = pricing_block(s)
    if not m:
        print('no pricing button', slug)
        return
    url, style, text = m.groups()
    if slug in PALATKA_PAGES:
        style2 = style.replace('margin-top:32px;', '')
        new = (f'<div class="loc-book"><a href="{url}" target="_blank" rel="noopener" class="btn-primary" style="{style2}">Book for Ocala</a>'
               f'<a href="{url.replace(OCALA, PALATKA)}" target="_blank" rel="noopener" class="btn-primary" style="{style2}">Book for Palatka</a></div>')
    else:
        new = m.group(0) + '\n      <p class="loc-note">Offered at our Ocala location.</p>'
    s = s[:m.start()] + new + s[m.end():]
    if 'glo-locbook-css' not in s:
        s = s.replace('</head>', CSS + '</head>', 1)
    open(p, 'w').write(s)
    print('updated', p)


if __name__ == '__main__':
    s = open('index.html').read()
    open('index.html', 'w').write(home(s))
    for slug in PALATKA_PAGES + OCALA_ONLY:
        treatment(slug)
