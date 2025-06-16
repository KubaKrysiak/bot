Autorzy:

- Jakub Krysiak
- Wojtek Cieślik

Notka prawna:

Program jest uruchamiany w środowisku testowym dołączonym do bota, dlatego nie łamie żadnych aktów prawnych
.
Cel:

Celem projektu jest stworzenie programu do automatyzowania aplikacji okienkowych poprzez rozpoznawanie wzorów/kolorów i symulacji kliknięć klawiatury, myszy oraz innych operacji winapi.
Zadaniem nie było stworzenie użytecznego narzędzia do użytku zewnętrznego, lecz nauka oraz praktyczne zastosowanie zagadnień związanych z automatyzacją interfejsów graficznych.
Projekt został zrealizowany w kontrolowanym środowisku testowym, przy użyciu prostego prototypu gry stworzonego na potrzeby demonstracji.
Projekt nie jest powiązany z żadną grą komercyjną i nie będzie udostępniany ani wykorzystywany poza kontekstem edukacyjnym oraz może być
w łatwy sposób rozszerzony do uniwersalnego programu automatyzującego dzięki skalowalnej architekturze aplikacji i programowaniu obiektowym gdyż narazie autologin jest przystosowany
do jednego typu systemu logowania i 1 minigry.
Przykładowe funkcje programu:
- Odczyt/zapis konfiguracji stworzonych przez użytkownika
- Konfigurator
- Template matching służacy do wykrywania charakterystycznych elementów logowania
- Obsługa wielu okienek na raz i ich obsługa ( odpowiedni focus, minimalizowanie, rozmieszczenie, resize, oddawanie klikniec, symulacja klawiatury )
- Automatyzacja mini-gry przy użyciu wykrywania koloru
- Prototyp gry

Środowisko deweloperskie (na czym był przetestowany):
- windows 11
- Python 3.13.3
biblioteki:
-opencv-python
-pyautogui
-pynput
-mss
-psutil
-pygetwindow
-pywin32
-pygame
-keyboard
-customtkinter

Uruchomienie:

-pip install -r requirements.txt

-uruchom jako administrator run_admin.bat

-lub uruchom cmd jako administrator cd sciezka python gui.py

Test:

- Zeby program dzialal trzeba wybrac odpowiednia konfiguracje, tytul okna, mozna jeszcze stworzyc wlasna konfiguracje, tworzy sie je po to, zeby program byl dostosowany do dowolnego interfejsu, mozna wybrac rozmiar okna, to sie wtedy wiecej okien zmiesci na ekranie. Sa domyslne konfiguracje zaczynajace sie od T900, t600, nazwa okna musi byc ustalona na tytul testu. W konfiguratorze trzeba wiedziec co klikac, sa zalaczone nizej odpowiednie punkty

![image](https://github.com/user-attachments/assets/7c8c9019-c471-4fe2-97e9-4d31ae3ec84d)

3. 
Instrukcja konfiguracji:

![Screenshot 2025-05-14 020507](https://github.com/user-attachments/assets/3f4dffe4-49b4-4111-b505-6571ae709243)
