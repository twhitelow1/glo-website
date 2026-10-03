"""Shared helpers for generated GLO pages: the page shell, SEO head, trust line and schema.

Every generated page gets: title <= 60, meta 140-160, canonical, Open Graph/Twitter tags, one keyword H1,
a 40-60 word direct answer, an "Updated" line, BreadcrumbList + FAQPage schema and the medical disclaimer.
"""
import html, json, re

SITE = 'https://gloocala.com'
UPDATED = ('2026-10-01', 'October 1, 2026')
IMG = 'https://d8j0ntlcm91z4.cloudfront.net/user_3JRDtqjRvBX48mQoPYnwuq2wzO6/hf_20261001_004311_{}.png'
BUSINESS_ID = SITE + '/#business'
TEMPLATE = 'treatments/index.html'

BTN = ('class="btn-primary" style="display:inline-block;background:#B8894F;color:#FAF9F6;padding:15px 30px;border-radius:2px;'
       'font-size:13px;letter-spacing:0.1em;font-weight:500;text-transform:uppercase;"')
BTN_OUT = ('class="btn-outline" style="display:inline-block;border:1px solid #221F1B;color:#221F1B;padding:15px 30px;border-radius:2px;'
           'font-size:13px;letter-spacing:0.1em;font-weight:500;text-transform:uppercase;"')
LINK = 'style="color:#B8894F;font-weight:500;"'


def esc(s):
    return html.escape(s, quote=True)


def plain(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s))


def shell():
    """(head_top, nav, footer) cut from the Treatments pillar so generated pages share its nav, styles and footer."""
    s = open(TEMPLATE).read()
    head, body = s.split('</head>', 1)
    top = head[:head.index('<meta name="viewport"')] + '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    nav = body.split('  <!-- ===================== HERO ===================== -->', 1)[0]
    marker = '  <!-- ===================== MEDICAL / COMPLIANCE DISCLAIMER'
    footer = marker + body.split(marker, 1)[1]
    return top, nav, footer


def seo_head(title, desc, path, image, og_type='website'):
    url = SITE + path
    t, d = esc(title), esc(desc)
    return f'''<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="GLO Aesthetics + Wellness Lounge">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{image}">
'''


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, indent=1, ensure_ascii=False) + '\n</script>\n'


def breadcrumbs(items):
    """items: [(name, path)], last is the current page."""
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + p} for i, (n, p) in enumerate(items)]}


def crumbs_html(items):
    parts = [f'<a href="{p}">{esc(n)}</a>' for n, p in items[:-1]] + [f'<span aria-current="page">{esc(items[-1][0])}</span>']
    return '<nav class="glo-hero-crumbs" aria-label="Breadcrumb">' + ' &nbsp;/&nbsp; '.join(parts) + '</nav>'


def faq_schema(faqs):
    return {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': plain(q), 'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}} for q, a in faqs]}


def faq_html(heading, faqs, section_id='faq', bg='#FAF9F6'):
    rows = ''.join(f'''
      <div class="faq-row" style="padding:24px 0;">
        <h3 style="font-size:21px;color:#221F1B;margin:0 0 10px;">{q}</h3>
        <p style="font-size:16px;line-height:1.75;color:#5C574E;margin:0;">{a}</p>
      </div>''' for q, a in faqs)
    return f'''
  <!-- ===================== FAQ ===================== -->
  <div id="{section_id}" style="width:100%;background:{bg};">
    <div class="glo-container" style="max-width:860px;margin:0 auto;padding:90px 48px;">
      <h2 class="glo-h2" style="font-size:38px;line-height:1.2;color:#221F1B;text-align:center;margin-bottom:36px;">{heading}</h2>{rows}
    </div>
  </div>
'''


def updated_line(extra=''):
    iso, human = UPDATED
    return (f'<p class="glo-updated" style="margin:20px 0 0;font-size:13.5px;line-height:1.6;color:#8A8377;">'
            f'Updated <time datetime="{iso}">{human}</time> &middot; Treatments performed by licensed providers under the direction of our Florida-licensed Medical Director{extra}</p>')


def eyebrow(text, center=False):
    line = '<div style="width:36px;height:1px;background:#B8894F;"></div>'
    return (f'<div style="display:flex;align-items:center;{"justify-content:center;" if center else ""}gap:14px;margin-bottom:20px;">'
            f'{line}<span style="font-size:14px;letter-spacing:0.28em;color:#B8894F;font-weight:600;">{text}</span>{line if center else ""}</div>')


def split_hero(crumbs, eyebrow_text, h1, answer, buttons, image, alt, pos='center 30%', note=None, size=(1024, 1365)):
    return f'''  <!-- ===================== HERO ===================== -->
  <div class="glo-split-hero">
    <div class="glo-split-text">{crumbs_html(crumbs)}
      <div class="glo-split-text-inner">
      {eyebrow(eyebrow_text)}
      <h1 class="glo-hero-h1" style="font-size:54px;line-height:1.12;color:#221F1B;max-width:600px;">{h1}</h1>
      <p class="glo-answer" style="margin-top:22px;font-size:18px;line-height:1.8;color:#5C574E;max-width:560px;">{answer}</p>
      <div style="display:flex;gap:14px;margin-top:32px;flex-wrap:wrap;">{buttons}</div>
      {updated_line()}
    </div></div>
    <div class="glo-split-media"><img src="{image}" alt="{esc(alt)}" width="{size[0]}" height="{size[1]}" fetchpriority="high" style="object-position:{pos};">{f'<span class="glo-hero-note">{note}</span>' if note else ''}</div>
  </div>
'''


def cta(heading, text, book_href='/#book', label='Book a Consultation'):
    return f'''
  <!-- ===================== CTA ===================== -->
  <div class="glo-dark" style="width:100%;background:#6B5435;">
    <div class="glo-container" style="max-width:900px;margin:0 auto;padding:80px 48px;text-align:center;">
      <h2 class="glo-h2" style="font-size:34px;color:#FAF9F6;margin-bottom:14px;">{heading}</h2>
      <p style="font-size:17px;line-height:1.7;color:#EADFCC;margin:0 auto 28px;max-width:560px;">{text}</p>
      <a href="{book_href}" {BTN}>{label}</a>
    </div>
  </div>
'''


def write_page(path_file, title, desc, path, image, schema_graph, body):
    assert len(title) <= 60, (path_file, len(title), title)
    assert 120 <= len(desc) <= 160, (path_file, len(desc), desc)
    top, nav, footer = shell()
    graph = {'@context': 'https://schema.org', '@graph': schema_graph}
    page = top + seo_head(title, desc, path, image) + ld(graph) + _head_rest() + '</head>' + nav + body + footer
    open(path_file, 'w').write(page)


def _head_rest():
    s = open(TEMPLATE).read().split('</head>', 1)[0]
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', s, flags=re.S)
    return s[s.index('<link rel="preconnect"'):]


# GLO's review widgets (LeadConnector reputation, api.gloocala.com): live reviews, resized by review-widget.js.
REVIEWS_SLIDER = 'https://api.gloocala.com/reputation/widgets/review_widget/AydYhaW9nUR8bWdvPa8A?widgetId=6a9042b9fe997b700ec5efc9'
REVIEWS_GRID = 'https://api.gloocala.com/reputation/widgets/review_widget/AydYhaW9nUR8bWdvPa8A'


def reviews_widget(src=REVIEWS_SLIDER):
    return ("<script src=\"https://api.gloocala.com/reputation/assets/review-widget.js\"></script>"
            f"<iframe class=\"lc_reviews_widget\" src=\"{src}\" title=\"Reviews of GLO Aesthetics + Wellness Lounge\" "
            "frameborder=\"0\" scrolling=\"no\" style=\"min-width:100%;width:100%;border:0;\"></iframe>")


def reviews_section(heading, intro, src=REVIEWS_SLIDER, bg='#FFFFFF', more=True, section_id='reviews'):
    """A reviews band: question H2, one-line answer, the live widget, and a link to /reviews."""
    link = ('<p style="text-align:center;margin:26px 0 0;"><a href="/reviews" style="font-size:15px;color:#B8894F;font-weight:600;">'
            'Read all GLO reviews &rarr;</a></p>') if more else ''
    return f'''
  <!-- ===================== REVIEWS ===================== -->
  <section id="{section_id}" class="glo-reviews" style="width:100%;background:{bg};scroll-margin-top:130px;">
    <div class="glo-container" style="max-width:1240px;margin:0 auto;padding:90px 48px;">
      <div style="max-width:720px;margin:0 auto 34px;text-align:center;">
        {eyebrow('CLIENT REVIEWS', center=True)}
        <h2 class="glo-h2" style="font-size:40px;line-height:1.2;color:#221F1B;margin-bottom:14px;">{heading}</h2>
        <p style="font-size:17px;line-height:1.75;color:#5C574E;margin:0;">{intro}</p>
      </div>
      <div class="glo-reviews-widget">{reviews_widget(src)}</div>{link}
    </div>
  </section>
'''
