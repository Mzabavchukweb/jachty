# jachtymazury.pl — makieta nowej strony

Statyczna makieta strony czarteru jachtów z Giżycka (Stanica Wodna Stranda). Na jej podstawie powstanie własny motyw WordPress bez wtyczek.

## Jak obejrzeć

Strony leżą w katalogach, pod tymi samymi adresami co na obecnej jachtymazury.pl (np. `antila-27-furaha/`, `czarter-jachtow-zaglowych/antila-27/`), więc do podglądu potrzebny jest serwer:

```
python3 -m http.server 8000
```

i adres http://localhost:8000/. Podgląd online: https://mzabavchukweb.github.io/jachty/

## Struktura

- `index.html` — strona główna
- `jacht.html` — karta jachtu (Antila 33 „Kassari”)
- `fundusze-europejskie.html` — dofinansowanie UE
- pozostałe `*.html` — podstrony i artykuły poradnika, **generowane**
- `assets/css/system.css` — tokeny i wspólne komponenty
- `assets/css/pages.css`, `assets/css/head-dark.css` — style podstron, **generowane**
- `assets/js/site.js` — menu, menu mobilne, filtr modeli, animacje wejścia
- `assets/img/` — zdjęcia (warianty WebP/AVIF/JPG) i grafiki liniowe (`deco/`)
- `_build/` — generator podstron i źródła CSS
- `_a/`, `_u/`, `_p/`, `_img/` — dane źródłowe z obecnej strony (treści, specyfikacje, cennik, zdjęcia)
- `_seo/` — inwentaryzacja SEO obecnej strony (`obecna-strona.json`: tytuły, opisy, H1–H3, canonical, hreflang, Open Graph, dane strukturalne, alt zdjęć, linki), mapa adresów (`mapa-adresow.csv`) i docelowa mapa strony
- `_build/seo_crawl.py` — ponowna inwentaryzacja obecnej strony

## Po zmianach

Podstrony, stopka i nagłówek są generowane. Zmiany wprowadzaj w `_build/podstrony.py`, `_build/pages-extra.css` albo `_build/head-dark.css`, a potem uruchom:

```
python3 _build/podstrony.py
```

## Źródła i decyzje

Każda informacja na stronie pochodzi z obecnego serwisu albo od klienta. Skąd co jest, co zostało do potwierdzenia i dlaczego strona wygląda tak, a nie inaczej, opisuje `RATIONALE.md`.
