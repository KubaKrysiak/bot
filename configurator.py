import json
import os
import shutil

import keyboard
import pyautogui
import win32con
import win32gui
from pynput import mouse

from config import Config


class ConfigBuilder:
    def __init__(self):
        self._width = None
        self._height = None
        self._ch = None
        self._ch_ok = None
        self._select_btn = None
        self._name = None
        self._stop_id = None
        self._circle_region = None

    def set_name(self, name):
        self._name = name
        return self

    def set_width(self, width):
        self._width = width
        self._height = int(width * 0.75)
        return self

    def set_ch(self, ch):
        self._ch = ch
        return self

    def set_ch_ok(self, ch_ok):
        self._ch_ok = ch_ok
        return self

    def set_select_btn(self, select_btn):
        self._select_btn = select_btn
        return self

    def set_stop_id(self, stop_id):
        self._stop_id = stop_id
        return self

    def set_circle_region(self, circle_region):
        self._circle_region = circle_region
        return self

    def build(self):
        return Config(
            self._width, self._height,
            self._ch, self._ch_ok, self._select_btn,
            self._name, self._stop_id, self._circle_region
        )


class Configurator:
    @staticmethod
    def configure():
        name = input("Podaj nazwę konfiguracji: ")
        width = int(input("Podaj docelową szerokość okna : "))
        window_title = input("Podaj tytuł okna gry obecnie konfigurowanego: ")
        height = int(width * 0.75)

        def enum_handler(hwnd, _):
            title = win32gui.GetWindowText(hwnd)
            if window_title in title:
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    win32gui.MoveWindow(hwnd, 0, 0, width, height, True)
                    win32gui.SetForegroundWindow(hwnd)
                except Exception:
                    pass

        win32gui.EnumWindows(enum_handler, None)
        print("Wciskaj myszką i 's'")
        ch = []
        for j in range(6):
            x, y = Configurator.get_click_coordinates(f"Kliknij ch {j + 1}")
            ch.append((x, y))
        ch_ok = Configurator.get_click_coordinates("Kliknij zatwierdzenie ch przycisk (ok)")
        left, top = Configurator.get_click_coordinates(
            "wybor identyfikatora stopu loginu w wyborze postaci kliknij lewy gorny rog id")
        right, bottom = Configurator.get_click_coordinates(
            "wybor identyfikatora stopu loginu w wyborze postaci kliknij prawy dolny rog id")
        button_width = right - left
        button_height = bottom - top
        stop_id = pyautogui.screenshot(region=(left, top, button_width, button_height))
        os.makedirs(name, exist_ok=True)
        path = os.path.join(name, f"stop_id.png")
        stop_id.save(path)
        stop_id = path
        select_btn = (left + button_width // 2, top + button_height // 2)
        print("Konfiguracja fish bota kliknij 4x wewnatrz kola lewa gorna prawa i dolna granice")
        lcircle = Configurator.get_click_coordinates("Kliknij lewo")
        ucircle = Configurator.get_click_coordinates("Kliknij gora")
        rcircle = Configurator.get_click_coordinates("Kliknij prawo")
        dcircle = Configurator.get_click_coordinates("Kliknij dol")
        circle_region = (lcircle, ucircle, rcircle, dcircle)

        # Użycie buildera
        config = (
            ConfigBuilder()
            .set_name(name)
            .set_width(width)
            .set_ch(ch)
            .set_ch_ok(ch_ok)
            .set_select_btn(select_btn)
            .set_stop_id(stop_id)
            .set_circle_region(circle_region)
            .build()
        )
        ConfigSerializer.save(config)
        return config

    @staticmethod
    def load_config(name):
        return ConfigSerializer.load(name)

    @staticmethod
    def delete_config(name):
        ConfigSerializer.delete(name)

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


class ConfigSerializer:
    @staticmethod
    def save(config):
        data = config.to_dict()
        os.makedirs(config.name, exist_ok=True)
        path = os.path.join(config.name, "config.json")
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Zapisano konfigurację do {path}")

    @staticmethod
    def load(name):
        path = os.path.join(name, "config.json")
        with open(path, "r") as f:
            data = json.load(f)
        print(f"Wczytano konfigurację z {path}")
        return Config.from_dict(data)

    @staticmethod
    def delete(name):
        path = os.path.join(name)
        shutil.rmtree(path)
