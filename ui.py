import os
import psutil
import subprocess
from time import sleep

from configurator import Configurator
from windows_manager import WindowsManager


class UI:
    """pewnie mozna cos zrobic z wm zeby tego nie powtarzac i zmieniac konfiguracje tam ale nwm"""
    def display_menu(self):
        print("1. Stwórz konfigurację, resize test (pygame) nie dziala, trzeba ustawic szerokosc na 800")
        print("2. Autologin (tyle postaci ile zmiesci sie na ekranie)")
        print("3. Włącz fishbota (1 postac narazie (brak multithreading / rozszerzenia klas))")
        print("4. Usun konfiguracje (NIE DZIALA) mozna usunac recznie windows chyba nie pozwala:")
        print("5. Uruchom test.py z folderu test")

    def create_configuration(self):
        cfg = Configurator.configure()
        Configurator.save_config(cfg)

    def delete_configuration(self):
        print("Wybierz konfigurację do usunięcia: ")
        directory_path = os.getcwd()
        folders = [f for f in os.listdir(directory_path) if
                   os.path.isdir(os.path.join(directory_path, f)) and f != "default"]
        for folder in folders:
            print(folder)
        print("Wpisz odpowiednią nazwę konfiguracji do usunięcia")
        try:
            cur_conf = input()
            if cur_conf != "default":
                Configurator.delete_config(cur_conf)
            else:
                print("Nie możesz usunąć domyślnej konfiguracji.")
        except:
            print("Nie udało się usunąć konfiguracji.")

    def load_configuration(self):
        print("Nazwy konfiguracji: ")
        directory_path = os.getcwd()
        folders = [f for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))]
        for folder in folders:
            print(folder)
        print("Wpisz odpowiednią nazwę")
        cur_conf = input()
        cfg = Configurator.load_config(cur_conf)
        return cfg

    def auto_login(self, cfg):
        if cfg:
            wm = WindowsManager(cfg)
            wm.place_all_windows()
            wm.automatic_login()

    def launch_fishbots(self, cfg):
        if cfg:
            tim = int(input("Podaj czas lowienia w sekundach: "))
            wm = WindowsManager(cfg)
            wm.place_all_windows()
            wm.start_fishing(tim)

    def run_test_script(self):
        test_script_path = os.path.join(os.getcwd(), "test", "test.py")
        test_dir = os.path.join(os.getcwd(), "test")
        if os.path.exists(test_script_path):
            print(f"Uruchamianie: {test_script_path}")
            subprocess.Popen(["python", "test.py"], cwd=test_dir)
            print("test.py uruchomiony w tle.")
        else:
            print("Nie znaleziono test/test.py")

    def run(self):
        while True:
            self.display_menu()
            option = input()
            if option == "":
                print("wczytano '' jeszcze raz")
                continue
            try:
                option = int(option)
            except ValueError:
                print("Nieprawidłowa opcja.")
                continue

            if option == 1:
                self.create_configuration()
            elif option == 2:
                cfg = self.load_configuration()
                self.auto_login(cfg)
            elif option == 3:
                cfg = self.load_configuration()
                self.launch_fishbots(cfg)
            elif option == 4:
                self.delete_configuration()
            elif option == 5:
                self.run_test_script()


if __name__ == "__main__":
    pid = os.getpid()
    process = psutil.Process(pid)
    process.nice(psutil.HIGH_PRIORITY_CLASS)
    ui = UI()
    ui.run()
