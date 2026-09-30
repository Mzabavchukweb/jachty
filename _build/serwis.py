# Strony wg uwag klientki: strona główna, jednostki (-1), modele, hub „Czarter jachtów”, Wiedza. Wykonywane wewnątrz podstrony.py.
import jednostki
IBS = json.load(open('_u/ibs-spacery.json'))   # z obecnej strony i systemu IBS (29.09): kod stacji, spacer wirtualny
SPACERY = {k: v['tour'] for k, v in IBS.items() if v.get('tour')}   # jednostka → spacer wirtualny; zastępuje zdjęcie obok opisu
GAL = json.load(open('_img/galerie-ws.json'))
KIND = {u[0]: 'sail' for u in SAIL} | {u[0]: 'motor' for u in MOTOR}
MAPS = PIN
LIVE_MODEL = {m: p.split('/')[-1] for m, p in LIVE_MODEL_PAGES.items()}          # nazwa modelu u nas → adres strony modelu u klienta

def gpic(slug, n, ws, W, H, sizes, big=False, eager=False, alt=None):
    src = lambda e: ', '.join(f'assets/img/j/{slug}/{n}-{w}.{e} {w}w' for w in ws)
    w0 = ws[-1] if big else ws[0]
    return (f'<picture><source type="image/webp" srcset="{src("webp")}" sizes="{sizes}">'
            f'<img src="assets/img/j/{slug}/{n}-{w0}.jpg" srcset="{src("jpg")}" sizes="{sizes}" width="{W}" height="{H}" alt="{esc(gal_alt(slug, n) if alt is None else alt)}"'
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
    add('move-vertical', 'Długość', spec_val('Długość', sp.get('Długość', '')))      # strzałki zamienione (uwagi 29.09)
    add('move-horizontal', 'Szerokość', spec_val('Szerokość', sp.get('Szerokość', '')))
    add('waves', 'Zanurzenie', spec_val('Zanurzenie', sp.get('Zanurzenie', '')))
    add('bed-double', 'Miejsca do spania', berths(sp.get('Liczba osób', '–'))[0] if sp.get('Liczba osób') else '')
    kab = IBS.get(slug, {}).get('kabiny') or sp.get('Zamykane kabiny', '')   # IBS uzupełnia brak w tabeli (np. Nautic 880)
    add('door-closed', 'Kabiny', 'otwarte' if kab == '0' else kab)
    if 'wc morskie' in eq or 'toaleta morska' in eq: add('bath', 'Toaleta', 'morska')
    elif 'chemiczn' in eq: add('bath', 'Toaleta', 'chemiczna')
    if 'prysznic' in eq: add('shower-head', 'Prysznic', 'z ciepłą wodą' if 'ciepłą wodą' in eq else 'tak')
    ster = sp.get('Typ steru', '').lower()
    if IBS.get(slug, {}).get('ster'): ster = IBS[slug]['ster']   # typ steru z systemu rezerwacji klientki (IBS), gdy go podaje
    if 'koło' in ster or 'koło sterowe' in eq: add('ship-wheel', 'Ster', 'koło')
    elif 'rumpel' in ster or 'rumpel' in eq: add('ship-wheel', 'Ster', 'rumpel')
    elif ster: add('ship-wheel', 'Ster', ster)   # np. „płetwa na pawęży” — wartość z tabeli danych jednostki
    eng = sp.get('Typ silnika', '').lower()
    power = re.search(r'silnik[^|]*?(\d+[.,]?\d*)\s*km', eq)
    if eng:
        e = 'zaburtowy' if 'przyczep' in eng or 'zaburt' in eng else ('stacjonarny' if 'stacjonarn' in eng else eng)
        eic = {'zaburtowy': 'img:silnik-zaburtowy', 'stacjonarny': 'img:silnik-stacjonarny', 'elektryczny': 'img:silnik-elektryczny'}.get(e, 'cog')   # ikony z grafiki klientki
        add(eic, 'Silnik', e + (f' · {power.group(1).replace(".", ",")} KM' if power else ''))
    if 'dziobowy i rufowy ster strumieniowy' in eq: add('img:ster-strumieniowy', 'Ster strumieniowy', '2')
    elif 'ster strumieniowy' in eq: add('img:ster-strumieniowy', 'Ster strumieniowy', '1')
    add('calendar', 'Rok produkcji', sp.get('Rok produkcji', ''))
    return out

def ico(ic, size=30):
    """Ikona parametru: Lucide albo raster z grafiki klientki (prefiks img:)."""
    if ic.startswith('img:'):
        return f'<img class="ico" src="assets/img/ikony/{ic[4:]}.png" width="{size}" height="{size}" alt="" aria-hidden="true">'
    return f'<i data-lucide="{ic}" class="lucide" aria-hidden="true"></i>'

def price_html(row):
    p = od(row)
    return (f'<span class="micro muted">Cena od</span><p class="unit__price num"><b>{zl(p)}</b> <span>/ doba</span></p>' if p
            else '<span class="micro muted">Cena</span><p class="unit__price unit__price--ask">na zapytanie</p>')

def model_units(m): return [u for u in SAIL + MOTOR if u[1] == m]
def kind_of_model(m): return 'sail' if any(u[1] == m for u in SAIL) else 'motor'
def list_of(kind): return ('jachty-zaglowe.html', 'Jachty żaglowe') if kind == 'sail' else ('jachty-motorowe.html', 'Jachty motorowe')

# ---------------------------------------------------------------- strona jednostki (wizualizacja -1)
def unit_card(w):
    s2, m2, n2, r2 = w; sp2 = UNITS[s2]['spec']; g2 = GAL.get(s2, [])
    ph = gpic(s2, *g2[0], '(min-width:1024px) 22vw, 70vw') if g2 else pic('u-' + s2, uname(w), '(min-width:1024px) 22vw, 70vw')
    mj = berths(sp2.get('Liczba osób', '–'))[0]; kab = sp2.get('Zamykane kabiny', ''); kab = 'otwarte' if kab == '0' else kab
    eng = _engine(s2)
    meta = (f'<span><i data-lucide="users" class="lucide" aria-hidden="true"></i> {mj} os.</span>' if mj and mj != '–' else '')
    meta += (f'<span><i data-lucide="door-closed" class="lucide" aria-hidden="true"></i> {esc(kab)}{" kab." if kab != "otwarte" else ""}</span>' if kab and kab not in ('–', '-') else '')
    meta += (f'<span class="rc__eng">{_engine_ico(s2)} silnik {esc(eng)}</span>' if eng else '')
    return (f'<a class="rc" href="{s2}.html"><figure class="rc__ph">{ph}<span class="rc__tag">{"Jacht żaglowy" if KIND[s2] == "sail" else "Jacht motorowy"}</span></figure>'
            f'<span class="rc__b"><span class="rc__t">{esc(uname(w))}</span><span class="rc__go" aria-hidden="true"><i data-lucide="arrow-right" class="lucide"></i></span>'
            f'<span class="rc__m num">{meta}</span></span></a>')

def unit_page(u):
    slug, model, name, row = u
    kind = KIND[slug]; full = uname(u); lst, lst_name = list_of(kind)
    x = jednostki.extract(slug); sp = UNITS[slug]['spec']; g = GAL.get(slug, [])
    main = gpic(slug, g[0][0], g[0][1], g[0][2], g[0][3], '100vw', big=True, eager=True) if g else ''
    thumbs = ''.join(f'<button type="button" data-i="{i}" aria-label="Powiększ zdjęcie {i+1} z {len(g)}"{" aria-current=\"true\"" if i == 0 else ""}>'
                     f'{gpic(slug, n, ws, W, H, "180px")}</button>' for i, (n, ws, W, H) in enumerate(g))
    def fv(v):
        main, _, extra = v.partition(' · ')
        return f'<b>{main}</b>' + (f'<small>{extra}</small>' if extra else '')
    facts = ''.join(f'<li>{ico(ic)}<span class="uic__k">{k}</span>{fv(v)}</li>' for ic, k, v in unit_facts(slug))
    cut = next((i for i, (tag, t) in enumerate(x['desc']) if tag == 'h2'), len(x['desc']))
    cut = max(cut, 1)
    def blk(part):   # opis: nagłówki, akapity i listy w kolejności z obecnej strony
        o, lst = '', False
        for tag, t in part:
            if tag == 'li' and not lst: o += '<ul class="udesc__l">'; lst = True
            if tag != 'li' and lst: o += '</ul>'; lst = False
            o += f'<li>{t}</li>' if tag == 'li' else (f'<h3 class="udesc__h">{esc(t)}</h3>' if tag == 'h2' else f'<p>{t}</p>')
        return o + ('</ul>' if lst else '')
    lead_d, more_d = blk(x['desc'][:cut]), blk(x['desc'][cut:])
    # suwak: najpierw zdjęcia wnętrza (rozpoznane po opisie zdjęcia na obecnej stronie), potem reszta
    INSIDE = ('wnętrz', 'wnetrz', 'mes', 'kambuz', 'kabin', 'salon', 'łazien', 'toalet', 'kuchni', 'sterówk', 'koj')
    order = list(range(len(g)))
    inside = [i for i in order if any(k in gal_alt(slug, g[i][0]).lower() for k in INSIDE)]
    start = inside[0] if inside else min(1, len(g) - 1) if g else 0
    order = order[start:] + order[:start]
    slides = ''.join(f'<figure class="usl__s{" is-on" if k == 0 else ""}" data-i="{i}"{"" if k == 0 else " hidden"}>{gpic(slug, *g[i], "(min-width:1024px) 58vw, 100vw", big=True)}'
                     f'{f"<figcaption>{esc(gal_alt(slug, g[i][0]))}</figcaption>" if gal_alt(slug, g[i][0]) else ""}</figure>' for k, i in enumerate(order))
    side = (f'<div class="usl" data-n="{len(order)}">{slides}'
            f'<button class="usl__nav usl__nav--prev" type="button" data-dir="-1" aria-label="Poprzednie zdjęcie"><i data-lucide="arrow-left" class="lucide"></i></button>'
            f'<button class="usl__nav usl__nav--next" type="button" data-dir="1" aria-label="Następne zdjęcie"><i data-lucide="arrow-right" class="lucide"></i></button>'
            f'<button class="usl__zoom" type="button" aria-label="Powiększ zdjęcie"></button>'
            f'<span class="usl__n num" aria-hidden="true"><b>1</b> / {len(order)}</span></div>') if g else ''
    equip = ''.join(f'<li>{esc(e)}</li>' for e in x['equip'])
    keys = [k for k in SPEC_ORDER if k in sp] + [k for k in sp if k not in SPEC_ORDER]
    spec = ''.join(f'<div><dt>{esc(k)}</dt><dd>{spec_val(k, sp[k])}</dd></div>' for k in keys)
    terms = ''.join(f'<li>{esc(t)}</li>' for t in x['terms'])
    v = ROWS.get(row); ptab = ''
    if v:
        lis = ''.join(f'<li><span class="up__r num">{r}</span><span class="up__t">{t}</span><span class="up__p num"><b>{zl(int(val)) if val.strip().isdigit() else "—"}</b><small>{un}</small></span></li>' for (r, un, t), val in zip(periods, v[:11]))
        ptab = (f'<ul class="unit__prices">{lis}<li class="unit__px"><span class="up__r">Kaucja</span><span class="up__t"></span><span class="up__p num"><b>{zl(int(v[11]))}</b></span></li>'
                f'<li class="unit__px"><span class="up__r">Sprzątanie</span><span class="up__t"></span><span class="up__p num"><b>{zl(int(v[12]))}</b></span></li></ul>'
                f'<p class="unit__note">Cena za dobę obowiązuje przy czarterze minimum tygodniowym. Przy krótszych terminach cena ustalana jest indywidualnie.</p>')
    subject = f'Zapytanie o czarter: {full}'
    # karuzela: najpierw jednostki tego samego modelu, potem reszta tego typu (uwagi 29.09, J8)
    more = ([w for w in SAIL + MOTOR if w[0] != slug and w[1] == model] + [w for w in (SAIL if kind == 'sail' else MOTOR) if w[0] != slug and w[1] != model])[:10]
    form_html = f'''<form class="kf uform" novalidate data-subject="{esc(subject)}">
        <h2 class="h2 sec-line kf__h">Zapytaj o czarter</h2>
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
        <p>Dotyczy: {esc(full)}. Odpowiemy telefonicznie albo e-mailem.</p></div>'''
    # J4: kalendarz rezerwacji IBS (wersja testowa od klientki) tam, gdzie system zna jednostkę; bez „ceny od”, godzin i broszury
    if IBS.get(slug, {}).get('ibs'):
        ibs_url = f'https://beta.ibs-integra.pl/ClientScheduler/Availability?pointOfServiceCode=jachty-mazury&amp;station={slug}&amp;mode=select&amp;months=3&amp;monthsMobile=1&amp;embed=1&amp;reservationTarget=parent'
        avail = f'''<section class="psec uav" id="dostepnosc">
  <div class="wrap">
    <h2 class="h2 sec-line">Dostępność i&nbsp;rezerwacja</h2>
    <div class="ibs"><iframe title="Wybór terminu czarteru: {esc(full)}" src="{ibs_url}" data-ibs loading="lazy"></iframe></div>
    <div class="uav__ask g12">
      <div class="c5"><h2 class="h3">Wolisz zapytać?</h2><p>Napisz przez formularz albo zadzwoń: <a class="u u--on num" href="{TEL_H}">{TEL}</a>. Biuro czynne codziennie 8:00 – 20:00.</p></div>
      <div class="c7">{form_html}</div>
    </div>
  </div>
</section>'''
    else:
        avail = f'''<section class="psec uav" id="dostepnosc">
  <div class="wrap g12">
    <div class="c5"><h2 class="h2 sec-line">Dostępność i&nbsp;rezerwacja</h2><p>Zapytaj o wolne terminy — odpowiemy telefonicznie albo e-mailem.</p>
      <p>Telefon: <a class="u u--on num" href="{TEL_H}">{TEL}</a> · biuro czynne codziennie 8:00 – 20:00.</p></div>
    <div class="c7">{form_html}</div>
  </div>
</section>'''
    body = f'''<section class="uh ugal" data-n="{len(g)}">
  <figure class="ugal__main uh__ph">{main}
    <button class="ugal__zoom" type="button" aria-label="Powiększ zdjęcie"></button>
  </figure>
  <div class="uh__shade" aria-hidden="true"></div>
  <button class="uh__arrow uh__arrow--prev" type="button" data-dir="-1" aria-label="Poprzednie zdjęcie"><i data-lucide="arrow-left" class="lucide"></i></button>
  <button class="uh__arrow uh__arrow--next" type="button" data-dir="1" aria-label="Następne zdjęcie"><i data-lucide="arrow-right" class="lucide"></i></button>
  <div class="wrap uh__in">
    {crumbs([(lst, lst_name), (murl(model), model), (f"{slug}.html", name or model)])}
    <h1 class="uh__h unit__h"><span class="uh__m">{esc(model)}</span>{f'<span class="uh__n"><span class="sr"> „</span>{esc(name)}<span class="sr">”</span></span>' if name else ''}</h1>
    <span class="uh__count num" aria-hidden="true"><span class="ugal__n">1</span> / {len(g)}</span>
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
<section class="udesc2">
  <div class="udesc2__g">
    <div class="udesc2__t">
      <p class="micro udesc2__eye">{esc(model)}{f" · {esc(name)}" if name else ""}</p>
      <h2 class="h2 sec-line">O jachcie</h2>
      <div class="udesc2__lead">{lead_d}</div>
      {f'<div class="udesc2__more" id="opis-{slug}">{more_d}</div><button class="udesc2__btn" type="button" aria-expanded="false" aria-controls="opis-{slug}"><span>Czytaj cały opis</span> <i data-lucide="chevron-down" class="lucide"></i></button>' if more_d else ''}
    </div>
    <div class="udesc2__m">{f'<div class="vt" data-src="{esc(SPACERY[slug])}"><button class="vt__play" type="button"><i data-lucide="rotate-3d" class="lucide" aria-hidden="true"></i> Spacer wirtualny po jachcie</button></div>' if slug in SPACERY else side}</div>
  </div>
</section>

<section class="psec udet2">
  <div class="wrap">
    <div class="udet2__g">
      {f'<details class="udet__i udet2__c" open><summary><h2 class="h3">Wyposażenie</h2></summary><ul class="unit__eq">{equip}</ul></details>' if equip else ''}
      {f'<details class="udet__i udet2__c" open><summary><h2 class="h3">Warunki rezerwacji</h2></summary><ul class="unit__terms">{terms}</ul></details>' if terms else ''}
    </div>
    <details class="udet__i udet2__spec"><summary><h2 class="h3">Dane techniczne</h2></summary><dl class="unit__spec num">{spec}</dl></details>
  </div>
</section>
{avail}
<section class="psec urel">
  <div class="wrap">
    <div class="sech"><h2 class="h2">Inne jednostki</h2>
      <div class="sech__a"><button class="rec__nav" type="button" data-car="-1" aria-label="Poprzednie jednostki"><i data-lucide="arrow-left" class="lucide"></i></button>
        <button class="rec__nav" type="button" data-car="1" aria-label="Następne jednostki"><i data-lucide="arrow-right" class="lucide"></i></button></div></div>
    <div class="rec__t car__t">{''.join(unit_card(w) for w in more)}</div>
  </div>
</section>'''
    first = re.sub(r'<[^>]+>', '', next((t for tag, t in x['desc'] if tag == 'p'), f'{full} — czarter z Giżycka, Stanica Wodna Stranda.'))
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
/* suwak zdjęć przy opisie */
(function(){var w=document.querySelector('.usl');if(!w)return;var ss=[].slice.call(w.querySelectorAll('.usl__s')),n=w.querySelector('.usl__n b'),c=0;
 function go(k){ss[c].hidden=true;ss[c].classList.remove('is-on');c=(k+ss.length)%ss.length;ss[c].hidden=false;ss[c].classList.add('is-on');n.textContent=c+1}
 [].forEach.call(w.querySelectorAll('.usl__nav'),function(b){b.addEventListener('click',function(){go(c+(+b.dataset.dir))})});
 var tx=null;w.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
 w.addEventListener('touchend',function(e){if(tx===null)return;var d=e.changedTouches[0].clientX-tx;tx=null;if(Math.abs(d)>45)go(c+(d<0?1:-1))});
 w.querySelector('.usl__zoom').addEventListener('click',function(){var t=document.querySelectorAll('.ustrip__t button')[+ss[c].dataset.i];if(t)t.click()});
})();
/* telefon: szczegóły domyślnie zwinięte */
if(matchMedia('(max-width:640px)').matches)[].forEach.call(document.querySelectorAll('.udet__i'),function(d){d.open=false});
/* opis: rozwiń / zwiń */
(function(){var b=document.querySelector('.udesc2__btn');if(!b)return;var m=document.getElementById(b.getAttribute('aria-controls'));
 b.addEventListener('click',function(){var o=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',o);m.classList.toggle('is-open',o);b.querySelector('span').textContent=o?'Zwiń opis':'Czytaj cały opis'})})();
/* kalendarz: dwa miesiące, kliknięty dzień trafia do formularza */
(function(){var ms=document.querySelectorAll('.ucal__m');if(!ms.length)return;var now=new Date(),M=['Styczeń','Luty','Marzec','Kwiecień','Maj','Czerwiec','Lipiec','Sierpień','Wrzesień','Październik','Listopad','Grudzień'],off=0;
 var from=document.getElementById('u-od'),to=document.getElementById('u-do');
 function pad(x){return(x<10?'0':'')+x}
 function draw(){[].forEach.call(ms,function(el,k){var d=new Date(now.getFullYear(),now.getMonth()+off+k,1),y=d.getFullYear(),m=d.getMonth(),first=(d.getDay()+6)%7,days=new Date(y,m+1,0).getDate();
  var h='<div class="ucal__hd"><button type="button" class="ucal__nav" data-d="-1" aria-label="Poprzedni miesiąc">‹</button><b>'+M[m]+' '+y+'</b><button type="button" class="ucal__nav" data-d="1" aria-label="Następny miesiąc">›</button></div><div class="ucal__g"><span>Pn</span><span>Wt</span><span>Śr</span><span>Cz</span><span>Pt</span><span>So</span><span>Nd</span>';
  for(var i=0;i<first;i++)h+='<i></i>';
  var t=new Date();t.setHours(0,0,0,0);
  for(var dd=1;dd<=days;dd++){var iso=y+'-'+pad(m+1)+'-'+pad(dd),past=new Date(y,m,dd)<t,sel=(from&&from.value===iso)||(to&&to.value===iso),inr=from&&to&&from.value&&to.value&&iso>from.value&&iso<to.value;
   h+='<button type="button" class="ucal__d'+(sel?' is-sel':'')+(inr?' is-in':'')+'" data-iso="'+iso+'"'+(past?' disabled':'')+'>'+dd+'</button>'}
  el.innerHTML=h+'</div>'})}
 document.querySelector('.ucal').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
  if(b.dataset.d){off+=+b.dataset.d;return draw()}
  var iso=b.dataset.iso;if(!from.value||(from.value&&to.value)||iso<=from.value){from.value=iso;to.value=''}else to.value=iso;draw()});
 [from,to].forEach(function(i){i&&i.addEventListener('change',draw)});draw();
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
    for mm in re.finditer(r'<(h1|h2|h3|li|p)\b[^>]*>(.*?)</\1>', s[a:b], re.S):
        t = jednostki._txt(mm.group(2))
        if not t or mm.group(1) == 'h1': continue
        if mm.group(1) == 'li': out.append(('li', inline(re.sub(r'</?p\b[^>]*>', '', mm.group(2))).strip()))   # punkty list (dotąd pomijane)
        else: out.append(('h', esc(t)) if mm.group(1) != 'p' else ('p', inline(mm.group(2))))
    return out

def model_page(m):
    kind = kind_of_model(m); lst, lst_name = list_of(kind); us = model_units(m)
    g = GAL.get(us[0][0], [])
    hero = gpic(us[0][0], g[0][0], g[0][1], g[0][2], g[0][3], '100vw', big=True, eager=True) if g else ''
    d = model_extract(m) or []
    desc = ''.join(f'<h3 class="udesc__h">{t}</h3>' if tag == 'h' else f'<p>{t}</p>' for tag, t in d)
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
</section>""" if desc else ''}''' + cta('Wybrałeś termin?', 'Sprawdź, które jachty są wolne, albo zadzwoń do nas.')
    lead = re.sub(r'<[^>]+>', '', next((t for tag, t in d if tag == 'p'), f'{m} — czarter z Giżycka.'))
    page(murl(m), f'{m} — czarter na Mazurach, Giżycko | Jachty Mazury', lead[:155], body, lst)

# ---------------------------------------------------------------- hub „Czarter jachtów” z FAQ (treść 1:1 z /czarter-jachtow-gizycko/)
def hub_extract():
    s = open('_m/czarter-jachtow-gizycko.html', encoding='utf-8').read()
    s = re.sub(r'<script.*?</script>|<style.*?</style>|<header.*?</header>|<footer.*?</footer>|<nav.*?</nav>', '', s, flags=re.S)
    h1 = jednostki._txt(re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1))
    a = s.find('<h1'); q = s.find('Poznaj odpowiedzi'); z = s.find('Zarządzaj opcjami')
    intro = [inline(p) for p in re.findall(r'<p\b[^>]*>(.*?)</p>', s[a:q], re.S) if jednostki._txt(p)]
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
        h = re.sub(r'<a\b[^>]*>.*?</a>', lambda m: inline(m.group(0)), h, flags=re.S)
        h = re.sub(r'<(?!/?(?:p|ul|li|strong|a)\b)[^>]+>', '', h)
        h = re.sub(r'<(p|ul|li)\b[^>]*>', r'<\1>', h)
        h = re.sub(r'<li>\s*<p>(.*?)</p>', r'<li>\1', h, flags=re.S)
        h = re.sub(r'<p>\s*</p>', '', h); h = re.sub(r'<li>\s*</li>', '', h)
        return re.sub(r'\s+', ' ', H.unescape(h)).replace('<strong> </strong>', ' ').strip()
    faq = [(qq, clean(aa)) for qq, aa in faq if qq]
    rest = s[q + (ol.find('</ol>') if '</ol>' in ol else 0):z]
    sections = []
    for mm in re.finditer(r'<(h4|h3|p|li)\b[^>]*>(.*?)</\1>', s[s.find('Nasza Giżycka flota') - 60:z], re.S):
        t = jednostki._txt(mm.group(2))
        if t: sections.append((mm.group(1), esc(t) if mm.group(1) in ('h3', 'h4') else inline(mm.group(2))))
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
            seo += f'<li>{t}</li>'; continue
        if lst: seo += '</ul>'; lst = False
        seo += f'<h2 class="h3">{t}</h2>' if tag in ('h4', 'h3') else f'<p>{t}</p>'
    if lst: seo += '</ul>'
    body = (phead([('czarter-jachtow.html', 'Czarter jachtów')], 'Stanica Wodna Stranda · Giżycko', esc(h1), intro[0] if intro else '')
     + f'''<section class="psec">
  <div class="wrap">
    <div class="hts">{tile("jachty-zaglowe.html", "Jachty żaglowe", SAIL)}{tile("jachty-motorowe.html", "Jachty motorowe", MOTOR)}{tile("czarter-bez-patentu.html", "Czarter bez patentu", bez)}</div>
    <div class="hub__intro">{''.join(f"<p>{p}</p>" for p in intro[1:])}</div>
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
</section>''' + cta('Wybrałeś termin?', 'Sprawdź, które jachty są wolne, albo zadzwoń do nas.'))
    page('czarter-jachtow.html', 'Czarter jachtów Giżycko — jachty żaglowe, motorowe i houseboaty | Jachty Mazury',
         re.sub(r'<[^>]+>', '', intro[0] if intro else h1)[:155], body, 'czarter-jachtow.html', f'<script type="application/ld+json">{ld}</script>')

# ---------------------------------------------------------------- Wiedza: filmy i aktualności
def filmy_page():
    body = (phead([('poradnik.html', 'Wiedza'), ('filmy-szkoleniowe.html', 'Filmy szkoleniowe')], 'Wiedza', 'Filmy szkoleniowe',
                  'Praktyczne porady, manewry, trasy i życie na jachcie. Zobacz, zanim wyruszysz.')
     + '''<section class="psec">
  <div class="wrap">
    <div class="slot slot--wide" data-slot="filmy-youtube"><i data-lucide="play" class="lucide" aria-hidden="true"></i>
      <p><b>Filmy z kanału YouTube</b>Lista filmów pojawi się tu automatycznie po podpięciu kanału.</p></div>
  </div>
</section>''' + cta('Wybrałeś termin?', 'Sprawdź, które jachty są wolne, albo zadzwoń do nas.'))
    page('filmy-szkoleniowe.html', 'Filmy szkoleniowe | Jachty Mazury', 'Praktyczne porady, manewry, trasy i życie na jachcie — filmy szkoleniowe Jachty Mazury.', body, 'filmy-szkoleniowe.html')

def news_card(a, big=False):
    return (f'<a class="nc" href="{a["slug"]}.html"><figure class="nc__ph">{pic("art-" + a["slug"], a["h1"], "(min-width:1024px) 30vw, 100vw")}</figure>'
            f'<span class="nc__k micro">{pl_date(a.get("date", "")) or "Poradnik"}</span><span class="nc__t">{esc(a["h1"])}</span><span class="nc__l">{esc(a["lead"])}</span>'
            f'<span class="nc__go">Czytaj więcej <i data-lucide="arrow-right" class="lucide"></i></span></a>')

# Aktualności to osobna lista (_a/news.json) — wpisy z ART należą do poradnika (uwagi klientki 29.09).
# Na razie pusta: strona pokazuje komunikat, a układ listy (A1) pojawi się przy pierwszym wpisie.
NEWS = json.load(open('_a/news.json')) if os.path.exists('_a/news.json') else []
NEWS_EMPTY = ('<div class="nr__empty"><p><b>Na razie nie ma aktualności.</b> Praktyczne informacje o czarterze i trasach znajdziesz w poradniku.</p>'
              '<a class="btn" href="poradnik.html">Przejdź do poradnika <i data-lucide="arrow-right" class="lucide"></i></a></div>')
def news_row(a):
    return (f'<article class="nr"><a class="nr__ph" href="{a["slug"]}.html" tabindex="-1" aria-hidden="true">{pic("art-" + a["slug"], a["h1"], "(min-width:1024px) 34vw, 100vw")}</a>'
            f'<div class="nr__b"><p class="micro nr__d">{pl_date(a.get("date", ""))}</p><h2 class="h3 nr__t"><a href="{a["slug"]}.html">{esc(a["h1"])}</a></h2>'
            f'<p class="nr__l">{esc(a["lead"])}</p><a class="nr__go u u--on" href="{a["slug"]}.html">Czytaj dalej →</a></div></article>')

def news_page():
    rows = ''.join(news_row(a) for a in sorted(NEWS, key=lambda a: a.get('date', ''), reverse=True))
    empty = ('<div class="nr__empty"><p><b>Na razie nie ma aktualności.</b> Praktyczne informacje o czarterze i trasach znajdziesz w poradniku.</p>'
             '<a class="btn" href="poradnik.html">Przejdź do poradnika <i data-lucide="arrow-right" class="lucide"></i></a></div>')
    body = (phero([('aktualnosci.html', 'Aktualności')], 'Aktualności', '', pic('port', 'Marina Stranda w Giżycku', '100vw', True), '50% 55%')
     + f'<section class="psec"><div class="wrap"><div class="nrs">{rows or empty}</div></div></section>')
    page('aktualnosci.html', 'Aktualności | Jachty Mazury', 'Aktualności Jachty Mazury z mariny Stranda w Giżycku.', body, 'aktualnosci.html')

# ---------------------------------------------------------------- strona główna (wizualizacje -2/-3 wg wyboru klientki)
def model_card(m):
    us = model_units(m); u = us[0]; sp = UNITS[u[0]]['spec']; kind = kind_of_model(m)
    mj = berths(sp.get('Liczba osób', '–'))[0]
    return (f'<a class="rc" href="{murl(m)}"><figure class="rc__ph">{pic("u-" + u[0], m, "(min-width:1024px) 22vw, 70vw")}'
            f'<span class="rc__tag">{"Jacht żaglowy" if kind == "sail" else "Jacht motorowy"}</span></figure>'
            f'<span class="rc__b"><span class="rc__t">{esc(m)}</span><span class="rc__go" aria-hidden="true"><i data-lucide="arrow-right" class="lucide"></i></span>'
            f'<span class="rc__m num"><span><i data-lucide="users" class="lucide" aria-hidden="true"></i> {mj} os.</span>'
            f'<span><i data-lucide="door-closed" class="lucide" aria-hidden="true"></i> {sp.get("Zamykane kabiny", "–")} kab.</span>'
            + (f'<span class="rc__eng">{_engine_ico(u[0])} silnik {esc(eng)}</span>' if (eng := _engine(u[0])) else '')
            + '</span></span></a>')

def _engine_ico(slug):   # ta sama ikona silnika co na stronach modeli i jachtów
    ic = next((ic for ic, k, v in unit_facts(slug) if k == 'Silnik'), 'cog')
    return (f'<img class="ico ico--s" src="assets/img/ikony/{ic[4:]}.png" width="16" height="16" alt="" aria-hidden="true">'
            if ic.startswith('img:') else f'<i data-lucide="{ic}" class="lucide" aria-hidden="true"></i>')

def _engine(slug):   # typ silnika z tabeli jednostki, bez mocy
    for ic, k, v in unit_facts(slug):
        if k == 'Silnik': return v.split(' · ')[0]
    return ''

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
             ('heart', 'Wsparcie na każdym etapie', 'Jesteśmy dostępni – przed, w trakcie i po rejsie.')]
    body = f'''<section class="hh">
  <figure class="hh__ph">{pic("fl-a30", "Antila 30 pod żaglami na jeziorze", "100vw", True) if "fl-a30" in WS else '<picture><source type="image/webp" srcset="assets/img/r/fl-a30-600.webp 600w, assets/img/r/fl-a30-1280.webp 1280w" sizes="100vw"><img src="assets/img/r/fl-a30-1280.jpg" srcset="assets/img/r/fl-a30-600.jpg 600w, assets/img/r/fl-a30-1280.jpg 1280w" sizes="100vw" width="1280" height="960" alt="Antila 30 pod żaglami na jeziorze" fetchpriority="high" decoding="async"></picture>'}</figure>
  <div class="hh__shade" aria-hidden="true"></div>
  <div class="wrap hh__in">
    <h1 class="hh__h"><span class="sr">Czarter jachtów Mazury — </span>Mazury w&nbsp;najlepszym wydaniu</h1>
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
    <div class="sech"><h2 class="h2">Aktualności</h2><div class="sech__a"><a class="u u--on" href="aktualnosci.html">Wszystkie aktualności →</a></div></div>
    {f'<div class="nrs">{"".join(news_row(a) for a in sorted(NEWS, key=lambda a: a.get("date", ""), reverse=True)[:3])}</div>' if NEWS else NEWS_EMPTY}
  </div>
</section>
<section class="psec psec--sand ab">
  <div class="wrap g12">
    <div class="c5 ab__t">
      <h2 class="h2 ab__h">O nas</h2>
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
</section>'''
    js = '''<script>
(function(){
 var t=document.getElementById('rec-t');
 [].forEach.call(document.querySelectorAll('.rec__nav'),function(b){b.addEventListener('click',function(){var c=t.querySelector('.rc');t.scrollBy({left:+b.dataset.dir*(c?c.getBoundingClientRect().width+20:300),behavior:'smooth'})})});
})();
</script>'''
    page('index.html', 'Czarter jachtów Giżycko — jachty żaglowe i motorowe na Mazurach | Jachty Mazury',
         'Czarter jachtów żaglowych i motorowych z Giżycka. Stanica Wodna Stranda, flota Antila, Maxus, Nautic, Nexus. Cennik 2027, biuro codziennie 8:00–20:00.',
         body, 'index.html', js)

for u in SAIL + MOTOR: unit_page(u)
for m in models(SAIL + MOTOR):
    if has_model_page(m): model_page(m)
hub_page(); filmy_page(); home_page()

# ---------------------------------------------------------------- /houseboat-mazury/ (treść 1:1 z obecnej strony)
def houseboat_page():
    s = open('_seo/html/houseboat-mazury.html', encoding='utf-8').read()
    s = re.sub(r'<script.*?</script>|<style.*?</style>|<header.*?</header>|<footer.*?</footer>|<nav.*?</nav>', '', s, flags=re.S)
    a = s.find('<h1'); z = s.find('Zarządzaj opcjami')
    blocks = [(m.group(1), m.group(2)) for m in re.finditer(r'<(h1|h2|p|li)\b[^>]*>(.*?)</\1>', s[a:z], re.S) if jednostki._txt(m.group(2))]
    h1 = jednostki._txt(blocks[0][1])
    intro, sections, faq = [], [], []; cur = None
    for tag, raw in blocks[1:]:
        if tag == 'h2': cur = jednostki._txt(raw); sections.append([cur, []]); continue
        if cur is None: intro.append(inline(raw)); continue
        if tag == 'li' and 'pytania' in cur:
            txt = inline(raw); q, _, ans = jednostki._txt(raw).partition('? ')
            faq.append((q + '?', inline(raw)[len(q) + 1:].lstrip(' ?') if ans else txt)); continue
        sections[-1][1].append(inline(raw))
    bez = [u for u in MOTOR if u[0] != 'stillo-31-star']
    parts = ''
    for title, ps in sections:
        if 'pytania' in title: continue
        parts += f'<h2 class="h3">{esc(title)}</h2>' + ''.join(f'<p>{p}</p>' for p in ps)
    items = ''.join(f'<details class="faq__i"><summary>{esc(qq)}</summary><div class="faq__a"><p>{aa}</p></div></details>' for qq, aa in faq)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': qq, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'<[^>]+>', '', aa)}} for qq, aa in faq]}, ensure_ascii=False)
    half = (len(faq) + 1) // 2
    col = lambda part: ''.join(f'<details class="faq__i"><summary>{esc(qq)}</summary><div class="faq__a"><p>{aa}</p></div></details>' for qq, aa in part)
    ms = [m for m in models(MOTOR) if m != 'Stillo 31']
    img = gpic('futura-860-eufemia', *GAL['futura-860-eufemia'][0], '100vw', big=True, eager=True)
    # nowy styl (HB1): strona ukryta w menu, ale z tą samą treścią i adresem (SEO)
    body = (phero([('houseboat-mazury.html', 'Houseboaty')], esc(h1), '', img, '50% 55%')
     + f'''<section class="psec lst">
  <div class="wrap">
    <div class="lst__intro">{"".join(f"<p>{p}</p>" for p in intro)}</div>
    <h2 class="h2 sec__t bez__h">Dostępne houseboaty</h2>
    <div class="mcs">{''.join(model_card(m) for m in ms)}</div>
  </div>
</section>
<section class="psec psec--sand">
  <div class="wrap"><div class="art__body hb__body">{parts}</div></div>
</section>
{f"""<section class="psec"><div class="wrap faq faq--wide"><h2 class="h2 sec__t">Najczęściej zadawane pytania</h2><div class="faq__cols"><div class="faq__l">{col(faq[:half])}</div><div class="faq__l">{col(faq[half:])}</div></div></div></section>""" if faq else ''}'''
     + cta('Wybrałeś termin?', 'Sprawdź, które jachty są wolne, albo zadzwoń do nas.'))
    page('houseboat-mazury.html', 'Houseboat Mazury', re.sub(r'<[^>]+>', '', intro[0])[:155] if intro else h1, body, 'houseboat-mazury.html',
         f'<script type="application/ld+json">{ld}</script>' if faq else '')

# ================================================================ WIZUALIZACJE 2 (25.09.2026): hub, listy, modele, Wiedza, cennik

def rpic(key, alt, sizes, eager=False):
    """Zdjęcie z assets/img/r spoza spisu ws.json (warianty szuka na dysku)."""
    import glob as _g
    ws = sorted({int(re.search(r'-(\d+)\.jpg$', f).group(1)) for f in _g.glob(f'assets/img/r/{key}-*.jpg') if re.search(r'-(\d+)\.jpg$', f)})
    src = lambda e: ', '.join(f'assets/img/r/{key}-{w}.{e} {w}w' for w in ws if os.path.exists(f'assets/img/r/{key}-{w}.{e}'))
    from PIL import Image as _I
    W, H = _I.open(f'assets/img/r/{key}-{ws[-1]}.jpg').size
    mid = min(ws, key=lambda w: abs(w - 1280))
    return (f'<picture><source type="image/avif" srcset="{src("avif")}" sizes="{sizes}"><source type="image/webp" srcset="{src("webp")}" sizes="{sizes}">'
            f'<img src="assets/img/r/{key}-{mid}.jpg" srcset="{src("jpg")}" sizes="{sizes}" width="{W}" height="{H}" alt="{esc(alt)}"'
            f'{" fetchpriority=\"high\"" if eager else ""} decoding="async"></picture>')

def phero(cr, h1, lead, img, pos='50% 50%'):
    return f'''<section class="ph">
  <figure class="ph__ph" style="--pos:{pos}">{img}</figure>
  <div class="ph__shade" aria-hidden="true"></div>
  <div class="wrap ph__in">
    {crumbs(cr)}
    <h1 class="ph__h">{h1}</h1>
    {f'<p class="ph__lead">{lead}</p>' if lead else ''}
  </div>
</section>'''

def swap_head(fname, hero):
    s = open(fname, encoding='utf-8').read()
    s = re.sub(r'<section class="phead[^"]*">.*?</section>', lambda m: hero, s, count=1, flags=re.S)
    open(fname, 'w', encoding='utf-8').write(s)

def live_blocks(name):
    s = open(f'_seo/html/{name}.html', encoding='utf-8').read()
    s = re.sub(r'<script.*?</script>|<style.*?</style>|<header.*?</header>|<footer.*?</footer>|<nav.*?</nav>', '', s, flags=re.S)
    a = s.find('<h1'); z = s.find('Zarządzaj opcjami')
    return [(m.group(1), m.group(2)) for m in re.finditer(r'<(h1|h2|h3|h4|p|li)\b[^>]*>(.*?)</\1>', s[a:z], re.S) if jednostki._txt(m.group(2))]

def seo_html(blocks):
    o, lst = '', False
    for tag, raw in blocks:
        if tag == 'li':
            if not lst: o += '<ul>'; lst = True
            o += f'<li>{inline(raw)}</li>'; continue
        if lst: o += '</ul>'; lst = False
        o += f'<h2 class="h3">{esc(jednostki._txt(raw))}</h2>' if tag in ('h2', 'h3', 'h4') else f'<p>{inline(raw)}</p>'
    return o + ('</ul>' if lst else '')

def fact(slug, key):
    for ic, k, v in unit_facts(slug):
        if k == key: return ic, v
    return None, None

def model_card(m):
    us = model_units(m); u = us[0]; sp = UNITS[u[0]]['spec']
    rows = []
    ic, v = fact(u[0], 'Silnik')
    if v: rows.append((ic, 'Silnik', v.split(' · ')[0]))
    if kind_of_model(m) == 'motor':
        ic, v = fact(u[0], 'Ster strumieniowy')
        if v: rows.append((ic, 'Ster strumieniowy', v))
    else:
        ic, v = fact(u[0], 'Ster')
        if v: rows.append(('ship-wheel', 'Ster', v))
    mj = berths(sp.get('Liczba osób', '–'))[0]
    if mj and mj != '–': rows.append(('users', 'Miejsca', f'{mj} os.'))
    kab = next((v for w in us for ic_, k, v in unit_facts(w[0]) if k == 'Kabiny'), '')
    if kab: rows.append(('door-closed', 'Kabiny', kab))
    specs = ''.join(f'<li>{ico(i, 22)}<span><small>{k}</small>{esc(v)}</span></li>' for i, k, v in rows)
    n = len(us)
    return (f'<article class="mc"><a class="mc__ph" href="{murl(m)}" tabindex="-1" aria-hidden="true">{pic("u-" + u[0], m, "(min-width:1024px) 24vw, (min-width:641px) 45vw, 100vw")}</a>'
            f'<div class="mc__b"><h2 class="mc__t"><a href="{murl(m)}">{esc(m)}</a></h2><p class="mc__n">{n} {"jednostka" if n == 1 else ("jednostki" if n < 5 else "jednostek")}</p>'
            f'<ul class="mc__s">{specs}</ul>'
            f'<a class="btn mc__btn" href="{murl(m)}">{"Zobacz jacht" if n == 1 else "Zobacz jachty"} <i data-lucide="arrow-right" class="lucide"></i></a></div></article>')

def list_page(kind):
    fname, name = ('jachty-zaglowe.html', 'czarter-jachtow-zaglowych') if kind == 'sail' else ('jachty-motorowe.html', 'czarter-jachtow-motorowych')
    units = SAIL if kind == 'sail' else MOTOR
    b = live_blocks(name); h1 = jednostki._txt(b[0][1])
    intro = [raw for tag, raw in b[1:] if tag == 'p'][:1]
    unit_titles = {jednostki._txt(raw) for tag, raw in b if tag in ('h2', 'h3', 'h4') and (re.match(r'(Antila|Maxus|Solina|Nautic|Nexus|Stillo|Futura|Nautiner|Calipso)', jednostki._txt(raw)))}
    start = next(i for i, (tag, raw) in enumerate(b) if i > 0 and tag in ('h2', 'h4') and jednostki._txt(raw) not in unit_titles)
    seo = [x for x in b[start:] if not (x[0] == 'p' and jednostki._txt(x[1]).startswith('Poniżej znajduje się oferta'))]
    lead_txt = SEO.get(f'{LIVE}/{name}/', {}).get('description') or ''
    img = rpic('life1', 'Antila 27 „Hiuma” w marinie', '100vw', True) if kind == 'sail' else gpic('stillo-31-star', *GAL['stillo-31-star'][0], '100vw', big=True, eager=True)
    body = (phero([('czarter-jachtow.html', 'Czarter jachtów'), (fname, 'Jachty żaglowe' if kind == 'sail' else 'Jachty motorowe')], esc(h1), '', img, '50% 60%' if kind == 'sail' else '50% 55%')
      + f'''<section class="psec lst">
  <div class="wrap">
    {f'<div class="lst__intro">{"".join(f"<p>{inline(p)}</p>" for p in intro)}</div>' if intro else ''}
    <div class="mcs">{''.join(model_card(m) for m in models(units))}</div>
  </div>
</section>''' + cta('Wybrałeś termin?', 'Sprawdź, które jachty są wolne, albo zadzwoń do nas.'))
    page(fname, h1, lead_txt, body, fname)

# ---- strona modelu wg wizualizacji „strona modelu – 2”: najpierw jednostki (do wysyłania ofert), potem opis i dane
def unit_mini(u):
    sp = UNITS[u[0]]['spec']; g = GAL.get(u[0], [])
    ph = gpic(u[0], *g[0], '(min-width:1024px) 20vw, 50vw') if g else pic('u-' + u[0], uname(u), '50vw')
    p = od(u[3])
    return (f'<article class="um"><a class="um__ph" href="{u[0]}.html" tabindex="-1" aria-hidden="true">{ph}</a>'
            f'<div class="um__b"><h3 class="um__t"><a href="{u[0]}.html">{esc(u[2] or u[1])}</a></h3>'
            f'<p class="um__m num">{esc(sp.get("Rok produkcji", ""))}{" · od " + zl(p) + " / doba" if p else ""}</p>'
            f'<a class="btn btn--sm um__btn" href="{u[0]}.html">Zobacz szczegóły <i data-lucide="arrow-right" class="lucide"></i></a></div></article>')

# ikony do punktów „Czy … to dobry wybór?” — dobór po słowach z treści punktu (treść bez zmian, ze strony modelu)
WHY_IC = [('rodzin', 'users'), ('toalet', 'bath'), ('kabin', 'door-closed'), ('osób', 'users'), ('osoby', 'users'), ('łazienk', 'shower-head'), ('prysznic', 'shower-head'),
          ('dynamiczn', 'gauge'), ('stabiln', 'anchor'), ('bezpiecz', 'shield-check'), ('nautyczn', 'wind'), ('przestron', 'maximize-2'),
          ('przestrzen', 'maximize-2'), ('długości', 'maximize-2'), ('nowoczes', 'sparkles'), ('komfort', 'sofa'), ('standard', 'sofa')]
def why_icon(t):
    t = t.lower()
    return next((ic for k, ic in WHY_IC if k in t), 'check')

def model_page(m):
    kind = kind_of_model(m); lst, lst_name = list_of(kind); us = model_units(m)
    g = GAL.get(us[0][0], [])
    hero = gpic(us[0][0], *g[0], '100vw', big=True, eager=True) if g else ''
    d = model_extract(m) or []
    ps = [t for tag, t in d if tag == 'p']
    first_h = next((i for i, (tag, t) in enumerate(d) if tag == 'h'), len(d))
    about = ''.join(f'<p>{t}</p>' for tag, t in d[:first_h] if tag == 'p')
    cols, cur = [], None
    for tag, t in d[first_h:]:
        if tag == 'h': cur = [t, []]; cols.append(cur)
        elif cur: cur[1].append((tag, t))
    # MOD6: „Dlaczego warto wybrać …” z punktów sekcji „Czy … to dobry wybór?”
    why = next((c for c in cols if 'dobry wybór' in jednostki._txt(c[0]).lower()), None)
    pts, rest = [], []
    if why:
        for tg, p_ in why[1]:
            if tg == 'li':
                pts.append(p_.strip(' ,.;'))
            elif '•' in p_:
                pts += [x.strip(' ,.') for x in re.split(r'•', re.sub(r'<br[^>]*>', '', p_)) if jednostki._txt(x).strip(' ,.')]
            elif not re.match(r'jeśli (szukasz|zależy)', jednostki._txt(p_).lower()):
                rest.append(p_)
    if not pts and m == 'Antila 27':   # zgoda klientki 30.09: punkty z innego modelu, klientka je potem zredaguje
        src_ = model_extract('Antila 30') or []
        take = False
        for tg, t in src_:
            if tg == 'h': take = 'dobry wybór' in jednostki._txt(t).lower(); continue
            if take and '•' in t: pts += [x.strip(' ,.') for x in re.split(r'•', re.sub(r'<br[^>]*>', '', t)) if jednostki._txt(x).strip(' ,.')]
    more = [c for c in cols if c is not why]
    MODEL_FIELDS = [('move-vertical', 'Długość'), ('move-horizontal', 'Szerokość'), ('waves', 'Zanurzenie'), ('bed-double', 'Miejsca do spania'),
                    ('door-closed', 'Kabiny'), ('bath', 'Toaleta'), ('shower-head', 'Prysznic'), ('ship-wheel', 'Ster'),
                    ('img:silnik-stacjonarny', 'Silnik'), ('img:ster-strumieniowy', 'Ster strumieniowy')]
    got = {}
    for u in us:   # pierwsza jednostka modelu, która podaje daną wartość
        for ic, k, v in unit_facts(u[0]):
            got.setdefault(k, (ic, v))
    facts = [(got[k][0], k, got[k][1]) if k in got else (ic, k, '–') for ic, k in MODEL_FIELDS]
    fh = ''.join(f'<li>{ico(ic)}<span class="uic__k">{k}</span><b>{v}</b></li>' for ic, k, v in facts)
    def body_html(items):   # akapity i listy w kolejności z obecnej strony
        o, lst = '', False
        for tg, t in items:
            if tg == 'li' and not lst: o += '<ul>'; lst = True
            if tg != 'li' and lst: o += '</ul>'; lst = False
            o += f'<li>{t}</li>' if tg == 'li' else f'<p>{t}</p>'
        return o + ('</ul>' if lst else '')
    more_html = ''.join(f'<h3 class="h3">{h}</h3>{body_html(pp)}' for h, pp in more)
    body = f'''<section class="uh uh--model">
  <figure class="uh__ph">{hero}</figure>
  <div class="uh__shade" aria-hidden="true"></div>
  <div class="wrap uh__in">
    <h1 class="uh__h"><span class="uh__m">{esc(m)}</span></h1>
  </div>
</section>
<section class="psec mfl">
  <div class="wrap">
    <h2 class="h2 sec__t">Dostępne jachty {esc(m)} w naszej flocie</h2>
    <div class="ums">{''.join(unit_mini(u) for u in us)}</div>
  </div>
</section>
<section class="psec mab">
  <div class="wrap mab__g">
    <div class="mab__t"><h2 class="h2 sec__t">O modelu {esc(m)}</h2>{about}
      {f'<div class="more" id="mab-more">{more_html}</div><button class="more__btn" type="button" aria-expanded="false" aria-controls="mab-more" hidden><span>Przeczytaj całość</span> <i data-lucide="chevron-down" class="lucide"></i></button>' if more else ''}</div>
    <div class="mab__f"><h2 class="h3 sec__t">Najważniejsze informacje</h2><ul class="uic__l mab__icons num">{fh}</ul></div>
  </div>
</section>
{f"""<section class="psec psec--sand mwhy2">
  <div class="wrap"><h2 class="h2 sec__t">Dlaczego warto wybrać model {esc(m)}?</h2>
    <ul class="mwhy2__l">{''.join(f'<li><span class="why__i"><i data-lucide="{why_icon(t)}" class="lucide" aria-hidden="true"></i></span><b>{t[0].upper() + t[1:]}</b></li>' for t in pts)}</ul>
    {''.join(f'<p class="mwhy2__p">{p}</p>' for p in rest)}</div>
</section>""" if pts else ''}''' + cta('Wybrałeś termin?', 'Sprawdź, które jachty są wolne, albo zadzwoń do nas.')
    lead = re.sub(r'<[^>]+>', '', ps[0] if ps else f'{m} — czarter z Giżycka.')
    page(murl(m), f'{m} — czarter na Mazurach, Giżycko | Jachty Mazury', lead[:155], body, lst)

# ---- „Czarter jachtów” wg wizualizacji
def hub_page():
    h1, intro, faq, secs = hub_extract()
    raw = open('_seo/html/czarter-jachtow-gizycko.html', encoding='utf-8').read()
    ben = re.search(r'Najważniejsze korzyści:.*?<ul[^>]*>(.*?)</ul>', raw, re.S)
    bens = [jednostki._txt(x).rstrip(',.') for x in re.findall(r'<li[^>]*>(.*?)</li>', ben.group(1), re.S)] if ben else []
    icons = ['sailboat', 'layers', 'wrench', 'receipt-text', 'map', 'life-buoy']
    def tile(href, title, desc, img):
        return (f'<a class="bt" href="{href}"><figure class="bt__ph">{img}</figure><span class="bt__b"><span class="bt__t">{title}</span>'
                f'<span class="bt__go" aria-hidden="true"><i data-lucide="arrow-right" class="lucide"></i></span></span></a>')
    dz = SEO.get(f'{LIVE}/czarter-jachtow-zaglowych/', {}).get('description', ''); dm = SEO.get(f'{LIVE}/czarter-jachtow-motorowych/', {}).get('description', '')
    half = (len(faq) + 1) // 2
    col = lambda part: ''.join(f'<details class="faq__i"><summary>{esc(qq)}</summary><div class="faq__a">{aa}</div></details>' for qq, aa in part)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': qq, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'<[^>]+>', ' ', aa).strip()}} for qq, aa in faq]}, ensure_ascii=False)
    seo = ''; lst = False
    for tag, t in secs:
        if 'korzyści' in t.lower() or t in bens or t.rstrip(',.') in bens: continue
        if tag == 'li':
            if not lst: seo += '<ul>'; lst = True
            seo += f'<li>{t}</li>'; continue
        if lst: seo += '</ul>'; lst = False
        seo += f'<h2 class="h3">{t}</h2>' if tag in ('h4', 'h3') else f'<p>{t}</p>'
    if lst: seo += '</ul>'
    body = (phero([('czarter-jachtow.html', 'Czarter jachtów')], esc(h1), '', pic('art-jaki-jacht-wybrac-dla-pary-rodziny-lub-grupy', 'Jachty w marinie Stranda', '100vw', True), '50% 60%')
     + f'''<section class="psec">
  <div class="wrap">
    <div class="hub__intro">{''.join(f"<p>{p}</p>" for p in intro)}</div>
    <div class="bts">{tile("jachty-zaglowe.html", "Jachty żaglowe", dz, rpic("fl-a30", "Antila 30 pod żaglami", "(min-width:1024px) 45vw, 100vw"))}{tile("jachty-motorowe.html", "Jachty motorowe", dm, gpic("stillo-31-star", *GAL["stillo-31-star"][1], "(min-width:1024px) 45vw, 100vw", big=True))}</div>
  </div>
</section>
{f"""<section class="psec psec--sand why">
  <div class="wrap"><h2 class="h2 sec__t">Co zyskujesz, wybierając naszą ofertę</h2>
    <ul class="why__l">{''.join(f'<li><span class="why__i"><i data-lucide="{icons[i % len(icons)]}" class="lucide" aria-hidden="true"></i></span><span>{esc((b[0].upper() + b[1:]).replace(', w tym flotę jachtów żaglowych', ''))}</span></li>' for i, b in enumerate(bens))}</ul></div>
</section>""" if bens else ''}
<section class="psec">
  <div class="wrap faq faq--wide">
    <h2 class="h2 sec__t">Najczęściej zadawane pytania</h2>
    <div class="faq__cols"><div class="faq__l">{col(faq[:half])}</div><div class="faq__l">{col(faq[half:])}</div></div>
  </div>
</section>
''' + cta('Wybrałeś termin?', 'Sprawdź, które jachty są wolne, albo zadzwoń do nas.'))
    page('czarter-jachtow.html', 'Czarter jachtów Giżycko', re.sub(r'<[^>]+>', '', intro[0] if intro else h1)[:155], body, 'czarter-jachtow.html',
         f'<script type="application/ld+json">{ld}</script>')

# ---- Wiedza (nowa strona zbiorcza działu)
def wiedza_page():
    def card(href, icon, title, desc, btn, img):
        return (f'<a class="wk" href="{href}"><figure class="wk__ph">{img}</figure><span class="wk__i" aria-hidden="true"><i data-lucide="{icon}" class="lucide"></i></span>'
                f'<span class="wk__t">{title}</span><span class="wk__d">{desc}</span><span class="btn wk__btn">{btn} <i data-lucide="arrow-right" class="lucide"></i></span></a>')
    arts = sorted(ART, key=lambda a: a.get('date', ''), reverse=True)
    body = (phero([('wiedza.html', 'Wiedza')], 'Wiedza', 'Poradnik czarterowy, filmy szkoleniowe i aktualności.',
                  pic('art-tygodniowy-rejs-po-mazurach', 'Marina o zachodzie słońca', '100vw', True), '50% 55%')
     + f'''<section class="psec">
  <div class="wrap">
    <div class="wks">
      {card("poradnik.html", "book-open", "Poradnik czarterowy", "Wybór jachtu, formalności, bezpieczeństwo, trasy i najlepszy termin na rejs.", "Przejdź do poradnika", pic("art-" + ART[0]["slug"], "", "(min-width:1024px) 30vw, 100vw"))}
      {card("filmy-szkoleniowe.html", "play", "Filmy szkoleniowe", "Praktyczne porady, manewry, trasy i życie na jachcie.", "Oglądaj filmy", gpic("antila-30-1-e-cleopatra", *GAL["antila-30-1-e-cleopatra"][4], "(min-width:1024px) 30vw, 100vw"))}
      {card("aktualnosci.html", "megaphone", "Aktualności", "Najnowsze wpisy i informacje z mariny w Giżycku.", "Zobacz aktualności", pic("port", "", "(min-width:1024px) 30vw, 100vw"))}
    </div>
  </div>
</section>
<section class="psec psec--sand">
  <div class="wrap">
    <div class="sech"><h2 class="h2">Najnowsze z poradnika</h2><div class="sech__a"><a class="u u--on" href="poradnik.html">Zobacz wszystkie artykuły →</a></div></div>
    <div class="ncs">{''.join(news_card(a) for a in arts[:3])}</div>
  </div>
</section>
<section class="psec">
  <div class="wrap">
    <div class="sech"><h2 class="h2">Najnowsze filmy</h2><div class="sech__a"><a class="u u--on" href="filmy-szkoleniowe.html">Zobacz wszystkie filmy →</a></div></div>
    <div class="slot slot--wide" data-slot="filmy-youtube"><i data-lucide="play" class="lucide" aria-hidden="true"></i><p><b>Filmy z kanału YouTube</b>Trzy najnowsze filmy pojawią się tu automatycznie po podpięciu kanału.</p></div>
  </div>
</section>''' + f'''<section class="psec psec--sand">
  <div class="wrap">
    <div class="sech"><h2 class="h2">Najnowsze aktualności</h2><div class="sech__a"><a class="u u--on" href="aktualnosci.html">Wszystkie aktualności →</a></div></div>
    {f'<div class="nrs">{"".join(news_row(a) for a in sorted(NEWS, key=lambda a: a.get("date", ""), reverse=True)[:3])}</div>' if NEWS else NEWS_EMPTY}
  </div>
</section>''')
    page('wiedza.html', 'Wiedza — poradnik czarterowy, filmy i aktualności | Jachty Mazury',
         'Poradnik czarterowy, filmy szkoleniowe i aktualności Jachty Mazury — wszystko, co warto wiedzieć przed rejsem po Mazurach.', body, 'wiedza.html')

list_page('sail'); list_page('motor')
for m in models(SAIL + MOTOR):
    if has_model_page(m): model_page(m)
# ---- czarter bez patentu w stylu list jachtów (uwagi klientki 29.09, BP1): hero ze zdjęciem, wstęp,
#      trzy warunki jako ikony, karty modeli. Treść 1:1 z obecnej strony (_seo/html/czarter-bez-patentu.html).
def bez_page():
    b = live_blocks('czarter-bez-patentu')
    ps = [raw for tag, raw in b[1:] if tag == 'p']
    rules = [('gauge', 'Moc silnika', 'do 75 kW'), ('ruler', 'Długość kadłuba', 'do 13 m'), ('timer', 'Prędkość', 'do 15 km/h, ograniczona konstrukcyjnie')]
    ms = [m for m in models(MOTOR) if m != 'Stillo 31']   # jak dotąd: motorowe poza Stillo 31
    img = gpic('nexus-870-revo-wiktor', *GAL['nexus-870-revo-wiktor'][0], '100vw', big=True, eager=True)
    body = (phero([('czarter-bez-patentu.html', 'Czarter bez patentu')], 'Czarter bez patentu', '', img, '50% 55%')
      + f'''<section class="psec lst">
  <div class="wrap">
    <div class="lst__intro">{"".join(f"<p>{inline(p)}</p>" for p in ps[:2]).replace('houseboaty</strong>', 'houseboaty</strong> (<a class="u u--on" href="houseboat-mazury.html">zobacz houseboaty</a>)', 1)}</div>
    <ul class="why__l why__l--3">{"".join(f'<li><span class="why__i"><i data-lucide="{i}" class="lucide" aria-hidden="true"></i></span><span><b>{k}</b> {v}</span></li>' for i, k, v in rules)}</ul>
    <h2 class="h2 sec__t bez__h">Jachty, które poprowadzisz bez patentu</h2>
    <div class="mcs">{''.join(model_card(m) for m in ms)}</div>
    {f'<div class="lst__intro bez__po"><p>{inline(ps[2])}</p></div>' if len(ps) > 2 else ''}
  </div>
</section>''' + cta('Wybrałeś termin?', 'Sprawdź, które jachty są wolne, albo zadzwoń do nas.'))
    page('czarter-bez-patentu.html', 'Czarter bez patentu na Mazurach — houseboaty i motorówki | Jachty Mazury',
         'Jachty motorowe i houseboaty, które można prowadzić bez patentu: silnik do 75 kW, kadłub do 13 m, prędkość do 15 km/h.', body, 'czarter-bez-patentu.html')

hub_page(); wiedza_page(); bez_page(); houseboat_page(); news_page()
swap_head('cennik.html', phero([('cennik.html', 'Cennik')], 'Cennik czarteru jachtów 2027',
    'Cena za dobę obowiązuje przy czarterze minimum tygodniowym. Przy krótszych terminach cena ustalana jest indywidualnie.',
    pic('port', 'Stanica Wodna Stranda z lotu ptaka', '100vw', True), '50% 60%'))

