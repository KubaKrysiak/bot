import json
import os
from time import sleep, time
import keyboard
import pyautogui
import win32api
import win32con
import win32gui
from pyautogui import click, moveTo
from pynput import mouse
import numpy as np
import cv2


class Screen:
    def __init__(self):
        self.screenWidth = self.get_screen_x()
        self.screenHeight = self.get_screen_y()

    def get_screen_x(self):
        return win32api.GetSystemMetrics(0)

    def get_screen_y(self):
        return win32api.GetSystemMetrics(1)


class Configurator:
    @staticmethod
    def configure():
        name = input("Podaj nazwę konfiguracji: ")
        mt2Width = int(input("Podaj docelową szerokość okna MT2: "))
        mt2Height = int(mt2Width * 0.75)

        ch = []
        for j in range(6):
            x, y = Configurator.get_click_coordinates(f"Kliknij ch {j + 1}")
            ch.append((x, y))
        ok_ch = Configurator.get_click_coordinates("Kliknij zatwierdzenie ch przycisk (ok)")
        left, top = Configurator.get_click_coordinates("Kliknij szybko lewy gorny rog wyboru postaci")
        right, bottom = Configurator.get_click_coordinates("Kliknij szybko prawy dolny rog wyboru postaci")
        width = right - left
        height = bottom - top
        stop_id = pyautogui.screenshot(region=(left, top, width, height))
        os.makedirs(name, exist_ok=True)
        path = os.path.join(name, f"stop_id.png")
        stop_id.save(path)
        stop_id = path
        select_btn = (left + width//2, top + height//2)
        config = Config(
            mt2Width, mt2Height,
            ch, ok_ch, select_btn, name, stop_id
        )
        Configurator.save_config(config)

    @staticmethod
    def save_config(config):
        data = {
            "mt2Width": config.mt2Width,
            "mt2Height": config.mt2Height,
            "ch": config.ch,
            "ok_ch": config.ok_ch,
            "select_btn": config.select_btn,
            "name": config.name,
            "stop_id": config.stop_id
        }
        os.makedirs(config.name, exist_ok=True)
        path = os.path.join(config.name, "config.json")
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Zapisano konfigurację do {path}")

    @staticmethod
    def load_config(name):
        path = os.path.join(name, "config.json")
        with open(path, "r") as f:
            data = json.load(f)
        print(f"Wczytano konfigurację z {path}")
        return Config(
            data["mt2Width"],
            data["mt2Height"],
            data["ch"],
            tuple(data["ok_ch"]),
            tuple(data["select_btn"]),
            data["name"],
            data["stop_id"]
        )

    @staticmethod
    def get_click_coordinates(prompt):
        print(prompt)
        coords = []

        def on_click(x, y, button, pressed):
            if pressed and keyboard.is_pressed('s'):
                coords.append((x, y))
                return False

        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
        return coords[0]


class Config:
    def __init__(self, mt2Width, mt2Height, ch, ok_ch, select_btn, name, stop_id):
        self.screen = Screen()
        self.mt2Width = mt2Width
        self.mt2Height = mt2Height
        self.screenWidth = self.screen.screenWidth
        self.screenHeight = self.screen.screenHeight
        self.ch = ch
        self.ok_ch = ok_ch
        self.select_btn = select_btn
        self.name = name
        self.stop_id = stop_id


class WindowsManager:
    def __init__(self, config):
        self.config = config
        self.windows = self.update_METIN2_windows()
        self.mt2Width = config.mt2Width
        self.mt2Height = config.mt2Height
        self.screenWidth = config.screenWidth
        self.screenHeight = config.screenHeight

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
            window.place_mt2window(setx, sety, self.mt2Width, self.mt2Height)
            if setx + self.mt2Width > self.screenWidth:
                setx = 0
                sety += self.mt2Height
                if sety > self.screenHeight:
                    print("Za dużo okien – usuń kilka.")
                    break
            else:
                setx += self.mt2Width
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
                window.click_relative(*self.config.ok_ch)
                sleep(0.15)
                window.click_relative(*self.config.select_btn)
                if not window.launched and window.match_at_position(self.config.select_btn, self.config.stop_id):
                    launched_counter += 1


class Mt2Window:
    def __init__(self, hwnd, config):
        self.hwnd = hwnd
        self.config = config
        self.mt2Width = config.mt2Width
        self.mt2Height = config.mt2Height
        self.inGame = False
        self.launched = False

    def get_top_left_coordinates(self):
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        return left, top

    def restore_window(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)

    def get_focus(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(self.hwnd)

    def click_relative(self, x, y):
        anch_x, anch_y = self.get_top_left_coordinates()
        self.get_focus()
        sleep(0.1)
        moveTo(anch_x + x, anch_y + y)
        click()

    def match_at_position(self, center, template_path, confidence=0.95):
        template = cv2.imread(template_path)
        h, w = template.shape[:2]

        x_center, y_center = center
        x1 = int(x_center - w / 2)
        y1 = int(y_center - h / 2)

        screenshot = pyautogui.screenshot(region=(x1, y1, w, h))
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        max_val = cv2.minMaxLoc(result)[1]

        return max_val >= confidence
    def place_mt2window(self, x, y, width, height):
        win32gui.SetWindowPos(
            self.hwnd,
            win32con.HWND_TOPMOST,
            x, y, width, height,
            win32con.SWP_NOACTIVATE
        )

if __name__ == "__main__":
    while True:
        print("1. stworz konfiguracje")
        print("2. wlacz bota (boty maja byc w wyborze ch): ")
        option = int(input())
        if option == 1:
            Configurator.configure()
        if option == 2:
            print("nazwy konfiguracji: ")
            directory_path = os.getcwd()
            folders = [f for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))]
            for folder in folders:
                print(folder)
            print("Wpisz odpowiednia nazwe")
            try:
                cur_conf = input()
                cfg = Configurator.load_config(cur_conf)
            except:
                print("Nie ma takiej nazwy")
                continue
            wm = WindowsManager(cfg)
            wm.place_all_windows()
            wm.automatic_login()