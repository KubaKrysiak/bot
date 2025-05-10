![image](https://github.com/user-attachments/assets/602f7862-458a-4b17-98ac-77975e583648)

Przed zrobieniem dokumentacji:
Obowiazkowo
1. usunac usuwanie konfiguracji z ui i z zbednych funkcji bo nie dziala
2. dodac ladne printy ze np. zaczynanie lowienia / itp. w mt2window jesli trzeba lub nie i ogolnie ladne printy w ui
3. dodac 6 opcje w ui.py wyjscie z programu
7. Po zrobiebiu pkt. 4 5 i 6 jak juz beda finalne funkcje zrobic dokumentacje, zaktualizowane uml jak na skosie i na wykladzie nr 9.
Ja bym zrobil jakos podstawowo punkt nr 4 zeby nie bylo chamsko metin 2 a te 5 to nie wiem albo zaznaczyc ze nazwy tak sa nazwane ale nie uzywamy do tego itd bo cos tam na zajeciach i tak odpale mt2 ale zeby tego na skosa nie wysylac tak np zamiast wszedzie gdzie sie pojawia metin2 dac nazwe alibaba w uml itd xDd nie wiem
4. Do wyboru albo pozmieniac nazwy i metod klas ze zamiast find fish find color in region itp. bo czat tak pisze wtedy trzeba zroic cos takiego:
-  pozmieniac nazwy i metod klas
- dodac do konfiguracji wybor nazwy okienka jaka ma byc znajdowania wtedy trzeba zaaktulazizowac tez config.py configurator.py oraz zmienic wszedzie w place mt2 window  i WSZEDZIE gdzie trzeba ze zamiast METIN2
  zmienia sie po nazwie ktora jest w konfiguracji
- W tescie tez zeby sprawdzic czy dziala usunac nazwe METIN2 bo taka pygame daje nazwe okienku na cos jak test albo cos
- w skrocie leciec w bambuko ze to nie bot do metina xD
5. Bardzo opcjonalnie
- zrobic zeby lowienie bylo na kilka okienek a nie na jedno bo autologin dziala na dowolna ilosc ( nie ma tego w tescie wiec no mozna to tez potem zrobic nie trzeba do 12 maja)
- wybieranie robakow ma byc co 200 i po 200 zamiast wciskac 1 wciska sie 2 potem 3 itd. w sensie ze robaki sa wybierane z kolejnego slota ( tego w tescie nie ma tylko w metinie)
6. poprawic ogolnie ze test jest lepszy itd jesli chcesz
7. stworzyc nowe repozytorium z 1 commitem i projektem zrobionym
8. oprocz opisu klas zauwazone wzorce projektowe moze itp
9. do 12 maja na skos trzeba wyslac cel i biblioteki ktore mamy w documentation.txt juz wiec no juz to mamy ale my juz konczymy projekt wiec no xd
  Czat pisze cos takiego
bugi:
okna z pygame sie nie resizuja bo to pewnie pygame
po wykryciu przycisku login stop nie klika sie enter

notatka do pkt 4:
---------------------------
Twój projekt może wiązać się z pewnymi ryzykami prawnymi, nawet jeśli jest tworzony wyłącznie w celach edukacyjnych. Oto kilka kwestii, które warto rozważyć, aby zrozumieć, jakie konsekwencje mogą wynikać z używania tego typu aplikacji i jak możesz uniknąć potencjalnych problemów prawnych: 1. Legalność botów i autoclickerów Boty i autoclickery: Z punktu widzenia prawa, używanie botów i autoclickerów (np. za pomocą pyautogui) w grach online jest generalnie nielegalne w kontekście regulaminów gier. Wiele gier (w tym Metin2) ma w swoich regulaminach zapisy zabraniające automatyzacji działań w grze, ponieważ wpływa to na sprawiedliwość rywalizacji oraz narusza zasady uczciwego grania. Przepisy: Nawet jeśli nie rozpowszechniasz swojego bota i używasz go tylko do celów edukacyjnych, może to być traktowane jako naruszenie warunków użytkowania gry, co w praktyce może skutkować blokadą konta. Gry takie jak Metin2 zazwyczaj mają systemy anty-cheatowe, które wykrywają i karają takie zachowania. 2. Cel edukacyjny a legalność Twój projekt w celach edukacyjnych nie zmienia faktu, że boty i automatyzacja procesów w grze mogą naruszać regulamin gier online. Nawet jeśli nie używasz go publicznie, testowanie tego typu aplikacji może być problematyczne z punktu widzenia prawnego. Istnieje jednak duża różnica między używaniem takiego narzędzia w kontekście edukacyjnym (np. nauka programowania) a jego rozpowszechnianiem lub udostępnianiem w internecie, co może przyciągnąć uwagę twórców gry i ich zespołów prawnych. 3. Zmiana nazwy klas i funkcji: Zmiana nazwy klas na bardziej neutralne (np. "findFish" na "findImage" lub "clickIt") może być pomocna w kontekście programu edukacyjnego, ale to nie zmienia jego charakteru. Bot nadal może być rozpoznawany jako narzędzie do automatyzacji działań w grze, co nadal jest niezgodne z regulaminem gry. Zmiana kontekstu: Jeśli zamierzasz używać tego projektu na zajęciach z programowania obiektowego, warto upewnić się, że projekt nie ma nic wspólnego z konkretną grą, która może wprowadzić problemy prawne. Możesz zamiast tego stworzyć podobny projekt, ale niezwiązany z grą, np. automatyzacja kliknięć w prostych aplikacjach komputerowych (np. kliknięcie na obrazy w GUI), które nie naruszają żadnych regulaminów gier. 4. Alternatywne rozwiązanie: Aby uniknąć potencjalnych problemów prawnych, możesz rozważyć modyfikację projektu w taki sposób, aby zamiast automatyzowania działań w grze, służył on do nauki programowania ogólnych technik automatyzacji (np. do automatycznego klikania w aplikacjach do testów GUI, rozpoznawania obrazów itp.), które nie mają żadnego związku z grami online. Możesz także zmienić cel projektu, by nie bazował na grze, ale np. na automatyzacji działań w aplikacjach edukacyjnych, co umożliwi ci skupienie się na programowaniu i algorytmach bez ryzyka naruszenia regulaminów. 5. Jakie kroki możesz podjąć, by nie naruszać prawa: Usunięcie związku z grą: Jeśli twój projekt jest ściśle związany z Metin2, najlepiej zmień jego kontekst. Usuń wszelkie odniesienia do konkretnej gry i zmień cel aplikacji, np. na ogólną automatyzację kliknięć w aplikacjach komputerowych. Zajmowanie się ogólnymi technikami automatyzacji: Skup się na automatyzacji działań w ogólnych aplikacjach, gdzie nie będziesz naruszać regulaminów związanych z grami online. Nie rozpowszechniaj projektu publicznie: Nawet jeśli projekt jest edukacyjny, nie udostępniaj go publicznie w internecie, by uniknąć ryzyka prawnego. Podsumowanie: Choć twój projekt może być interesujący od strony edukacyjnej, związywanie go z grą online, taką jak Metin2, może wiązać się z naruszeniem prawa, niezależnie od tego, czy używasz go tylko na własny użytek. Zmiana nazw klas i dostosowanie projektu do ogólnych aplikacji, które nie naruszają regulaminów gier, może być najlepszym rozwiązaniem, by uniknąć problemów prawnych. Jeśli celem jest edukacja, warto znaleźć sposób na stworzenie narzędzia, które będzie uniwersalne, ale nie będzie miało związku z nielegalną automatyzacją w grach online.

Drugi raz pisze tak 
W Polsce, stosowanie autoclickerów lub innych narzędzi automatyzujących w grze MMO, o ile nie łamie prawa karnego, nie grozi żadną karą z mocy prawa państwowego – to nie jest przestępstwo, tylko naruszenie regulaminu gry. Co to oznacza w praktyce:

✅ CO MOŻESZ ZROBIĆ JAKO TWÓRCA GRY:
Zbanować konto
Najczęstsza i najskuteczniejsza kara – usunięcie lub zablokowanie konta, zgodnie z EULA/regulaminem.

Zresetować postępy, usunąć przedmioty lub zasoby zdobyte nielegalnie
Możesz przewidzieć takie działania w regulaminie jako konsekwencję używania automatyzacji.

Zablokować dostęp do gry na danym urządzeniu/IP (w granicach prawa)
Choć nie zawsze skuteczne (VPN, zmiana urządzenia), jest to dodatkowa bariera.

❌ CZEGO NIE MOŻESZ (lub co raczej nie ma sensu):
Domagać się pieniędzy (np. 500 zł) na drodze sądowej – sąd prawie na pewno to odrzuci, chyba że użytkownik podpisał z Tobą indywidualną umowę (co w grach się nie dzieje).

Zgłaszać na policję – używanie autoclickera nie jest przestępstwem samo w sobie. Co innego np. włamanie na serwer, kradzież konta czy DDoS.

⚖️ Wyjątek: gdy automatyzacja prowadzi do realnej szkody
Jeśli:

ktoś masowo generuje konta-boty,

niszczy ekonomię gry,

wykorzystuje grę do oszustw (np. generowanie zysku, sprzedaż zasobów),

…można rozważyć pozew cywilny o odszkodowanie za realną szkodę (np. spadek reputacji gry, straty finansowe). Ale to wymaga:

dokładnych dowodów,

obliczenia wartości szkody,

identyfikacji sprawcy,

i pieniędzy na prawnika.

W skrócie:
Użycie autoclickera to naruszenie zasad gry, nie przestępstwo. Możesz tylko:

zbanować gracza,

usunąć zdobyte nieuczciwie rzeczy,

i ewentualnie odciąć go od gry.

Chcesz gotowy szablon regulaminu, który Ci to umożliwi? wiec nie wiem czy zmieniac te klasy itd moze zamiast mt2windows samo window czy cos
