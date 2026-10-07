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
