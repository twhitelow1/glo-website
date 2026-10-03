"""Build /reviews (reviews.html): GLO's live Google reviews in the grid widget, plus how to leave one.
Run from the repo root, then run scripts/design_layer.py:  python3 scripts/build_reviews.py
Reviews come only from the live widget. Never type reviews, ratings or review counts into this page or its schema.
"""
import sys
sys.path.insert(0, 'scripts')
from glo_page import *  # noqa

PATH, URL = '/reviews', SITE + '/reviews'
IMG_HERO = SITE + '/assets/ocala/lounge.jpg'
TITLE = 'GLO Med Spa Reviews in Ocala, FL | GLO Aesthetics'
META = 'Read real Google reviews from GLO Aesthetics + Wellness Lounge clients in Ocala and Palatka, FL, then book a no-pressure consultation to start your plan.'
GOOGLE = 'https://www.google.com/maps/search/?api=1&query=GLO+Aesthetics+%2B+Wellness+Lounge+1925+SW+18th+Ct+Ocala+FL'

answer = ('These are real reviews from GLO Aesthetics + Wellness Lounge clients, shown live from Google and updated as new ones arrive. '
          'Clients visit us in Ocala and Palatka, FL for injectables, laser and skin treatments, facials and medical wellness. '
          'Read their words, then book a no-pressure consultation of your own.')

crumbs = [('Home', '/'), ('Reviews', '/reviews')]
body = split_hero(crumbs, 'CLIENT REVIEWS', 'GLO Med Spa Reviews in <span style="font-style:italic;color:#B8894F;">Ocala</span>, FL', answer,
                  f'<a href="#reviews" {BTN}>Read the Reviews</a><a href="/#book" {BTN_OUT}>Book a Consultation</a>',
                  '/assets/ocala/lounge.webp', 'The client lounge at GLO Aesthetics + Wellness Lounge in Ocala, FL', 'center 45%', size=(900, 1599))

body += reviews_section('What are GLO clients <span class="glo-accent">saying</span>?',
                        'In their own words, here&rsquo;s what clients say about their visits. Every review below comes straight from Google, so what you read is exactly what they posted.',
                        src=REVIEWS_GRID, bg='#FAF9F6', more=False)

body += f'''
  <!-- ===================== LEAVE A REVIEW ===================== -->
  <div style="width:100%;background:#F3F0EA;">
    <div class="glo-container glo-row" style="max-width:1140px;margin:0 auto;padding:90px 48px;display:flex;gap:56px;align-items:center;">
      <div class="glo-flex-half" style="flex:1;">
        <h2 class="glo-h2" style="font-size:38px;line-height:1.2;color:#221F1B;margin-bottom:16px;">How can I <span class="glo-accent">leave</span> GLO a review?</h2>
        <p style="font-size:17px;line-height:1.75;color:#5C574E;margin:0 0 14px;">Open GLO Aesthetics + Wellness Lounge on Google, tap &ldquo;Write a review&rdquo; and share a few words about your visit. It takes about a minute.</p>
        <p style="font-size:17px;line-height:1.75;color:#5C574E;margin:0 0 28px;">Was there a moment that made you feel more like yourself again? Your story helps someone who&rsquo;s still wondering whether GLO is right for them.</p>
        <a href="{GOOGLE}" target="_blank" rel="noopener" {BTN}>Review GLO on Google</a>
      </div>
      <div class="glo-flex-half" style="flex:1;">
        <h3 style="font-size:24px;color:#221F1B;margin:0 0 14px;">Curious what clients come to us for?</h3>
        <ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px;font-size:16.5px;">
          <li><a href="/injectables" {LINK}>Injectables: Xeomin, Daxxify and filler &rarr;</a></li>
          <li><a href="/skin-services" {LINK}>Skin services: lasers, facials and microneedling &rarr;</a></li>
          <li><a href="/wellness" {LINK}>Medical wellness: weight loss, hormones and peptides &rarr;</a></li>
          <li><a href="/about#team" {LINK}>Meet the team behind the reviews &rarr;</a></li>
          <li><a href="/locations" {LINK}>Find us in Ocala or Palatka &rarr;</a></li>
        </ul>
      </div>
    </div>
  </div>
'''

FAQ = [
    ('Are these reviews from real GLO clients?', 'Yes. The reviews on this page are shown live from GLO Aesthetics + Wellness Lounge&rsquo;s Google reviews. We don&rsquo;t write or edit them, and new reviews appear here automatically.'),
    ('Will I get the same results as the people in these reviews?', 'Not necessarily. Results vary from person to person. At your consultation, a licensed provider will talk through what you can realistically expect from the treatment you&rsquo;re considering.'),
    ('How do I leave a review for GLO?', f'Open <a href="{GOOGLE}" target="_blank" rel="noopener" {LINK}>GLO on Google</a>, tap &ldquo;Write a review&rdquo; and share a few words about your visit. We read every one.'),
    ('What if I had a concern about my visit?', 'Please tell us directly. Call 352-559-8034 or email info@gloocala.com and we&rsquo;ll listen and work with you to make it right.'),
    ('How do I book my first visit?', 'Book a consultation online or call 352-559-8034. Your first visit is a no-pressure conversation about your goals, health history and budget.'),
]
body += faq_html('GLO Reviews <span class="glo-accent">FAQs</span>', FAQ)
body += cta('Ready to write your own <span class="glo-accent">GLO</span> story?',
            'Book a no-pressure consultation. We&rsquo;ll listen first, then help you choose what feels right for you.') + '\n'

graph = [
    {'@type': 'WebPage', '@id': URL + '#page', 'url': URL, 'name': TITLE, 'description': META, 'inLanguage': 'en-US',
     'dateModified': UPDATED[0], 'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': BUSINESS_ID},
     'primaryImageOfPage': IMG_HERO, 'breadcrumb': {'@id': URL + '#breadcrumb'}},
    dict(breadcrumbs(crumbs), **{'@id': URL + '#breadcrumb'}),
    faq_schema(FAQ),
]
write_page('reviews.html', TITLE, META, PATH, IMG_HERO, graph, body)
print('built reviews.html', len(TITLE), len(META), len(plain(answer).split()))
