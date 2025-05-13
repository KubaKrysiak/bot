import threading
import win32con
import win32api
from time import sleep
import time
class FishBot:
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
        self.mt2_window.send_key_input(key)

    def take_worm(self):
        sleep(0.25)
        self.worms_count += 1

        key_to_press = str((self.worms_count // 50) + 1)

        if int(key_to_press) > 9:
            return "stop"

        self.send_key_input(key_to_press)

    def cast_the_fishing_rod(self):
        self.send_key_input(' ')

    def find_fish(self):
        return self.mt2_window.find_fish()

    def click(self, pos):
        self.mt2_window.click_relative_fast(*pos)

    def find_fish_window(self):
        return self.mt2_window.find_fish_window()
    
    def get_focus(self):
        self.mt2_window.get_focus()

    def wait(self, timee):
        self.time_counter = time.time()
        self.time_acc  = timee
        self.action += 1
    