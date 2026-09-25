# Struktura adresów 1:1 z obecną stroną jachtymazury.pl. Wykonywane wewnątrz podstrony.py (po nawigacja.py).
import urllib.parse
LIVE = 'https://jachtymazury.pl'
SEO = json.load(open('_seo/obecna-strona.json'))
LIVE_MODEL_PAGES = {'Antila 27': 'czarter-jachtow-zaglowych/antila-27', 'Antila 28.2': 'czarter-jachtow-zaglowych/antila-28-2',
    'Antila 30.1 E': 'czarter-jachtow-zaglowych/antila-30-1', 'Antila 30': 'czarter-jachtow-zaglowych/antila-30',
    'Antila 33.3': 'czarter-jachtow-zaglowych/antila-33-3', 'Antila 33': 'czarter-jachtow-zaglowych/antila-33',
    'Maxus 24 Evo': 'czarter-jachtow-zaglowych/maxus-24-evo', 'Maxus 28': 'czarter-jachtow-zaglowych/maxus-28',
    'Nautic 880': 'czarter-jachtow-motorowych/nautic-880', 'Nexus 870 Revo': 'czarter-jachtow-motorowych/nexus-870-revo'}
def _units_of(m): return [u for u in SAIL + MOTOR if u[1] == m]
def has_model_page(m): return m in LIVE_MODEL_PAGES or len(_units_of(m)) >= 2
def murl(m):   # model z jedną jednostką i bez strony modelu u klienta → od razu strona jednostki (tak działa obecna strona)
    return f'model-{mslug(m)}.html' if has_model_page(m) else f'{_units_of(m)[0][0]}.html'

# plik makiety → adres docelowy (katalog, jak na obecnej stronie)
NEWPATH = {'index.html': '', 'czarter-jachtow.html': 'czarter-jachtow-gizycko/', 'jachty-zaglowe.html': 'czarter-jachtow-zaglowych/',
    'jachty-motorowe.html': 'czarter-jachtow-motorowych/', 'czarter-bez-patentu.html': 'czarter-bez-patentu/', 'houseboat-mazury.html': 'houseboat-mazury/',
    'cennik.html': 'cennik/', 'jachty-na-sprzedaz.html': 'jachty-na-sprzedaz/', 'poradnik.html': 'poradnik-czarterowy/', 'port.html': 'port/',
    'wspolpraca.html': 'inwestycje-i-posrednictwo/', 'kontakt.html': 'kontakt/', 'polityka-prywatnosci.html': 'polityka-prywatnosci/',
    'fundusze-europejskie.html': 'fundusze-europejskie/', 'filmy-szkoleniowe.html': 'filmy-szkoleniowe/', 'aktualnosci.html': 'aktualnosci/', 'wiedza.html': 'wiedza/'}
for u in SAIL + MOTOR: NEWPATH[f'{u[0]}.html'] = f'{u[0]}/'
for a in ART: NEWPATH[f'{a["slug"]}.html'] = f'{a["slug"]}/'
for m in models(SAIL + MOTOR):
    if has_model_page(m):
        NEWPATH[f'model-{mslug(m)}.html'] = LIVE_MODEL_PAGES.get(m, f'czarter-jachtow-{"zaglowych" if any(u[1] == m for u in SAIL) else "motorowych"}/{mslug(m)}') + '/'
LIVE2FLAT = {v.strip('/'): k for k, v in NEWPATH.items()}
LIVE2FLAT.update({'czarter-jachtow-zaglowych/antila-24-4': 'antila-24-4.html', 'czarter-jachtow-motorowych/calipso-750': 'calipso-750-fire-cruiser.html',
                  'bezpieczenstwo-na-jachcie-2': 'bezpieczenstwo-na-jachcie.html'})   # przekierowania 301 działające dziś na obecnej stronie

def live_to_flat(url):
    p = urllib.parse.urlparse(url)
    if p.netloc not in ('jachtymazury.pl', 'www.jachtymazury.pl') or p.path.startswith('/en/'): return None
    f = LIVE2FLAT.get(p.path.strip('/'))
    return (f + (f'#{p.fragment}' if p.fragment else '')) if f else None

def inline(frag):
    """Fragment treści z obecnej strony: zostają linki (przepięte na strony makiety), pogrubienia i kursywa."""
    def a(m):
        href = re.search(r'href=["\']([^"\']+)', m.group(1))
        if not href: return m.group(2)
        url = H.unescape(href.group(1)); f = live_to_flat(url)
        ext = '' if f else ' rel="noopener" target="_blank"'
        return f'<a class="u u--on" href="{H.escape(f or url)}"{ext}>{m.group(2)}</a>'
    frag = re.sub(r'<a\b([^>]*)>(.*?)</a>', a, frag, flags=re.S)
    frag = re.sub(r'<(/?)b>', r'<\1strong>', frag)
    frag = re.sub(r'<(?!/?(?:strong|em|a|br)\b)[^>]+>', '', frag)
    frag = re.sub(r'<(strong|em)\b[^>]*>', r'<\1>', frag)
    return re.sub(r'\s+', ' ', frag).replace(' ,', ',').replace(' .', '.').strip()

import jednostki, artykuly
jednostki.INLINE = inline
artykuly.RESOLVE = live_to_flat

# daty publikacji artykułów (BlogPosting na obecnej stronie)
def _pub(slug):
    for j in SEO.get(f'{LIVE}/{slug}/', {}).get('jsonld', []):
        for x in (j.get('@graph', [j]) if isinstance(j, dict) else j):
            if isinstance(x, dict) and x.get('datePublished'): return x['datePublished'][:10]
    return ''
for a in ART: a['date'] = _pub(a['slug'])
MIES = ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia']
def pl_date(d): return f'{int(d[8:10])} {MIES[int(d[5:7]) - 1]} {d[:4]}' if d else ''

# teksty alternatywne zdjęć z obecnej strony: nazwa pliku → alt
ALT = {}
for r in SEO.values():
    for i in r.get('images', []):
        if i.get('alt'):
            n = re.sub(r'-\d+x\d+(?=\.\w+$)', '', i['src'].split('/')[-1].split('?')[0])
            ALT.setdefault(n.replace('-scaled.', '.').lower(), i['alt'])
GAL_SRC = json.load(open('_img/galerie.json'))
def gal_alt(slug, n):
    try: fn = GAL_SRC[slug][int(n)]
    except (KeyError, IndexError, ValueError): return ''
    return ALT.get(re.sub(r'-e\d{9,}(?=\.)', '', fn).replace('-scaled.', '.').lower(), '')
