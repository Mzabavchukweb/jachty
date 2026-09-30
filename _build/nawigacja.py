# Nawigacja, menu mobilne i stopka — wg uwag klientki (wizualizacje -2/-3). Wykonywane wewnątrz podstrony.py.
def mslug(model): return re.sub(r'[^a-z0-9]+', '-', model.lower()).strip('-')
def models(units):
    out = []
    for u in units:
        if u[1] not in out: out.append(u[1])
    return out
def murl(model): return f'model-{mslug(model)}.html'
def uname(u): return f'{u[1]} „{u[2]}”' if u[2] else u[1]

# Wiedza: sama strona „Wiedza” jest pod kliknięciem w pozycję menu, więc w rozwinięciu jej nie powtarzamy (uwaga klientki 29.09)
WIEDZA_SUB = [('poradnik.html', 'Poradnik czarterowy'), ('filmy-szkoleniowe.html', 'Filmy szkoleniowe'), ('aktualnosci.html', 'Aktualności')]
WIEDZA = [('wiedza.html', 'Wiedza')] + WIEDZA_SUB
# „Port” usunięty z menu — informacje o porcie są w Kontakcie (uwaga klientki 29.09)
NAV_ITEMS = [('cennik.html', 'Cennik'), ('jachty-na-sprzedaz.html', 'Na sprzedaż'), ('wspolpraca.html', 'Współpraca'), ('kontakt.html', 'Kontakt')]
CZ_ITEMS = [('czarter-jachtow.html', 'Czarter jachtów'), ('jachty-zaglowe.html', 'Jachty żaglowe'), ('jachty-motorowe.html', 'Jachty motorowe'), ('czarter-bez-patentu.html', 'Czarter bez patentu')]
# kolejność modeli żaglowych jak w menu obecnej strony
SAIL_ORDER = ['Maxus 24 Evo', 'Maxus 28', 'Antila 24.4', 'Antila 27', 'Antila 28.2', 'Antila 30', 'Antila 30.1', 'Antila 33', 'Antila 33.3', 'Antila 34']
def _sail_models():
    ms = models(SAIL)
    return sorted(ms, key=lambda m: SAIL_ORDER.index(m) if m in SAIL_ORDER else 99)
# rozwinięcie „Czarter jachtów” jak na obecnej stronie: typy jachtów, a przy nich modele — bez konkretnych jednostek
def _cz_tree():
    return [('jachty-zaglowe.html', 'Jachty żaglowe', [(murl(m), m) for m in _sail_models()]),
            ('jachty-motorowe.html', 'Jachty motorowe', [(murl(m), m) for m in models(MOTOR)]),
            ('czarter-bez-patentu.html', 'Czarter bez patentu', [])]

def nav(cur):
    cz_pages = [h for h, _ in CZ_ITEMS] + ['houseboat-mazury.html'] + [murl(m) for m in models(SAIL + MOTOR)] + [u[0] + '.html' for u in SAIL + MOTOR]
    w_pages = [h for h, _ in WIEDZA] + [a['slug'] + '.html' for a in ART]
    cc = lambda h: ' aria-current="page"' if h == cur else ''
    def sub(h, t, kids):
        if not kids:
            return f'<a href="{h}"{cc(h)}>{t}</a>'
        fly = ''.join(f'<a href="{kh}"{cc(kh)}>{esc(kt)}</a>' for kh, kt in kids)
        return (f'<div class="sub"><a class="sub__a" href="{h}"{cc(h)}>{t} <i data-lucide="chevron-right" class="lucide"></i></a>'
                f'<div class="menu menu--fly">{fly}</div></div>')
    cz = ''.join(sub(*x) for x in _cz_tree())
    wm = ''.join(f'<a href="{h}"{cc(h)}>{t}</a>' for h, t in WIEDZA_SUB)
    items = ''.join(f'\n      <a class="u{" u--on" if h == cur else ""}" href="{h}"{cc(h)}>{t}</a>' for h, t in NAV_ITEMS)
    def top(key, href, label, menu, is_cur):
        return (f'<div class="has{" is-cur" if is_cur else ""}"><a class="nav__a" href="{href}"{cc(href)}>{label}</a>'
                f'<button class="nav__b" type="button" aria-expanded="false" aria-controls="m-{key}" aria-label="Rozwiń: {label}"><i data-lucide="chevron-down" class="lucide"></i></button>'
                f'\n        <div class="menu" id="m-{key}">{menu}</div></div>')
    return (f'''<nav class="nav" aria-label="Główne">
      {top("czarter", "czarter-jachtow.html", "Czarter jachtów", cz, cur in cz_pages)}
      {top("wiedza", "wiedza.html", "Wiedza", wm, cur in w_pages)}{items}
    </nav>''')

def mnav(cur):
    cc = lambda h: ' aria-current="page"' if h == cur else ''
    n = [0]
    units_of = {murl(m): [u[0] + '.html' for u in SAIL + MOTOR if u[1] == m] for m in models(SAIL + MOTOR)}
    def inside(h, kids):   # czy bieżąca strona leży w tej gałęzi (strona jachtu liczy się do swojego modelu)
        return h == cur or cur in units_of.get(h, []) or any(inside(k[0], k[2] if len(k) == 3 else []) for k in kids)
    def acc(h, t, kids, lvl=1):
        if not kids:
            return f'<li><a href="{h}"{cc(h)}>{esc(t)}</a></li>'
        n[0] += 1; i = f'mn-{n[0]}'
        op = any(inside(k[0], k[2] if len(k) == 3 else []) for k in kids)   # rozwinięta, gdy jesteśmy na jednej z podstron
        inner = ''.join(acc(*k, lvl=lvl + 1) if len(k) == 3 else acc(k[0], k[1], [], lvl + 1) for k in kids)
        return (f'<li class="mnav__acc{" is-open" if op else ""}"><div class="mnav__row"><a href="{h}"{cc(h)}>{esc(t)}</a>'
                f'<button class="mnav__t" type="button" aria-expanded="{"true" if op else "false"}" aria-controls="{i}" aria-label="Pokaż podstrony: {esc(t)}"><span class="mnav__pm" aria-hidden="true"></span></button></div>'
                f'<div class="mnav__sub" id="{i}"><ul class="mnav__subl mnav__subl--{lvl + 1}">{inner}</ul></div></li>')
    tree = ([('index.html', 'Start', []),
             ('czarter-jachtow.html', 'Czarter jachtów', _cz_tree()),
             ('wiedza.html', 'Wiedza', [(h, t, []) for h, t in WIEDZA_SUB])]
            + [(h, t, []) for h, t in NAV_ITEMS])
    links = ''.join(acc(*x) for x in tree)
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

UE = '''<div class="ue">
      <a class="ue__img" href="fundusze-europejskie.html" aria-label="Fundusze Europejskie — szczegóły dofinansowania">
        <picture><source type="image/webp" srcset="assets/img/r/ue-logotypy-630.webp 630w, assets/img/r/ue-logotypy-1260.webp 1260w, assets/img/r/ue-logotypy-1890.webp 1890w" sizes="(min-width:768px) 560px, 100vw">
        <img src="assets/img/r/ue-logotypy-630.png" srcset="assets/img/r/ue-logotypy-630.png 630w, assets/img/r/ue-logotypy-1260.png 1260w, assets/img/r/ue-logotypy-1890.png 1890w" sizes="(min-width:768px) 560px, 100vw" width="630" height="57" alt="Fundusze Europejskie dla Warmii i Mazur, Rzeczpospolita Polska, Dofinansowane przez Unię Europejską, Warmia Mazury" decoding="async"></picture>
      </a>
      <p class="ue__txt">Projekt dofinansowany ze środków Unii Europejskiej. <a class="u u--on" href="fundusze-europejskie.html">Szczegóły dofinansowania →</a></p>
    </div>'''

# stopka wg wizualizacji -2, bez newslettera; YouTube pominięty, bo kanał z obecnej strony nie istnieje
FOOT = f'''<footer class="inkband foot on-dark" id="kontakt">
  <div class="wrap">
    <div class="foot__g">
      <div class="foot__brand"><img class="foot__logo" src="assets/img/logo-mono.png" width="450" height="76" alt="Jachtymazury.pl">
        <p>Czarter jachtów żaglowych, motorowych i houseboatów ze Stanicy Wodnej Stranda w Giżycku.</p>
        <p class="foot__soc"><a class="soc" href="{FB}" rel="noopener" target="_blank" aria-label="Facebook"><img src="assets/img/ikony/facebook-bialy.png" width="20" height="20" alt=""></a><a class="soc" href="{IG}" rel="noopener" target="_blank" aria-label="Instagram"><img src="assets/img/ikony/instagram-bialy.png" width="20" height="20" alt=""></a><a class="soc" href="{YT}" rel="noopener" target="_blank" aria-label="YouTube"><img src="assets/img/ikony/youtube-bialy.png" width="20" height="20" alt=""></a></p></div>
      <div><span class="micro">Szybkie linki</span><ul class="foot__list"><li><a class="u" href="czarter-jachtow.html">Czarter jachtów</a></li><li><a class="u" href="wiedza.html">Wiedza</a></li><li><a class="u" href="cennik.html">Cennik</a></li><li><a class="u" href="wspolpraca.html">Współpraca</a></li><li><a class="u" href="kontakt.html">Kontakt</a></li><li><a class="u" href="polityka-prywatnosci.html">Polityka prywatności</a></li></ul></div>
      <div><span class="micro">Czarter jachtów</span><ul class="foot__list"><li><a class="u" href="jachty-zaglowe.html">Jachty żaglowe</a></li><li><a class="u" href="jachty-motorowe.html">Jachty motorowe</a></li><li><a class="u" href="czarter-bez-patentu.html">Czarter bez patentu</a></li><li><a class="u" href="houseboat-mazury.html">Houseboaty</a></li><li><a class="u" href="jachty-na-sprzedaz.html">Jachty na sprzedaż</a></li></ul></div>
      <div><span class="micro">Kontakt</span><ul class="foot__list"><li>Stanica Wodna Stranda</li><li><a class="u" href="{PIN}" rel="noopener" target="_blank">Pierkunowo 36, 11-500 Giżycko</a></li><li class="num"><a class="u" href="{TEL_H}">{TEL}</a></li><li><a class="u" href="mailto:{MAIL}">{MAIL}</a></li><li class="num">Biuro 8:00 – 20:00, codziennie</li></ul></div>
    </div>
    {UE}
    <div class="foot__bot"><span>© 2026 jachtymazury.pl</span><span><a class="u" href="fundusze-europejskie.html">Fundusze Europejskie</a> · <a class="u" href="polityka-prywatnosci.html">Polityka prywatności</a></span><span class="foot__by">Projekt i realizacja: <a class="u" href="https://codingmaks.com" rel="noopener" target="_blank">codingmaks.com</a></span></div>
  </div>
</footer>'''
