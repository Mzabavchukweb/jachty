# Wyciąga treść stron jednostek z zapisanych stron obecnego serwisu (_u/*.html) — bez dopisywania czegokolwiek
import re, html as H
INLINE = None   # ustawiane przez adresy.py: zachowuje linki w treści

def _txt(x):
    return H.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x))).replace(' ,', ',').replace(' .', '.').strip()

def extract(slug):
    s = open(f'_u/{slug}.html', encoding='utf-8').read()
    s = re.sub(r'<script.*?</script>|<style.*?</style>|<header.*?</header>|<footer.*?</footer>|<nav.*?</nav>', '', s, flags=re.S)
    a = s.find('<h1')
    end = min([i for i in (s.find('ZOBACZ RÓWNIEŻ'), s.find('ZAPYTAJ O CZARTER')) if i > 0] or [len(s)])
    body = s[a:end]
    blocks = [(m.group(1), _txt(m.group(2)), m.group(2)) for m in re.finditer(r'<(h1|h2|h3|h4|p|li)\b[^>]*>(.*?)</\1>', body, re.S)]
    blocks = [(t, x, raw) for t, x, raw in blocks if x]
    h1 = next((x for t, x, _ in blocks if t == 'h1'), slug)
    desc, equip, terms = [], [], []
    mode = 'desc'
    for t, x, raw in blocks:
        up = x.upper() == x and len(x) > 3
        if t in ('h3', 'h4') and up and 'WYPOSAŻENIE' in x: mode = 'equip'; continue
        if t in ('h3', 'h4') and up and 'DANE TECHNICZNE' in x: mode = 'spec'; continue
        if t in ('h3', 'h4') and 'WARUNKI REZERWACJI' in x.upper(): mode = 'terms'; continue
        if t in ('h3', 'h4') and up and 'CENNIK' in x: mode = 'stop'; continue
        if mode == 'desc' and t in ('p', 'h3', 'h2'):
            desc.append(('h2', x) if t != 'p' else ('p', INLINE(raw) if INLINE else H.escape(x)))
        elif mode == 'equip' and t == 'li': equip.append(x.rstrip(',.'))
        elif mode == 'terms' and t == 'li': terms.append(x)
    imgs = []
    for u in re.findall(r'wp-content/uploads/([^"\'\s),]+?\.(?:jpg|jpeg|png|webp))', s[:end]):
        if 'logotyp' in u or re.search(r'-\d+x\d+\.', u): continue
        base = u.replace('-scaled.', '.')
        if base in [i.replace('-scaled.', '.') for i in imgs]: continue
        imgs.append(u)
    return dict(h1=h1, desc=desc, equip=equip, terms=terms, imgs=imgs)
