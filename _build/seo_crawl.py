# Inwentaryzacja SEO obecnej strony jachtymazury.pl: każdy adres z sitemap.xml + adresy znalezione w linkach.
import re, json, os, html as H, urllib.request, urllib.parse, concurrent.futures as cf
BASE = 'https://jachtymazury.pl'
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh) SEO-inventory'}

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    class NoRedir(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k): return None
    op = urllib.request.build_opener(NoRedir)
    try:
        r = op.open(req, timeout=30); return r.status, r.headers.get('Location'), r.read().decode('utf-8', 'ignore')
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get('Location'), ''
    except Exception as e:
        return 0, None, ''

def t(x): return H.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x or ''))).strip()
def meta(s, attr, name):
    m = re.search(rf'<meta[^>]+{attr}=["\']{re.escape(name)}["\'][^>]*>', s, re.I)
    if not m: return None
    c = re.search(r'content=["\']([^"\']*)["\']', m.group(0), re.I)
    return H.unescape(c.group(1)) if c else None

def parse(url, s):
    body = re.sub(r'<script(?![^>]*ld\+json).*?</script>|<style.*?</style>', '', s, flags=re.S)
    main = re.sub(r'<header.*?</header>|<footer.*?</footer>', '', body, flags=re.S)
    d = {
        'title': t((re.search(r'<title[^>]*>(.*?)</title>', s, re.S) or [None, ''])[1]),
        'description': meta(s, 'name', 'description'),
        'robots': meta(s, 'name', 'robots'),
        'canonical': (re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', s) or [None, None])[1],
        'hreflang': dict(re.findall(r'<link[^>]+rel=["\']alternate["\'][^>]+hreflang=["\']([^"\']+)["\'][^>]+href=["\']([^"\']+)', s)),
        'og': {k: meta(s, 'property', 'og:' + k) for k in ('title', 'description', 'image', 'type', 'url', 'locale', 'site_name')},
        'twitter': {k: meta(s, 'name', 'twitter:' + k) for k in ('card', 'title', 'description', 'image')},
        'lang': (re.search(r'<html[^>]+lang=["\']([^"\']+)', s) or [None, None])[1],
        'h1': [t(x) for x in re.findall(r'<h1[^>]*>(.*?)</h1>', main, re.S)],
        'h2': [t(x) for x in re.findall(r'<h2[^>]*>(.*?)</h2>', main, re.S)][:40],
        'h3': [t(x) for x in re.findall(r'<h3[^>]*>(.*?)</h3>', main, re.S)][:40],
        'jsonld': [],
        'images': [],
        'links_internal': [],
        'links_external': [],
    }
    for j in re.findall(r'<script[^>]+ld\+json[^>]*>(.*?)</script>', s, re.S):
        try: d['jsonld'].append(json.loads(j))
        except Exception: d['jsonld'].append({'_raw': j.strip()[:2000]})
    seen = set()
    for m in re.finditer(r'<img\b[^>]*>', main):
        tag = m.group(0); src = (re.search(r'\ssrc=["\']([^"\']+)', tag) or [None, None])[1]
        if not src or 'data:image' in src or src in seen: continue
        seen.add(src); alt = re.search(r'\salt=["\']([^"\']*)', tag)
        d['images'].append({'src': src, 'alt': H.unescape(alt.group(1)) if alt else None})
    ls = set()
    for m in re.finditer(r'<a\b[^>]*href=["\']([^"\'#]+)[^>]*>(.*?)</a>', main, re.S):
        href, txt = m.group(1).strip(), t(m.group(2))
        if href.startswith(('mailto:', 'tel:', 'javascript:')): continue
        full = urllib.parse.urljoin(url, href)
        key = (full, txt)
        if key in ls: continue
        ls.add(key)
        (d['links_internal'] if full.startswith(BASE) else d['links_external']).append({'href': full, 'text': txt})
    d['words'] = len(t(main).split())
    return d

def crawl():
    sm = fetch(BASE + '/sitemap.xml')[2]
    urls = re.findall(r'<loc>([^<]+)</loc>', sm)
    lastmod = dict(re.findall(r'<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>', sm))
    out = {}
    def one(u):
        code, loc, s = fetch(u)
        if s: open(f'_seo/html/{(urllib.parse.urlparse(u).path.strip("/") or "index").replace("/", "__")}.html', 'w').write(s)
        r = {'status': code, 'redirect': loc, 'in_sitemap': u in urls, 'lastmod': lastmod.get(u)}
        if s and code == 200: r.update(parse(u, s))
        return u, r
    with cf.ThreadPoolExecutor(8) as ex:
        for u, r in ex.map(one, urls): out[u] = r
    # adresy z linków, których nie ma w sitemap
    extra = set()
    for r in out.values():
        for l in r.get('links_internal', []):
            h = l['href'].split('?')[0].split('#')[0]
            if h not in out and not re.search(r'\.(jpg|jpeg|png|webp|pdf|svg|gif|css|js|xml)$', h, re.I) and '/wp-' not in h:
                extra.add(h)
    with cf.ThreadPoolExecutor(8) as ex:
        for u, r in ex.map(one, sorted(extra)): out[u] = r
    json.dump(out, open('_seo/obecna-strona.json', 'w'), ensure_ascii=False, indent=1)
    print('adresy:', len(out), '| z sitemap:', len(urls), '| spoza sitemap:', len(extra))

if __name__ == '__main__': crawl()
