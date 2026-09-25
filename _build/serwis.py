# Strony wg uwag klientki: strona główna, jednostki (-1), modele, hub „Czarter jachtów”, Wiedza. Wykonywane wewnątrz podstrony.py.
import jednostki
GAL = json.load(open('_img/galerie-ws.json'))
KIND = {u[0]: 'sail' for u in SAIL} | {u[0]: 'motor' for u in MOTOR}
MAPS = 'https://www.google.com/maps/search/?api=1&amp;query=Stanica+Wodna+Stranda+Pierkunowo+36+Gi%C5%BCycko'
LIVE_MODEL = {'Antila 30.1 E': 'antila-30-1'}          # nazwa modelu u nas → adres strony modelu u klienta

def gpic(slug, n, ws, W, H, sizes, big=False, eager=False):
    src = lambda e: ', '.join(f'assets/img/j/{slug}/{n}-{w}.{e} {w}w' for w in ws)
    w0 = ws[-1] if big else ws[0]
    return (f'<picture><source type="image/webp" srcset="{src("webp")}" sizes="{sizes}">'
            f'<img src="assets/img/j/{slug}/{n}-{w0}.jpg" srcset="{src("jpg")}" sizes="{sizes}" width="{W}" height="{H}" alt=""'
            f'{" fetchpriority=\"high\"" if eager else ""} decoding="async"></picture>')

SPEC_ORDER = ['Długość', 'Szerokość', 'Zanurzenie', 'Liczba osób', 'Zamykane kabiny', 'Wysokość kabiny', 'Typ miecza', 'Typ steru', 'Typ silnika', 'Moc silnika', 'Powierzchnia żagli', 'Rok produkcji']
def spec_val(k, v):
    v = v.replace('-', ' – ') if k == 'Zanurzenie' else v
    v = re.sub(r'(\d)\.(\d)', r'\1,\2', v)
    if k == 'Powierzchnia żagli' and re.search(r'\d m$', v): v += '²'
    return esc(v)

def unit_facts(slug):
    """Ikony z danymi jednostki — tylko to, co wynika z tabeli danych i listy wyposażenia na stronie jednostki."""
    sp = UNITS[slug]['spec']; eq = ' | '.join(jednostki.extract(slug)['equip']).lower()
    out = []
    def add(icon, k, v):
        if v and v not in ('–', '-'): out.append((icon, k, v))
    add('move-horizontal', 'Długość', spec_val('Długość', sp.get('Długość', '')))
    add('move-vertical', 'Szerokość', spec_val('Szerokość', sp.get('Szerokość', '')))
    add('anchor', 'Zanurzenie', spec_val('Zanurzenie', sp.get('Zanurzenie', '')))
    add('bed-double', 'Miejsca do spania', berths(sp.get('Liczba osób', '–'))[0] if sp.get('Liczba osób') else '')
    add('door-closed', 'Kabiny', sp.get('Zamykane kabiny', ''))
    if 'wc morskie' in eq or 'toaleta morska' in eq: add('bath', 'Toaleta', 'morska')
    elif 'chemiczn' in eq: add('bath', 'Toaleta', 'chemiczna')
    if 'prysznic' in eq: add('shower-head', 'Prysznic', 'z ciepłą wodą' if 'ciepłą wodą' in eq else 'tak')
    ster = sp.get('Typ steru', '').lower()
    if 'koło' in ster or 'koło sterowe' in eq: add('ship-wheel', 'Ster', 'koło')
    elif 'rumpel' in ster or 'rumpel' in eq: add('ship-wheel', 'Ster', 'rumpel')
    eng = sp.get('Typ silnika', '').lower()
    power = re.search(r'silnik[^|]*?(\d+[.,]?\d*)\s*km', eq)
    if eng:
        e = 'zaburtowy' if 'przyczep' in eng or 'zaburt' in eng else ('stacjonarny' if 'stacjonarn' in eng else eng)
        add('cog', 'Silnik', e + (f' · {power.group(1).replace(".", ",")} KM' if power else ''))
    if 'dziobowy i rufowy ster strumieniowy' in eq: add('waves', 'Ster strumieniowy', '2')
    elif 'ster strumieniowy' in eq: add('waves', 'Ster strumieniowy', '1')
    add('calendar', 'Rok produkcji', sp.get('Rok produkcji', ''))
    return out

def price_html(row):
    p = od(row)
    return (f'<span class="micro muted">Cena od</span><p class="unit__price num"><b>{zl(p)}</b> <span>/ doba</span></p>' if p
            else '<span class="micro muted">Cena</span><p class="unit__price unit__price--ask">na zapytanie</p>')

def model_units(m): return [u for u in SAIL + MOTOR if u[1] == m]
def kind_of_model(m): return 'sail' if any(u[1] == m for u in SAIL) else 'motor'
def list_of(kind): return ('jachty-zaglowe.html', 'Jachty żaglowe') if kind == 'sail' else ('jachty-motorowe.html', 'Jachty motorowe')

# ---------------------------------------------------------------- strona jednostki (wizualizacja -1)
def unit_page(u):
    slug, model, name, row = u
    kind = KIND[slug]; full = uname(u); lst, lst_name = list_of(kind)
    x = jednostki.extract(slug); sp = UNITS[slug]['spec']; g = GAL.get(slug, [])
    main = gpic(slug, g[0][0], g[0][1], g[0][2], g[0][3], '100vw', big=True, eager=True) if g else ''
    thumbs = ''.join(f'<button type="button" data-i="{i}" aria-label="Powiększ zdjęcie {i+1} z {len(g)}"{" aria-current=\"true\"" if i == 0 else ""}>'
                     f'{gpic(slug, n, ws, W, H, "180px")}</button>' for i, (n, ws, W, H) in enumerate(g))
    facts = ''.join(f'<li><i data-lucide="{ic}" class="lucide" aria-hidden="true"></i><span class="uic__k">{k}</span><b>{v}</b></li>' for ic, k, v in unit_facts(slug))
    desc = ''.join(f'<h3 class="udesc__h">{esc(t)}</h3>' if tag == 'h2' else f'<p>{esc(t)}</p>' for tag, t in x['desc'])
    side = gpic(slug, *g[1], '(min-width:1024px) 40vw, 100vw', big=True) if len(g) > 1 else ''
    equip = ''.join(f'<li>{esc(e)}</li>' for e in x['equip'])
    keys = [k for k in SPEC_ORDER if k in sp] + [k for k in sp if k not in SPEC_ORDER]
    spec = ''.join(f'<div><dt>{esc(k)}</dt><dd>{spec_val(k, sp[k])}</dd></div>' for k in keys)
    terms = ''.join(f'<li>{esc(t)}</li>' for t in x['terms'])
    v = ROWS.get(row); ptab = ''
    if v:
        lis = ''.join(f'<li><span>{r}{t}</span><b class="num">{zl(int(val)) if val.strip().isdigit() else "—"} <small>{un}</small></b></li>' for (r, un, t), val in zip(periods, v[:11]))
        ptab = (f'<ul class="unit__prices">{lis}<li class="unit__px"><span>Kaucja</span><b class="num">{zl(int(v[11]))}</b></li>'
                f'<li class="unit__px"><span>Sprzątanie</span><b class="num">{zl(int(v[12]))}</b></li></ul>'
                f'<p class="unit__note">Cena za dobę obowiązuje przy czarterze minimum tygodniowym. Przy krótszych terminach cena ustalana jest indywidualnie.</p>')
    subject = f'Zapytanie o czarter: {full}'
    more = ([w for w in SAIL + MOTOR if w[0] != slug and w[1] == model] + [w for w in (SAIL if kind == 'sail' else MOTOR) if w[0] != slug and w[1] != model])[:4]
    body = f'''<section class="uh ugal" data-n="{len(g)}">
  <figure class="ugal__main uh__ph">{main}
    <button class="ugal__zoom" type="button" aria-label="Powiększ zdjęcie"></button>
  </figure>
  <div class="uh__shade" aria-hidden="true"></div>
  <div class="wrap uh__in">
    {crumbs([(lst, lst_name), (murl(model), model), (f"{slug}.html", name or model)])}
    <p class="micro uh__type">{"Jacht żaglowy" if kind == "sail" else "Jacht motorowy"}</p>
    <h1 class="uh__h unit__h"><span class="uh__m">{esc(model)}</span>{f'<span class="uh__n">{esc(name)}</span>' if name else ''}</h1>
    <span class="uh__count num" aria-hidden="true"><i data-lucide="images" class="lucide"></i><span class="ugal__n">1</span> / {len(g)}</span>
  </div>
  <div class="ustrip">
    <div class="wrap ustrip__in">
      <button class="ustrip__nav" type="button" data-dir="-1" aria-label="Poprzednie miniatury"><i data-lucide="arrow-left" class="lucide"></i></button>
      <div class="ugal__thumbs ustrip__t" role="group" aria-label="Zdjęcia jachtu">{thumbs}</div>
      <button class="ustrip__nav" type="button" data-dir="1" aria-label="Następne miniatury"><i data-lucide="arrow-right" class="lucide"></i></button>
    </div>
  </div>
</section>
<section class="uic">
  <div class="wrap"><ul class="uic__l num">{facts}</ul></div>
</section>
<section class="psec udesc">
  <div class="wrap g12">
    <div class="c6 udesc__t">
      <p class="micro muted">{esc(model)}{f" · {esc(name)}" if name else ""}</p>
      <h2 class="h2">O jachcie</h2>
      {desc}
    </div>
    <figure class="c5 o8 udesc__ph">{side}</figure>
  </div>
</section>
<section class="psec psec--sand udet">
  <div class="wrap">
    <div class="udet__g">
      {f'<details class="udet__i" open><summary><h2 class="h3">Wyposażenie</h2></summary><ul class="unit__eq">{equip}</ul></details>' if equip else ''}
      <details class="udet__i" open><summary><h2 class="h3">Dane techniczne</h2></summary><dl class="unit__spec num">{spec}</dl></details>
      {f'<details class="udet__i" open><summary><h2 class="h3">Cennik 2027</h2></summary>{ptab}</details>' if ptab else ''}
      {f'<details class="udet__i" open><summary><h2 class="h3">Warunki rezerwacji</h2></summary><ul class="unit__terms">{terms}</ul></details>' if terms else ''}
    </div>
  </div>
</section>
<section class="psec uav" id="dostepnosc">
  <div class="wrap g12">
    <div class="c6 uav__cal">
      <h2 class="h2">Dostępność i&nbsp;rezerwacja</h2>
      <div class="uav__price">{price_html(row)}</div>
      <div class="slot" data-slot="kalendarz-dostawcy"><i data-lucide="calendar-days" class="lucide" aria-hidden="true"></i>
        <p><b>Kalendarz dostępności</b>Tu wyświetli się kalendarz tej jednostki z systemu rezerwacji.</p></div>
      <p class="uav__hours">Wydanie jachtu 16:00 – 20:00 · zdanie 8:00 – 10:00</p>
    </div>
    <div class="c5 o8">
      <form class="kf uform" novalidate data-subject="{esc(subject)}">
        <h2 class="h3 kf__h">Zapytaj o czarter</h2>
        <p class="uform__about">Zapytanie dotyczy: <b>{esc(full)}</b></p>
        <input type="hidden" name="subject" value="{esc(subject)}">
        <div class="kf__f" data-f="name"><label for="u-name">Imię i nazwisko</label><input id="u-name" name="name" autocomplete="name" required><span class="kf__err">Podaj imię i nazwisko.</span></div>
        <div class="kf__row">
          <div class="kf__f" data-f="phone"><label for="u-tel">Telefon</label><input id="u-tel" name="phone" type="tel" autocomplete="tel" required><span class="kf__err">Podaj numer telefonu.</span></div>
          <div class="kf__f" data-f="email"><label for="u-mail">E-mail</label><input id="u-mail" name="email" type="email" autocomplete="email" required><span class="kf__err">Podaj poprawny adres e-mail.</span></div>
        </div>
        <div class="kf__row">
          <div class="kf__f"><label for="u-od">Termin od</label><input id="u-od" name="from" type="date"></div>
          <div class="kf__f"><label for="u-do">Termin do</label><input id="u-do" name="to" type="date"></div>
        </div>
        <div class="kf__f"><label for="u-msg">Wiadomość</label><textarea id="u-msg" name="message" rows="3"></textarea></div>
        <label class="uform__ok"><input type="checkbox" name="consent" required> <span>Wyrażam zgodę na przetwarzanie danych w celu odpowiedzi na zapytanie. Szczegóły w <a class="u u--on" href="polityka-prywatnosci.html">polityce prywatności</a>.</span></label>
        <span class="kf__err uform__okerr">Zaznacz zgodę, żebyśmy mogli odpowiedzieć.</span>
        <button class="btn kf__btn" type="submit"><span class="btn__label">Wyślij zapytanie</span> <i data-lucide="arrow-right" class="lucide"></i></button>
      </form>
      <div class="kf kf--ok" hidden tabindex="-1" role="status"><i data-lucide="check" class="lucide kf__ic"></i><h2 class="h3">Zapytanie wysłane</h2>
        <p>Dotyczy: {esc(full)}. Odpowiemy telefonicznie albo e-mailem.</p></div>
    </div>
  </div>
</section>
<section class="psec fleet">
  <div class="wrap">
    <h2 class="h3 psec__h">Inne jednostki</h2>
    <div class="fl">
{''.join(card(*w) for w in more)}    </div>
  </div>
</section>
<section class="ucta">
  <div class="wrap ucta__in">
    <div><h2 class="h2">{esc(model)}{f" „{esc(name)}”" if name else ""}</h2><p>Sprawdź dostępność i zaplanuj swój rejs już dziś.</p></div>
    <a class="btn btn--lg ucta__btn" href="#dostepnosc">Rezerwuj online <i data-lucide="arrow-right" class="lucide"></i></a>
  </div>
</section>'''
    first = next((t for tag, t in x['desc'] if tag == 'p'), f'{full} — czarter z Giżycka, Stanica Wodna Stranda.')
    page(f'{slug}.html', f'{full} — czarter na Mazurach, Giżycko | Jachty Mazury', first[:155], body, lst, UFORM_JS)

UFORM_JS = '''<script>
(function(){var f=document.querySelector('.uform');if(!f)return;var ok=f.nextElementSibling;
 var re={name:function(v){return v.trim().length>2},phone:function(v){return v.replace(/\\D/g,'').length>=9},email:function(v){return /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(v.trim())}};
 f.addEventListener('submit',function(e){e.preventDefault();var first=null;
  [].forEach.call(f.querySelectorAll('[data-f]'),function(w){var i=w.querySelector('input'),bad=!re[w.dataset.f](i.value);w.classList.toggle('has-error',bad);i.setAttribute('aria-invalid',bad);if(bad&&!first)first=i});
  var c=f.querySelector('[name=consent]');f.classList.toggle('no-consent',!c.checked);if(!c.checked&&!first)first=c;
  if(first){first.focus();return}
  var b=f.querySelector('.btn');b.classList.add('is-loading');
  setTimeout(function(){b.classList.remove('is-loading');f.hidden=true;ok.hidden=false;ok.focus();window.lucide&&lucide.createIcons()},900)});
})();
/* pasek miniatur: strzałki */
[].forEach.call(document.querySelectorAll('.ustrip__nav'),function(b){b.addEventListener('click',function(){var t=document.querySelector('.ustrip__t');t.scrollBy({left:+b.dataset.dir*t.clientWidth*.8,behavior:'smooth'})})});
</script>'''

# ---------------------------------------------------------------- strona modelu (do wysyłania ofert)
def model_extract(m):
    key = LIVE_MODEL.get(m, mslug(m)); kind = kind_of_model(m)
    f = f'_m/czarter-jachtow-{"zaglowych" if kind == "sail" else "motorowych"}_{key}.html'
    if not os.path.exists(f): return None
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<script.*?</script>|<style.*?</style>|<header.*?</header>|<footer.*?</footer>|<nav.*?</nav>', '', s, flags=re.S)
    a = s.find('<h1'); b = s.find('Zarządzaj opcjami'); out = []
    for mm in re.finditer(r'<(h1|h2|h3|p)\b[^>]*>(.*?)</\1>', s[a:b], re.S):
        t = jednostki._txt(mm.group(2))
        if not t or mm.group(1) == 'h1': continue
        if re.match(r'(Szukasz|Nie posiadasz|Jeśli planujesz|Sprawdź|Zobacz)', t): continue
        out.append(('h' if mm.group(1) != 'p' else 'p', t))
    return out

def model_page(m):
    kind = kind_of_model(m); lst, lst_name = list_of(kind); us = model_units(m)
    g = GAL.get(us[0][0], [])
    hero = gpic(us[0][0], g[0][0], g[0][1], g[0][2], g[0][3], '100vw', big=True, eager=True) if g else ''
    d = model_extract(m) or []
    desc = ''.join(f'<h3 class="udesc__h">{esc(t)}</h3>' if tag == 'h' else f'<p>{esc(t)}</p>' for tag, t in d)
    prices = [od(u[3]) for u in us if od(u[3])]
    body = f'''<section class="uh uh--model">
  <figure class="uh__ph">{hero}</figure>
  <div class="uh__shade" aria-hidden="true"></div>
  <div class="wrap uh__in">
    {crumbs([("czarter-jachtow.html", "Czarter jachtów"), (lst, lst_name), (murl(m), m)])}
    <p class="micro uh__type">{"Jachty żaglowe" if kind == "sail" else "Jachty motorowe"} · {len(us)} {"jednostka" if len(us) == 1 else ("jednostki" if 2 <= len(us) <= 4 else "jednostek")}</p>
    <h1 class="uh__h"><span class="uh__m">{esc(m)}</span></h1>
    {f'<p class="uh__price num">od {zl(min(prices))} / doba</p>' if prices else ''}
  </div>
</section>
<section class="psec fleet">
  <div class="wrap">
    <h2 class="h3 psec__h">Jednostki {esc(m)}</h2>
    <div class="fl">
{''.join(card(*w) for w in us)}    </div>
  </div>
</section>
{f"""<section class="psec psec--sand udesc">
  <div class="wrap"><div class="udesc__t udesc__t--wide"><h2 class="h2">O modelu {esc(m)}</h2>{desc}</div></div>
</section>""" if desc else ''}''' + cta('Wybrałeś termin?', 'Sprawdź, które jachty są wolne, albo zadzwoń do biura.')
    lead = next((t for tag, t in d if tag == 'p'), f'{m} — czarter z Giżycka.')
    page(murl(m), f'{m} — czarter na Mazurach, Giżycko | Jachty Mazury', lead[:155], body, lst)

# ---------------------------------------------------------------- hub „Czarter jachtów” z FAQ (treść 1:1 z /czarter-jachtow-gizycko/)
def hub_extract():
    s = open('_m/czarter-jachtow-gizycko.html', encoding='utf-8').read()
    s = re.sub(r'<script.*?</script>|<style.*?</style>|<header.*?</header>|<footer.*?</footer>|<nav.*?</nav>', '', s, flags=re.S)
    h1 = jednostki._txt(re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1))
    a = s.find('<h1'); q = s.find('Poznaj odpowiedzi'); z = s.find('Zarządzaj opcjami')
    intro = [jednostki._txt(p) for p in re.findall(r'<p\b[^>]*>(.*?)</p>', s[a:q], re.S)]
    ol = s[q:]; ol = ol[ol.find('<ol'):]
    # pytania: <li> najwyższego poziomu w <ol>
    faq = []; depth = 0; i = ol.find('>') + 1; cur = None; buf = ''
    for mm in re.finditer(r'<(/?)(ol|ul|li)\b[^>]*>', ol):
        tag, close = mm.group(2), mm.group(1)
        if tag == 'ol' and close: 
            if cur is not None: faq.append((cur, buf + ol[i:mm.start()]))
            end = mm.end(); break
        if tag == 'li' and not close and depth == 0:
            if cur is not None: faq.append((cur, buf + ol[i:mm.start()]))
            cur = None; buf = ''; i = mm.end()
            nxt = ol.find('<p', i); cur = jednostki._txt(ol[i:nxt]); i = nxt
        if tag in ('ul',): depth += -1 if close else 1
    def clean(h):
        h = re.sub(r'<(/?)(?:b|strong)\b[^>]*>', r'<\1strong>', h)
        h = re.sub(r'<(?!/?(?:p|ul|li|strong)\b)[^>]+>', '', h)
        h = re.sub(r'<(p|ul|li)\b[^>]*>', r'<\1>', h)
        h = re.sub(r'<li>\s*<p>(.*?)</p>', r'<li>\1', h, flags=re.S)
        h = re.sub(r'<p>\s*</p>', '', h); h = re.sub(r'<li>\s*</li>', '', h)
        return re.sub(r'\s+', ' ', H.unescape(h)).replace('<strong> </strong>', ' ').strip()
    faq = [(qq, clean(aa)) for qq, aa in faq if qq]
    rest = s[q + (ol.find('</ol>') if '</ol>' in ol else 0):z]
    sections = []
    for mm in re.finditer(r'<(h4|h3|p|li)\b[^>]*>(.*?)</\1>', s[s.find('Nasza Giżycka flota') - 60:z], re.S):
        t = jednostki._txt(mm.group(2))
        if t: sections.append((mm.group(1), t))
    return h1, intro, faq, sections

def hub_page():
    h1, intro, faq, secs = hub_extract()
    def tile(href, title, units):
        u = units[0]
        return (f'<a class="ht" href="{href}"><figure class="ht__ph">{pic("u-" + u[0], title, "(min-width:1024px) 30vw, 100vw")}</figure>'
                f'<span class="ht__t">{title}</span><span class="ht__n num">{len(units)} {"jednostek" if len(units) > 4 else "jednostki"}</span></a>')
    bez = [u for u in MOTOR if u[0] != 'stillo-31-star']
    items = ''.join(f'<details class="faq__i"><summary>{esc(qq)}</summary><div class="faq__a">{aa}</div></details>' for qq, aa in faq)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': qq, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'<[^>]+>', ' ', aa).strip()}} for qq, aa in faq]}, ensure_ascii=False)
    seo = ''
    lst = False
    for tag, t in secs:
        if tag == 'li':
            if not lst: seo += '<ul>'; lst = True
            seo += f'<li>{esc(t)}</li>'; continue
        if lst: seo += '</ul>'; lst = False
        seo += f'<h2 class="h3">{esc(t)}</h2>' if tag in ('h4', 'h3') else f'<p>{esc(t)}</p>'
    if lst: seo += '</ul>'
    body = (phead([('czarter-jachtow.html', 'Czarter jachtów')], 'Stanica Wodna Stranda · Giżycko', esc(h1), esc(intro[0]) if intro else '')
     + f'''<section class="psec">
  <div class="wrap">
    <div class="hts">{tile("jachty-zaglowe.html", "Jachty żaglowe", SAIL)}{tile("jachty-motorowe.html", "Jachty motorowe", MOTOR)}{tile("czarter-bez-patentu.html", "Czarter bez patentu", bez)}</div>
    <div class="hub__intro">{''.join(f"<p>{esc(p)}</p>" for p in intro[1:])}</div>
  </div>
</section>
<section class="psec psec--sand">
  <div class="wrap faq">
    <h2 class="h2">Najczęściej zadawane pytania</h2>
    <div class="faq__l">{items}</div>
  </div>
</section>
<section class="psec">
  <div class="wrap"><div class="art__body hub__seo">{seo}</div></div>
</section>''' + cta('Wybrałeś termin?', 'Sprawdź, które jachty są wolne, albo zadzwoń do biura.'))
    page('czarter-jachtow.html', 'Czarter jachtów Giżycko — jachty żaglowe, motorowe i houseboaty | Jachty Mazury',
         (intro[0] if intro else h1)[:155], body, 'czarter-jachtow.html', f'<script type="application/ld+json">{ld}</script>')

# ---------------------------------------------------------------- Wiedza: filmy i aktualności
def filmy_page():
    body = (phead([('poradnik.html', 'Wiedza'), ('filmy-szkoleniowe.html', 'Filmy szkoleniowe')], 'Wiedza', 'Filmy szkoleniowe',
                  'Praktyczne porady, manewry, trasy i życie na jachcie. Zobacz, zanim wyruszysz.')
     + '''<section class="psec">
  <div class="wrap">
    <div class="slot slot--wide" data-slot="filmy-youtube"><i data-lucide="play" class="lucide" aria-hidden="true"></i>
      <p><b>Filmy z kanału YouTube</b>Lista filmów pojawi się tu automatycznie po podpięciu kanału.</p></div>
  </div>
</section>''' + cta('Wybrałeś termin?', 'Sprawdź, które jachty są wolne, albo zadzwoń do biura.'))
    page('filmy-szkoleniowe.html', 'Filmy szkoleniowe | Jachty Mazury', 'Praktyczne porady, manewry, trasy i życie na jachcie — filmy szkoleniowe Jachty Mazury.', body, 'filmy-szkoleniowe.html')

def news_card(a, big=False):
    return (f'<a class="nc" href="{a["slug"]}.html"><figure class="nc__ph">{pic("art-" + a["slug"], a["h1"], "(min-width:1024px) 30vw, 100vw")}</figure>'
            f'<span class="nc__k micro">Poradnik</span><span class="nc__t">{esc(a["h1"])}</span><span class="nc__l">{esc(a["lead"])}</span>'
            f'<span class="nc__go">Czytaj więcej <i data-lucide="arrow-right" class="lucide"></i></span></a>')

def news_page():
    body = (phead([('poradnik.html', 'Wiedza'), ('aktualnosci.html', 'Aktualności')], 'Wiedza', 'Aktualności',
                  'Najnowsze wpisy z działu Wiedza.')
     + f'<section class="psec"><div class="wrap"><div class="ncs">{"".join(news_card(a) for a in ART)}</div></div></section>'
     + cta('Wybrałeś termin?', 'Sprawdź, które jachty są wolne, albo zadzwoń do biura.'))
    page('aktualnosci.html', 'Aktualności | Jachty Mazury', 'Najnowsze wpisy Jachty Mazury: poradniki, trasy i informacje z mariny w Giżycku.', body, 'aktualnosci.html')

# ---------------------------------------------------------------- strona główna (wizualizacje -2/-3 wg wyboru klientki)
def model_card(m):
    us = model_units(m); u = us[0]; sp = UNITS[u[0]]['spec']; kind = kind_of_model(m)
    mj = berths(sp.get('Liczba osób', '–'))[0]
    return (f'<a class="rc" href="{murl(m)}"><figure class="rc__ph">{pic("u-" + u[0], m, "(min-width:1024px) 22vw, 70vw")}'
            f'<span class="rc__tag">{"Jacht żaglowy" if kind == "sail" else "Jacht motorowy"}</span></figure>'
            f'<span class="rc__b"><span class="rc__t">{esc(m)}</span><span class="rc__go" aria-hidden="true"><i data-lucide="arrow-right" class="lucide"></i></span>'
            f'<span class="rc__m num"><span><i data-lucide="users" class="lucide" aria-hidden="true"></i> {mj} os.</span>'
            f'<span><i data-lucide="door-closed" class="lucide" aria-hidden="true"></i> {sp.get("Zamykane kabiny", "–")} kab.</span></span></span></a>')

def home_page():
    ms = []
    for a, b in zip(models(SAIL), models(MOTOR) + [None] * 20):
        ms.append(a)
        if b: ms.append(b)
    ms += [m for m in models(MOTOR) if m not in ms]
    team = [('SP', 'Sebastian Pażyszek', 'Właściciel', 'ink'), ('B', 'Beata', 'Obsługa czarteru', 'deep'), ('K', 'Kamil', 'Obsługa czarteru', 'sage'), ('P', 'Patrycja', 'Obsługa czarteru', 'paper')]
    icons = [('calendar-days', 'Szybka rezerwacja', 'Sprawdź dostępność i zarezerwuj w kilka minut.'),
             ('sailboat', 'Sprawdzone jachty', 'Komfortowe i świetnie wyposażone.'),
             ('map', 'Lokalna wiedza', 'Doradzimy najlepsze trasy i miejsca.'),
             ('heart', 'Wsparcie na każdym etapie', 'Jesteśmy blisko – przed, w trakcie i po rejsie.')]
    body = f'''<section class="hh">
  <figure class="hh__ph">{pic("fl-a30", "Antila 30 pod żaglami na jeziorze", "100vw", True) if "fl-a30" in WS else '<picture><source type="image/webp" srcset="assets/img/r/fl-a30-600.webp 600w, assets/img/r/fl-a30-1280.webp 1280w" sizes="100vw"><img src="assets/img/r/fl-a30-1280.jpg" srcset="assets/img/r/fl-a30-600.jpg 600w, assets/img/r/fl-a30-1280.jpg 1280w" sizes="100vw" width="1280" height="960" alt="Antila 30 pod żaglami na jeziorze" fetchpriority="high" decoding="async"></picture>'}</figure>
  <div class="hh__shade" aria-hidden="true"></div>
  <div class="wrap hh__in">
    <p class="micro hh__eye">Czarter jachtów · Giżycko</p>
    <h1 class="hh__h">Mazury w&nbsp;najlepszym wydaniu</h1>
    <p class="hh__lead">Wolność. Przygoda. Niezapomniane chwile.</p>
    <a class="btn btn--lg hh__btn" href="#rezerwuj" data-open-modal>Sprawdź dostępność i zarezerwuj online <i data-lucide="arrow-right" class="lucide"></i></a>
  </div>
</section>
<section class="hi">
  <div class="wrap"><ul class="hi__l">{''.join(f'<li><i data-lucide="{ic}" class="lucide" aria-hidden="true"></i><b>{t}</b><span>{d}</span></li>' for ic, t, d in icons)}</ul></div>
</section>
<section class="psec rec">
  <div class="wrap">
    <div class="sech"><h2 class="h2">Polecane jachty</h2>
      <div class="sech__a"><a class="u u--on" href="czarter-jachtow.html">Zobacz wszystkie jachty →</a>
        <button class="rec__nav" type="button" data-dir="-1" aria-label="Poprzednie jachty"><i data-lucide="arrow-left" class="lucide"></i></button>
        <button class="rec__nav" type="button" data-dir="1" aria-label="Następne jachty"><i data-lucide="arrow-right" class="lucide"></i></button></div></div>
    <div class="rec__t" id="rec-t">{''.join(model_card(m) for m in ms)}</div>
  </div>
</section>
<section class="kt">
  <a class="kt__i kt__i--film" href="filmy-szkoleniowe.html">
    <figure class="kt__ph">{gpic("antila-30-1-e-cleopatra", *GAL["antila-30-1-e-cleopatra"][4], "(min-width:1024px) 50vw, 100vw", big=True)}</figure>
    <span class="kt__b"><span class="kt__play" aria-hidden="true"><i data-lucide="play" class="lucide"></i></span><span class="kt__t">Filmy szkoleniowe na naszym YouTube</span><span class="kt__d">Praktyczne porady, manewry, trasy i życie na jachcie. Zobacz, zanim wyruszysz!</span><span class="btn kt__btn">Zobacz filmy <i data-lucide="arrow-right" class="lucide"></i></span></span>
  </a>
  <a class="kt__i kt__i--guide" href="poradnik.html">
    <figure class="kt__ph">{pic("art-" + ART[0]["slug"], "Poradnik czarterowy", "(min-width:1024px) 50vw, 100vw")}</figure>
    <span class="kt__b"><span class="kt__t">Poradnik czarterowy</span><span class="kt__d">Praktyczna wiedza, inspiracje i sprawdzone trasy po Mazurach.</span><span class="btn kt__btn">Przejdź do poradnika <i data-lucide="arrow-right" class="lucide"></i></span></span>
  </a>
</section>
<section class="psec news">
  <div class="wrap">
    <div class="sech"><h2 class="h2">Aktualności</h2><div class="sech__a"><a class="u u--on" href="aktualnosci.html">Zobacz wszystkie aktualności →</a></div></div>
    <div class="ncs">{''.join(news_card(a) for a in ART[:3])}</div>
  </div>
</section>
<section class="psec psec--sand ab">
  <div class="wrap g12">
    <div class="c5 ab__t">
      <p class="micro muted">O nas</p>
      <h2 class="h2">Ludzie. Pasja. Mazury.</h2>
      <p class="ab__lead">Od <strong>ponad 10&nbsp;lat</strong> oferujemy czarter jachtów na Mazurach, zapewniając bezpieczny i spokojny wypoczynek na wodzie. Stawiamy na jakość techniczną, niezawodność i realny komfort załogi.</p>
      <p>Nasza flota to starannie przygotowane jachty żaglowe, motorowe i houseboaty, regularnie serwisowane i w pełni wyposażone. Zapewniamy szkolenie przed rejsem, pomoc w planowaniu trasy oraz wsparcie techniczne na Szlaku Wielkich Jezior Mazurskich.</p>
    </div>
    <ul class="c7 ab__team">{''.join(f'<li class="mem mem--{c}"><span class="mem__ini" aria-hidden="true">{i}</span><b class="mem__n">{n}</b><span class="mem__r">{r}</span></li>' for i, n, r, c in team)}</ul>
  </div>
</section>
<section class="loc on-dark">
  <figure class="loc__ph">{pic("port", "Stanica Wodna Stranda w Giżycku z lotu ptaka", "(min-width:1024px) 60vw, 100vw")}</figure>
  <div class="wrap loc__in">
    <div class="loc__t">
      <h2 class="h2">Nasza lokalizacja</h2>
      <p class="loc__sub">Giżycko – serce Mazur</p>
      <p>Stacjonujemy w Giżycku w porcie Stranda, położonym nad zatoką Tracz na jeziorze Kisajno. Stranda to nowoczesny kompleks wypoczynkowy znajdujący się ok. 2 km od centrum Giżycka.</p>
      <a class="btn loc__btn" href="{MAPS}" rel="noopener" target="_blank">Zobacz na mapie <i data-lucide="arrow-up-right" class="lucide"></i></a>
    </div>
    <ul class="loc__bar">
      <li><i data-lucide="map-pin" class="lucide" aria-hidden="true"></i><span><b>Stanica Wodna Stranda</b>Pierkunowo 36, 11-500 Giżycko</span></li>
      <li><i data-lucide="clock" class="lucide" aria-hidden="true"></i><span><b>Biuro</b>Codziennie 8:00 – 20:00</span></li>
      <li><i data-lucide="phone" class="lucide" aria-hidden="true"></i><a class="num" href="{TEL_H}">{TEL}</a></li>
      <li><i data-lucide="mail" class="lucide" aria-hidden="true"></i><a href="mailto:{MAIL}">{MAIL}</a></li>
    </ul>
  </div>
</section>
<div class="bk" id="rezerwuj-okno" role="dialog" aria-modal="true" aria-labelledby="bk-h" hidden>
  <div class="bk__bg" data-close-modal></div>
  <div class="bk__p">
    <button class="bk__x" type="button" data-close-modal aria-label="Zamknij"><i data-lucide="x" class="lucide"></i></button>
    <p class="micro muted">Rezerwacja online</p><h2 class="h3" id="bk-h">Sprawdź dostępność</h2>
    <div class="slot" data-slot="okno-rezerwacji"><i data-lucide="calendar-days" class="lucide" aria-hidden="true"></i><p><b>Okno rezerwacji</b>Tu wyświetli się kalendarz z systemu rezerwacji.</p></div>
    <div class="bk__a"><a class="btn" href="czarter-jachtow.html">Zobacz jachty</a><a class="btn btn--outline" href="{TEL_H}"><i data-lucide="phone" class="lucide"></i> {TEL}</a></div>
  </div>
</div>'''
    js = '''<script>
(function(){
 var m=document.getElementById('rezerwuj-okno'),last=null;
 function open(e){if(e)e.preventDefault();last=document.activeElement;m.hidden=false;document.body.classList.add('lb-open');m.querySelector('.bk__x').focus()}
 function close(){m.hidden=true;document.body.classList.remove('lb-open');if(last)last.focus()}
 [].forEach.call(document.querySelectorAll('[data-open-modal],a[href="index.html#rezerwuj"],a[href="#rezerwuj"]'),function(a){a.addEventListener('click',open)});
 [].forEach.call(m.querySelectorAll('[data-close-modal]'),function(b){b.addEventListener('click',close)});
 m.addEventListener('keydown',function(e){if(e.key==='Escape')close();if(e.key!=='Tab')return;var f=[].slice.call(m.querySelectorAll('a,button')),a=f[0],z=f[f.length-1];
  if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}});
 if(location.hash==='#rezerwuj')setTimeout(open,200);
 var t=document.getElementById('rec-t');
 [].forEach.call(document.querySelectorAll('.rec__nav'),function(b){b.addEventListener('click',function(){var c=t.querySelector('.rc');t.scrollBy({left:+b.dataset.dir*(c?c.getBoundingClientRect().width+20:300),behavior:'smooth'})})});
})();
</script>'''
    page('index.html', 'Czarter jachtów Giżycko — jachty żaglowe i motorowe na Mazurach | Jachty Mazury',
         'Czarter jachtów żaglowych i motorowych z Giżycka. Stanica Wodna Stranda, flota Antila, Maxus, Nautic, Nexus. Cennik 2027, biuro codziennie 8:00–20:00.',
         body, 'index.html', js)

for u in SAIL + MOTOR: unit_page(u)
for m in models(SAIL + MOTOR): model_page(m)
hub_page(); filmy_page(); news_page(); home_page()
