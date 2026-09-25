# Wyciąga treść artykułów z zapisanych stron żywego serwisu (_a/*.html) — bez dopisywania czegokolwiek
import re, html as H
LINKS = {
    '': 'index.html', 'poradnik-czarterowy': 'poradnik.html', 'cennik': 'cennik.html', 'kontakt': 'kontakt.html', 'port': 'port.html',
    'czarter-jachtow-motorowych': 'jachty-motorowe.html', 'czarter-jachtow-zaglowych': 'jachty-zaglowe.html',
    'czarter-bez-patentu': 'czarter-bez-patentu.html', 'houseboat-mazury': 'jachty-motorowe.html',
    'jachty-na-sprzedaz': 'jachty-na-sprzedaz.html', 'inwestycje-i-posrednictwo': 'wspolpraca.html',
    'czarter-jachtow-zaglowych/antila-28-2': 'jachty-zaglowe.html?model=Antila%2028.2',
    'czarter-jachtow-zaglowych/maxus-28': 'jachty-zaglowe.html?model=Maxus%2028',
    'antila-34-progresja': 'jachty-zaglowe.html?model=Antila%2034',
}
KEEP_INLINE = ('strong', 'b', 'em', 'i', 'a', 'br')

def _link(href, slugs):
    m = re.match(r'https?://(?:www\.)?jachtymazury\.pl/?(.*?)/?$', href)
    if not m: return href, True
    path = m.group(1)
    if path in slugs: return f'{path}.html', False
    if path in LINKS: return LINKS[path], False
    return href, True

def _inline(frag, slugs):
    def a(m):
        href = re.search(r'href="([^"]+)"', m.group(1))
        if not href: return m.group(2)
        url, ext = _link(H.unescape(href.group(1)), slugs)
        extra = ' rel="noopener" target="_blank"' if ext else ''
        return f'<a class="u u--on" href="{H.escape(url)}"{extra}>{m.group(2)}</a>'
    frag = re.sub(r'<a\b([^>]*)>(.*?)</a>', a, frag, flags=re.S)
    frag = re.sub(r'<(/?)(?:b)>', r'<\1strong>', frag)
    frag = re.sub(r'<(?!/?(?:strong|em|i|a|br)\b)[^>]+>', '', frag)          # reszta tagów out
    frag = re.sub(r'<(strong|em|i)\b[^>]*>', r'<\1>', frag)
    return re.sub(r'\s+', ' ', frag).strip()

def extract(slug, slugs):
    s = open(f'_a/{slug}.html', encoding='utf-8').read()
    a = s.index('<h1 class="entry-title"'); b = s.index('</article', a)
    body = re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', '', s[a:b], flags=re.S)
    body = body[body.index('</h1>') + 5:]
    out = []
    for m in re.finditer(r'<(h2|h3|h4|p|ul|ol|table)\b[^>]*>(.*?)</\1>', body, re.S):
        tag, inner = m.group(1), m.group(2)
        if tag in ('ul', 'ol'):
            lis = [_inline(x, slugs) for x in re.findall(r'<li\b[^>]*>(.*?)</li>', inner, re.S)]
            lis = [x for x in lis if x]
            if lis: out.append((tag, lis))
        elif tag == 'table':
            rows = []
            for r in re.findall(r'<tr\b[^>]*>(.*?)</tr>', inner, re.S):
                rows.append([(c[0], _inline(c[1], slugs)) for c in re.findall(r'<(th|td)\b[^>]*>(.*?)</\1>', r, re.S)])
            if rows: out.append(('table', rows))
        else:
            t = _inline(inner, slugs)
            if t and t != '&nbsp;': out.append((tag, t))
    return out

def render(blocks):
    o = []
    for tag, v in blocks:
        if tag in ('ul', 'ol'):
            o.append(f'<{tag}>' + ''.join(f'<li>{x}</li>' for x in v) + f'</{tag}>')
        elif tag == 'table':
            head, *rest = v
            th = ''.join(f'<th scope="col">{c}</th>' for _, c in head)
            tb = ''.join('<tr>' + ''.join(f'<{k}>{c}</{k}>' for k, c in r) + '</tr>' for r in rest)
            o.append(f'<div class="art__tw"><table class="art__t"><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')
        elif tag == 'h4':
            o.append(f'<h3>{v}</h3>')
        else:
            o.append(f'<{tag}>{v}</{tag}>')
    return '\n'.join(o)

def words(blocks):
    n = 0
    for tag, v in blocks:
        t = ' '.join(v) if tag in ('ul', 'ol') else (' '.join(c for r in v for _, c in r) if tag == 'table' else v)
        n += len(re.sub(r'<[^>]+>', ' ', t).split())
    return n
