# PRZYPADKI — studia z życia (dlaczego protokół wygląda tak, a nie inaczej)

> Zbiór realnych zdarzeń z projektów prowadzonych z asystentami AI.
> Cel: każda zasada protokołu ma tu swoje uzasadnienie empiryczne.
> Nazwy użytkowników/reposominięte celowo; sekwencje zdarzeń wiernie.

## Przypadek 1: śmierć czatu = śmierć projektu (koszt braku protokołu)

**Kontekst:** równoległy, długoterminowy projekt prowadzony na czacie
z innym modelem (wersja 5.2), bez zewnętrznego zapisu.

**Przebieg:** czat przestał odpowiadać — przez ~2 dni wyłącznie błędy.
Właściciel nie mógł ani czytać historii, ani wykonywać zmian w projekcie
związanym z tamtym czatem. Wiedza projektowa (decyzje, uzgodnienia,
kod z sesji) istniała tylko w rozmowie.

**Szkoda:** nieodwracalna utrata kontekstu projektu.

**Wniosek → zasady 1, 3:** prawda musi mieszkać poza czatem; wejście do
projektu nie może wymagać dostępu do starej rozmowy.

## Przypadek 2: cztery resety środowiska (protokół pod ostrzałem)

**Kontekst:** projekt strony klubowej na platformie z piaskownicą;
zależność od serwera deweloperskiego, bazy i setek plików kodu.

**Przebieg:** piaskownica resetowała się wielokrotnie. Typowy obraz:
pliki projektu znikają razem ze środowiskiem. Odbudowa za każdym razem
była możliwa, bo w Gicie leżały: zapis rozmowy (ustalenia), dziennik
prac i stopniowo rosnąca migawka kodu. Wariant złośliwy (reset nr 4):
pliki PRZETRWAŁY, ale rozsypały się zależności — zniknęła binarka
serwera deweloperskiego; objaw: strona martwa, przy czym kod i baza
całe. Naprawa: reinstalacja zależności + restart (diagnoza: „środowisko
rozpadło się, projekt nie").

**Wniosek → zasady 7, 8:** migawka ma obejmować WSZYSTKO, czego nie da
się odtworzyć z jednego polecenia; odtwarzalność bazy danych testuj
celowo (pełny powrót danych z seed + automatycznego syncu był
przeprowadzony po czyszczeniu bazy — i zadziałał).

## Przypadek 3: zapis, który blokuje rozmowę (protokół też bywa błędny)

**Kontekst:** pierwszy mechanizm zapisu: podzadanie/delegacja wysyłająca
pliki na Git w trakcie tury.

**Przebieg:** asystent delegował zapis i czekał na wynik — czat był
zablokowany dokładnie tak samo, jak gdyby zapisu nie delegował.
Asystent niedostępny, rozmowa zamrożona do końca zapisu.

**Wniosek → zasada 6:** asynchroniczność daje PROCES W TLE, nie delegacja.
Poprawka: `nohup` + log + pidfile chroniący przed podwójnym zapisem;
powrót do rozmowy < 1 s.

## Przypadek 4: granice przypomnień (uczciwość zamiast obietnic)

**Kontekst:** użytkownik prosił: „przypomnij mi jutro, że trzeba
dokończyć".

**Przebieg:** asystent nie może sam otworzyć czatu o wyznaczonej porze —
obietnica „przypomnę jutro" byłaby nadinterpretacją możliwości.

**Rozwiązanie:** baner przypomnień na górze dziennika prac (pierwsza
rzecz czytana na starcie sesji) + zapis w pliku startowym; przypomnienie
odpala się przy pierwszej wiadomości użytkownika następnego dnia.

**Wniosek → zasada 10:** o ograniczeniach mówi się wprost i projektuje
obejścia, zamiast obiecywać niemożliwe.

## Przypadek 5: drill ciągłości (jak wiedzieć, że to działa)

**Przebieg:** celowy test: z GitHub API pobrano drzewo repo, plik startowy
i dziennik; sprawdzono obecność najnowszych wpisów i fraz kluczowych —
symulując dokładnie to, co robi nowa sesja po stracie poprzedniej.
Test przeszedł; wykrył też drobiazg (wielkość liter w frazie), co
potwierdziło wartość dosłownej weryfikacji zamiast zakładania.

**Wniosek:** ciągłość się testuje jak wszystko inne — end-to-end,
od odczytu z repo do podjęcia pracy, nie „na oko".

## Przypadek 6: kompresja kontekstu w trakcie sesji (regres formy i „zapominanie")

**Kontekst:** długi projekt na platformie, która przy przepełnieniu
okna kontekstowego sama skraca starszą część rozmowy do streszczenia
— sesja formalnie trwa dalej.

**Przebieg:** po skrócie asystent zachował twardy stan projektu
(wersje plików, podjęte decyzje — bo te żyły w repo), ale stracił
ustalenia „miękkie": dwukrotnie wrócił do formalnej formy zwracania
się do właściciela (per „Pan"), mimo wielotygodniowej umowy o formie
bezpośredniej, i zapomniał o bieżącej dyrektywie archiwizacji rozmowy.
Oba regresy wyłapał Człowiek — zanim asystent sam zauważył, że coś
jest nie tak. Powtórzony rytuał startowy (plik startowy → dziennik
prac → baner) przywrócił pełny obraz w kilka minut.

**Szkoda:** dwie tury rozmowy na wyłapanie i naprawę regresów;
w samym projekcie zero strat — ten żył w repo.

**Wniosek → zasada 9:** kompresja kontekstu = nowa sesja — rytuał
startowy powtarza się także po skrócie W TRAKCIE formalnie tej samej
sesji. Ustalenia „miękkie" (forma, ton, bieżące dyrektywy) wpisuj do
banera dziennika prac — streszczenie gubi je pierwsze, a nie są ani
zadaniem, ani obietnicą terminową. Drugi wniosek: Człowiek bywa
szybszym czujnikiem dymu niż asystent — nagły regres formy to sygnał
„odśwież się z repo", nie powód do pretensji.

## Przypadek 7: mapa zapisu, która nie rosła (plik istnieje ≠ plik zarchiwizowany)

**Kontekst:** migawka projektu wysyłana skryptem z JAWNĄ LISTĄ plików
(mapą zapisu) — push po kolei z porównaniem blob-SHA; projekt w fazie
najintensywniejszego wzrostu: dziennie powstawało kilkanaście nowych
plików klasy „produkt" (wyniki analiz, skrypty, zrzuty ekranu).

**Przebieg:** mapa nie była dopisywana od wielu zadań — nowe pliki
powstawały w piaskownicy i tam kończyły żywot. Asystent i właściciel
widzieli je na dysku („są!"), więc nic nie alarmowało. Dziura wyszła
na jaw dopiero przy weryfikacji PO STRONIE REPO (odczyt surowych URL-i
przez API): kilkanaście plików z ostatnich zadań zwracało 404. Zapis
formalnie „działał" — po prostu zapisywał nie to, co istniało.

**Szkoda:** utraty danych nie było (piaskownica żyła), ale migawka
była cicho dziurawa — reset środowiska w tym momencie oznaczałby
nieodtwarzalność 1:1 i powtórzenie wielodniowej pracy.

**Wniosek → zasady 1, 7, 9:** mapa zapisu jest CZĘŚCIĄ migawki, nie
szczegółem implementacyjnym — nowy plik klasy „produkt" dopisuj do
mapy w chwili tworzenia, a rytuał końca zadania ma krok „sprawdź mapę".
Odwrotnie: kompletność migawki weryfikuj zawsze OD STRONY REPO (tam
mieszka prawda), nigdy od strony katalogu roboczego — katalog potrafi
udawać, że wszystko jest już zapisane.

## Przypadek 8: emoji w nazwie pliku kontra API (nazwa pliku to interfejs)

**Kontekst:** wypychanie paczki plików na repo przez GitHub Contents
API; wśród okładek znalazła się nazwa z emoji i znakami specjalnymi
(wariant: „…2025-2026🏓‼️.webp" — poprawna, czytelna dla człowieka,
zweryfikowana graficznie przed deployem).

**Przebieg:** push padł w połowie z UnicodeEncodeError — skrypt wklejał
ścieżkę surowo do URL-a, a klient odmówił zakodowania znaków spoza
ASCII. Błąd był GŁOŚNY (fail fast), więc nic nie utracono; łata =
jawny percent-encoding ścieżki przy budowaniu URL-a (dla nazw czysto
ASCII zachowanie identyczne). Ten sam projekt złapał wcześniej
bliźniaczy problem od strony ODCZYTU — ta sama granica piaskownica–repo,
dwa kierunki, jedna lekcja.

**Wniosek → zasada 7:** nazwa pliku to interfejs między systemami.
Na styku z API nazywaj pliki defensywnie (ASCII), a gdy znaki narodowe
czy emoji są wpisane w treść projektu — koduj ścieżki jawnie
i testuj przesyłkę end-to-end po stronie repo. Weryfikacja „na oko"
w katalogu roboczym tego błędu nie widzi; weryfikacja w repo — tak.
