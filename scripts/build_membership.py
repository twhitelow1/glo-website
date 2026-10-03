"""Build /membership-programs (membership-programs.html): The GLO Club, GLO's real monthly facial membership.

Facts come from GLO's own site (gloocala.com/facials, The GLO Club): $145/month, one Signature Facial each month,
priority booking, 10% off skincare products, 10% off all treatments offered, free gift at sign-up. Billing and
cancellation terms are not published, so the page says we'll walk through them rather than inventing any.
Stays noindex until GLO confirms the current price (Jane lists the Custom Facial at $125).
Run from the repo root, then scripts/design_layer.py:  python3 scripts/build_membership.py
"""
import sys
sys.path.insert(0, 'scripts')
from glo_page import *  # noqa

PATH, URL = '/membership-programs', SITE + '/membership-programs'
IMG_HERO = SITE + '/assets/ocala/facial-room.jpg'
TITLE = 'GLO Club Facial Membership in Ocala, FL | GLO'
META = ('Join the GLO Club in Ocala, FL: a Signature Facial every month, 10% off treatments and skincare, and '
        'priority booking for $145 a month. Call to join today.')
PRICE = '145'
TEL = 'tel:+13525598034'
FACIAL = 'https://gloocala.janeapp.com/locations/ocala-location-glo-aesthetics-wellness-lounge/book#/discipline/10/treatment/51'
INDEXABLE = False  # flip to True once GLO confirms the $145 price and terms

answer = ("The GLO Club is GLO&rsquo;s monthly membership in Ocala: one Signature Facial every month, 10% off every "
          "treatment we offer and our medical-grade skincare, priority booking and a free gift when you join, all for "
          "$145 a month. It&rsquo;s made for anyone who wants consistently glowing skin without having to plan for it.")

crumbs = [('Home', '/'), ('Memberships', '/membership-programs')]
body = split_hero(crumbs, 'THE GLO CLUB', 'The GLO Club: Facial Membership in <span style="font-style:italic;color:#B8894F;">Ocala</span>, FL',
                  answer,
                  f'<a href="{TEL}" {BTN}>Call to Join</a><a href="#included" {BTN_OUT}>See What&rsquo;s Included</a>',
                  '/assets/ocala/facial-room.webp', 'A private facial suite with a heated treatment bed at GLO in Ocala',
                  'center 55%', size=(900, 1599))

perks = [
    ('One Signature Facial every month', 'A fully customized corrective facial, built around what your skin needs that month.'),
    ('10% off every treatment', 'Member pricing on everything GLO offers, from Xeomin and filler to CoolPeel, Everesse and microneedling.'),
    ('10% off skincare', 'Save on the medical-grade products we recommend for keeping your results going at home.'),
    ('Priority booking', 'First access to the appointment times that fit your life, so your monthly facial never slips.'),
    ('A free gift when you join', 'A welcome gift from us when you sign up for the GLO Club.'),
]
perk_html = ''.join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in perks)
body += f'''
  <!-- ===================== WHAT'S INCLUDED ===================== -->
  <section id="included" style="width:100%;background:#FAF9F6;scroll-margin-top:130px;">
    <div class="glo-container" style="max-width:1180px;margin:0 auto;padding:90px 48px;">
      <div style="max-width:720px;margin-bottom:38px;">
        {eyebrow('MEMBER BENEFITS')}
        <h2 class="glo-h2" style="font-size:40px;line-height:1.2;color:#221F1B;margin-bottom:12px;">What&rsquo;s <span class="glo-accent">included</span> in the GLO Club?</h2>
        <p style="font-size:17px;line-height:1.75;color:#5C574E;margin:0;">Every month you get a Signature Facial, plus member savings on everything else you do with us. One simple monthly price, no counting punch cards.</p>
      </div>
      <div class="gc-wrap">
        <ul class="gc-perks">{perk_html}</ul>
        <aside class="gc-price">
          <div class="gc-price-label">The GLO Club</div>
          <div class="gc-price-amt">$145<span>/month</span></div>
          <p>Consistent care. Exclusive benefits. Real results.</p>
          <a href="{TEL}" class="gc-btn">Call 352-559-8034 to Join</a>
          <a href="{FACIAL}" target="_blank" rel="noopener" class="gc-link">Or book a Signature Facial first &rarr;</a>
        </aside>
      </div>
    </div>
  </section>
'''

mods = ['Enzyme therapy', 'Corrective treatment masks', 'Medical-grade serums', 'Oxygen infusion',
        'Radiofrequency skin tightening', 'Ultrasonic skin scrubber', 'Red light therapy', 'Sculpting facial massage',
        'Gua sha', 'Lymphatic massage', 'Shoulder, arm &amp; d&eacute;collet&eacute; massage', 'Dermaplaning',
        'No-downtime corrective peels', 'Barrier repair &amp; hydration']
body += f'''
  <!-- ===================== THE MONTHLY FACIAL ===================== -->
  <section style="width:100%;background:#FFFFFF;">
    <div class="glo-container" style="max-width:1180px;margin:0 auto;padding:90px 48px;">
      <div class="hiw-flex"><div>
        {eyebrow('YOUR MONTHLY FACIAL')}
        <h2 class="glo-h2" style="font-size:40px;line-height:1.2;color:#221F1B;margin-bottom:14px;">What happens in your <span class="glo-accent">Signature</span> Facial?</h2>
        <p style="font-size:17px;line-height:1.75;color:#5C574E;margin:0 0 14px;">Your Signature Facial is fully customized every month. Your aesthetician looks at your skin that day, asks what&rsquo;s changed, and chooses from more than a dozen techniques so each visit treats what your skin needs now.</p>
        <p style="font-size:17px;line-height:1.75;color:#5C574E;margin:0 0 18px;">Depending on your skin, your facial may include:</p>
        <ul class="gc-mods">{''.join(f'<li>{m}</li>' for m in mods)}</ul>
      </div><figure class="hiw-figure"><img src="/assets/ocala/lounge-retail.webp" alt="Lounge seating, coffee bar and medical-grade skincare shelves at GLO Aesthetics + Wellness Lounge in Ocala" width="900" height="1599" loading="lazy" decoding="async"><figcaption>Our Ocala lounge, with the medical-grade skincare members save on.</figcaption></figure></div>
    </div>
  </section>
'''

asks = [
    ('Do you already book a facial most months?', 'The GLO Club makes it automatic, and every visit comes with member perks.'),
    ('Thinking about Xeomin, CoolPeel or microneedling this year?', 'Members save 10% on every treatment, so the bigger plans cost less too.'),
    ('Do you use medical-grade skincare at home?', 'Your 10% skincare savings help your results last between visits.'),
    ('Is it hard to get the appointment times you want?', 'Priority booking means your monthly facial fits your schedule, not the other way around.'),
]
body += f'''
  <!-- ===================== IS IT FOR ME ===================== -->
  <section style="width:100%;background:#F3F0EA;">
    <div class="glo-container" style="max-width:1180px;margin:0 auto;padding:90px 48px;">
      <div style="max-width:720px;margin-bottom:34px;">
        <h2 class="glo-h2" style="font-size:40px;line-height:1.2;color:#221F1B;margin-bottom:12px;">Is the GLO Club <span class="glo-accent">right</span> for me?</h2>
        <p style="font-size:17px;line-height:1.75;color:#5C574E;margin:0;">It&rsquo;s right for you if glowing skin is something you&rsquo;d like to keep, not chase. Ask yourself:</p>
      </div>
      <ul class="gc-asks">{''.join(f'<li><h3>{q}</h3><p>{a}</p></li>' for q, a in asks)}</ul>
      <p style="margin:30px 0 0;font-size:16px;color:#5C574E;">Looking for weight loss support instead? See <a href="/treatments/functional-weight-loss" {LINK}>medical weight loss</a> and <a href="/treatments/peptide-therapy" {LINK}>peptide therapy</a>, or <a href="/financing" {LINK}>pay over time with Cherry</a>.</p>
    </div>
  </section>
'''

body += f'''
  <!-- ===================== WHERE ===================== -->
  <section style="width:100%;background:#FAF9F6;">
    <div class="glo-container" style="max-width:1180px;margin:0 auto;padding:90px 48px;">
      <div style="max-width:720px;margin-bottom:34px;">
        <h2 class="glo-h2" style="font-size:40px;line-height:1.2;color:#221F1B;margin-bottom:12px;">Where will I come for my <span class="glo-accent">monthly</span> facial?</h2>
        <p style="font-size:17px;line-height:1.75;color:#5C574E;margin:0;">To our Ocala lounge at 1925 SW 18th Ct, Unit 109. Settle in with a coffee, then head down the hall to a private facial suite. These are real photos of the space.</p>
      </div>
      <div class="gc-gallery">
        <figure><img src="/assets/ocala/lounge.webp" alt="The GLO client lounge in Ocala with ivory chairs and a gold table" width="900" height="1599" loading="lazy" decoding="async"><figcaption>The client lounge</figcaption></figure>
        <figure><img src="/assets/ocala/hallway.webp" alt="Gold-lit hallway leading to private treatment rooms at GLO Ocala" width="900" height="1599" loading="lazy" decoding="async"><figcaption>The way to your facial suite</figcaption></figure>
        <figure><img src="/assets/ocala/facial-room.webp" alt="A softly lit private facial suite at GLO Ocala" width="900" height="1599" loading="lazy" decoding="async"><figcaption>Your facial suite</figcaption></figure>
      </div>
      <p style="margin:24px 0 0;font-size:15px;"><a href="/locations/ocala" {LINK}>Directions and hours for our Ocala location &rarr;</a></p>
    </div>
  </section>
'''

FAQ = [
    ('How much is the GLO Club?', 'The GLO Club is $145 a month. That includes one Signature Facial each month, 10% off all treatments and skincare products, priority booking and a free gift when you join.'),
    ('What do I get each month?', 'One Signature Facial, a fully customized corrective facial. Your aesthetician tailors it to your skin each visit, from enzyme therapy and dermaplaning to red light, oxygen infusion and corrective peels.'),
    ('Does the 10% off include injectables and lasers?', 'Yes. GLO Club members get 10% off all treatments we offer, including injectables like Xeomin and Daxxify and laser and radiofrequency treatments, plus 10% off skincare products.'),
    ('How do I join the GLO Club?', f'Call us at <a href="{TEL}" {LINK}>352-559-8034</a> or ask at your next visit, and we&rsquo;ll get you set up. You&rsquo;ll receive a free gift when you sign up.'),
    ('What are the billing and cancellation terms?', 'We&rsquo;ll walk you through billing, cancellation and any minimum before you sign up, so there are no surprises. Questions before then? Call 352-559-8034.'),
    ('Can I try a facial before joining?', f'Of course. <a href="{FACIAL}" target="_blank" rel="noopener" {LINK}>Book a Signature Facial</a> first, see how your skin feels, and join when you&rsquo;re ready.'),
]
body += faq_html('GLO Club <span class="glo-accent">FAQs</span>', FAQ)
body += cta('Ready to make glowing skin a <span class="glo-accent">habit</span>?',
            'Join the GLO Club and your monthly facial is always on the calendar, with member savings on everything else.',
            TEL, 'Call 352-559-8034 to Join') + '\n'

body += f'''<style id="glo-club-css">
  .gc-wrap{{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:34px;align-items:start;}}
  .gc-perks{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;}}
  .gc-perks li{{background:#FFFFFF;border:1px solid #E6E1D6;border-radius:10px;padding:24px 24px 22px;}}
  .gc-perks li:first-child{{grid-column:1 / -1;border-color:#B8894F;}}
  .gc-perks h3{{font-size:21px;color:#221F1B;margin:0 0 6px;}}
  .gc-perks p{{font-size:15px;line-height:1.65;color:#5C574E;margin:0;}}
  .gc-price{{position:sticky;top:150px;background:#6B5435;color:#F3F0EA;border-radius:12px;padding:34px 30px;text-align:center;box-shadow:0 24px 48px rgba(34,31,27,.16);}}
  .gc-price-label{{font-family:'Montserrat',sans-serif;font-size:12.5px;letter-spacing:.24em;text-transform:uppercase;color:#E8D3A8;font-weight:600;}}
  .gc-price-amt{{font-family:'Playfair Display',Georgia,serif;font-size:58px;color:#FAF9F6;line-height:1.1;margin:12px 0 6px;}}
  .gc-price-amt span{{font-size:19px;color:#E8D3A8;}}
  .gc-price p{{font-family:'Playfair Display',Georgia,serif;font-style:italic;font-size:17px;color:#EADFCC;margin:0 0 22px;}}
  .gc-btn{{display:block;background:#E8D3A8;color:#3A2D1E;padding:15px 18px;border-radius:2px;font-family:'Montserrat',sans-serif;font-size:12.5px;letter-spacing:.1em;font-weight:600;text-transform:uppercase;}}
  .gc-btn:hover{{background:#FAF9F6;}}
  .gc-link{{display:inline-block;margin-top:14px;font-size:14.5px;color:#E8D3A8;}}
  .gc-mods{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px;}}
  .gc-mods li{{font-size:13.5px;color:#6B5435;background:#F3F0EA;border:1px solid #E6E1D6;border-radius:999px;padding:6px 13px;}}
  .gc-asks{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;}}
  .gc-asks li{{background:#FAF9F6;border:1px solid #E6E1D6;border-radius:10px;padding:24px;}}
  .gc-asks h3{{font-size:20px;color:#221F1B;margin:0 0 6px;}}
  .gc-asks p{{font-size:15px;line-height:1.65;color:#5C574E;margin:0;}}
  .gc-gallery{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;}}
  .gc-gallery figure{{margin:0;}}
  .gc-gallery img{{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;border-radius:10px;display:block;}}
  .gc-gallery figcaption{{font-size:13.5px;color:#8A8377;margin-top:8px;}}
  @media (max-width:900px){{.gc-wrap{{grid-template-columns:1fr;}}.gc-price{{position:static;order:-1;}}.gc-asks{{grid-template-columns:1fr;}}}}
  @media (max-width:600px){{.gc-perks{{grid-template-columns:1fr;}}.gc-gallery{{grid-template-columns:1fr 1fr;gap:12px;}}.gc-gallery figure:last-child{{grid-column:1 / -1;}}.gc-gallery figure:last-child img{{aspect-ratio:16/10;}}.gc-price-amt{{font-size:50px;}}}}
</style>
'''

graph = [
    {'@type': 'WebPage', '@id': URL + '#page', 'url': URL, 'name': TITLE, 'description': META, 'inLanguage': 'en-US',
     'dateModified': UPDATED[0], 'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': URL + '#glo-club'},
     'primaryImageOfPage': IMG_HERO, 'breadcrumb': {'@id': URL + '#breadcrumb'}},
    {'@type': 'Service', '@id': URL + '#glo-club', 'name': 'The GLO Club', 'serviceType': 'Monthly facial membership',
     'description': 'One Signature Facial each month, 10% off all treatments and skincare products, priority booking and a free gift at sign-up.',
     'provider': {'@id': BUSINESS_ID}, 'areaServed': {'@type': 'City', 'name': 'Ocala'},
     'offers': {'@type': 'Offer', 'url': URL, 'priceCurrency': 'USD', 'price': PRICE,
                'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': PRICE, 'priceCurrency': 'USD',
                                       'unitText': 'month', 'description': '$145 per month'},
                'seller': {'@id': BUSINESS_ID}}},
    dict(breadcrumbs(crumbs), **{'@id': URL + '#breadcrumb'}),
    faq_schema(FAQ),
]
write_page('membership-programs.html', TITLE, META, PATH, IMG_HERO, graph, body)
if not INDEXABLE:
    p = 'membership-programs.html'
    s = open(p).read().replace('<meta name="robots" content="index, follow, max-image-preview:large">',
                               '<meta name="robots" content="noindex, follow">', 1)
    open(p, 'w').write(s)
print('built membership-programs.html', len(TITLE), len(META), len(plain(answer).split()))
