#!/usr/bin/env python3
"""Generator podstron jachtymazury.pl (makieta statyczna).
Wszystkie treści pochodzą z jachtymazury.pl (zrzuty w _p/, _u/, _a/) — patrz RATIONALE.md, sekcja „Podstrony".
Uruchom z katalogu projektu:  python3 _build/podstrony.py
"""
import json, re, html as H, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
esc = H.escape

# ---------------------------------------------------------------- dane
UNITS = json.load(open('_u/data.json'))
WS = json.load(open('_img/ws.json'))
CEN = json.load(open('_p/cennik.json'))
ART = json.load(open('_a/articles.json'))

TEL = '+48 511 420 100'; TEL_H = 'tel:+48511420100'
MAIL = 'info@jachtymazury.pl'
PIN = 'https://maps.app.goo.gl/tr9a722sVFmJB8iD6'   # pinezka firmy w Mapach Google (od klientki, 29.09) — cel wszystkich linków „mapa / trasa”
GREV = 'https://share.google/dC6VqBSRLYOjmESdY'   # profil firmy w Google (link od klienta)
FB = 'https://www.facebook.com/jachtymazury/'
IG = 'https://www.instagram.com/jachtymazury.pl/'
YT = 'https://www.youtube.com/@jachtymazury'   # kanał firmy (link z obecnej strony prowadził do nieistniejącego kanału)
WA = 'https://wa.me/48511420100'   # numer potwierdzony przez klientkę 30.09
MSG = 'https://m.me/jachtymazury'  # Messenger strony facebook.com/jachtymazury

# poprawki tabel, w których brakowało jednej wartości (uzupełnione z opisu na tej samej stronie jednostki)
FIX = {
 'calipso-750-fire-cruiser': {'Zamykane kabiny': '2', 'Wysokość kabiny': '1.90 m', 'Typ silnika': 'przyczepny', 'Moc silnika': '30 KM', 'Rok produkcji': '2020'},
 'maxus-28-prawy-hals': {'Zamykane kabiny': '2', 'Wysokość kabiny': '1.85 m', 'Typ silnika': 'przyczepny', 'Powierzchnia żagli': '39 m²', 'Rok produkcji': '2019'},
 'nautic-880-cuba-libre': {'Zamykane kabiny': '–', 'Typ silnika': 'przyczepny', 'Moc silnika': '50 KM', 'Rok produkcji': '2023', 'Wysokość kabiny': '–'},
 'nautic-880-mojito': {'Zamykane kabiny': '–', 'Typ silnika': 'przyczepny', 'Moc silnika': '50 KM', 'Rok produkcji': '2023', 'Wysokość kabiny': '–'},
 'nexus-870-revo-bolek': {'Zamykane kabiny': '–', 'Wysokość kabiny': '1.86 m', 'Typ silnika': 'przyczepny', 'Moc silnika': '25 KM', 'Rok produkcji': '2018'},
}
for k, v in FIX.items(): UNITS[k]['spec'].update(v)

# lista floty wg strony głównej jachtymazury.pl (16 żaglowych, 7 motorowych) + Stillo 31 (ma stronę i stawki w cenniku)
SAIL = [('antila-34-progresja','Antila 34','Progresja','Antila 34 2025/2026'),
        ('antila-33-3-infinitum','Antila 33.3','Infinitum','Antila 33.3'),
        ('antila-33-kassari','Antila 33','Kassari','Antila 33'),
        ('antila-33-strega','Antila 33','Strega','Antila 33'),
        ('antila-33-biala-perla','Antila 33','Biała Perła','Antila 33'),
        ('antila-30-1-e-cleopatra','Antila 30.1','Cleopatra','Antila 30.1 - 2026'),
        ('antila-30-1-bradl','Antila 30.1','Bradl','Antila 30.1'),   # dopisany 29.09: jest na obecnej stronie (w mapie strony i na stronie modelu Antila 30.1), w cenniku i w IBS
        ('antila-30-tutto-bene','Antila 30','Tutto Bene','Antila 30'),
        ('antila-30-sarema','Antila 30','Sarema','Antila 30'),
        ('antila-28-2-pakri','Antila 28.2','Pakri','Antila 28.2'),
        ('antila-27-marmolada','Antila 27','Marmolada','Antila 27'),
        ('antila-27-hiuma','Antila 27','Hiuma','Antila 27'),
        ('antila-27-furaha','Antila 27','Furaha','Antila 27'),
        ('antila-27-ramzesowa','Antila 27','Ramzesowa','Antila 27'),
        ('maxus-28-prawy-hals','Maxus 28','Prawy Hals','Maxus 28'),
        ('antila-24-4','Antila 24.4','','—'),
        ('maxus-24-evo-waski','Maxus 24 Evo','Wąski','Maxus 24 Evo')]
MOTOR = [('stillo-31-star','Stillo 31','Star','Stillo 31 "Star"'),
         ('nautiner-38-black-stilo','Nautiner 38','Blask Stilo','Nautiner 38 "Blask Stilo"'),
         ('nautic-880-cuba-libre','Nautic 880','Cuba Libre','Nautic 880'),
         ('nautic-880-mojito','Nautic 880','Mojito','Nautic 880'),
         ('nexus-870-revo-wiktor','Nexus 870 Revo','Wiktor','Nexus 870 Revo "Wiktor"'),
         ('nexus-870-revo-bolek','Nexus 870 Revo','Bolek','—'),
         ('futura-860-eufemia','Futura 860','Eufemia','Futura 860 "Eufemia"'),
         ('calipso-750-fire-cruiser','Calipso 750','Fire Cruiser','—')]

HEAD_COLS = CEN[0][0][2:]   # nagłówki okresów + kaucja + sprzątanie
ROWS = {r[1]: r[2:] for t in CEN for r in t[1:]}
DOBA_IDX = [0, 2, 4, 5, 6, 7, 8, 9, 10]      # kolumny „za dobę”

def od(row):
    v = ROWS.get(row)
    if not v: return None
    nums = [int(v[i]) for i in DOBA_IDX if v[i].strip().isdigit()]
    return min(nums) if nums else None

def zl(n): return f'{n:,}'.replace(',', ' ') + '&nbsp;zł'

# ---------------------------------------------------------------- wspólne fragmenty
NAV_ITEMS = [('jachty-na-sprzedaz.html','Na sprzedaż'),('poradnik.html','Poradnik'),('cennik.html','Cennik'),
             ('port.html','Port'),('wspolpraca.html','Współpraca'),('kontakt.html','Kontakt')]
CZ_ITEMS = [('jachty-zaglowe.html','Jachty żaglowe'),('jachty-motorowe.html','Jachty motorowe'),('czarter-bez-patentu.html','Czarter bez patentu')]

def nav(cur):
    cz_cur = cur in [h for h, _ in CZ_ITEMS]
    menu = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a>' for h, t in CZ_ITEMS)
    items = ''.join(f'\n      <a class="u{" u--on" if h == cur else ""}" href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a>' for h, t in NAV_ITEMS)
    return (f'''<nav class="nav" aria-label="Główne">
      <div class="has{" is-cur" if cz_cur else ""}"><button class="nav__b" type="button" aria-expanded="false" aria-controls="m-czarter">Czarter jachtów <i data-lucide="chevron-down" class="lucide"></i></button>
        <div class="menu" id="m-czarter">{menu}</div></div>{items}
    </nav>''')

def mnav(cur):
    links = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a></li>' for h, t in [('index.html','Start')] + CZ_ITEMS + NAV_ITEMS)
    return (f'''<div class="mnav" id="mnav" hidden>
  <nav class="mnav__in" aria-label="Menu">
    <ul class="mnav__l">{links}</ul>
    <div class="mnav__cta">
      <a class="btn btn--block" href="#rezerwuj" data-open-modal>Sprawdź dostępność <i data-lucide="arrow-right" class="lucide"></i></a>
      <a class="btn btn--outline btn--block" href="{TEL_H}"><i data-lucide="phone" class="lucide"></i> {TEL}</a>
      <p class="mnav__meta">Biuro 8:00 – 20:00, siedem dni w tygodniu · <a href="mailto:{MAIL}">{MAIL}</a></p>
    </div>
  </nav>
</div>''')

LANG = '<nav class="head__lang" aria-label="Wybór języka"><a href="#" aria-current="true" lang="pl">PL</a><span aria-hidden="true">·</span><a href="https://jachtymazury.pl/en/" lang="en" hreflang="en" aria-label="English version">EN</a></nav>'

def header(cur, photo=False, dark=False):
    logo = ('<img class="head__logo head__logo--mono" src="assets/img/logo-mono.png" width="450" height="76" alt="Jachtymazury.pl"><img class="head__logo head__logo--color" src="assets/img/logo.png" width="450" height="76" alt="">'
            if photo or dark else '<img class="head__logo" src="assets/img/logo.png" width="450" height="76" alt="Jachtymazury.pl">')
    btn = ('<a class="btn btn--outline" href="#rezerwuj" data-open-modal>Rezerwuj online</a>' if photo else '<a class="btn" href="#rezerwuj" data-open-modal>Rezerwuj online</a>')
    return (f'''<header class="head{" on-photo" if photo else ""}{" head--dark" if dark else ""}" id="head">
  <div class="wrap head__bar">
    <a href="index.html" aria-label="Jachty Mazury — strona główna">{logo}</a>
    {nav(cur)}
    {LANG}
    {btn}
    <button class="burger" type="button" aria-label="Otwórz menu" aria-expanded="false" aria-controls="mnav"><i data-lucide="menu" class="lucide burger__m"></i><i data-lucide="x" class="lucide burger__x"></i></button>
  </div>
</header>
{mnav(cur)}''')

FOOT = f'''<footer class="inkband foot on-dark" id="kontakt">
  <div class="wrap">
    <div class="g12">
      <div class="c4"><img class="foot__logo" src="assets/img/logo-mono.png" width="450" height="76" alt="Jachtymazury.pl"><p>Czarter jachtów żaglowych, motorowych i houseboatów ze Stanicy Wodnej Stranda w Giżycku.</p></div>
      <div class="c3"><span class="micro">Kontakt</span>
        <ul class="foot__list"><li>Stanica Wodna Stranda</li><li>Pierkunowo 36</li><li class="num">11-500 Giżycko</li><li class="num"><a class="u" href="{TEL_H}">{TEL}</a></li><li><a class="u" href="mailto:{MAIL}">{MAIL}</a></li></ul></div>
      <div class="c3"><span class="micro">Biuro</span><ul class="foot__list"><li class="num">8:00 – 20:00</li><li>siedem dni w tygodniu</li></ul></div>
      <div class="c2"><span class="micro">Social</span><ul class="foot__list"><li><a class="u" href="{FB}" rel="noopener" target="_blank">Facebook</a></li><li><a class="u" href="{IG}" rel="noopener" target="_blank">Instagram</a></li><li><a class="u" href="{YT}" rel="noopener" target="_blank">YouTube</a></li></ul></div>
    </div>

    <div class="ue">
      <a class="ue__img" href="fundusze-europejskie.html" aria-label="Fundusze Europejskie — szczegóły dofinansowania">
        <picture><source type="image/webp" srcset="assets/img/r/ue-logotypy-630.webp 630w, assets/img/r/ue-logotypy-1260.webp 1260w, assets/img/r/ue-logotypy-1890.webp 1890w" sizes="(min-width:768px) 560px, 100vw">
        <img src="assets/img/r/ue-logotypy-630.png" srcset="assets/img/r/ue-logotypy-630.png 630w, assets/img/r/ue-logotypy-1260.png 1260w, assets/img/r/ue-logotypy-1890.png 1890w" sizes="(min-width:768px) 560px, 100vw" width="630" height="57" alt="Fundusze Europejskie dla Warmii i Mazur, Rzeczpospolita Polska, Dofinansowane przez Unię Europejską, Warmia Mazury" decoding="async"></picture>
      </a>
      <p class="ue__txt">Projekt dofinansowany ze środków Unii Europejskiej. <a class="u u--on" href="fundusze-europejskie.html">Szczegóły dofinansowania →</a></p>
    </div>

    <div class="foot__bot"><span>© 2026 jachtymazury.pl</span><span class="num">Pierkunowo 36, 11-500 Giżycko</span><span><a class="u" href="fundusze-europejskie.html">Fundusze Europejskie</a> · <a class="u" href="polityka-prywatnosci.html">Polityka prywatności</a></span></div>
  </div>
</footer>'''

exec(open(os.path.join(ROOT, '_build/nawigacja.py'), encoding='utf-8').read())   # nowa nawigacja i stopka
exec(open(os.path.join(ROOT, '_build/adresy.py'), encoding='utf-8').read())      # struktura adresów 1:1 z obecną stroną

CALL = f'''<div class="fabs">
  <a class="fabx fabx--wa" href="{WA}" rel="noopener" target="_blank" aria-label="Napisz na WhatsApp" title="WhatsApp"><img src="assets/img/ikony/whatsapp-bialy.png" width="26" height="26" alt=""></a>
  <a class="fabx fabx--ms" href="{MSG}" rel="noopener" target="_blank" aria-label="Napisz na Messengerze" title="Messenger"><img src="assets/img/ikony/messenger-bialy.png" width="24" height="24" alt=""></a>
</div>
<a class="callfab" href="{TEL_H}" aria-label="Zadzwoń: {TEL}" title="{TEL}">
  <span class="callfab__ico" aria-hidden="true"><i data-lucide="phone" class="lucide"></i><span class="callfab__fb">✆</span></span>
</a>'''

# R1: okno rezerwacji na każdej stronie — harmonogram IBS (kod od klientki 29.09, wersja testowa); ramka ładuje się przy pierwszym otwarciu
BOOK = f'''<div class="bk" id="rezerwuj-okno" role="dialog" aria-modal="true" aria-labelledby="bk-h" hidden>
  <div class="bk__bg" data-close-modal></div>
  <div class="bk__p bk__p--ibs">
    <div class="bk__hd"><h2 class="h3" id="bk-h">Sprawdź dostępność i zarezerwuj</h2>
      <button class="bk__x" type="button" data-close-modal aria-label="Zamknij okno rezerwacji"><i data-lucide="x" class="lucide"></i></button></div>
    <iframe class="bk__f" title="Rezerwacja czarteru — wybór jednostki i terminu" data-src="https://beta.ibs-integra.pl/ClientScheduler?pointOfServiceCode=jachty-mazury&amp;embed=1"></iframe>
    <p class="bk__alt">Wolisz zadzwonić? <a class="u u--on num" href="{TEL_H}">{TEL}</a> · biuro codziennie 8:00 – 20:00</p>
  </div>
</div>'''

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400;1,6..72,500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">'

def page(fname, title, desc, body, cur, extra_js=''):
    out = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" href="assets/img/mark.png">
{FONTS}
<link rel="stylesheet" href="assets/css/system.css">
<link rel="stylesheet" href="assets/css/pages.css">
<link rel="stylesheet" href="assets/css/mobile.css">
</head>
<body class="sub">
<a class="skip" href="#main">Przejdź do treści</a>

{header(cur, dark=True)}

<main id="main">
{body}
</main>

{FOOT}

{CALL}
{BOOK}

<script src="https://unpkg.com/lucide@latest" defer></script>
<script src="assets/js/site.js" defer></script>
{extra_js}
</body>
</html>
'''
    open(fname, 'w').write(out)
    print('  →', fname, len(out))

def crumbs(items):
    return ''   # okruszki usunięte z hero na wszystkich stronach (uwagi klientki 29.09, zadanie G3)
    lis = ''.join(f'<li><a class="u" href="{h}">{t}</a></li>' for h, t in items[:-1])
    return f'<nav aria-label="Okruszki"><ol class="crumbs"><li><a class="u" href="index.html">Start</a></li>{lis}<li aria-current="page">{items[-1][1]}</li></ol></nav>'

# grafiki nagłówków podstron — osobny zestaw; pokazują się dopiero, gdy plik istnieje
PDECO = {'jachty-zaglowe.html': 'p-zaglowe', 'jachty-motorowe.html': 'p-motorowe', 'czarter-bez-patentu.html': 'p-bez-patentu',
         'cennik.html': 'p-cennik', 'jachty-na-sprzedaz.html': 'p-sprzedaz', 'poradnik.html': 'p-poradnik', 'port.html': 'p-port',
         'wspolpraca.html': 'p-wspolpraca', 'kontakt.html': 'p-kontakt'}
def phead(cr, eyebrow, h1, lead=''):
    d = PDECO.get(cr[-1][0])
    if d and not os.path.exists(os.path.join(ROOT, 'assets/img/deco', d + '-c.webp')): d = None
    deco = f'<span class="deco deco--{d}" aria-hidden="true"></span>' if d else ''
    return (f'''<section class="phead{f" phead--{d}" if d else ""}">
  {deco}
  <div class="wrap">
    {crumbs(cr)}
    {f'<p class="micro phead__eye">{eyebrow}</p>' if eyebrow else ''}
    <h1 class="h1 phead__h">{h1}</h1>
    {f'<p class="phead__lead">{lead}</p>' if lead else ''}
  </div>
</section>''')

def pic(key, alt, sizes, eager=False):
    ws, w, h = WS[key]
    f = lambda e: ', '.join(f'assets/img/r/{key}-{x}.{e} {x}w' for x in ws)
    mid = min(ws, key=lambda x: abs(x - 600))
    lazy = ''   # bez leniwego ładowania: na części iPhone'ów leniwe zdjęcia w <picture> nie wczytywały się wcale
    return (f'<picture><source type="image/webp" srcset="{f("webp")}" sizes="{sizes}">'
            f'<img src="assets/img/r/{key}-{mid}.jpg" srcset="{f("jpg")}" sizes="{sizes}" width="{w}" height="{h}" alt="{esc(alt)}"{lazy} decoding="async"></picture>')

# ---------------------------------------------------------------- karta jednostki
MAXM = 12.0
SCALE = '<div class="meas__sc" aria-hidden="true">' + ''.join(f'<i style="left:{round(v/MAXM*100,2)}%">{v}{" m" if v == 12 else ""}</i>' for v in (0,2,4,6,8,10,12)) + '</div>'

def num(s): return float(re.sub(r'[^\d.,]', '', s).replace(',', '.') or 0)
def pl(s): return s.replace('.', ',')

def berths(raw):
    raw = raw.strip()
    m = re.match(r'max\s*(\d+)', raw)
    if m: return m.group(1), int(m.group(1)), 0
    m = re.match(r'(\d+)\s*\(max\s*(\d+)\)', raw)
    if m: a, b = int(m.group(1)), int(m.group(2)); return f'{a} + {b-a}', a, b - a
    m = re.match(r'(\d+)', raw)
    if m: return m.group(1), int(m.group(1)), 0
    return raw, 0, 0

def card(slug, model, name, row, detail=None):
    if detail is None: detail = f'{slug}.html'
    sp = UNITS[slug]['spec']
    L = num(sp.get('Długość', '0')); pct = min(100, round(L / MAXM * 100, 1))
    mj, a, b = berths(sp.get('Liczba osób', '–'))
    tk = ''.join('<i></i>' for _ in range(a)) + ''.join('<i class="x"></i>' for _ in range(b))
    kab = sp.get('Zamykane kabiny', '–'); kab = kab
    zan = sp.get('Zanurzenie', '–'); zan = pl(zan.replace('-', ' / ')) if zan not in ('–', '') else '–'
    rok = sp.get('Rok produkcji', '–')
    p = od(row)
    price = (f'<span class="fli__k">Cena od</span><span class="fli__pricev"><b>{zl(p)}</b> <span class="per">/ doba</span></span>' if p
             else '<span class="fli__k">Cena</span><span class="fli__pricev fli__pricev--ask">na zapytanie</span>')
    full = f'{model} „{name}”' if name else model
    title = "„" + name + "”" if name else model
    has = detail != '#'
    nm = f'<span class="fli__model">{model}</span>' + (f'<a class="u" href="{detail}">{title}</a>' if has else title)
    ph = pic("u-" + slug, full, "(min-width:641px) 440px, 100vw")
    ph = f'<a class="fli__ph" href="{detail}" tabindex="-1" aria-hidden="true">{ph}</a>' if has else f'<div class="fli__ph">{ph}</div>'
    see = f'<a class="btn btn--outline btn--sm" href="{detail}" aria-label="Zobacz jacht {esc(full)}">Zobacz jacht <i data-lucide="arrow-right" class="lucide"></i></a>' if has else ''
    return f'''      <article class="fli" data-model="{esc(model)}">
        {ph}
        <div class="fli__body">
          <h3 class="fli__name">{nm}</h3>
          <dl class="fli__spec num">
            <div><dt>Miejsca</dt><dd>{mj}</dd><div class="berth" aria-hidden="true">{tk}</div></div>
            <div><dt>Kabiny</dt><dd>{kab}</dd></div>
            <div><dt>Zanurzenie</dt><dd>{zan}{" m" if zan not in ("–",) and not zan.endswith("m") else ""}</dd></div>
            <div><dt>Rok produkcji</dt><dd>{rok}</dd></div>
          </dl>
          <div class="meas"><div class="meas__hd"><span>Długość całkowita</span><b>{pl(f"{L:.2f}")} m</b></div>
            <div class="meas__t" aria-hidden="true"><span class="meas__b" style="width:{pct}%"></span></div>{SCALE}</div>
          <div class="fli__buy">
            <div class="fli__price">{price}</div>
            <div class="fli__act">{see}<a class="btn btn--sm" href="#rezerwuj" data-open-modal aria-label="Rezerwuj {esc(full)}">Rezerwuj</a></div>
          </div>
        </div>
      </article>
'''

def chips(units):
    models = []
    for u in units:
        if u[1] not in models: models.append(u[1])
    cnt = {m: sum(1 for u in units if u[1] == m) for m in models}
    b = f'<button class="chip" type="button" data-f="*" aria-pressed="true">Wszystkie <span class="n num">{len(units)}</span></button>'
    b += ''.join(f'<button class="chip" type="button" data-f="{esc(m)}" aria-pressed="false">{m} <span class="n num">{cnt[m]}</span></button>' for m in models)
    return f'<div class="chips" role="group" aria-label="Filtr modeli">{b}</div>'

def fleet_list(units, sand=False):
    cards = ''.join(card(s, m, n, r) for s, m, n, r in units)
    return f'''<section class="psec fleet{" fleet--sand" if sand else ""}">
  <div class="wrap">
    {chips(units)}
    <p class="chips__st micro muted" aria-live="polite"></p>
    <div class="fl" data-fl>
{cards}    </div>
  </div>
</section>'''

def cta(h, p):
    return f'''<section class="inkband band pcta on-dark on-photo">
  <div class="wrap pcta__in">
    <div><h2 class="h2">{h}</h2><p class="pcta__p">{p}</p></div>
    <div class="pcta__b"><a class="btn" href="#rezerwuj" data-open-modal>Sprawdź dostępność <i data-lucide="arrow-right" class="lucide"></i></a>
      <a class="btn btn--outline" href="{TEL_H}"><i data-lucide="phone" class="lucide"></i> {TEL}</a></div>
  </div>
</section>'''

# ================================================================= PODSTRONY
print('Podstrony:')

# ---- jachty żaglowe
page('jachty-zaglowe.html', 'Jachty żaglowe — czarter na Mazurach, Giżycko | Jachty Mazury',
 'Czarter jachtów żaglowych Antila i Maxus ze Stanicy Wodnej Stranda w Giżycku. Dane techniczne i ceny z cennika 2027.',
 phead([('czarter-jachtow.html', 'Czarter jachtów'), ('jachty-zaglowe.html', 'Jachty żaglowe')], f'{len(SAIL)} jednostek', 'Jachty żaglowe',
       'W ofercie znajdują się zarówno jachty motorowe, jak i klasyczne konstrukcje pod żagle, a nasza flota jest regularnie serwisowana i przygotowana do sezonu. W katalogu dostępne są modele takie jak Antila czy Maxus.')
 + fleet_list(SAIL)
 + cta('Nie wiesz, który jacht wybrać?', 'Zadzwoń — pomożemy dobrać jednostkę do liczby osób i planowanej trasy.'),
 'jachty-zaglowe.html')

# ---- jachty motorowe
page('jachty-motorowe.html', 'Jachty motorowe i houseboaty — czarter na Mazurach | Jachty Mazury',
 'Czarter jachtów motorowych i houseboatów z Giżycka. Wiele jednostek można prowadzić bez patentu.',
 phead([('czarter-jachtow.html', 'Czarter jachtów'), ('jachty-motorowe.html', 'Jachty motorowe')], f'{len(MOTOR)} jednostek, w tym houseboaty', 'Jachty motorowe',
       'Nie trzeba być zawodowym sternikiem ani posiadać wieloletniego doświadczenia. Wiele jednostek można prowadzić nawet bez formalnych uprawnień, a przed wypłynięciem zapewniamy szczegółowe szkolenie z obsługi.')
 + fleet_list(MOTOR)
 + cta('Pierwszy rejs motorówką?', 'Przed wypłynięciem przeszkolimy Cię z obsługi jednostki i zasad bezpieczeństwa.'),
 'jachty-motorowe.html')

# ---- czarter bez patentu
BEZ = [u for u in MOTOR if u[0] != 'stillo-31-star']
page('czarter-bez-patentu.html', 'Czarter bez patentu na Mazurach — houseboaty i motorówki | Jachty Mazury',
 'Jachty motorowe i houseboaty, które można prowadzić bez patentu: silnik do 75 kW, kadłub do 13 m, prędkość do 15 km/h.',
 phead([('czarter-jachtow.html', 'Czarter jachtów'), ('czarter-bez-patentu.html', 'Czarter bez patentu')], 'Czarter jachtów', 'Czarter bez patentu',
       'Oferta dla osób, które chcą wypocząć na wodzie bez konieczności posiadania uprawnień: jachty motorowe oraz houseboaty, które można prowadzić legalnie i bezpiecznie bez patentu motorowodnego.')
 + f'''<section class="psec">
  <div class="wrap g12">
    <div class="c7 prose reveal">
      <h2 class="h3">Kiedy nie potrzebujesz patentu</h2>
      <p>Wynajem łodzi bez patentu jest możliwy w przypadku jednostek, które spełniają trzy warunki jednocześnie:</p>
    </div>
    <dl class="c12 rules num reveal">
      <div><dt>Moc silnika</dt><dd>do 75&nbsp;kW</dd></div>
      <div><dt>Długość kadłuba</dt><dd>do 13&nbsp;m</dd></div>
      <div><dt>Prędkość</dt><dd>do 15&nbsp;km/h</dd><p>ograniczona konstrukcyjnie</p></div>
    </dl>
    <div class="c7 prose reveal">
      <p>Dzięki temu czarter jachtu bez uprawnień na Mazurach jest dostępny dla szerokiego grona klientów — również bez wcześniejszego szkolenia czy patentu.</p>
      <p>Przed rozpoczęciem rejsu zapewniamy <strong>szkolenie z obsługi jednostki oraz zasad bezpieczeństwa</strong>, co pozwala spokojnie rozpocząć czarter i komfortowo poruszać się po szlaku Wielkich Jezior Mazurskich. Houseboaty i łodzie motorowe bez patentu to wygodna forma wypoczynku, szczególnie ceniona przez rodziny i osoby szukające spokojnego rejsu.</p>
    </div>
  </div>
</section>
<section class="psec fleet">
  <div class="wrap">
    <h2 class="h3 psec__h">Jednostki dostępne bez patentu</h2>
    <div class="fl" data-fl>
{''.join(card(s, m, n, r) for s, m, n, r in BEZ)}    </div>
  </div>
</section>'''
 + cta('Masz pytania do naszej oferty?', 'Skontaktuj się — biuro czynne codziennie od 8:00 do 20:00.'),
 'czarter-bez-patentu.html')

# ---- cennik
periods = []
for h in HEAD_COLS[:11]:
    t = h.replace('....', '…').replace('...', '…')
    tag = ' <span class="ptag">−5%</span>' if '-5%' in t else ''
    t = t.replace(' -5%', '')
    unit = 'za okres' if 'za okres' in t else 'za dobę'
    rng = t.replace(' za dobę', '').replace(' za okres', '').strip()
    rng = re.sub(r'^…\s*', 'do ', rng); rng = re.sub(r'\s*…$', ' i później', rng)
    parts = rng.split(' ')
    if len(parts) == 2 and parts[0][0].isdigit(): rng = f'{parts[0]} – {parts[1]}'
    if rng.startswith('od '): pass
    if rng.endswith(' i później'): rng = 'od ' + rng.replace(' i później', '')
    periods.append((rng, unit, tag))

def row_photo(name):
    """Zdjęcie do wiersza cennika: jednostka przypisana do wiersza, a gdy jej nie ma — jednostka tego samego modelu."""
    units = SAIL + MOTOR
    for u in units:
        if u[3] == name: return u
    for u in sorted(units, key=lambda u: -len(u[1])):
        if name.startswith(u[1]) or u[1].startswith(name): return u
    return None

def thumb(name, cls):
    u = row_photo(name)
    if not u: return f'<span class="{cls} {cls}--none" aria-hidden="true"></span>'
    ws, w, h = WS['u-' + u[0]]; small = min(ws)
    return (f'<span class="{cls}" aria-hidden="true"><picture><source type="image/webp" srcset="assets/img/r/u-{u[0]}-{small}.webp">'
            f'<img src="assets/img/r/u-{u[0]}-{small}.jpg" width="{w}" height="{h}" alt="" decoding="async"></picture></span>')

def ctable(tab):
    th = ''.join(f'<th scope="col"><span class="num">{r}</span><small>{u}</small>{g}</th>' for r, u, g in periods)
    body = ''
    for row in tab[1:]:
        name, v = row[1], row[2:]
        tds = ''.join(f'<td class="num">{zl(int(x)) if x.strip().isdigit() else "<span class=muted>—</span>"}</td>' for x in v[:11])
        u = row_photo(name); href = murl(u[1]) if u else ''
        cell = f'<span class="cen__y">{thumb(name, "cen__ph")}<span>{esc(name)}</span></span>'
        body += f'<tr><th scope="row">{f'<a class="cen__a" href="{href}">{cell}</a>' if href else cell}</th>{tds}<td class="num">{zl(int(v[11]))}</td><td class="num">{zl(int(v[12]))}</td></tr>'
    return f'<div class="ctab" tabindex="0" role="region" aria-label="Tabela cen, przewijaj poziomo"><table class="cen"><thead><tr><th scope="col">Jacht</th>{th}<th scope="col">Kaucja</th><th scope="col">Sprzątanie</th></tr></thead><tbody>{body}</tbody></table></div>'

def cmobile(tab):
    out = ''
    for row in tab[1:]:
        name, v = row[1], row[2:]
        nums = [int(v[i]) for i in DOBA_IDX if v[i].strip().isdigit()]
        head = f'od {zl(min(nums))} / doba' if nums else 'cena indywidualna'
        lis = ''.join(f'<li><span>{r}{g}</span><b class="num">{zl(int(x)) if x.strip().isdigit() else "—"}<small> {u}</small></b></li>' for (r, u, g), x in zip(periods, v[:11]))
        out += f'''<details class="cmob"><summary>{thumb(name, "cmob__ph")}<span class="cmob__n">{esc(name)}</span><span class="cmob__p num">{head}</span></summary>
  <ul class="cmob__l">{lis}<li class="cmob__x"><span>Kaucja</span><b class="num">{zl(int(v[11]))}</b></li><li class="cmob__x"><span>Sprzątanie</span><b class="num">{zl(int(v[12]))}</b></li>{f'<li class="cmob__lnk"><a class="u u--on" href="{murl(row_photo(name)[1])}">Zobacz jacht →</a></li>' if row_photo(name) else ''}</ul></details>'''
    return f'<div class="cmobs">{out}</div>'

page('cennik.html', 'Cennik czarteru jachtów 2027 | Jachty Mazury',
 'Cennik czarteru jachtów żaglowych i motorowych na sezon 2027: stawki za dobę i za okres, kaucje, sprzątanie, rabaty i opłaty dodatkowe.',
 phead([('cennik.html', 'Cennik')], 'Sezon 2027 · ceny brutto', 'Cennik czarteru jachtów 2027',
       'Cena za dobę obowiązuje przy czarterze minimum tygodniowym. Przy krótszych terminach cena ustalana jest indywidualnie.')
 + f'''<section class="psec">
  <div class="wrap">
    <div class="hours num reveal">
      <div><span class="micro muted">Wydanie jachtu</span><b>16:00 – 20:00</b></div>
      <div><span class="micro muted">Zdanie jachtu</span><b>8:00 – 10:00</b></div>
      <div><span class="micro muted">Inne godziny</span><b>do ustalenia</b></div>
    </div>
    <h2 class="h3 psec__h">Jachty żaglowe</h2>
    {ctable(CEN[0])}{cmobile(CEN[0])}
    <h2 class="h3 psec__h">Jachty motorowe</h2>
    {ctable(CEN[1])}{cmobile(CEN[1])}
    <p class="note">„—” — stawka ustalana indywidualnie. Oznaczenie <span class="ptag">−5%</span> pochodzi z cennika. Wszystkie ceny podane na stronie są cenami brutto i nie zawierają rabatów.</p>
  </div>
</section>
<section class="psec psec--sand">
  <div class="wrap g12 war">
    <section class="c4 war__b reveal"><h2 class="war__h">W cenie</h2>
      <ul class="war__l"><li>Ubezpieczenie</li><li>Serwis na szlaku w przypadku awarii z winy armatora</li><li>Nabita butla gazowa</li><li>Zatankowany zbiornik wody</li>
      <li>Zatankowany zbiornik paliwa — jacht zwracasz z pełnym zbiornikiem</li><li>Pusty zbiornik na fekalia — jacht zwracasz z pustym zbiornikiem</li></ul></section>
    <section class="c4 war__b reveal"><h2 class="war__h">Rabaty</h2>
      <ul class="war__l num"><li><b>5%</b> — klienci pływający z nami co najmniej dwa sezony</li><li><b>5%</b> — czarter dwutygodniowy</li>
      <li><b>5%</b> — studenci w maju, czerwcu i wrześniu (od poniedziałku do czwartku)</li></ul></section>
    <section class="c4 war__b reveal"><h2 class="war__h">Opłaty dodatkowe</h2>
      <p class="war__sub">Obligatoryjne</p>
      <dl class="war__d num"><div><dt>Dopłata za krótki czarter</dt><dd>indywidualnie</dd></div>
        <div><dt>Sprzątanie porejsowe</dt><dd>wg tabeli</dd></div></dl>
      <p class="war__tiny">Sprzątanie obejmuje mycie powierzchni użytkowych, odkurzanie i mycie pokładu. Nie obejmuje mycia naczyń (50 zł) ani klarowania pokładu i bakist (50 zł).</p>
      <p class="war__sub">Nieobligatoryjne</p>
      <dl class="war__d num"><div><dt>Wynajem sternika</dt><dd>od 300 zł / dzień</dd></div><div><dt>Wypożyczenie SUP-a</dt><dd>200 zł / tydzień</dd></div>
        <div><dt>Rejs one way</dt><dd>od 500 zł</dd></div><div><dt>Opróżnienie zbiornika na fekalia</dt><dd>250 zł</dd></div>
        <div><dt>Wypożyczenie pościeli</dt><dd>70 zł / komplet</dd></div><div><dt>Niezatankowany jacht motorowy</dt><dd>200 zł + paliwo</dd></div>
        <div><dt>Pies lub kot na jachcie</dt><dd>150 zł</dd></div><div><dt>Wypożyczenie sprzętu nurkowego</dt><dd>od 2000 zł / tydzień</dd></div></dl>
    </section>
  </div>
</section>''',
 'cennik.html')

# ---- jachty na sprzedaż
SALE = [('sale-antila27','Antila 27','2022','229 000',['silnik zaburtowy 9.9 KM Mercury','echosonda Garmin','trzy zamykane kabiny','kabina łazienkowa z WC morskim oraz prysznicem','prysznic zewnętrzny'],'Jacht żaglowy'),
        ('sale-antila30','Antila 30','2021','280 000',['silnik stacjonarny 21 KM Yanmar','plotter Raymarine','trzy zamykane kabiny','kabina łazienkowa z WC morskim oraz prysznicem','prysznic zewnętrzny'],'Jacht żaglowy'),
        ('sale-nautic-a','Nautic 880','2023','359 000',['silnik zaburtowy 50 KM Honda','plotter Simrad','dwie duże kabiny','kabina łazienkowa z WC morskim oraz prysznicem'],'Jacht motorowy'),
        ('sale-nautic-b','Nautic 880','2023','359 000',['silnik zaburtowy 50 KM Honda','plotter Simrad','dwie duże kabiny','kabina łazienkowa z WC morskim oraz prysznicem'],'Jacht motorowy'),
        ('sale-nexus','Nexus 870 Revo','2018','259 000',['silnik zaburtowy 25 KM Mercury','echosonda Garmin','dwie kabiny zamykane','kabina łazienkowa z WC morskim oraz prysznicem'],'Jacht motorowy'),
        ('sale-calipso','Calipso 750','2020','170 000',['silnik zaburtowy 30 KM Tohatsu','echosonda Garmin','dwie duże kabiny','kabina łazienkowa z WC morskim oraz prysznicem'],'Jacht motorowy')]
def sale_card(k, n, y, p, feats, typ):
    li = ''.join(f'<li>{f}</li>' for f in feats)
    return f'''<article class="sale reveal">
  <figure class="sale__ph">{pic(k, n, "(min-width:1024px) 400px, (min-width:641px) 50vw, 100vw")}</figure>
  <div class="sale__b">
    <p class="micro muted">{typ} · rocznik <span class="num">{y}</span></p>
    <h3 class="sale__n">{n}</h3>
    <p class="sale__p num"><b>{p}&nbsp;zł</b> <span>+ VAT</span></p>
    <ul class="sale__l">{li}</ul>
    <div class="sale__a"><a class="btn btn--outline btn--sm" href="kontakt.html">Zapytaj o jacht</a><a class="u sale__t num" href="{TEL_H}">{TEL}</a></div>
  </div>
</article>'''
page('jachty-na-sprzedaz.html', 'Jachty na sprzedaż — Antila, Nautic, Nexus, Calipso | Jachty Mazury',
 'Jachty żaglowe i motorowe na sprzedaż z floty czarterowej Jachty Mazury: rocznik, cena netto i wyposażenie.',
 phead([('jachty-na-sprzedaz.html', 'Jachty na sprzedaż')], 'Z naszej floty czarterowej', 'Jachty na sprzedaż')
 + f'''<section class="psec">
  <div class="wrap">
    <h2 class="h3 psec__h">Jachty żaglowe</h2>
    <div class="sales">{''.join(sale_card(*x) for x in SALE if x[5] == 'Jacht żaglowy')}</div>
  </div>
</section>
<section class="psec psec--sand">
  <div class="wrap">
    <h2 class="h3 psec__h">Jachty motorowe</h2>
    <div class="sales">{''.join(sale_card(*x) for x in SALE if x[5] == 'Jacht motorowy')}</div>
  </div>
</section>'''
 + cta('Chcesz obejrzeć jacht?', 'Umów się telefonicznie — jednostki stoją w Stanicy Wodnej Stranda.'),
 'jachty-na-sprzedaz.html')

# ---- poradnik
feat, rest = ART[0], ART[1:]
rows = ''.join(f'''<li class="gd reveal"><a class="gd__a" href="{a["slug"]}.html">
  <span class="gd__t">{esc(a["h1"])}</span>
  <span class="gd__l">{esc(a["lead"])}</span>
  <span class="gd__go" aria-hidden="true"><i data-lucide="arrow-right" class="lucide"></i></span></a></li>''' for a in rest)
page('poradnik.html', 'Poradnik czarterowy — koszty, trasy i wybór jachtu | Jachty Mazury',
 'Praktyczne informacje o czarterze jachtów na Mazurach: wybór jachtu, formalności, bezpieczeństwo, trasy i najlepszy termin.',
 phead([('poradnik.html', 'Poradnik')], f'{len(ART)} artykułów', 'Jak wyczarterować jacht i zaplanować rejs po Mazurach',
       'Kompletne i praktyczne informacje o czarterze jachtów na Mazurach — od wyboru jachtu, przez koszty i formalności, po planowanie tras, porty i najlepszy termin na rejs.')
 + f'''<section class="psec">
  <div class="wrap">
    <p class="micro gd__start">Zacznij tutaj</p>
    <a class="gfeat reveal" href="{feat["slug"]}.html">
      <figure class="gfeat__ph">{pic("art-" + feat["slug"], feat["h1"], "(min-width:1024px) 640px, 100vw", True)}</figure>
      <div class="gfeat__b"><h2 class="h2">{esc(feat["h1"])}</h2><p>{esc(feat["lead"])}</p><span class="u u--on gfeat__go">Czytaj przewodnik →</span></div>
    </a>
    <span class="deco deco--reeds gds__rope" aria-hidden="true"></span>
    <ul class="gds">{rows}</ul>
  </div>
</section>''',
 'poradnik.html')

# ---- port
# „Port” usunięty z menu (uwagi klientki 29.09): treść jest w Kontakcie, adres /port/ przekierowuje do kontakt/#port.
# Na produkcji ma to być 301 (wpis w _seo/mapa-adresow.csv); w makiecie — strona przekierowująca.
open('port.html', 'w').write('''<!doctype html><html lang="pl"><head><meta charset="utf-8"><title>Port — przeniesiono do Kontaktu | Jachty Mazury</title>
<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=../kontakt/#port"><link rel="canonical" href="https://jachtymazury.pl/kontakt/"></head>
<body><p>Informacje o porcie są teraz w zakładce <a href="kontakt.html#port">Kontakt</a>.</p></body></html>''')

# ---- współpraca
page('wspolpraca.html', 'Inwestycje i pośrednictwo jachtowe na Mazurach | Jachty Mazury',
 'Zarządzanie jachtami czarterowymi na Mazurach: sprzedaż czarterów, przygotowanie do sezonu, serwis i nadzór, doradztwo przy zakupie jachtu pod czarter.',
 phead([('wspolpraca.html', 'Współpraca')], 'Inwestycje i pośrednictwo', 'Twój jacht jako zarządzane aktywo',
       'Posiadasz jacht żaglowy lub motorowy i chcesz, aby był efektywnie zarządzanym aktywem, a nie czasochłonnym obowiązkiem? Jesteśmy operatorem czarterowym na Mazurach, specjalizującym się w zarządzaniu jachtami czarterowymi.')
 + f'''<section class="psec">
  <div class="wrap g12">
    <div class="c5 prose reveal">
      <h2 class="h3">Zakres współpracy</h2>
      <p>W ramach pośrednictwa czarterowego obsługujemy zarówno jednostki prywatne, jak i jachty inwestycyjne, zapewniając im pełną obsługę operacyjną, techniczną i handlową.</p>
      <p>Dzięki kompleksowej obsłudze właściciel jachtu może korzystać z potencjału rynku czarterowego bez konieczności osobistego angażowania się w bieżącą eksploatację jednostki.</p>
    </div>
    <ul class="c6 o7 ticks-l reveal">
      <li>Sprzedaż i obsługa czarterów jachtów na Mazurach</li><li>Profesjonalne przygotowanie jachtu do sezonu czarterowego</li>
      <li>Bieżące kontrole techniczne, serwis i nadzór</li><li>Organizacja napraw, przeglądów i prac technicznych</li>
      <li>Obsługa oraz szkolenie klientów czarterowych</li><li>Stały nadzór nad stanem technicznym jednostki</li>
    </ul>
  </div>
</section>
<section class="psec psec--sand">
  <div class="wrap g12">
    <div class="c5 reveal"><p class="micro muted">Jacht jako inwestycja</p><p class="big num">ok. 10%</p><p class="big__s">rocznego zwrotu przy właściwym zarządzaniu — według operatora</p></div>
    <div class="c6 o7 prose reveal">
      <h2 class="h3">Realne modele współpracy</h2>
      <p>Rynek czarterowy dojrzał. Dziś jacht jako inwestycja to nie „szybki zysk”, lecz stabilny i przewidywalny model, który przy właściwym zarządzaniu może generować około 10% rocznego zwrotu, przy jednoczesnym zachowaniu wartości jednostki.</p>
      <p>Współpraca z operatorem czarterowym pozwala ograniczyć ryzyko operacyjne oraz uporządkować koszty i przychody związane z czarterem jachtu.</p>
    </div>
  </div>
</section>
<section class="psec">
  <div class="wrap g12">
    <div class="c5 prose reveal"><h2 class="h3">Zakup jachtu pod czarter</h2><p>Jeśli dopiero rozważasz zakup jachtu pod czarter:</p></div>
    <ul class="c6 o7 ticks-l reveal">
      <li>doradzimy w wyborze jednostki dostosowanej do rynku czarterowego na Mazurach,</li>
      <li>pomożemy w zakupie jachtu inwestycyjnego,</li>
      <li>zaprojektujemy model współpracy dopasowany do Twoich oczekiwań i możliwości.</li>
    </ul>
    <p class="c12 lead reveal">Stawiamy na transparentność, realne liczby i długoterminowe relacje.</p>
  </div>
</section>
<section class="inkband band pcta on-dark on-photo">
  <span class="deco deco--compass" aria-hidden="true"></span>
  <div class="wrap pcta__in">
    <div><h2 class="h2">Zapraszamy do współpracy</h2><p class="pcta__p">Porozmawiajmy o Twoim jachcie.</p></div>
    <div class="pcta__b"><a class="btn" href="{TEL_H}"><i data-lucide="phone" class="lucide"></i> {TEL}</a>
      <a class="btn btn--outline" href="mailto:{MAIL}">{MAIL}</a></div>
  </div>
</section>''',
 'wspolpraca.html')

# ---- kontakt
MAPS = PIN
SPRAWY = ['Czarter', 'Zakup jachtu', 'Współpraca', 'Inne']
page('kontakt.html', 'Kontakt — obsługa i rezerwacje | Jachty Mazury',
 f'Telefon {TEL}, e-mail {MAIL}, biuro codziennie od 8:00 do 20:00. Stanica Wodna Stranda, Pierkunowo 36, Giżycko.',
 f'''<section class="phead konh">
  <span class="deco deco--p-kontakt" aria-hidden="true"></span>
  <div class="wrap g12">
    <div class="c12">
      {crumbs([('kontakt.html', 'Kontakt')])}
      <p class="micro phead__eye">Obsługa i rezerwacje</p>
      <h1 class="h1 phead__h">Kontakt</h1>
    </div>
    <div class="c5 konh__d">
      <a class="konh__ch" href="{TEL_H}"><span class="micro">Zadzwoń</span><b class="num">{TEL}</b><span class="konh__sub">codziennie od 8:00 do 20:00</span></a>
      <a class="konh__ch" href="mailto:{MAIL}"><span class="micro">Napisz</span><b>{MAIL}</b></a>
      <div class="konh__ch"><span class="micro">Przyjedź</span><b>Stanica Wodna Stranda</b><span class="konh__sub">Pierkunowo 36, 11-500 Giżycko</span>
        <a class="konh__lnk" href="{MAPS}" rel="noopener" target="_blank">Wyznacz trasę <i data-lucide="arrow-up-right" class="lucide"></i></a></div>
    </div>
    <div class="c6 o7 konh__f">
      <form class="kf" id="kform" novalidate>
        <h2 class="h3 kf__h">Napisz do nas</h2>
        <fieldset class="kf__topic"><legend>W jakiej sprawie?</legend>
          <div class="kf__opts">{''.join(f'<label class="kf__opt"><input type="radio" name="topic" value="{esc(t)}"{" checked" if i == 0 else ""}><span>{t}</span></label>' for i, t in enumerate(SPRAWY))}</div>
        </fieldset>
        <div class="kf__row">
          <div class="kf__f" data-f="name"><label for="k-name">Imię</label><input id="k-name" name="name" autocomplete="given-name" required>
            <span class="kf__err" id="k-name-e">Podaj imię.</span></div>
          <div class="kf__f" data-f="contact"><label for="k-con">Telefon lub e-mail</label><input id="k-con" name="contact" autocomplete="email" inputmode="email" required>
            <span class="kf__err" id="k-con-e">Podaj numer telefonu albo adres e-mail.</span></div>
        </div>
        <div class="kf__f" data-f="msg"><label for="k-msg">Wiadomość</label><textarea id="k-msg" name="message" rows="4" required></textarea>
          <span class="kf__err" id="k-msg-e">Napisz, w czym możemy pomóc.</span></div>
        <button class="btn kf__btn" type="submit"><span class="btn__label">Wyślij wiadomość</span> <i data-lucide="arrow-right" class="lucide"></i></button>
        <p class="kf__rodo">Dane wykorzystamy tylko do odpowiedzi. Administrator: Sebastian Pażyszek, szczegóły w <a class="u u--on" href="polityka-prywatnosci.html">polityce prywatności</a>.</p>
      </form>
      <div class="kf kf--ok" id="kok" hidden tabindex="-1" role="status">
        <i data-lucide="check" class="lucide kf__ic"></i>
        <h2 class="h3">Wiadomość wysłana</h2>
        <p>Odpowiemy telefonicznie albo e-mailem, zależnie od podanego kontaktu.</p>
        <p>Pilna sprawa? Zadzwoń: <a class="u u--on num" href="{TEL_H}">{TEL}</a></p>
      </div>
    </div>
  </div>
</section>
<section class="psec kond" id="port">
  <div class="wrap g12">
    <figure class="c7 kond__img reveal">{pic("port", "Stanica Wodna Stranda w Giżycku z lotu ptaka", "(min-width:1024px) 55vw, 100vw")}</figure>
    <div class="c5 kond__t reveal">
      <p class="micro muted">Nasz port</p>
      <h2 class="h2">Stanica Wodna Stranda</h2>
      <p>Stranda to nowoczesny kompleks wypoczynkowy znajdujący się ok. 2 km od centrum Giżycka. Marina jest dobrą bazą wypadową w sercu Mazur.</p>
      <p>Do dyspozycji żeglarzy jest pompa do odbioru nieczystości, a w promieniu 2 km znajdują się dwie wodne stacje paliw. W Strandzie bezpłatnie opróżnimy toalety chemiczne.</p>
      <dl class="dl num">
        <div><dt>Adres</dt><dd>Pierkunowo 36<br>11-500 Giżycko</dd></div>
        <div><dt>Położenie</dt><dd>zatoka Tracz, jez. Kisajno</dd></div>
        <div><dt>Do centrum</dt><dd>ok. 2 km</dd></div>
        <div><dt>Stacje paliw</dt><dd>dwie wodne, w promieniu 2 km</dd></div>
      </dl>
      <a class="btn" href="{MAPS}" rel="noopener" target="_blank">Wyznacz trasę <i data-lucide="arrow-up-right" class="lucide"></i></a>
    </div>
  </div>
  <div class="wrap">
    <h3 class="h3 kond__h">Co znajdziesz w marinie</h3>
    <ul class="amen">
      <li>Monitorowany parking</li><li>Sanitariaty</li><li>Prysznice</li><li>Pralnia</li><li>Plac zabaw dla dzieci</li>
      <li>Pompa do odbioru nieczystości</li><li>Bezpłatne opróżnianie toalet chemicznych</li>
      <li>Tawerna — pizza i dania na miejscu</li><li>Muzyka na żywo w wakacje</li><li>Własny browar Strandy (od sezonu 2022)</li>
    </ul>
  </div>
</section>''',
 'kontakt.html',
 '''<script>
(function(){const f=document.getElementById('kform'),ok=document.getElementById('kok');
 const rules={name:v=>v.trim().length>1,contact:v=>{v=v.trim();return /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(v)||v.replace(/\\D/g,'').length>=9},msg:v=>v.trim().length>2};
 const check=w=>{const i=w.querySelector('input,textarea'),bad=!rules[w.dataset.f](i.value);w.classList.toggle('has-error',bad);
  i.setAttribute('aria-invalid',bad);if(bad)i.setAttribute('aria-describedby',i.id+'-e');else i.removeAttribute('aria-describedby');return bad};
 f.querySelectorAll('[data-f]').forEach(w=>{const i=w.querySelector('input,textarea');i.addEventListener('blur',()=>{if(i.value)check(w)});
  i.addEventListener('input',()=>{if(w.classList.contains('has-error'))check(w)})});
 f.addEventListener('submit',e=>{e.preventDefault();let first=null;
  f.querySelectorAll('[data-f]').forEach(w=>{if(check(w)&&!first)first=w.querySelector('input,textarea')});
  if(first){first.focus();return}
  const b=f.querySelector('.btn');b.classList.add('is-loading');
  setTimeout(()=>{b.classList.remove('is-loading');f.hidden=true;ok.hidden=false;ok.focus();window.lucide&&lucide.createIcons()},900)});
})();
</script>''')

# ---- polityka prywatności
POL = json.load(open('_p/polityka.json')); POL1 = json.load(open('_p/pol1.json'))
def pol_html():
    o = '<h2>I. Informacje ogólne</h2><p>Niniejsza polityka prywatności określa zasady przetwarzania danych osobowych oraz korzystania z plików cookies na stronie internetowej www.jachtymazury.pl.</p>'
    o += f'<p>Administratorem danych osobowych jest:<br><b>Sebastian Pażyszek</b><br>ul. Rolnicza 56<br>11-500 Giżycko<br>NIP: 845-199-56-50</p>'
    o += f'<p>Kontakt z administratorem możliwy jest pod adresem e-mail: <a class="u u--on" href="mailto:{MAIL}">{MAIL}</a></p>'
    o += '<p>Serwis pozyskuje informacje o użytkownikach i ich zachowaniu w następujący sposób:</p><ul><li>poprzez dobrowolne dane wprowadzone w formularzach,</li><li>poprzez zapisywanie plików cookies w urządzeniach końcowych użytkowników,</li><li>poprzez zapisywanie technicznych informacji o połączeniu (adres IP, data i godzina, typ przeglądarki).</li></ul>'
    started = False; lst = False
    for tag, t in POL:
        if tag == 'h2' and t.startswith('II.'): started = True
        if not started: continue
        if t.startswith('Zarządzaj') or t.startswith('Przeczytaj więcej') or t == '{title}': break
        if tag == 'li':
            if not lst: o += '<ul>'; lst = True
            o += f'<li>{esc(t)}</li>'
        else:
            if lst: o += '</ul>'; lst = False
            o += f'<{tag}>{esc(t)}</{tag}>'
    if lst: o += '</ul>'
    return o
page('polityka-prywatnosci.html', 'Polityka prywatności | Jachty Mazury',
 'Zasady przetwarzania danych osobowych i korzystania z plików cookies na stronie jachtymazury.pl.',
 phead([('polityka-prywatnosci.html', 'Polityka prywatności')], 'Dokument', 'Polityka prywatności i plików cookies')
 + f'<section class="psec"><div class="wrap"><article class="legal">{pol_html()}</article></div></section>',
 'polityka-prywatnosci.html')

# ---- artykuły poradnika (treść z żywej strony, 1:1)
import sys; sys.path.insert(0, os.path.join(ROOT, '_build')); import artykuly
SLUGS = {a['slug'] for a in ART}
def art_row(a):
    return f'''<li class="gd reveal"><a class="gd__a" href="{a["slug"]}.html">
  <span class="gd__t">{esc(a["h1"])}</span>
  <span class="gd__l">{esc(a["lead"])}</span>
  <span class="gd__go" aria-hidden="true"><i data-lucide="arrow-right" class="lucide"></i></span></a></li>'''
for i, a in enumerate(ART):
    blocks = artykuly.extract(a['slug'], SLUGS)
    mins = max(1, round(artykuly.words(blocks) / 200))
    lead = ''
    if blocks and blocks[0][0] == 'p':
        lead = blocks[0][1]; blocks = blocks[1:]
    more = [ART[(i + k) % len(ART)] for k in (1, 2, 3)]
    page(f'{a["slug"]}.html', f'{a["title"]} | Jachty Mazury', re.sub(r'<[^>]+>', '', lead)[:155],
     phead([('poradnik.html', 'Poradnik'), (f'{a["slug"]}.html', a['h1'])], f'{pl_date(a.get("date", "")) + " · " if a.get("date") else ""}{mins} min czytania', esc(a['h1']), lead)
     + f'''<section class="psec art">
  <div class="wrap">
    <figure class="art__img">{pic("art-" + a["slug"], a["h1"], "(min-width:1024px) 900px, 100vw", True)}</figure>
    <div class="art__body">
{artykuly.render(blocks)}
    </div>
  </div>
</section>
<section class="psec psec--sand">
  <div class="wrap">
    <h2 class="h3 psec__h">Czytaj dalej</h2>
    <ul class="gds">{''.join(art_row(m) for m in more)}</ul>
    <p class="art__all"><a class="u u--on" href="poradnik.html">Wszystkie artykuły →</a></p>
  </div>
</section>'''
     + cta('Wybrałeś termin?', 'Sprawdź, które jachty są wolne, albo zadzwoń do nas.'),
     'poradnik.html')

# ---- strony wg uwag klientki: jednostki, modele, hub, Wiedza, strona główna
exec(open(os.path.join(ROOT, '_build/serwis.py'), encoding='utf-8').read())

# ---- 404
page('404.html', 'Nie ma takiej strony | Jachty Mazury', 'Strona nie istnieje albo zmieniła adres.',
 phead([('404.html', 'Błąd 404')], '', 'Nie ma takiej strony',
       'Adres mógł się zmienić po przenosinach serwisu. Wybierz, dokąd chcesz przejść.')
 + f'''<section class="psec">
  <div class="wrap">
    <ul class="nf">
      <li><a class="nf__a" href="jachty-zaglowe.html"><span class="nf__t">Jachty żaglowe</span><span class="nf__go" aria-hidden="true"><i data-lucide="arrow-right" class="lucide"></i></span></a></li>
      <li><a class="nf__a" href="jachty-motorowe.html"><span class="nf__t">Jachty motorowe</span><span class="nf__go" aria-hidden="true"><i data-lucide="arrow-right" class="lucide"></i></span></a></li>
      <li><a class="nf__a" href="cennik.html"><span class="nf__t">Cennik</span><span class="nf__go" aria-hidden="true"><i data-lucide="arrow-right" class="lucide"></i></span></a></li>
      <li><a class="nf__a" href="kontakt.html"><span class="nf__t">Kontakt</span><span class="nf__go" aria-hidden="true"><i data-lucide="arrow-right" class="lucide"></i></span></a></li>
    </ul>
    <p class="nf__home"><a class="u u--on" href="index.html">Strona główna</a> · <a class="u u--on num" href="{TEL_H}">{TEL}</a></p>
  </div>
</section>''', '')

print('gotowe')

# ================================================================= ISTNIEJĄCE STRONY: nagłówek, stopka, skrypt
def patch(fname, cur, photo=False, own_booking=False, dark=False):
    s = open(f'_build/src/{fname}').read()   # źródło ręcznie tworzonej strony
    a = s.index('<header class="head'); b = s.index('</header>', a) + 9
    # usuń poprzednie menu mobilne, jeśli było
    os.makedirs('_build/kopie', exist_ok=True); open(f'_build/kopie/{fname}', 'w').write(s)   # kopia przed zmianą
    s2 = s[b:]
    m = re.match(r'\s*<div class="mnav" id="mnav" hidden>.*?</nav>\n</div>', s2, re.S)   # stare menu mobilne — dokładnie jego blok
    if m: s2 = s2[m.end():]
    h = header(cur, photo, dark)
    if own_booking: h = h.replace('<a class="btn" href="#rezerwuj" data-open-modal>Rezerwuj online</a>', '<a class="btn" href="#dostepnosc" data-open-modal>Rezerwuj online</a>')
    s = s[:a] + h + s2
    fa = s.index('<footer'); fb = s.index('</footer>', fa) + 9
    s = s[:fa] + FOOT.replace(' id="kontakt"', '' if not photo else ' id="kontakt"') + s[fb:]
    if 'assets/css/pages.css' not in s:   # style stopki, menu, pływających przycisków i okna rezerwacji — wspólne ze stronami z generatora
        s = re.sub(r'(<link rel="stylesheet" href="assets/css/system\.css[^"]*">)', r'\1\n<link rel="stylesheet" href="assets/css/pages.css">', s, count=1)
    if dark and 'assets/css/head-dark.css' not in s:
        s = s.replace('<link rel="stylesheet" href="assets/css/system.css">', '<link rel="stylesheet" href="assets/css/system.css">\n<link rel="stylesheet" href="assets/css/head-dark.css">', 1)
    if 'assets/css/mobile.css' not in s:
        s = s.replace('</head>', '<link rel="stylesheet" href="assets/css/mobile.css">\n</head>', 1)
    if 'class="fabs"' not in s:   # WhatsApp, Messenger i telefon — ten sam zestaw co na stronach z generatora
        s = re.sub(r'<a class="callfab".*?</a>', lambda m: CALL, s, count=1, flags=re.S) if 'class="callfab"' in s else s.replace('</body>', CALL + '\n</body>', 1)
    if 'id="rezerwuj-okno"' not in s:
        s = s.replace('</body>', BOOK + '\n</body>', 1)   # R1: wspólne okno rezerwacji
    if 'assets/js/site.js' not in s:
        s = s.replace('</body>', '<script src="assets/js/site.js" defer></script>\n</body>', 1)
    open(fname, 'w').write(s); print('  ✎', fname)

print('Nawigacja na istniejących stronach:')
patch('fundusze-europejskie.html', '', dark=True)

# ================================================================= pages.css
def _styles(p):
    return '\n'.join(re.findall(r'<style>(.*?)</style>', open(p).read(), re.S))
def _blocks(css):
    out = []; i = 0; n = len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        pre = css[i:j].strip(); d = 1; k = j + 1
        while k < n and d:
            if css[k] == '{': d += 1
            elif css[k] == '}': d -= 1
            k += 1
        out.append((pre, css[j + 1:k - 1])); i = k
    return out
def _clean(p): return re.sub(r'/\*.*?\*/', '', p, flags=re.S).strip()
_KEEP = re.compile(r'\.(?:fli|fl|meas|berth|fleet|foot|ue|gstars|war|deco|hl|callfab)(?:__|--|(?![\w-]))')
def _pick(css):
    out = []
    for pre, body in _blocks(css):
        p = _clean(pre)
        if p.startswith('@media'):
            inner = [f'{_clean(a)}{{{b}}}' for a, b in _blocks(body) if _KEEP.search(_clean(a))]
            if inner: out.append(p + '{\n  ' + '\n  '.join(inner) + '\n}')
        elif not p.startswith('@') and _KEEP.search(p):
            out.append(f'{p}{{{body}}}')
    return '\n'.join(out)
def build_pages_css():
    jh = open('_build/legacy-head.css').read()        # zamrożone style z dawnej karty jachtu
    css = ('/* jachtymazury.pl — style podstron. Generowane przez _build/podstrony.py z CSS strony głównej i karty jachtu + _build/pages-extra.css */\n\n'
           '/* nagłówek papierowy */\n' + jh + '\n/* komponenty ze strony głównej */\n' + _pick(open('_build/legacy-index.css').read()) + '\n\n' + open('_build/head-dark.css').read() + '\n' + open('_build/pages-extra.css').read())
    css = css.replace('url(assets/', 'url(../')   # plik leży w assets/css/
    open('assets/css/pages.css', 'w').write(css); print('  pages.css', len(css))
    hd = open('_build/head-dark.css').read().replace('url(assets/', 'url(../')
    open('assets/css/head-dark.css', 'w').write('/* ciemny nagłówek dla stron spoza generatora (karta jachtu, fundusze). Generowane z _build/head-dark.css */\n' + hd)
build_pages_css()

# numer wersji przy CSS/JS (skrót zawartości) — każda zmiana omija pamięć podręczną przeglądarki i GitHub Pages
import hashlib, glob
def stamp_assets():
    ver = {}
    for f in glob.glob('assets/css/*.css') + glob.glob('assets/js/*.js'):
        ver[f] = hashlib.md5(open(f, 'rb').read()).hexdigest()[:8]
    for h in glob.glob('*.html'):
        t = open(h, encoding='utf-8').read()
        t2 = re.sub(r'((?:href|src)="(assets/(?:css|js)/[\w.-]+\.(?:css|js)))(?:\?v=\w+)?"',
                    lambda m: f'{m.group(1)}?v={ver[m.group(2)]}"' if m.group(2) in ver else m.group(0), t)
        if t2 != t: open(h, 'w', encoding='utf-8').write(t2)
    print('  wersje zasobów:', ', '.join(f'{k.split("/")[-1]}={v}' for k, v in sorted(ver.items())))
stamp_assets()
exec(open(os.path.join(ROOT, '_build/struktura.py'), encoding='utf-8').read())   # katalogi jak na obecnej stronie + SEO

print('koniec')
