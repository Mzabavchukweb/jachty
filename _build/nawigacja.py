# Nawigacja, menu mobilne i stopka — wg uwag klientki (wizualizacje -2/-3). Wykonywane wewnątrz podstrony.py.
def mslug(model): return re.sub(r'[^a-z0-9]+', '-', model.lower()).strip('-')
def models(units):
    out = []
    for u in units:
        if u[1] not in out: out.append(u[1])
    return out
def murl(model): return f'model-{mslug(model)}.html'
def uname(u): return f'{u[1]} „{u[2]}”' if u[2] else u[1]

WIEDZA = [('poradnik.html', 'Poradnik czarterowy'), ('filmy-szkoleniowe.html', 'Filmy szkoleniowe'), ('aktualnosci.html', 'Aktualności')]
NAV_ITEMS = [('cennik.html', 'Cennik'), ('jachty-na-sprzedaz.html', 'Na sprzedaż'), ('port.html', 'Port'), ('wspolpraca.html', 'Współpraca'), ('kontakt.html', 'Kontakt')]
CZ_ITEMS = [('czarter-jachtow.html', 'Czarter jachtów'), ('jachty-zaglowe.html', 'Jachty żaglowe'), ('jachty-motorowe.html', 'Jachty motorowe'), ('czarter-bez-patentu.html', 'Czarter bez patentu')]

def _mcol(title, href, units):
    rows = ''
    for m in models(units):
        us = [u for u in units if u[1] == m]
        subs = ''.join(f'<a class="mm__u" href="{u[0]}.html">{esc(u[2]) if u[2] else esc(m)}</a>' for u in us)
        rows += f'<li><a class="mm__m" href="{murl(m)}">{esc(m)}</a><span class="mm__us">{subs}</span></li>'
    return f'<div class="mm__col"><a class="mm__h" href="{href}">{title} <i data-lucide="arrow-right" class="lucide"></i></a><ul class="mm__l">{rows}</ul></div>'

def nav(cur):
    cz_pages = [h for h, _ in CZ_ITEMS] + [murl(m) for m in models(SAIL + MOTOR)] + [u[0] + '.html' for u in SAIL + MOTOR]
    w_pages = [h for h, _ in WIEDZA] + [a['slug'] + '.html' for a in ART]
    cc = lambda h: ' aria-current="page"' if h == cur else ''
    mega = (f'<div class="menu mm" id="m-czarter">'
            f'<div class="mm__top"><a href="czarter-jachtow.html"{cc("czarter-jachtow.html")}>Czarter jachtów — oferta i najczęstsze pytania</a>'
            f'<a href="czarter-bez-patentu.html"{cc("czarter-bez-patentu.html")}>Czarter bez patentu</a></div>'
            f'<div class="mm__cols">{_mcol("Jachty żaglowe", "jachty-zaglowe.html", SAIL)}{_mcol("Jachty motorowe", "jachty-motorowe.html", MOTOR)}</div></div>')
    wm = ''.join(f'<a href="{h}"{cc(h)}>{t}</a>' for h, t in WIEDZA)
    items = ''.join(f'\n      <a class="u{" u--on" if h == cur else ""}" href="{h}"{cc(h)}>{t}</a>' for h, t in NAV_ITEMS)
    return (f'''<nav class="nav" aria-label="Główne">
      <div class="has has--mega{" is-cur" if cur in cz_pages else ""}"><button class="nav__b" type="button" aria-expanded="false" aria-controls="m-czarter">Czarter jachtów <i data-lucide="chevron-down" class="lucide"></i></button>
        {mega}</div>
      <div class="has{" is-cur" if cur in w_pages else ""}"><button class="nav__b" type="button" aria-expanded="false" aria-controls="m-wiedza">Wiedza <i data-lucide="chevron-down" class="lucide"></i></button>
        <div class="menu" id="m-wiedza">{wm}</div></div>{items}
    </nav>''')

def mnav(cur):
    links = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a></li>'
                    for h, t in [('index.html', 'Start')] + CZ_ITEMS + WIEDZA + NAV_ITEMS)
    return (f'''<div class="mnav" id="mnav" hidden>
  <nav class="mnav__in" aria-label="Menu">
    <ul class="mnav__l">{links}</ul>
    <div class="mnav__cta">
      <a class="btn btn--block" href="index.html#rezerwuj">Sprawdź dostępność <i data-lucide="arrow-right" class="lucide"></i></a>
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
        <p class="foot__soc"><a class="u" href="{FB}" rel="noopener" target="_blank">Facebook</a><a class="u" href="{IG}" rel="noopener" target="_blank">Instagram</a></p></div>
      <div><span class="micro">Szybkie linki</span><ul class="foot__list"><li><a class="u" href="czarter-jachtow.html">Czarter jachtów</a></li><li><a class="u" href="poradnik.html">Poradnik czarterowy</a></li><li><a class="u" href="cennik.html">Cennik</a></li><li><a class="u" href="wspolpraca.html">Współpraca</a></li><li><a class="u" href="kontakt.html">Kontakt</a></li><li><a class="u" href="polityka-prywatnosci.html">Polityka prywatności</a></li></ul></div>
      <div><span class="micro">Czarter jachtów</span><ul class="foot__list"><li><a class="u" href="jachty-zaglowe.html">Jachty żaglowe</a></li><li><a class="u" href="jachty-motorowe.html">Jachty motorowe</a></li><li><a class="u" href="czarter-bez-patentu.html">Czarter bez patentu</a></li><li><a class="u" href="jachty-na-sprzedaz.html">Jachty na sprzedaż</a></li></ul></div>
      <div><span class="micro">Kontakt</span><ul class="foot__list"><li>Stanica Wodna Stranda</li><li>Pierkunowo 36, 11-500 Giżycko</li><li class="num"><a class="u" href="{TEL_H}">{TEL}</a></li><li><a class="u" href="mailto:{MAIL}">{MAIL}</a></li><li class="num">Biuro 8:00 – 20:00, codziennie</li></ul></div>
    </div>
    {UE}
    <div class="foot__bot"><span>© 2026 jachtymazury.pl</span><span><a class="u" href="fundusze-europejskie.html">Fundusze Europejskie</a> · <a class="u" href="polityka-prywatnosci.html">Polityka prywatności</a></span></div>
  </div>
</footer>'''
