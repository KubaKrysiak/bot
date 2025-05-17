from time import sleep, time

import win32gui

from fish_bot import FishBot
from auto_login import AutoLogin
from window_session import WindowSession
from fish_area import FishArea
from keyboard_automation import KeyboardAutomation
from mouse_automation import MouseAutomation
from bot_vision import BotVision
from window_automation import WindowAutomation





class WindowsManager:
    def __init__(self, config, window_title):
        self.config = config
        self.window_title = window_title
        self.width = config.width
        self.height = config.height
        self.screen_width = config.screen_width
        self.screen_height = config.screen_height
        self.windows = []
        self.fish_bots = []
        self.auto_logins = []

    def _enum_windows_callback(self, hwnd, windows):
        if win32gui.GetWindowText(hwnd) == self.window_title:
            windows.append(hwnd)

    def place_all_windows(self):
        setx, sety = 0, 0
        windows = []
        hwnds = []
        win32gui.EnumWindows(self._enum_windows_callback, hwnds)
        print(f"Znalezione okna o tytule {self.window_title}:")
        for hwnd in hwnds:
            if sety + self.height > self.screen_height:
                break
            if setx + self.width > self.screen_width:
                setx = 0
                sety += self.height
                if sety + self.height > self.screen_height:
                    break
            print(f"  HWND: {hwnd}")
            fish_area = FishArea(
                anch_x=setx,
                anch_y=sety,
                cir_left=self.config.circle_region[0],
                cir_top=self.config.circle_region[1],
                cir_right=self.config.circle_region[2],
                cir_bottom=self.config.circle_region[3]
            )
            window_session = WindowSession(
                self.config,
                window_automation=WindowAutomation(hwnd, setx, sety),
                mouse_automation=MouseAutomation(),
                keyboard_automation=KeyboardAutomation(),
                bot_vision=BotVision(),
                fish_area=fish_area
            )
            window_session.place_window(setx, sety)
            windows.append(window_session)
            setx += self.width
        self.windows = windows


    def automatic_login(self):
        auto_logins = [AutoLogin(window) for window in self.windows]
        logging_start = time()
        max_time = 30
        launched_counter = 0
        while time() - logging_start < max_time:
            if launched_counter == len(auto_logins):
                return 0
            for auto_login in auto_logins:
                if auto_login.do_auto_login_action():
                    launched_counter += 1
            sleep(0.1)

    def start_fishing(self, timee):
        fish_bots = [FishBot(window) for window in self.windows]
        start_time = time()
        while time() - start_time < timee:
            for bot in fish_bots:
                bot.do_fishing_action()
            sleep(0.1)

    def close_all_windows(self):
        for window in self.windows:
            try:
                window.close_window()
            except Exception as e:
                print(f"Nie udało się zamknąć okna {window}: {e}")