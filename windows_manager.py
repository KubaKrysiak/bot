from time import sleep, time

import win32gui

from fish_bot import FishBot
from window import Window


class WindowsManager:
    def __init__(self, config, window_title):
        self.config = config
        self.window_title = window_title
        self.windows = self.update_windows()
        self.width = config.width
        self.height = config.height
        self.screen_width = config.screen_width
        self.screen_height = config.screen_height
        self.max_catches = 400

    def _enum_windows_callback(self, hwnd, windows):
        if win32gui.GetWindowText(hwnd) == self.window_title:
            windows.append(hwnd)

    def update_windows(self):
        windows = []
        win32gui.EnumWindows(self._enum_windows_callback, windows)
        windows_objects = []
        print(f"Znalezione okna o tytule {self.window_title}:")
        for hwnd in windows:
            print(f"  HWND: {hwnd}")
            windows_objects.append(Window(hwnd, self.config))
        return windows_objects

    def place_all_windows(self):
        setx, sety = 0, 0
        # Odśwież listę okien przed ustawianiem
        self.windows = self.update_windows()
        for idx, window in enumerate(self.windows):
            if sety + self.height > self.screen_height:
                break
            if setx + self.width > self.screen_width:
                setx = 0
                sety += self.height
                if sety + self.height > self.screen_height:
                    break
            window.restore_window()
            window.place_window(setx, sety, self.width, self.height)
            setx += self.width
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
                sleep(0.5)
                window.click_relative(*self.config.ch[i % 6])
                i += 1
                sleep(0.5)
                window.click_relative(*self.config.ch_ok)
                if window.match_at_position(self.config.select_btn, self.config.stop_id):
                    launched_counter += 1
                    sleep(0.1)
                    window.send_key_input("enter")
                    sleep(0.1)
                    window.send_key_input(" ")
                    window.click_relative(*self.config.select_btn)

    def start_fishing(self, timee):
        fish_bots = []
        for window in self.windows:
            bot = FishBot(window)
            fish_bots.append(bot)
        start_time = time()
        while time() - start_time < timee:
            # 1 focus
            # 2 sleep 0.1
            # 3 take worm
            # 4 sleep 1
            # 5 get focus
            # 6 sleep 0.1
            # 7 cast the fishing rod
            # 8 czekaj az nie bedzie okienka z rybą
            # 9 dopoki okienko z rybką nie zniknie klikaj rybe
            # 10 sleep 2
            bot.get_focus()
            for bot in fish_bots:
                if bot.action == 0:
                    bot.get_focus()
                    sleep(0.1)
                    bot.take_worm()
                    bot.wait(1)
                elif bot.action == 1 and time() - bot.time_counter > bot.time_acc:
                    bot.get_focus()
                    sleep(0.1)
                    bot.cast_the_fishing_rod()
                    bot.wait(1)
                elif bot.action == 2:
                    if not bot.window.find_fish_window():
                        sleep(0.1)
                    else:
                        bot.action = 3
                elif bot.action == 3:
                    if bot.window.find_fish_window():
                        if time() - bot.time_counter > bot.time_acc:
                            pos = bot.find_fish()
                            if pos != None:
                                bot.get_focus()
                                bot.click(pos)
                                gizmo = bot.action
                                bot.wait(1)
                                bot.action = gizmo
                    else:
                        bot.zlowione += 1
                        if bot.zlowione == 400:
                            # na potem
                            return 0
                        bot.wait(2)
                elif bot.action == 4 and time() - bot.time_counter > bot.time_acc:
                    bot.action = 0

    def close_all_windows(self):
        for window in self.windows:
            try:
                window.close_window()
            except Exception as e:
                print(f"Nie udało się zamknąć okna {window}: {e}")

