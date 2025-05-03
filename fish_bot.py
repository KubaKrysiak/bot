import threading
import win32con
import win32api
from time import sleep
class FishBot:
    def __init__(self, mt2_window):
        self.mt2_window = mt2_window
        self.worms_count = 400
        self.keyboard_lock = threading.Lock()

    def send_key_input(self, key):
        self.mt2_window.send_key_input(key)

    def take_worm(self):
        self.mt2_window.get_focus()
        sleep(0.25)
        if self.worms_count > 0:
            print("Biorę przynętę...")
            self.send_key_input("1")
            self.worms_count -= 1
        else:
            print("Brak przynęty!")

    def cast_the_fishing_rod(self):
        print("Rzucam wędkę...")
        self.send_key_input(' ')

    def find_fish(self):
        return self.mt2_window.find_fish()

    def click(self, pos):
        self.mt2_window.click_relative_fast(*pos)
