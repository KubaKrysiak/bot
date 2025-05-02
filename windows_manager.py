import win32gui
import threading
from mt2_window import Mt2Window
from fish_bot import FishBot
from time import sleep, time

class WindowsManager:
    def __init__(self, config):
        self.config = config
        self.windows = self.update_METIN2_windows()
        self.mt2_width = config.mt2_width
        self.mt2_height = config.mt2_height
        self.screen_width = config.screen_width
        self.screen_height = config.screen_height

    @staticmethod
    def _enum_windows_callback(hwnd, windows):
        if win32gui.GetWindowText(hwnd) == "METIN2":
            windows.append(hwnd)

    def update_METIN2_windows(self):
        windows = []
        win32gui.EnumWindows(self._enum_windows_callback, windows)
        windows_objects = []
        print("Znalezione okna o tytule METIN2:")
        for hwnd in windows:
            print(f"  HWND: {hwnd}")
            windows_objects.append(Mt2Window(hwnd, self.config))
        return windows_objects

    def place_all_windows(self):
        setx, sety = 0, 0
        for window in self.windows:
            window.restore_window()
            window.place_mt2window(setx, sety, self.mt2_width, self.mt2_height)
            if setx + self.mt2_width > self.screen_width:
                setx = 0
                sety += self.mt2_height
                if sety > self.screen_height:
                    print("Za dużo okien – usuń kilka.")
                    break
            else:
                setx += self.mt2_width
        sleep(3)

    def automatic_login(self):
        logging_start = time()
        max_time = 30
        launched_counter = 0
        while time() - logging_start < max_time:
            # proste zeby dlugo nie robic

            if launched_counter == len(self.windows):
                return 0

            i = 0
            for window in self.windows:
                sleep(0.15)
                window.click_relative(*self.config.ch[i % 6])
                i += 1
                sleep(0.15)
                window.click_relative(*self.config.ch_ok)
                sleep(0.15)
                window.click_relative(*self.config.select_btn)
                if not window.in_game and window.match_at_position(self.config.select_btn, self.config.stop_id):
                    launched_counter += 1

    def start_fishing(self):
        fish_bots = []

        def bot_task(bot):
            start_time = time()
            while time() - start_time < 600:
                for i in range(3):
                    bot.take_worm()
                    sleep(1)
                    bot.cast_the_fishing_rod()
                    sleep(5)
                    while not bot.find_fish():
                        sleep(0.5)
                    pos = bot.find_fish()
                    print(pos)
                    if pos:
                        bot.click(pos)

        threads = []
        for window in self.windows:
            bot = FishBot(window)
            fish_bots.append(bot)
            thread = threading.Thread(target=bot_task, args=(bot,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()