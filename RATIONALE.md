# Jachty Mazury — design system i uzasadnienie

Pliki:
- `assets/css/system.css` — tokeny, skala, siatka, komponenty, stany (komentarz na górze = tabela kontrastów)
- `index.html` — strona główna (desktop + mobile w jednym pliku responsywnym)
- `jacht.html` — karta jachtu
- `stany.html` — wszystkie stany komponentów wymuszone klasami, do przeglądu bez interakcji
- `assets/img/` — wyłącznie realne zdjęcia i logo z obecnej strony

Koncept: **stół nawigacyjny i rejestr jednostek.** Linie włoskowate, znaczniki, współrzędne, dane tabelaryczne, namiary sekcji (01 / FLOTA). Zdjęcie niesie emocję, struktura niesie rzemiosło. Wszystko, co dałoby się przenieść na stronę spa, wycięte.

---

## Tokeny

**Kolor** — tylko sześć barw klienta plus jeden tint (`--ink-80`, 80% ink na paper) jako jedyna „szarość".

| token | hex | na paper | na sand | dozwolone użycie |
|---|---|---|---|---|
| `--ink` | #304044 | 10,3:1 | 8,8:1 | tekst, CTA primary, stopka, pas |
| `--deep` | #137396 | 5,1:1 | 4,3:1 | linki, focus, stany aktywne, akcent w nazwach |
| `--wave` | #3E9AB3 | 3,1:1 | 2,6:1 | **tylko** display ≥32 px, hover obramowań, linia ładowania |
| `--sage` | #71846F | 3,8:1 | 3,3:1 | **tylko** linie, znaczniki, siatka, cudzysłowy |
| `--sand` | #F1E6D6 | — | — | sekcje naprzemienne, szkielety, wypełnienia |
| `--paper` | #FCF9F4 | — | — | tło |
| `--ink-80` | #576161 | 6,1:1 | 5,2:1 | tekst drugorzędny |

Konsekwencja z tabeli: `--deep` na `--sand` to 4,3:1, poniżej AA dla tekstu <24 px. Dlatego na piaskowych sekcjach (opinie, podobne jachty) linki są w `--ink` z podkreśleniem w `--deep`. `--wave` i `--sage` nigdy nie są kolorem tekstu poniżej 32 px. Na ink: paper 10,3:1, sand 8,8:1, wave 3,3:1 (liczba „16" w pasie ma 96–224 px).

Podział powierzchni na stronie głównej: ~70% paper, ~20% sand (opinie, podobne), ~8% ink (pas + stopka), ~2% deep+wave (kursywa w nazwach, liczba w pasie, podkreślenia, focus).

**Typografia.** Dwa kroje: **Newsreader** (display; zastąpił Instrument Serif — patrz niżej) i **IBM Plex Sans** (grotesk techniczny, cyfry tabelaryczne włączone globalnie przez `font-variant-numeric: tabular-nums`). Skala 1,25 od 16 px, zdefiniowana w `--t-1…--t7` — żaden rozmiar nie jest dobrany na oko. Nagłówki z trackingiem −0,025/−0,03 em, łamane ręcznie (`<br>`). Body 16 px / 1,6, miara 68 ch. Każda liczba w jednym formacie: spacja tysięczna, przecinek dziesiętny, „zł" po liczbie, „/ doba" jako sufiks w `--ink-80`.

**Rytm.** Wszystkie odstępy z `--s1…--s9` = 8·16·24·32·48·64·96·128·160. Sekcje 128 px (mobile 96), sekcje ciasne 96 px, namiar → nagłówek 64 px, wiersz floty 32 px, bloki karty jachtu 96 px.

**Siatka.** 12 kolumn, gap 24, kontener 1280. Treść siedzi na podziałach 7/5 (rejestr, port), 8/4 (galeria, karta jachtu), 5/7 (pas ink). Nigdy 6/6. Zdjęcia wylewają się za jeden margines strony (`.bleed-l` / `.bleed-r`) naprzemiennie: rejestr lewo/prawo/lewo/prawo/lewo, port lewo, wiedza prawo.

**Elewacja.** Żadnych cieni poza modalem. Hover nie skaluje i nie rzuca cienia; uniesienie to `translateY(-8px)` bloku danych.

**Wylew zdjęć** jest stały: `--bleed: min(--edge, 64px)`. Na 1920 zdjęcie nie rośnie do krawędzi ekranu, bo wtedy kolumna danych obok zostawała z 300 px pustki.

**Reguła pustki.** Siatka jest tłem, nie treścią: żadne pole bez treści nie może być wyższe niż jeden krok skali (96 px). Stąd 8 pól danych w wierszu rejestru (kolumna domyka się do dołu zdjęcia przez `space-between`), 6 filmów w Wiedzy (lewa kolumna kończy się z prawą), flota z dolnym paddingiem 64 px przed pasem ink.

**Przyciski — trzy warianty, bez wyjątków poza fotografią.**
- primary `.btn` — ink solid, tekst paper; **jedno użycie na ekran** (hero / aside jachtu / pasek mobilny).
- secondary `.btn--outline` — obrys ink 1 px, tekst ink (nagłówek, „Pokaż na mapie", „Broszura PDF").
- ghost `.u` — sam tekst z podkreśleniem wjeżdżającym od lewej („Karta jachtu →", linki w listach).
Na fotografii (`.on-photo`: hero i nagłówek nad hero) primary i secondary odwracają barwy ink↔paper. To jedyny wyjątek i obowiązuje oba warianty tak samo.

**Konwersja z listy.** Każda pozycja floty (strona główna) i karuzeli „Inne jachty" ma własny „Rezerwuj" (primary, 48 px na mobile, pełna szerokość) + link „Karta →". Przycisk otwiera modal z nazwą jachtu w nagłówku (`data-yacht`). To świadome odstępstwo od „jeden primary na ekran" — na liście każdy wiersz jest osobną decyzją. Na mobile wiersz floty: zdjęcie 132 px + nazwa/parametry, pod spodem cena i pełnoszeroki przycisk.

**Mobile sprawdzane na realnych 390 px** (headless Chrome ma minimum 500 px; strona renderowana w `iframe` 390 px, media queries liczą się względem ramki). Na 390: eyebrow i CTA hero skrócone (`.hide-m`), etykiety legendy jednowyrazowe, nagłówki bloków i karuzeli składane w pion, okruszki bez „Start", nazwa jachtu w nagłówku kalendarza ukryta.

**Kursywa = nazwa własna jachtu.** Nic innego nie jest kursywą (hero i pas ink bez akcentu kursywą).

**Format danych.** Cena zawsze `950&nbsp;zł` + `/ doba` w klasie `.per` (rejestr, karuzela, aside, pasek mobilny). Parametry zawsze w kolejności etykieta → wartość: „Kabiny 3 · Koje 8 + 2". Legenda pod hero to same dane jednego rzędu: port, liczba jednostek, sezon, godziny biura.

**Logo.** Na ciemnym tle `logo-mono.png` (biały żagiel i tekst na przezroczystym, przygotowane z oryginału), na jasnym `logo.png`. Nagłówek przełącza je razem z tłem. Znak ma **42 px wysokości od 1024 px, 34 px niżej** (było 32 — za mało jak na jedyny nośnik marki w nagłówku), stopka 38 px; wysokość nagłówka `--head-h: 92px` na wszystkich szablonach.

**Hero** ma 96svh (min. 680 px, na mobile 620) — pełny kadr ma się bronić jako obraz, a wyszukiwarka nadal mieści się nad zgięciem.

**Zdjęcia w rejestrze — wytyczna do panelu.** Kadr pierwszy: burta albo jacht pod żaglami. Kadr drugi (hover): wnętrze albo kokpit. Wszystkie kadry 3:2; panel przycina do 3:2 przy uploadzie. Hover działa tylko na urządzeniach z kursorem (`@media (hover:hover)`), żeby na telefonie tap nie zamieniał zdjęcia.

**Media.** `assets/img/r/` zawiera warianty 640/960/1280/1600/2560 w AVIF, WebP i JPG; `<picture>` z `srcset` + `sizes` pod realne szerokości kontenerów (hero 100vw, rejestr/galeria ~60vw). Hero `fetchpriority="high"`, reszta `loading="lazy"`. W WordPressie: te same szerokości w `add_image_size`, AVIF przez `image_editor_output_format`.

---

## Decyzje układu

1. **Hero = jedno działanie.** Pełny kadr Antili 27 (realne zdjęcie), współrzędne mariny jako mikro‑typ na prawej krawędzi, nagłówek i **wyszukiwarka terminu** (dwa pola dat + jeden przycisk). Bez liczby osób, bez typu jachtu, bez filtrów — każda dodatkowa decyzja oddala od rezerwacji. Pasek wyszukiwarki jest papierowy na fotografii, więc czyta się jak przyrząd położony na zdjęciu; przycisk w nim jest w wersji odwróconej (`.on-photo`), wszędzie indziej primary = ink.
2. **Legenda pod hero zamiast paska ikon.** Cztery dane (port, liczba jednostek, sezon, godziny biura) jako typografia z liniami — zero ikon w rzędzie.
3c. **Pozycja floty mierzy jacht, nie tylko go opisuje.** Warstwa, która jest jednocześnie charakterem i informacją — w duchu stołu nawigacyjnego, wszystko z CSS, zero grafik:
   - **Numer pozycji w rejestrze** (01–04, 01–02) dużym serifem w `--sage` przy nazwie. Kolejność w rejestrze to realna informacja, więc numeracja nie jest ozdobą. Sage 39 px spełnia AA dla dużego tekstu (3,8:1 przy wymaganych 3:1).
   - **Koje jako znaczniki**: pełne kwadraty to miejsca w cenie, puste z obrysem to dostawki. „8 + 2" widać, zanim się je przeczyta — a liczba zostaje obok, więc nic nie traci na czytelności.
   - **Skala długości na pełną szerokość** z podziałką co metr do 10,5 m. Pierwsza wersja była wąska (150 px) i różnica 9,99 vs 9,05 m była nieczytelna — dlatego pasek dostał całą szerokość kolumny i własny wiersz. Teraz 8,20 m widocznie krótsze od 9,99 m, a skala jest uczciwa: zaczyna się od zera.
   - **Cena zeszła na koniec** i urosła do serifu 39 px, tuż nad przyciskiem. Kolejność czytania to teraz narastanie: nazwa → załoga → parametry → rozmiar → cena → akcja.

3b. **Pozycja floty prezentuje jacht, nie opisuje go w jednej linijce.** Wcześniej jednostka to był kadr 240×160 i zdanie „Koje 8 + 2 · Kabiny 3 · 9,99 m" — funkcjonalne, ale jacht nie miał w tym żadnej obecności. Teraz:
   - **kadr pionowy 4:5** (272 px na desktopie, 130 px na telefonie) — pionowy format daje sylwetce jachtu miejsce i wypełnia wysokość wiersza,
   - **sześć danych w siatce 2 × 3 z etykietami** (Koje · Kabiny · Długość · Zanurzenie · Silnik · Cena od) zamiast jednej linii — ten sam język co tabela porównawcza na karcie jachtu,
   - nazwa serifem 31 px, cena serifem, akcje dociśnięte do dołu kolumny, więc pod danymi nie zostaje pusty pas.
   Siatka floty ma dwie kolumny na desktopie: żaglowe wypełniają 2 rzędy po 2, motorowe 1 rząd po 2 — żadnych sierot ani pustych pól.

3a. **Grupy floty to rozdziały, nie etykiety.** Nagłówek grupy ma ikonę‑eyebrow (Lucide `sailboat` / `ship`), nazwę serifem 39 px, listę modeli w grupie, duży licznik jednostek i link do pełnej listy, zamknięty 2‑px linią ink. Grupa motorowa siedzi na **piaskowym pasie na pełną szerokość** (`--bleed` przez `margin-inline: -edge`), więc oba działy czytają się jako osobne bloki, nie jako jedna długa lista. Etykieta „Żaglowy/Motorowy" przy każdej pozycji zniknęła — dublowała nagłówek; ten sam element niesie teraz tylko stan (Zajęty / Na zapytanie). W każdej pozycji cena stoi w swojej linii, a pod nią rząd akcji — jeden układ na desktopie i na mobile.

3. **Flota jako zwarty rejestr.** Pełnoszerokie wiersze (5 × ~550 px) były za duże — nie dało się porównać dwóch jachtów bez przewijania. Teraz: dwie kolumny, wiersz = zdjęcie 3:2 (5/12) + nazwa, jedna linia parametrów (Koje · Kabiny · długość), cena i link. Sześć jednostek w ~800 px, grupy „żaglowe / motorowe” z linkiem do pełnej listy. Hover: crossfade na drugi kadr. Widoczna siatka hairline przez stronę **usunięta** (przecinała tekst i tabele, nie pokrywała się z kolumnami treści, robiła szum); zostają linie sekcji i znaczniki przy namiarach.
4. **Jeden pas ink z jednym zdaniem i jedną liczbą.** „16" w `--wave` na 5 kolumnach, zdanie w sand na 7. Zastępuje każdy „dlaczego my".
5. **Opinie jako widget Google (TrustIndex).** Decyzja klienta: opinie mają wyglądać jak osadzony widget, bo to rozpoznawalny dowód. Układ 1:1 ze wzorca: ocena słowna, gwiazdki, „Na podstawie N opinii”, logo Google po lewej; karty z awatarem, datą, znakiem G, gwiazdkami i znaczkiem weryfikacji, „Czytaj więcej”, strzałki karuzeli. Złoto gwiazdek, barwy Google i niebieski znaczka to kolory widgetu — jedyne spoza palety, ograniczone do tej sekcji. Docelowo sekcja jest kontenerem na kod TrustIndex.
6a. **„Podobne jednostki" to porównanie, nie karuzela kart.** Karuzela zdjęć z ceną była ozdobą i nie odpowiadała na pytanie, po co ktoś na nią patrzy — a patrzy po to, żeby sprawdzić, czy sąsiednia jednostka nie jest lepsza dla jego załogi. Sekcja jest **porównaniem kolumnowym**, które przewija się w poziomie jak karuzela, ale niesie dane:
   - **Oglądana jednostka to pełny blok `--ink`** na piaskowej sekcji — jedyny mocny akcent, widoczny z odległości. Stoi pierwsza jako punkt odniesienia, ma etykietę „Ta jednostka" i zamiast przycisku napis „Oglądasz tę jednostkę".
   - Kadry **4:5** (a nie 3:2) — pionowy kadr daje kolumnie obecność i mieści sylwetkę jachtu.
   - **Kolumna etykiet zniknęła zupełnie.** Każda komórka niesie własną etykietę jako zwykły tekst, nie pseudo-element — jest widoczna i czytana przez czytniki ekranu. Dzięki temu kolumna jest samodzielna i przewijanie nie gubi kontekstu, na desktopie i na mobile tak samo.
   - Cena wyrasta do serifu 39 px, więc różnica 950 / 750 / 650 czyta się od razu.
   - Pięć kolumn po 270 px nie mieści się w 1280, więc **strzałki pokazują się także na desktopie** — sekcja znów zachowuje się jak karuzela, tylko wyrazista. Na mobile kolumny mają 232 px, czyli widać oglądany jacht i jeden sąsiedni.
   - Dwie pułapki po stronie obrazów, warte zapamiętania przy przenoszeniu do WP: `<picture>` jest elementem liniowym, więc `img{width:100%}` w środku nie dostaje ramy — wrapper potrzebuje `display:block`; a element siatki z obrazem ma domyślnie `min-width:auto` i rozpycha kolumnę ponad zadaną szerokość, więc kontener kadru potrzebuje `min-width:0`. Obie objawiały się zdjęciem nachodzącym na tekst wyłącznie na wąskich ekranach.
   - Dwie pułapki tabeli: `position: sticky` na komórce tabeli w Chrome przesuwa się względem kolumny i chowa pod sobą treść sąsiedniej (dlatego nie ma sticky), a `table-layout: fixed` dokłada własne skalowanie szerokości (dlatego `auto` + `min-width` na komórkach).

6. **Karta jachtu.** Galeria 8/4 z wylewem w lewo, dane techniczne jako prawdziwa `<table>` z `th scope="row"`, wyposażenie w dwóch kolumnach z kwadratowymi znacznikami (wypełniony = w cenie, pusty = opcja), cennik z cenami serifem i etykietą „szczyt", fasada YouTube (iframe dopiero po kliknięciu), **kontener na kalendarz zewnętrzny** z paskiem tytułu, slotem ze szkieletem i legendą statusów (paper / ink / sand, bez nowych barw). Licznik odsłon w metryce tytułu. Booking: karta sticky po prawej na desktopie; na mobile pasek na dole, który wjeżdża dopiero, gdy galeria opuści ekran (`IntersectionObserver`), z ceną i jednym przyciskiem w zasięgu kciuka.
7. **Bez newslettera.** Stopka: kontakt, godziny, social jako linki tekstowe.

---

## Wyszukiwarka terminu — rdzeń produktu

Strona obiecywała „wybierasz termin, my pokazujemy, co wolne", ale data trafiała do pustego modala. Teraz obietnica jest wykonana w interfejsie:

1. **Hero ma wyszukiwarkę, nie przycisk.** Dwa pola dat na papierowym pasku (przyrząd na tle fotografii) i jedno działanie: „Pokaż wolne jachty". Nadal zero filtrów — tylko termin.
2. **Wybór terminu filtruje flotę.** Zajęte jednostki znikają, nad listą pojawia się „Wolne 11–18 lipca · ceny i suma za 7 dób" oraz przełącznik „Pokaż zajęte (2)". Zajęte wracają wyszarzone, z wyłączonym przyciskiem — użytkownik widzi, czego nie dostanie, ale nie musi tego oglądać domyślnie.
3. **Cena przestaje być „od".** Każda doba wyceniana jest wg sezonu swojego miesiąca, suma liczona po dobach (zakres na przełomie miesięcy liczy się poprawnie). Pozycja pokazuje cenę za dobę w tym terminie i „7 dób · 7 000 zł" — realną kwotę do zapłaty, czyli to, na podstawie czego zapada decyzja.
4. **Trzy stany jednostki:** wolna · zajęta · na zapytanie (pobyt powyżej 14 dób; przycisk zmienia się na „Zapytaj"). Te same trzy stany co legenda kalendarza na karcie jachtu.
5. **Pasek terminu** przykleja się pod nagłówkiem: „11–18 lipca · 7 dób · 4 wolne jachty · Zmień termin". Wybór nie ginie przy przewijaniu, a modal rezerwacji otwiera się z wypełnionymi datami i nazwą jachtu.
6. **Stan pusty** jest realny: nazywa przyczynę (soboty w szczycie schodzą pierwsze), proponuje przesunięcie startu i daje telefon.

**Ruch i hover — polityka.** Hover tylko tam, gdzie element jest **sterowaniem**: przycisk (ink → deep), pole (sage → wave), link (podkreślenie wjeżdża od lewej), strzałka karuzeli, zamknięcie modala, przycisk filmu. Wszystkie hovery dekoracyjne wycięte: podmiana kadru na drugie zdjęcie we flocie (razem z drugim plikiem — mniej do pobrania), powiększanie zdjęcia w porównaniu, unoszenie bloku danych, obramowanie miniatury w galerii. Zdjęcie nie reaguje na kursor; reaguje to, co da się kliknąć.

**Tempo.** Dwa czasy zamiast jednego: `--dur: 260ms` dla sterowań (krótko, bo to odpowiedź na rękę) i `--dur-in: 640ms` dla wejść (długo, bo to ma być spokojne). Wejście to wyłącznie `opacity` + `translateY(10px)` z `cubic-bezier(.22,.61,.36,1)` — wyhamowanie bez odbicia, zero skalowania i zero ruchu w poziomie. W grupach floty pozycje wchodzą kaskadą 0 / 70 / 140 / 210 ms, sterowaną przez rodzica — dzięki temu filtr terminu nigdy nie zostawi pozycji niewidocznej.

**Wejścia są zabezpieczone.** Stan ukryty obowiązuje tylko pod `html.js`, którą skrypt dokłada na starcie. Bez JS (albo gdy skrypt padnie) treść jest po prostu widoczna, zamiast zostać na `opacity: 0`. `prefers-reduced-motion` wyłącza całość.

**Zero własnych SVG.** Znak Google z kart opinii usunięty — nagłówek sekcji i tak niesie logo złożone z kolorowych liter (czysty CSS). W plikach nie ma już ani jednego `<svg>` w kodzie. Ikony pochodzą wyłącznie z Lucide, ładowanego z CDN; **to jedyne SVG w DOM-ie i jedyne, co zostało z ikon** — jeśli mają zniknąć również te, trzeba wskazać zamiennik, bo gwiazdki opinii, strzałki i znacznik weryfikacji nie mają sensownej wersji tekstowej.

**Ruch.** Hero wchodzi sekwencją: eyebrow → nagłówek → lead → wyszukiwarka → podpowiedź, 12 px + opacity, co ~90 ms. Wyłączone przy `prefers-reduced-motion`.

**Dane w prototypie są demonstracyjne.** Tablica `FLOTA` (zajęte terminy) i mnożniki `SEASON` siedzą w jednym miejscu na górze skryptu i są jedyną rzeczą do podmiany, gdy wejdzie system rezerwacji. Nic poza tym nie zależy od danych.

---

## Stany (podgląd: `stany.html`)

- **Przycisk** `.btn` (+ `--outline`, `--paper`, `--ghost-paper`, `--sm`, `--block`): default · hover (ink→deep) · focus-visible (pierścień 2 px `--deep`, offset 3 px) · active (ciemniejszy deep) · disabled (opacity .4) · loading (`.is-loading`: etykieta gaśnie do 45%, pod przyciskiem przesuwa się 2‑px linia w `--wave` — nie spinner).
- **Pole** `.input`: default · hover (border wave) · focus (border deep + pierścień) · disabled (tło sand) · invalid (`aria-invalid`, border ink 2 px, komunikat z ikoną w `--deep`). Bez czerwieni — paleta jej nie ma; błąd niesie ikona + kopia + grubszy border.
- **Szkielet** `.skeleton`: shimmer sand→paper, wyłączony przy reduce‑motion. Wariant `--media` 3:2 i `--line`.
- **Stan pusty / błąd** `.state`: wyrównany do lewej, linia górna, tag w `--deep`, nagłówek serifem, kopia, akcja. Realna mikrokopia („Ten termin jest już zajęty. Soboty w lipcu schodzą pierwsze…").
- **Wiersz rejestru** `.reg`: hover / focus-within → drugi kadr + uniesienie 8 px.
- **Okruszki** `.crumbs`: separator „/" w sage, `aria-current` w ink.
- **Karuzela** `.carousel`: scroll‑snap, przyciski kwadratowe 48 px, `:disabled` na krańcach, klawiatura przez natywny scroll (`tabindex="0"` na torze).
- **Modal** `.modal`: jedyna elewacja; pułapka focusu (Tab/Shift+Tab cyklują, Esc zamyka, focus wraca do wyzwalacza), `aria-modal`, `aria-labelledby`, `body.modal-open` blokuje scroll. Na mobile dokuje do dołu.
- **Ruch**: `.reveal` = 12 px + opacity, 400 ms, `cubic-bezier(.2,.7,.2,1)`; podkreślenia linków wjeżdżają od lewej (`.u`); crossfade zdjęć 400 ms. `prefers-reduced-motion` wyłącza wszystko.
- **Zero CLS**: każde `<img>` ma `width`/`height`, każdy kontener mediów `aspect-ratio` w CSS; hero, rejestr, galeria, wideo, karuzela — identyczne 3:2 (wideo 16:9).

Breakpointy: bazowo mobile, 768 (gutter 32, modal centrowany), 1024 (rejestr 7/5, nawigacja, aside sticky), 1440 (kontener 1280 domyka się).

---

## Treści i dane wzięte z żywej strony

Zrzut `_audyt/home.html` oraz strona `/fundusze-europejskie/` dały realne treści, które zastąpiły moje założenia:

- **Tekst „o nas"** na stronie głównej to skrócona wersja opisu z żywej strony (10 lat działalności, lokalna firma z Giżycka, flota żaglowa/motorowa/houseboaty, szkolenie przed rejsem, wsparcie na Szlaku WJM).
- **Adres i godziny**: Stanica Wodna Stranda, Pierkunowo 36, 11-500 Giżycko; biuro 8:00–20:00, siedem dni w tygodniu. Wcześniej w makiecie była „Marina Stranda" i 8:00–18:00 — obie wartości były zmyślone.
- **Wielkość floty**: 16 jednostek żaglowych i 7 motorowych, razem 23 — nie 16, jak zakładałem. Liczby i nazwy modeli w nagłówkach grup oraz liczba w pasie ink są teraz zgodne z listą na stronie głównej.
- **Dofinansowanie UE**: beneficjent, tytuł projektu, cel, efekty i obie kwoty (737 385,00 zł i 389 675,00 zł) pochodzą z oficjalnej grafiki na `/fundusze-europejskie/`. Na żywej stronie ta treść **jest obrazkiem**, czyli nieczytelnym dla wyszukiwarek i czytników ekranu. W makiecie przepisałem ją na prawdziwy tekst, a z grafiki wyciąłem wyłącznie **obowiązkowy pas logotypów** (Fundusze Europejskie dla Warmii i Mazur · Rzeczpospolita Polska · Dofinansowane przez Unię Europejską · Warmia Mazury), którego nie wolno odrysowywać ani zastępować. Pas pochodzi teraz z oficjalnego „Zestawienia znaków” FEWiM 2021–2027 (wersja kolorowa, pozioma, 3000 px; funduszeeuropejskie.warmia.mazury.pl, plik id 613, oryginał w `_img/ue-zestawienie-kolorowe.png`), a nie ze zrzutu ekranu z żywej strony. Warianty 630/1260/1890 px. Pas stoi na białym polu, bo logotypy wymagają jasnego tła — dlatego w ciemnej stopce ma własną białą płytkę.

**Bez cyfr rzymskich.** Sezon to „maj — wrzesień", nie „V — IX".

**Pasek danych pod hero** dostał trzy poziomy zamiast dwóch: etykieta, wartość serifem 25 px i wiersz uzupełniający (adres, rozbicie floty, zasada czarteru, dni tygodnia). Wcześniej same hasła („Stranda", „16") nie mówiły nic.

**Usunięte jako szum:** numery pozycji 01–04 przy jachtach i nadlinie grup („Pod żaglami", „Bez stawiania żagli") — nazwa grupy i tak to mówi.


**Hero nie udaje wyboru daty.** Wcześniej stały tam dwa natywne pola `type="date"`, co obiecywało, że termin wybiera się na miejscu. Docelowo termin pochodzi z **kalendarza osadzanego w HTML**, więc hero ma teraz jedno duże działanie („Sprawdź dostępność i zarezerwuj"), a wybór terminu odbywa się w modalu.

**Kalendarz w modalu to makieta gniazda.** Element `#cal` (`data-slot="kalendarz-dostawcy"`) pokazuje, jak ma wyglądać kalendarz po osadzeniu: nagłówek z miesiącem i strzałkami, wiersz dni od poniedziałku, siatka dni 7 × n, dzień początkowy i końcowy na `--ink`, zakres pomiędzy na `--sand`, dni poza sezonem wygaszone i przekreślone. Po wskazaniu dwóch dni podsumowanie mówi „Wybrano 11–18 lipca · 7 dób", a przycisk filtruje flotę. Kiedy przyjdzie HTML dostawcy, wchodzi w to miejsce, a jedyne, co trzeba podpiąć, to wywołanie `apply(od, do)`.

**`TODAY` jest stałą** (`2026-05-01`), żeby w makiecie cały sezon 2026 był klikalny. W produkcji to `new Date()`.

**Ikony nie mogą decydować o działaniu strony.** Lucide ładuje się z CDN i podczas testów raz nie wstał — a że `lucide.createIcons()` stało bez zabezpieczenia, wyjątek zabijał **cały** skrypt: kalendarz, modal, filtr floty i pojawianie sekcji. Teraz wywołanie siedzi w `icons()` z `try/catch`, skrypt ładuje się z `defer`, a strona działa bez ikon.

**Sekcja „O nas" prowadzi zdjęciami.** Tekst (skrócony opis z żywej strony) stoi w lewej kolumnie na 5 polach, a prawe 7 pól zajmuje kompozycja trzech kadrów z wylewem w prawo: duży kadr mariny z lotu ptaka 16:10 z podpisem lokalizacji, pod nim dwa mniejsze 4:3 — jacht w porcie i wnętrze. Pod tekstem trzy liczby (na wodzie ponad 10 lat · 23 jednostki · 4,9/5 w Google). Wcześniej sekcja była dwiema kolumnami tekstu i nie miała ani jednego zdjęcia.


---

## Audyt źródeł — co skąd pochodzi

Przegląd „każdy fakt musi mieć źródło" wykrył, że sporo danych w makiecie pochodziło ode mnie, nie z firmy. Wszystkie zostały zastąpione albo usunięte.

| Dane | Źródło |
|---|---|
| Opis firmy, flota, szkolenie przed rejsem | strona główna jachtymazury.pl |
| Adres: Stanica Wodna Stranda, Pierkunowo 36, 11-500 Giżycko | stopka żywej strony |
| Telefon +48 511 420 100, biuro 8:00–20:00, 7 dni | stopka żywej strony |
| Lista i liczba jednostek: 16 żaglowych, 7 motorowych | sekcje floty na stronie głównej |
| Modele w nagłówkach grup | menu żywej strony |
| Dane techniczne Antila 33 / 30, Nautic 880, Nexus 870 Revo | karty modeli na jachtymazury.pl |
| Ceny „od", cennik sezonowy 2027, kaucje, sprzątanie | `/cennik/` |
| Co w cenie, rabaty, dopłaty, godziny wydania i zdania | `/cennik/` |
| Opinie: nazwiska i treści | widget Google na stronie głównej |
| Zespół: Sebastian Pażyszek | dokument o dofinansowaniu UE |
| Zespół: Beata, Kamil, Patrycja | opinia klienta w Google |
| Dofinansowanie: projekt, cel, efekty, kwoty | `/fundusze-europejskie/` |
| Zdjęcia jednostek | pliki z kart modeli (`nexus-870-revo-burta.jpg`, `nautic880.jpg`, `antila-30-.jpg`, `antila-33-strega-kokpit.jpg`) |

**Usunięte, bo nie miały źródła:** ocena „4,9 / 5" i „127 opinii", gwiazdki przy opiniach, daty opinii („2 tygodnie temu”), licznik wyświetleń jachtu, numery rejestracyjne poza dwoma widocznymi na zdjęciach, współrzędne geograficzne, adres e-mail, tytuły artykułów i filmów w sekcji „Wiedza", rok rozpoczęcia działalności, nazwiska dwóch wymyślonych osób w zespole, numery pozycji w rejestrze.

**Zmienione, bo były błędne:** Antila 33 ma **10,79 m**, nie 9,99; szerokość **3,24 m**, nie 3,42; **10 miejsc do spania**, nie „8 + 2"; żagle **49 m²**, nie 46. Antila 27 ma 3 kabiny i 8 miejsc, nie 2 i „5 + 1". Ceny nie wynoszą 950/750/650 zł, tylko **650 / 650 / 330 zł** wg cennika 2027.

**Sekcja „Wiedza" zniknęła**, bo jej treść była zmyślona. W jej miejsce weszły **warunki czarteru** — co jest w cenie, rabaty, dopłaty i godziny wydania — wszystko wprost z cennika. To sekcja bardziej użyteczna niż wymyślone poradniki.

**Flota pokazuje teraz modele, nie nazwy własne.** Wcześniej przypisywałem konkretne jednostki („Kassari", „Strega") do zdjęć, których nie potrafiłem im przypisać — nazwy plików w moim archiwum były moimi etykietami, nie źródłem. Model jest poziomem, na którym zdjęcie, dane techniczne i cena pochodzą z jednej karty na stronie klienta.

**Co nadal wymaga danych od klienta:** ceny Nautica 880 i Futury 860 (w cenniku mają tylko kaucję i sprzątanie — w makiecie „na zapytanie"), dane techniczne Antili 27 poza kabinami i silnikiem, ocena i liczba opinii Google, adres e-mail, zajęte terminy do kalendarza, role Beaty, Kamila i Patrycji.


---

## Ostrość zdjęć, nagłówek mobilny, zespół

**Dlaczego zdjęcia floty były nieostre.** Dwie przyczyny naraz: (1) warianty 960 px były **powiększone** z oryginałów, które na stronie klienta mają 800 px (Antila 30 — 1280 px); (2) poziome zdjęcie rozciągałem w pionowy kadr ok. 300 × 430, więc przeglądarka powiększała je jeszcze raz. Teraz: oryginały pobrane ponownie, kadr 4:3 wycięty z oryginału, warianty wyłącznie **w dół** (400 / 600 / oryginał) z lekkim wyostrzeniem, a w `srcset` nigdy nie ma szerokości większej niż źródło.

**Układ floty — wrócił rejestr** (na życzenie klienta): zdjęcie po lewej, dane po prawej, dwa modele w rzędzie, działy jeden pod drugim, motorowe na piaskowym pasie. Żeby był ostry i czytelny, kolumna danych jest zagęszczona do ~330 px wysokości: cena i „Rezerwuj" w jednym wierszu, znaczniki koi obok liczby, wartości w jednej linii (`nowrap`). Dzięki temu kadr zdjęcia jest prawie kwadratowy (310 × ~340), łódź mieści się w całości, a oryginał 800 × 600 jest w nim pomniejszany albo powiększany najwyżej ~1,1× na ekranie 2× — niewidocznie. `sizes` deklaruje 440 px, żeby przeglądarka na ekranie 2× brała pełny oryginał. Osobny link „Karta modelu" zniknął — prowadzą do niej nazwa i zdjęcie.

**Nagłówek na telefonie:** przełącznik języka po lewej, logo na środku (32–42 px wysokości zależnie od szerokości ekranu), menu po prawej. Przełącznik pokazuje **tylko drugi język** jako obramowany przycisk symetryczny do menu: na polskiej stronie „EN", na angielskiej „PL"; kliknięcie przenosi do tej samej strony w drugim języku (`/en/…` jak na żywej stronie). Na desktopie zostaje „PL · EN". Reguła siedzi w `system.css`, więc działa na wszystkich szablonach.

**Panel ceny na karcie jachtu** jest teraz widoczny także na telefonie — w DOM stoi zaraz po tytule, więc na telefonie pojawia się pod nim w pełnej szerokości, a na desktopie zajmuje prawą kolumnę przez całą wysokość treści i przykleja się przy przewijaniu. Lista warunków w panelu powiększona z 12 do 15 px.

**Zespół dostał własną sekcję.** Piaskowy pas zaraz po „O nas", cztery równe karty — każda osoba osobno, z dużym monogramem na polu w kolorze palety (ink, deep, sage, paper), imieniem i rolą. Zdjęć zespołu klient nie udostępnia, więc monogram zajmuje dokładnie to miejsce i proporcję (4:5), w którą wejdzie portret. Pod kartami dwa cytaty z prawdziwych opinii Google: pod właścicielem — „Uczciwi właściciele, wzorowy kontakt." (Bartosz Borecki), pod obsługą — opinia Pavla Kantora, która wymienia Beatę, Kamila i Patrycję z imienia. Cytat po angielsku zostaje w oryginale (`lang="en"`) — tłumaczenie byłoby już moim tekstem.


**Stały przycisk telefonu** (`.callfab`, wszystkie szablony): okrągły widżet 60 px z samą ikoną słuchawki, prawy dolny róg, w zasięgu kciuka — bez numeru na ekranie, bo ikona sama mówi, do czego służy. Link `tel:+48511420100`, numer w `aria-label` i w dymku `title`. Jeśli biblioteka ikon się nie wczyta, w środku zostaje znak ✆. Kolor `--deep`, żeby nie mylił się z grafitowym przyciskiem rezerwacji. Pulsuje dwoma kołami w `--wave` (cykl 2,4 s); przy `prefers-reduced-motion` koła znikają. Na karcie jachtu podnosi się nad dolny pasek rezerwacji, przy otwartym modalu znika, a stopka na telefonie ma pod spodem zapas 80 px.

**Warstwa mobilna (≤ 640 px) — lekkość.** Strona główna na 390 px skróciła się z ~16 000 do ~14 000 px bez usuwania treści: sekcje 64 px zamiast 96, nagłówki h2 39 px zamiast 49, marginesy nagłówków 32 px. Pasek danych pod hero układa się 2 × 2 zamiast w cztery pełne wiersze. W kartach floty z czterech poziomych linii została jedna (nad ceną); podziałka długości chowa się, zostaje sama wartość. Monogramy zespołu są kwadratowe, cytaty 21 px. Zdjęcia wylane za margines idą na telefonie od krawędzi do krawędzi symetrycznie (reguła w `system.css`). Przycisk w hero skraca się do „Sprawdź dostępność", a długa nadlinia — do „Czarter jachtów · Giżycko" (`.hide-m`, przywrócona w systemie po tym, jak zniknęła przy wcześniejszej przebudowie CSS). Ze stopki usunięty „maj — wrzesień" — tego zakresu nie ma w źródle.

**Krój nagłówkowy: Newsreader zamiast Instrument Serif.** Instrument Serif jest kondensowany, z cienkimi kreskami i ciasnym światłem między literami — w dużym nagłówku wygląda elegancko, ale przy 20–31 px (pasek danych, nazwy modeli, imiona, ceny) zlewał się, szczególnie na telefonie. Porównanie trzech krojów na tych samych tekstach (`_podglad/M0-spec.png`) wskazało Newsreader: szersze litery, wyższe małe litery, a dzięki osi optycznej (`font-optical-sizing:auto`, zakres 6–72) przy małych rozmiarach sam się wzmacnia, przy dużych zostaje smukły. Duże nagłówki mają wagę 400, małe teksty szeryfowe 500. Ujemny tracking zmniejszony o połowę (np. −0,025 em → −0,012 em), bo szerszy krój go nie potrzebuje. Nadal dwie rodziny: Newsreader + IBM Plex Sans.

**Skala długości czytelna bez objaśnień.** Wcześniej był pasek z niepodpisaną podziałką — nie było wiadomo, co mierzy. Teraz: etykieta „Długość całkowita" + wartość, pasek wypełniony do długości jednostki z pionowym znacznikiem na końcu i podpisana podziałka 0 · 2 · 4 · 6 · 8 · 10 m (skala do 11 m, zaczyna się od zera). Na telefonie skala też jest widoczna.

**Przycisk „Zobacz" w kartach floty.** Nie każdy wie, że zdjęcie i nazwa są klikalne. Pod ceną stoją dwa równe przyciski: „Zobacz →" (obrys) prowadzi do karty modelu, „Rezerwuj" (pełny) otwiera rezerwację. Na telefonie oba mają 50 px wysokości i dzielą szerokość po połowie.

**„Ponad 10 lat" podkreślone** w leadzie sekcji O nas: pogrubienie, kolor `--deep` i zakreślenie w tincie `--wave` (26%). Piaskowe zakreślenie z pierwszej wersji było na papierowym tle prawie niewidoczne.

**Tekst w hero mocniej odcięty od zdjęcia:** trzywarstwowy cień pod nadlinią, nagłówkiem, leadem i przypisem, pełna biel leadu i ciemniejsza lewa część przyciemnienia (na telefonie — ciemniejszy dół, gdzie stoi tekst).

**Ocena Google w hero** (`.hero__rev`): gwiazdki + „Opinie klientów w Google", link do sekcji opinii. Liczby **nie są wpisane**, bo nie ma ich w żadnym źródle (zapis strony, żywa strona, wyszukiwarka). Po wpisaniu `data-rating="4,9" data-count="127"` z Profilu Firmy w Google notka sama pokaże „4,9 · 127 opinii w Google" (z polską odmianą), a złota warstwa gwiazdek przytnie się do oceny (`--r` = ocena/5). Te same gwiazdki stoją pod znakiem Google w sekcji opinii.

**Hover „Zobacz"**: przycisk-obrys na hoverze dostawał jasny tekst, a lokalna reguła zostawiała przezroczyste tło — napis znikał. Teraz hover to ink + papier.

**Elementy dekoracyjne:** rysunki liniowe w jednym kolorze (raster, bez SVG i bez tekstu), wstawione jako znaki wodne o kryciu 4–12%.

**Flota: 8 modeli (4 żaglowe + 4 motorowe).** Doszły Antila 28.2, Maxus 28, Stillo 31 i Futura 860 — każdy z danymi z tabeli „DANE TECHNICZNE" na stronie jednostki (Pakri, Prawy Hals, Star, Eufemia), ceną „od" z cennika 2027 i zdjęciem z jej galerii. Wybór poszerza zakres floty (8,6–10,8 m, od 330 do 900 zł) zamiast dublować Antilę 33 modelem 33.3 o tych samych wymiarach. Nautiner 38 (11,5 m) pominięty — wykracza poza skalę 11 m i ma dopisek, że nie jest dla początkujących. Stawki nowych modeli są w silniku sumy za pobyt.

**Ocena Google: 4,8 z 57 opinii** — źródło: zrzut panelu „Podsumowanie opinii w Google" od klienta (24.09.2026). Wpisana w notkę w hero (`data-rating="4,8" data-count="57"`, złota warstwa gwiazdek przycięta do 96%) i w podsumowanie sekcji opinii: logo Google → 4,8 → gwiazdki → „Na podstawie 57 opinii w Google". Liczby trzeba aktualizować ręcznie albo — docelowo — brać z widgetu TrustIndex.

**Elementy graficzne (paczka `jachtymazury-deco.zip`).** Biel zamieniona na przezroczystość, kreska lekko wzmocniona, pliki przycięte i pokolorowane kolorem z palety wpalonym w plik (`assets/img/deco/*-c.webp` + PNG). Wstawione jako tła CSS, bez SVG i bez masek (Chrome blokuje maski CSS przy otwieraniu stron z dysku). Rozmieszczenie:
- kontury mapy (`--sage`, 34%) — prawa strona nagłówka floty, poza tekstem leadu,
- sylwetka jachtu żaglowego i motorowego (`--ink`, 85%) — stoją na grubej linii nagłówków grup; na telefonie w prawym górnym rogu nagłówka,
- róża wiatrów (`--wave`, 20%) — prawa strona pasa „23 jachty"; pas wrócił ze zdaniem z opisu firmy („Dbamy o to, aby wynajem był przewidywalny i dobrze zorganizowany — niezależnie od doświadczenia sternika"),
- lina z węzłem (`--sage`) — przerywnik na górze sekcji Zespół,
- kotwica z kołem (`--sage`, 50%) — puste pole między nagłówkiem a leadem sekcji warunków,
- fale (`--wave`, 12%, kafel 280 px) — tło sekcji opinii.
Wszystkie mają `aria-hidden` i `pointer-events:none`.

---

## Podstrony (generowane: `python3 _build/podstrony.py`)

| Plik | Źródło treści |
|---|---|
| `jachty-zaglowe.html` | 16 jednostek z listy na stronie głównej; dane z tabel „Dane techniczne" na stronach jednostek; ceny „od" z `/cennik/` |
| `jachty-motorowe.html` | 7 jednostek z listy + Stillo 31 (ma stronę i stawki); jw. |
| `czarter-bez-patentu.html` | `/czarter-bez-patentu/` (warunki: do 75 kW, kadłub do 13 m, do 15 km/h) + jednostki z tej strony |
| `cennik.html` | `/cennik/` — obie tabele w całości, W cenie, Rabaty, Opłaty (obligatoryjne i nieobligatoryjne), godziny wydania/zdania |
| `jachty-na-sprzedaz.html` | `/jachty-na-sprzedaz/` — 6 ogłoszeń: rocznik, cena + VAT, wyposażenie, zdjęcia z tej strony |
| `poradnik.html` | `/poradnik-czarterowy/` + tytuły, pierwsze akapity i zdjęcia 7 artykułów |
| `port.html` | `/port/` + zdjęcie z tej strony |
| `wspolpraca.html` | `/inwestycje-i-posrednictwo/` (w tym „około 10% rocznego zwrotu" — deklaracja operatora, tak oznaczona) |
| `kontakt.html` | `/kontakt/` — telefon, e-mail (zdekodowany z ochrony Cloudflare), godziny; zdanie o porcie i zdjęcie z `/port/`. Formularz skrócony z 5 pól do 3 (imię, telefon lub e-mail, wiadomość) + wybór sprawy (Czarter, Zakup jachtu, Współpraca, Inne — odpowiadają działom strony). Teksty formularza i komunikat po wysłaniu są moje — do akceptacji klienta |
| `polityka-prywatnosci.html` | `/polityka-prywatnosci/` w całości (administrator: Sebastian Pażyszek, ul. Rolnicza 56, NIP) |

**Nawigacja** odwzorowuje strukturę żywej strony: Czarter jachtów ▾ (żaglowe, motorowe, bez patentu) · Na sprzedaż · Poradnik · Cennik · Port · Współpraca · Kontakt + „Rezerwuj online". Zniknęły wymyślone pozycje „Rezerwacja online" i „Wiedza" oraz link „Regulamin" (żywa strona nie ma regulaminu). Menu rozwijane działa na najechanie, kliknięcie i klawiaturę (Esc); na telefonie hamburger otwiera pełnoekranowe menu z pułapką fokusu. Wspólna logika w `assets/js/site.js`, style menu w `system.css`, style podstron w `assets/css/pages.css` (generowane: nagłówek z karty jachtu + komponenty wycięte z CSS strony głównej + `_build/pages-extra.css`). Nagłówek i stopka są wstrzykiwane przez generator także do `index.html`, `jacht.html` i `fundusze-europejskie.html`, więc są wszędzie identyczne. Przed zmianą generator zapisuje kopie stron do `_build/kopie/`.

**Stopka**: dodany e-mail `info@jachtymazury.pl` i prawdziwe adresy profili Facebook / Instagram / YouTube.

**Listy floty**: te same karty co na stronie głównej + filtr modeli (przyciski z liczbą jednostek, `aria-pressed`, komunikat „Pokazano n z m"). Skala długości do 12 m (Nautiner 38 ma 11,5 m), również na stronie głównej. „Zobacz" prowadzi do karty jachtu tylko dla Kassari (jedyna gotowa karta); pozostałe czekają na szablon karty jednostki w WP. Artykuły poradnika też linkują na razie do `#`.

**Nagłówek podstron** jest ciemny (`--ink`), a wszystkie teksty w nim są białe. Pasek z menu nad nim też jest ciemny, z białym logo, białym menu i białym przyciskiem. Po przewinięciu robi się jasny z kolorowym logo, tak jak na stronie głównej. Przy otwartym menu mobilnym pasek jest jasny. Listy jachtów mają pod spodem białe tło (`#fff`).

**Grafiki na podstronach**: to osobny zestaw z `jachtymazury-podstrony-deco.zip`. Pliki przerobione tak jak zestaw ze strony głównej: biel zamieniona na przezroczystość, kreska wzmocniona, przycięte, pokolorowane w pliku (`p-*-c.webp` i `-c.png`).
- nagłówki (`--sand`, 55%, lewa krawędź wygaszona gradientem): żaglowe — dwa jachty pod żaglami; motorowe — jacht motorowy z kilwaterem; bez patentu — koło sterowe i manetka; cennik — dziennik jachtowy z cyrklem; na sprzedaż — jacht na łożu; poradnik — węzły; port — pomost z trzcinami; współpraca — kluczyk na pływaku,
- kontakt — dzwon okrętowy nad formularzem,
- trzciny (`--sage`) zamiast liny w poradniku i porcie,
- kafel z motywami jeziora (`--wave`, 8%) zamiast fal w piaskowych sekcjach.
Na telefonie grafika w nagłówku stoi pod tekstem. Róża wiatrów w pasie „Wybrałeś termin?” zostaje ze strony głównej.

**Dopracowanie UI (24.09.2026)**
- Martwe linki usunięte. „Zobacz” przy modelach na stronie głównej prowadzi do listy jednostek z włączonym filtrem (`?model=`). Na listach jednostek „Zobacz” jest tylko przy Kassari, która ma kartę; reszta ma sam przycisk „Rezerwuj”. W porównaniu na karcie jachtu są linki „Jednostki … →” i „Rezerwuj”. „Broszura PDF” otwiera drukowanie strony (zapis do PDF z przeglądarki), docelowo PDF wygeneruje motyw. „Zobacz wszystkie opinie” prowadzi do profilu w Google (link od klienta). EN prowadzi na razie do żywej wersji `jachtymazury.pl/en/`.
- Artykuły poradnika mają własne strony (`<slug>.html`, generowane przez `_build/artykuly.py`). Treść wyciągnięta 1:1 z zapisanych stron żywego serwisu, linki wewnętrzne przepięte na strony makiety, czas czytania liczony z liczby słów (200 słów/min).
- Karta jachtu i strona funduszy mają ciemny nagłówek i ciemny pas u góry, jak reszta podstron (`assets/css/head-dark.css`).
- Nadtytuły nie powtarzają okruszków: liczba jednostek, liczba artykułów, czas czytania. „8 jednostek” na liście motorowych obejmuje Stillo 31, strona główna podaje 7 motorowych za żywą stroną — do potwierdzenia.
- Na telefonie okruszki pokazują tylko krok wstecz („← Czarter jachtów”), a filtr modeli jest wygaszony przy prawej krawędzi.
- Filtr stoi bliżej kart, „na zapytanie” jest złożone krojem tekstowym, cennik mieści się na komputerze bez przewijania w bok, dolny pasek stopki jest większy i jaśniejszy.
- Pływający telefon znika w kontakcie i przy otwartym menu mobilnym.
- Strona 404 z linkami do floty, cennika i kontaktu. Jej teksty są moje — do akceptacji.
- Ze strony głównej usunięty martwy skrypt starego formularza rezerwacji (wywoływał błąd JS i zawierał wymyślony komunikat o zajętych sobotach).

**Pas „Wybrałeś termin?"** nad stopką ma od dołu cienką jasną linię (`rgba(252,249,244,.5)`), bo oba bloki są ciemne i zlewały się w jeden.

**Cennik na telefonie**: szeroka tabela (13 kolumn) zamienia się w listę rozwijanych pozycji (`<details>`) — nazwa jachtu i „od … zł / doba", po rozwinięciu wszystkie okresy, kaucja i sprzątanie.

**Niezgodności w danych klienta (do potwierdzenia):**
- Nautic 880: strona modelu 9,17 m / 3,00 m / zanurzenie 0,65 m / 2 kabiny; strony jednostek 9,00 m / 3,05 m / brak zanurzenia i kabin. Strona główna pokazuje dane modelu, lista motorowych — dane jednostek.
- Nexus 870 Revo: strona modelu „kabina dziobowa + druga zamykana lub otwarta" (na stronie głównej: 2), jednostka „Wiktor" — 1 zamykana kabina, „Bolek" — brak wartości.
- Antila 33 „Kassari": tabela jednostki 51,2 m² żagli (jak 33.3), strona modelu Antila 33 — 49 m².
- Antila 33 „Biała Perła": nazywana „Antila 33", ale zdjęcia i dane (51,2 m², 2026) wskazują na 33.3 2025/2026 (w cenniku od 850 zł). Na liście cena wg nazwy — od 650 zł.
- Antila 30.1 „Bradl" ma stronę, ale nie ma jej na liście floty na stronie głównej — pominięta.
- Antila 24.4, Antila 30.1 E „Cleopatra" (wiersz „2026" pusty), Nexus „Bolek", Calipso 750, Futura 860, Nautic 880, Nautiner 38 — brak stawek w cenniku → „na zapytanie".

---

## Do potwierdzenia u klienta

Stan po audycie źródeł. Wszystko, czego tu nie ma, pochodzi z jachtymazury.pl (strona główna, `/cennik/`, karty modeli, strona jednostki „Kassari", `/fundusze-europejskie/`).

**Brakuje w źródle — w makiecie puste albo „na zapytanie":**
- **Stillo 31 „Star"** ma stronę, tabelę danych (rocznik 2025) i stawki w cenniku, ale nie ma go na liście jednostek na stronie głównej (16 żaglowych, 7 motorowych). Potwierdzić, czy jest we flocie — wtedy motorowych jest 8.
- **Antila 28.2** ma w cenniku dwa wiersze („Antila 28.2" od 550 zł i „Antila 28.2 2027" od 650 zł); karta używa pierwszego.
- **Futura 860** — w cenniku tylko kaucja i sprzątanie, więc „na zapytanie".
- Stawki Nautica 880, Futury 860 i Nautinera 38 — w cenniku są tylko kaucja i sprzątanie. W makiecie: „cena na zapytanie".
- Wymiary Antili 27 (strona modelu podaje tylko 3 kabiny, 8 miejsc i silnik Mercury 9,9 KM) — dlatego Antila 27 nie trafiła do zestawienia floty.
- **Ocena zbiorcza i liczba opinii w Google** — brak w źródłach; potrzebne do notki w hero (`data-rating`, `data-count`). **Gwiazdki przy opiniach są ze źródła:** widget TrustIndex rysuje każdą gwiazdkę jako obrazek `star/f.svg` (pełna) lub `e.svg`/`h.svg` (pusta/połówka); wszystkie sześć pokazanych opinii ma pięć pełnych, więc karty pokazują 5 z 5. Gwiazdki to znak ★ w złocie Google (#fbbc04), bez SVG, z `aria-label="Ocena 5 na 5"`. Sekcja pozostaje gniazdem na widget (`data-slot="widget-trustindex"`).
- Adres e-mail — w zapisie strony zakodowany przez wtyczkę; nie podaję go.
- Zajęte terminy — przyjdą z kalendarza dostawcy (`data-slot="kalendarz-dostawcy"`, wywołanie `apply(od, do)`). Do tego czasu strona nie twierdzi, że coś jest wolne lub zajęte — pokazuje tylko ceny z cennika.
- Role Beaty, Kamila i Patrycji — z opinii wiadomo tylko, że to obsługa. W makiecie „obsługa czarteru".
- Portrety zespołu — sekcja ma na nie miejsce (4:5); do tego czasu monogramy.
- Większe oryginały zdjęć jednostek (min. 1600 px) — obecne 800 px to granica ostrości na telefonach 3×.
- Film na karcie jachtu — placeholder ID YouTube.
- Broszura PDF — link bez pliku; w motywie WP generowana z danych modelu.

**Moje interpretacje, do akceptacji:**
- Podział 16 żaglowych / 7 motorowych policzony z sekcji floty na stronie głównej. „Nautiner 38 Blask Stilo" stoi tam wśród motorowych, choć opis firmy wspomina o houseboatach — potwierdzić przypisanie.
- Ceny „od" to najniższa stawka dobowa danego modelu w cenniku 2027.
- Suma za pobyt liczona dzień po dniu wg stawek z cennika; rabat 5% przy 14+ dobach (z cennika). Termin krótszy niż 7 dób albo zahaczający o okresy „za okres" (29.04–03.05, 26.05–30.05) → „cena ustalana indywidualnie", zgodnie z zasadą z cennika.
- Kolumny „−5%" w nagłówku cennika (26.06–28.08, 29.04–03.05) nie mają w źródle opisu — nie stosuję ich.
- Kalendarz przewija się od kwietnia do października 2027 — to decyzja interfejsu, nie dana od firmy.

**Zdjęcia:** galeria i plakat filmu na karcie Antili 33 pochodzą ze strony jednostki „Kassari" (nazwa widoczna na burcie). Karty floty i porównania — z kart modeli (`nexus-870-revo-burta.jpg`, `nautic880.jpg`, `antila-30-.jpg`, `antila-33-burta.jpg`). W „O nas" — Antila 27 „Marmolada" i „Hiuma" (nazwy widoczne na burtach). Wnętrze w „O nas" i widok mariny z lotu ptaka pochodzą z żywej strony, ale nie wiem, której jednostki ani której mariny dotyczą — dlatego nie mają podpisów wskazujących konkretne miejsce.
