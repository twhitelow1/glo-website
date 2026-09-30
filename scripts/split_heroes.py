"""One-off migration: convert full-bleed overlay heroes into edge-to-edge split heroes.

Text goes on a cream panel on one half; the photo fills the other half to the
viewport edge. On phones the photo stacks above the text.
"""
import glob
import re
import sys

CSS = """<style id="glo-split-hero-css">
  .glo-split-hero{display:grid;grid-template-columns:1fr 1fr;min-height:680px;background:#F3F0EA;width:100%;}
  .glo-split-text{display:flex;align-items:center;justify-content:flex-end;padding:100px 72px 124px 48px;}
  .glo-split-hero--media-left .glo-split-text{order:2;justify-content:flex-start;padding:100px 48px 124px 72px;}
  .glo-split-text-inner{width:100%;max-width:600px;text-align:left;}
  .glo-split-media{position:relative;min-height:680px;background-size:cover;background-repeat:no-repeat;background-position:center;}
  .glo-split-media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;}
  .glo-split-hero .btn-outline-light:hover{background:#221F1B !important;color:#FAF9F6 !important;}
  @media (max-width: 900px){
    .glo-split-hero{grid-template-columns:1fr;min-height:0;}
    .glo-split-media{order:-1 !important;min-height:380px;}
    .glo-split-text,.glo-split-hero--media-left .glo-split-text{order:2;justify-content:flex-start;padding:52px 28px 100px !important;}
  }
  @media (max-width: 600px){
    .glo-split-media{min-height:300px;}
    .glo-stats-strip{padding:22px 14px !important;margin-left:16px !important;margin-right:16px !important;}
    .glo-stats-strip > div > span:first-child{font-size:19px !important;white-space:nowrap;}
    .glo-stats-strip > div > span:last-child{font-size:10.5px !important;}
    .glo-split-text,.glo-split-hero--media-left .glo-split-text{padding:44px 20px 96px !important;}
  }
</style>
"""

LINE = '<div style="width:36px;height:1px;background:#B8894F;"></div>'


def hero_span(html):
    m = re.search(r'  <!-- =+ HERO[^>]*-->\n', html)
    if not m:
        return None
    end = html.index('<!-- =====', m.end())
    end = html.rindex('\n', 0, end) + 1
    return m.end(), end


def restyle(inner):
    inner = re.sub(r'text-shadow:[^;"]*;?', '', inner)
    inner = re.sub(r'(<h1\b[^>]*style="[^"]*?)color:#(?:FFFFFF|FAF9F6)', r'\1color:#221F1B', inner)
    inner = re.sub(r'(<p\b[^>]*style="[^"]*?)color:#(?:F3F0EA|F0EBE1)', r'\1color:#5C574E', inner)
    inner = inner.replace('border:1px solid #F3F0EA;color:#F3F0EA', 'border:1px solid #221F1B;color:#221F1B')
    inner = re.sub(r'text-align:(?:center|right)', 'text-align:left', inner)
    inner = re.sub(r'justify-content:(?:center|flex-end)', 'justify-content:flex-start', inner)
    inner = re.sub(r'margin:(\S+) auto (\S+?);', r'margin:\1 0 \2;', inner)
    inner = inner.replace('margin:0 auto;', 'margin:0;').replace('margin-left:auto;', '')
    # Eyebrow: single rule line on the left, then the label.
    def fix_eyebrow(m):
        block = m.group(0)
        block = re.sub(r'(</span>)\s*<div[^>]*(?:eyebrow-line|width:36px;height:1px)[^>]*></div>', r'\1', block)
        if not re.search(r'<div[^>]*(?:eyebrow-line|width:36px;height:1px)[^>]*></div>\s*<span', block):
            block = re.sub(r'(\s*)<span', r'\1' + LINE + r'\1<span', block, count=1)
        return block
    inner = re.sub(r'<div class="[^"]*eyebrow"[^>]*>.*?</span>(?:\s*<div[^>]*></div>)?', fix_eyebrow, inner, count=1, flags=re.S)
    return inner


def strip_outer_div(frag):
    """Return the content between a fragment's first opening <div ...> and its last </div>."""
    start = frag.index('>', frag.index('<div')) + 1
    end = frag.rindex('</div>')
    return frag[start:end]


def convert(frag):
    outer_open = re.match(r'\s*<div([^>]*)>', frag)
    id_attr = re.search(r'\bid="[^"]*"', outer_open.group(1))
    id_attr = ' ' + id_attr.group(0) if id_attr else ''
    media_left = 'justify-content:flex-end' in frag and 'glo-hero-text' in frag

    bg = re.search(r'<div role="img" aria-label="([^"]*)" style="[^"]*background-image:url\(\'([^\']+)\'\)[^"]*"></div>\n?', frag)
    img = re.search(r'<img src="([^"]+)" alt="([^"]*)"[^>]*>\n?', frag)
    if bg:
        label, url = bg.group(1), bg.group(2)
        pos = re.search(r'background-position:([^;"]+)', bg.group(0))
        pos = pos.group(1) if pos else 'center'
        media = f'<div class="glo-split-media" role="img" aria-label="{label}" style="background-image:url(\'{url}\');background-position:{pos};"></div>'
        body = frag.replace(bg.group(0), '')
        body = re.sub(r'\s*<div style="position:absolute;inset:0;background:linear-gradient[^"]*"></div>', '', body)
        content = strip_outer_div(strip_outer_div(body).strip() + '\n')
    elif img and 'glo-flex-half' in frag:  # location pages: contained split -> edge-to-edge
        media = f'<div class="glo-split-media"><img src="{img.group(1)}" alt="{img.group(2)}" /></div>'
        text_col = re.search(r'<div class="glo-flex-half" style="flex:1;">(.*?)\n      </div>\n      <div class="glo-flex-half"', frag, re.S)
        content = text_col.group(1)
    elif img:
        media = f'<div class="glo-split-media"><img src="{img.group(1)}" alt="{img.group(2)}" /></div>'
        body = frag.replace(img.group(0), '')
        body = re.sub(r'\s*<div style="position:absolute;inset:0;background:linear-gradient[^"]*"></div>', '', body)
        content = strip_outer_div(strip_outer_div(body).strip() + '\n')
    else:
        return None

    content = restyle(content.strip('\n'))
    cls = 'glo-split-hero glo-split-hero--media-left' if media_left else 'glo-split-hero'
    return (f'  <div class="{cls}"{id_attr}>\n'
            f'    <div class="glo-split-text"><div class="glo-split-text-inner">\n'
            f'{content}\n'
            f'    </div></div>\n'
            f'    {media}\n'
            f'  </div>\n\n')


changed, skipped = [], []
for f in sorted(glob.glob('*.html')):
    html = open(f).read()
    if 'glo-split-hero-css' in html:
        continue
    span = hero_span(html)
    if not span:
        skipped.append(f); continue
    new = convert(html[span[0]:span[1]])
    if not new:
        skipped.append(f); continue
    html = html[:span[0]] + new + html[span[1]:]
    html = html.replace('</head>', CSS + '</head>', 1)
    open(f, 'w').write(html)
    changed.append(f)
print('changed', len(changed), changed)
print('skipped', skipped)
