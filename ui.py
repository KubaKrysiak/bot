import os
from time import sleep

from configurator import Configurator
from windows_manager import WindowsManager


class UI:
    """pewnie mozna cos zrobic z wm zeby tego nie powtarzac i zmieniac konfiguracje tam ale nwm"""
    def display_menu(self):
        print("1. Stwórz konfigurację")
        print("2. Włącz bota i autologin (boty mają być w wyborze ch) ")
        print("3. Włącz fishbota postac ma miec w slotach na dole przynete wedke w reku i stac nad jeziorem")
        print("4. Usun konfiguracje: ")

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
        try:
            cur_conf = input()
            cfg = Configurator.load_config(cur_conf)
            return cfg
        except:
            print("Nie ma takiej nazwy")
            return None

    def auto_login(self):
        cfg = self.load_configuration()
        if cfg:
            wm = WindowsManager(cfg)
            wm.place_all_windows()
            wm.automatic_login()

    def launch_fishbots(self):
        cfg = self.load_configuration()
        if cfg:
            wm = WindowsManager(cfg)
            wm.place_all_windows()
            wm.start_fishing()

    def run(self):
        while True:
            self.display_menu()
            option = int(input())
            if option == 1:
                self.create_configuration()
            elif option == 2:
                self.auto_login()
                sleep(12)
                self.launch_fishbots()
            elif option == 3:
                self.launch_fishbots()
            elif option == 4:
                self.delete_configuration()


# __main__ blok
if __name__ == "__main__":
    ui = UI()
    ui.run()
