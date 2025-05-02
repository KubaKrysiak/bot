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
        with self.keyboard_lock:
            try:
                # Mapowanie klawiszy z uwzględnieniem skanów
                special_keys = {
                    ' ': (win32con.VK_SPACE, 0x39),
                    '1': (0x31, 0x02),
                    '2': (0x32, 0x03),
                    '3': (0x33, 0x04),
                    '4': (0x34, 0x05),
                    '5': (0x35, 0x06),
                    '6': (0x36, 0x07),
                    '7': (0x37, 0x08),
                    '8': (0x38, 0x09),
                    '9': (0x39, 0x0A),
                    '0': (0x30, 0x0B)
                }
                vk_code, scan_code = special_keys.get(key, (None, None))
                if vk_code is None:
                    raise ValueError(f"Nieobsługiwany klawisz: {key}")

                # Symulacja pełnego naciśnięcia klawisza
                win32api.keybd_event(vk_code, scan_code, 0, 0)
                sleep(0.1)
                win32api.keybd_event(vk_code, scan_code, win32con.KEYEVENTF_KEYUP, 0)
                sleep(0.2)

            except Exception as e:
                print(f"Błąd wysyłania klawisza {key}: {str(e)}")

    def take_worm(self):
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
        self.mt2_window.click_relative(*pos)
