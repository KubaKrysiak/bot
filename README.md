Do zrobienia:
Wojtek - przy 4 okienkach na raz są duże opoznienia przy lowieniu


Autorzy:

- Jakub Krysiak
- Wojtek Cieślik


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

pip install -r requirements.txt
uruchom jako administrator run_admin.bat
lub
uruchom cmd jako administrator cd sciezka python gui.py

3. 
Instrukcja konfiguracji:

![Screenshot 2025-05-14 020507](https://github.com/user-attachments/assets/3f4dffe4-49b4-4111-b505-6571ae709243)
