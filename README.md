# jachtymazury.pl — makieta nowej strony

Statyczna makieta strony czarteru jachtów z Giżycka (Stanica Wodna Stranda). Na jej podstawie powstanie własny motyw WordPress bez wtyczek.

## Jak obejrzeć

Otwórz `index.html` w przeglądarce. Wszystko działa z dysku, bez serwera.

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

## Po zmianach

Podstrony, stopka i nagłówek są generowane. Zmiany wprowadzaj w `_build/podstrony.py`, `_build/pages-extra.css` albo `_build/head-dark.css`, a potem uruchom:

```
python3 _build/podstrony.py
```

## Źródła i decyzje

Każda informacja na stronie pochodzi z obecnego serwisu albo od klienta. Skąd co jest, co zostało do potwierdzenia i dlaczego strona wygląda tak, a nie inaczej, opisuje `RATIONALE.md`.
