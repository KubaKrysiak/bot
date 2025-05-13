import os
import psutil
import subprocess
import threading
from time import sleep

from configurator import Configurator
from windows_manager import WindowsManager


class UI:
    """Klasa interfejsu użytkownika do obsługi programu automatyzującego"""
    def display_menu(self):
        print("===== AUTOMATYZACJA AKCJI W APLIKACJACH OKIENKOWYCH =====")
        print("1. Stwórz konfigurację (ustaw szerokość okna na 800)")
        print("2. Autologowanie (obsługuje wiele okien)")
        print("3. Włącz automatyzację klikania (jedna aplikacja)")
        print("4. Uruchom środowisko testowe")
        print("5. Informacje o programie")
        print("6. Wyjście z programu")
        print("========================================================")

    def create_configuration(self):
        print(">>> Rozpoczynam proces tworzenia nowej konfiguracji...")
        cfg = Configurator.configure()
        Configurator.save_config(cfg)
        print(">>> Konfiguracja została pomyślnie utworzona!")

    def load_configuration(self):
        print(">>> Dostępne konfiguracje: ")
        directory_path = os.getcwd()
        folders = [f for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))]
        for folder in folders:
            print(f"  - {folder}")
        print(">>> Podaj nazwę konfiguracji do wczytania:")
        cur_conf = input(">>> ")
        path = os.path.join(cur_conf, "config.json")
        if not os.path.exists(path):
            print("!!! Błąd: Podana konfiguracja nie istnieje!")
            return None
        cfg = Configurator.load_config(cur_conf)
        return cfg

    def auto_login(self, cfg):
        if cfg:
            print(">>> Rozpoczynam proces autologowania...")
            wm = WindowsManager(cfg)
            print(">>> Ustawiam pozycje i rozmiary okien...")
            wm.place_all_windows()
            print(">>> Wykonuję procedurę logowania automatycznego...")
            wm.automatic_login()
            print(">>> Zakończono proces autologowania!")

    def launch_automation(self, cfg):
        if cfg:
            try:
                tim = int(input(">>> Podaj czas działania automatyzacji w sekundach: "))
                print(f">>> Rozpoczynam proces automatyzacji na {tim} sekund...")
                wm = WindowsManager(cfg)
                print(">>> Ustawiam pozycje i rozmiary okien...")
                wm.place_all_windows()
                print(">>> Uruchamiam automatyzację...")
                wm.start_fishing(tim)
                print(">>> Zakończono proces automatyzacji!")
            except ValueError:
                print("!!! Błąd: Wprowadzona wartość musi być liczbą całkowitą!")

    def run_test_script(self):
        test_script_path = os.path.join(os.getcwd(), "test", "test.py")
        test_dir = os.path.join(os.getcwd(), "test")
        if os.path.exists(test_script_path):
            print(f"Uruchamianie: {test_script_path}")
            def reader():
                proc = subprocess.Popen(
                    ["python", "test.py"],
                    cwd=test_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                for line in proc.stdout:
                    print("[test.py]", line, end="")
            threading.Thread(target=reader, daemon=True).start()
            print("test.py uruchomiony w tle.")
        else:
            print("!!! Błąd: Nie znaleziono pliku test/test.py")

    def show_info(self):
        print("\n===== INFORMACJE O PROGRAMIE =====")
        print("Program do automatyzacji akcji w aplikacjach okienkowych")
        print("Stworzony w celach edukacyjnych jako projekt z programowania obiektowego")
        print("Wykorzystuje: OpenCV, Win32API, PyAutoGUI")
        print("Funkcje: wykrywanie kolorów, automatyzacja kliknięć, obsługa wielu okien")
        print("================================\n")

    def run(self):
        print("\n=== Program do automatyzacji aplikacji okienkowych ===\n")
        
        while True:
            self.display_menu()
            option = input(">>> Wybierz opcję: ")
            
            if option == "":
                print("!!! Błąd: Nie wprowadzono żadnej opcji.")
                continue
                
            try:
                option = int(option)
            except ValueError:
                print("!!! Błąd: Opcja musi być liczbą.")
                continue

            if option == 1:
                self.create_configuration()
            elif option == 2:
                cfg = self.load_configuration()
                self.auto_login(cfg)
            elif option == 3:
                cfg = self.load_configuration()
                self.launch_automation(cfg)
            elif option == 4:
                self.run_test_script()
            elif option == 5:
                self.show_info()
            elif option == 6:
                print(">>> Dziękuję za skorzystanie z programu. Do widzenia!")
                break
            else:
                print("!!! Błąd: Nieprawidłowa opcja. Wybierz wartość od 1 do 6.")


if __name__ == "__main__":
    pid = os.getpid()
    process = psutil.Process(pid)
    process.nice(psutil.HIGH_PRIORITY_CLASS)
    ui = UI()
    ui.run()