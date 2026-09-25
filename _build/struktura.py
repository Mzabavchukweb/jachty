# Ostatni krok generatora: pliki makiety → katalogi jak na obecnej stronie + dane SEO z obecnej strony.
# Wykonywane wewnątrz podstrony.py (zna NEWPATH, SEO, LIVE).
PREVIEW = True   # podgląd na GitHub Pages: noindex, żeby nie dublować treści żywej strony. Przy wdrożeniu: False.

def _is_local(u): return not re.match(r'^(?:[a-z]+:|//|#|data:)', u) and u != ''

def _resolve(u, depth):
    if not _is_local(u): return u
    path, sep, rest = re.match(r'([^?#]*)([?#]?)(.*)', u).groups()
    tail = sep + rest
    if path.endswith('.html') and path in NEWPATH: target = NEWPATH[path]
    elif path == '': return u
    else: target = path
    rel = '../' * depth + target
    return (rel or './') + tail

def _rewrite(s, depth):
    s = re.sub(r'\b(href|src|action)="([^"]*)"', lambda m: f'{m.group(1)}="{_resolve(m.group(2), depth)}"', s)
    s = re.sub(r'\b(srcset|imagesrcset)="([^"]*)"', lambda m: m.group(1) + '="' + ', '.join(
        ' '.join([_resolve(p.strip().split(' ')[0], depth)] + p.strip().split(' ')[1:]) for p in m.group(2).split(',')) + '"', s)
    s = re.sub(r'url\((assets/[^)]+)\)', lambda m: f'url({"../" * depth}{m.group(1)})', s)
    return s

def _caps(t):   # „CENNIK CZARTERU” → „Cennik czarteru”, nazwy własne wracają do właściwej formy
    if t.upper() != t: return t
    t = t.capitalize()
    for w in ['Stanica Wodna Stranda', 'Mazury', 'Giżycko', 'Antila', 'Maxus', 'Nautic', 'Nexus', 'Revo', 'Evo', 'Szlaku Wielkich Jezior Mazurskich']:
        t = re.sub(re.escape(w), w, t, flags=re.I)
    return t

def _seo_head(s, path, data):
    url = f'{LIVE}/{path}'
    s = s.replace('<html lang="pl">', f'<html lang="{(data or {}).get("lang") or "pl-PL"}">', 1)
    head = []
    if data:
        if data.get('title'): s = re.sub(r'<title>.*?</title>', f'<title>{esc(data["title"])}</title>', s, count=1, flags=re.S)
        if data.get('description'): s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(data["description"])}">', s, count=1)
        head.append(f'<link rel="canonical" href="{esc(data.get("canonical") or url)}">')
        for lang, href in data.get('hreflang', {}).items(): head.append(f'<link rel="alternate" hreflang="{lang}" href="{esc(href)}">')
        for k, v in data.get('og', {}).items():
            if v: head.append(f'<meta property="og:{k}" content="{esc(v)}">')
        for k, v in data.get('twitter', {}).items():
            if v: head.append(f'<meta name="twitter:{k}" content="{esc(v)}">')
        for j in data.get('jsonld', []):
            if isinstance(j, dict) and '_raw' in j: continue
            head.append('<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>')
        robots = data.get('robots') or 'index, follow'
        en = data.get('hreflang', {}).get('en-GB') or data.get('hreflang', {}).get('en')
        if en: s = s.replace('href="https://jachtymazury.pl/en/" lang="en"', f'href="{esc(en)}" lang="en"')
    else:
        head.append(f'<link rel="canonical" href="{url}">')   # nowa strona — nie ma jej na obecnej stronie
        robots = 'index, follow'
    head.append(f'<!-- robots po wdrożeniu: {robots} -->')
    head.append('<meta name="robots" content="noindex, nofollow">' if PREVIEW else f'<meta name="robots" content="{robots}">')
    return s.replace('</head>', '\n'.join(head) + '\n</head>', 1)

def _h1(s, data, path):
    if not data or path == '' or not data.get('h1'): return s
    m = re.search(r'(<h1\b[^>]*>)(.*?)(</h1>)', s, re.S)
    if not m: return s
    if 'uh__m' in m.group(2) and 'uh__n' not in m.group(2):   # strona modelu: H1 z obecnej strony
        return s[:m.start(2)] + f'<span class="uh__m">{esc(_caps(data["h1"][0]))}</span>' + s[m.end(2):]
    if '<span' in m.group(2): return s                         # jednostki: model + nazwa, jak na obecnej stronie
    live = _caps(data['h1'][0])
    return s[:m.start(2)] + esc(live) + s[m.end(2):]

def restructure():
    import shutil
    made = []
    for flat, path in NEWPATH.items():
        if not os.path.exists(flat): continue
        s = open(flat, encoding='utf-8').read()
        depth = path.count('/')
        data = SEO.get(f'{LIVE}/{path}')
        if data and data.get('status') != 200: data = None
        s = _h1(s, data, path)
        s = _seo_head(s, path, data)
        s = _rewrite(s, depth)
        out = path + 'index.html'
        if os.path.dirname(out): os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(s)
        if flat != out: os.remove(flat)
        made.append(out)
    # 404: podawana z dowolnej głębokości adresu, więc ścieżki liczone od katalogu projektu
    if os.path.exists('404.html'):
        s = open('404.html', encoding='utf-8').read()
        if '<base ' not in s: s = s.replace('<head>', '<head>\n<base href="/jachty/">', 1)   # tylko podgląd GitHub Pages
        s = _rewrite(s, 0)
        if 'name="robots"' not in s: s = s.replace('</head>', '<meta name="robots" content="noindex">\n</head>', 1)
        open('404.html', 'w', encoding='utf-8').write(s)
    print('  struktura adresów:', len(made), 'stron w katalogach')
    return made

MADE = restructure()

# mapa adresów, przekierowania i docelowa mapa strony
rows = [('adres na obecnej stronie', 'adres w nowej stronie', 'status', 'uwagi')]
live_pl = sorted(u for u, r in SEO.items() if r.get('in_sitemap') and '/en/' not in u)
new_paths = {f'{LIVE}/{p}' for p in NEWPATH.values()}
for u in live_pl:
    r = SEO[u]
    if r['status'] == 301: rows.append((u, r['redirect'], '301', 'przekierowanie działające na obecnej stronie — zachować'))
    elif u in new_paths: rows.append((u, u, 'ten sam adres', ''))
    else: rows.append((u, '', 'BRAK', 'do decyzji'))
for u, r in sorted(SEO.items()):
    if not r.get('in_sitemap') and r['status'] == 301 and '/en/' not in u: rows.append((u, r['redirect'], '301', 'przekierowanie spoza mapy strony — zachować'))
    if not r.get('in_sitemap') and r['status'] == 404 and '/en/' not in u and 'cdn-cgi' not in u:
        rows.append((u, '', '404 dziś', 'martwy link na obecnej stronie — nie przenosić'))
for p in sorted(set(NEWPATH.values())):
    u = f'{LIVE}/{p}'
    if u not in SEO: rows.append(('', u, 'nowa strona', ''))
for u in sorted(x for x, r in SEO.items() if '/en/' in x and r.get('in_sitemap')):
    rows.append((u, u, 'EN — do zbudowania', 'wersja angielska: treść, meta i hreflang w _seo/obecna-strona.json'))
import csv
with open('_seo/mapa-adresow.csv', 'w', newline='', encoding='utf-8') as f: csv.writer(f).writerows(rows)
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in sorted(set(NEWPATH.values()), key=lambda p: (p.count('/'), p)): sm.append(f'<url><loc>{LIVE}/{p}</loc></url>')
sm.append('</urlset>')
open('_seo/sitemap-docelowa.xml', 'w').write('\n'.join(sm) + '\n')
print('  mapa adresów:', len(rows) - 1, 'wierszy')
