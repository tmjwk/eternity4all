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
## Przypadek 6: encje HTML, których nie widziały testy (normalizacja na granicy)

**Kontekst:** galeria 131 albumów zaimportowana ze starego WordPressa;
tytuły wpisów przyszły z encjami HTML („&quot;GILU&quot;" zamiast
„"GILU""). Frontend dodatkowo escapował stringi przy renderze —
podwójne escapowanie.

**Przebieg:** przez lata nikt tego nie zauważył, bo żaden test
funkcjonalny nie łapie tej klasy błędu: funkcja działa, dane się
renderują — tylko żródło danych było nieczytelne dla człowieka.
Wykrył to odbiorca, czytając stronę („masz takie błędy w galerii...").
Naprawa musiała objąć źródło danych i obie kopie JSON-a naraz —
inaczej problem wróciłby przy najbliższej przebudowie.

**Wniosek → zasada 12:** normalizuj dane RAZ, na granicy importu;
utrzymuj jedno źródło prawdy, a okresowy przegląd efektu końcowego
„gołym okiem" wychwytuje to, czego nie widzą testy automatyczne.

## Przypadek 7: repo miękko dobija do limitów (warstwy i budżety)

**Kontekst:** projekt z ~300 MB zdjęć w repo; właściciel pyta o
ostrzeżenia GitHuba (1 GB) i blokadę pusha (5 GB).

**Przebieg:** definitywny pomiar (barę clone) pokazał 297 MB przy polu
`size` w API równym 82 MB — cache dostawcy mocno zaniżał, więc
monitoring oparty o API byłby fasadowy. Analiza obiektów: 0 martwych
blobów, czyli historia dotąd czysta. Ale zaplanowany przebieg
czyszczenia EXIF podmieniłby każde zdjęcie — i historia zaczęłaby
tyć o ~270 MB w jednym ruchu. Git LFS odpadł (GitHub Pages serwuje
wskaźniki zamiast plików), a Pages ma własny, niższy limit 1 GB
dla opublikowanej strony.

**Rozwiązanie:** monitoring lokalnym `git count-objects` w rytmie zapisów
(próg ~70% budżetu); czyszczenie EXIF zsynchronizowane ze squaszem do
finalnego repo (pojedynczy commit, historia od zera); wentyl bezpieczeństwa
= object storage dla binariów, gdyby galeria urosła ponad budżet.

**Wniosek → zasady 9, 11 + sekcja „Warstwy repo":** binaria mają
budżet i trzeba go pilnować miarą lokalną; operacje podmieniające
ciężkie pliki synchronizuj z resetem historii.

## Przypadek 8: pipeline idempotentny (decyzja architektoniczna przed potrzebą)

**Kontekst:** galeria ładuje oryginalne zdjęcia (298 KB średnio) do
siatki miniaturek; właściciel chce WebP + blur-up. Pytanie otwarte:
co będzie, gdy źródłem zdjęć stanie się Facebook?

**Przebieg:** zamiast jednorazowego skryptu „pod 916 plików" zbudowano
pipeline: skanuje katalogi, dorabia brakujące miniatury i LQIP-y,
istniejących nie rusza; źródło-agnostyczny (nie interesuje go, skąd
pliki się wzięły — stary WP, import z FB, dysk). Gdy później doszło
pytanie o import z FB, odpowiedź była: „wrzucasz pliki, odpalasz
pipeline, działa" — zero przeróbek. Oryginały plików źródłowych
zostały bajt-w-bajt (enkodowanie odwracalne, metadane nietknięte);
miniatury są plikami pochodnymi, regenerowalnymi w każdej chwili.

**Wniosek → zasada 7:** rozdziel pliki źródłowe od pochodnych;
pipeline pochodnych trzymaj w repo, idempotentny i agnostyczny wobec
źródła — decyzję architektoniczną podejmujesz PRZED potrzebą,
bo po jej wystąpieniu jest już za drogo na refaktor.
