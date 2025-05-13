import threading
import win32con
import win32api
from time import sleep
import time


class FishBot:
    """Klasa automatu wykonującego sekwencję akcji w oknie aplikacji"""
    def __init__(self, mt2_window):
        self.mt2_window = mt2_window
        self.worms_count = 0
        self.keyboard_lock = threading.Lock()
        self.fishing_action = None
        self.zlowione = 0
        self.time_acc = 0
        self.time_counter = 0
        self.action = 0 

    def send_key_input(self, key):
        """Wysyła polecenie klawiatury do okna"""
        print(f">>> Wysyłanie polecenia klawiatury: {key}")
        self.mt2_window.send_key_input(key)

    def take_worm(self):
        sleep(0.25)
        self.worms_count += 1

        # Wybierz slot na podstawie liczby użytych przedmiotów (co 50 użyć zmiana slotu)
        key_to_press = str((self.worms_count // 50) + 1)
        print(f">>> Używam przedmiot ze slotu {key_to_press}, łącznie użyto: {self.worms_count}")

        if int(key_to_press) > 9:
            print("!!! Wykorzystano wszystkie dostępne przedmioty (sloty 1-9)")
            return "stop"

        self.send_key_input(key_to_press)
        return "continue"

    def cast_the_fishing_rod(self):
        """Rozpoczyna główną akcję (rzucenie wędki)"""
        print(">>> Wykonuję główną akcję (spacja)")
        self.send_key_input(' ')

    def find_fish(self):
        """Wykrywa obiekt interakcji w oknie (dla kompatybilności wstecznej)"""
        return self.find_target()

    def find_target(self):
        """Wykrywa obiekt interakcji w oknie"""
        print(">>> Wyszukiwanie obiektu interakcji...")
        result = self.mt2_window.find_color_in_region()
        if result:
            print(f">>> Znaleziono obiekt na pozycji: {result}")
        else:
            print(">>> Nie wykryto obiektu interakcji")
        return result

    def click(self, pos):
        """Wykonuje szybkie kliknięcie w podanej pozycji"""
        print(f">>> Kliknięcie w pozycji: {pos}")
        self.mt2_window.click_relative_fast(*pos)

    def find_fish_window(self):
        return self.mt2_window.find_fish_window()
    
    def get_focus(self):
        self.mt2_window.get_focus()

    def wait(self, timee):
        self.time_counter = time.time()
        self.time_acc  = timee
        self.action += 1
    
