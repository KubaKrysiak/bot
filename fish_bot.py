import threading
import win32con
import win32api
from time import sleep
class FishBot:
    def __init__(self, mt2_window):
        self.mt2_window = mt2_window
        self.worms_count = 0
        self.keyboard_lock = threading.Lock()

    def send_key_input(self, key):
        self.mt2_window.send_key_input(key)

    def take_worm(self):
        self.mt2_window.get_focus()
        sleep(0.25)
        self.worms_count += 1

        key_to_press = str((self.worms_count // 50) + 1)

        if int(key_to_press) > 9:
            print("Stop: Przekroczono limit przynęt!")
            return "stop"

        self.send_key_input(key_to_press)

    def cast_the_fishing_rod(self):
        print("Rzucam wędkę...")
        self.send_key_input(' ')

    def find_fish(self):
        return self.mt2_window.find_fish()

    def click(self, pos):
        self.mt2_window.click_relative_fast(*pos)
