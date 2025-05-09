import win32gui
import win32con
import pyautogui
import numpy as np
import cv2
from time import sleep
from ctypes import windll
import win32api
import os
import mss


class Mt2Window:
    def __init__(self, hwnd, config):
        self.hwnd = hwnd
        self.config = config
        self.mt2_width = config.mt2_width
        self.mt2_height = config.mt2_height
        self.in_game = False
    def get_top_left_coordinates(self):
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        return left, top

    def restore_window(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)

    def get_focus(self):
        try:
            if windll.user32.GetForegroundWindow() == self.hwnd:
                return True
            placement = win32gui.GetWindowPlacement(self.hwnd)
            print("focustime")
            if placement[1] == win32con.SW_SHOWMINIMIZED:
                win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
            windll.user32.ShowWindow(self.hwnd, win32con.SW_SHOW)
            windll.user32.BringWindowToTop(self.hwnd)
            windll.user32.SetWindowPos(self.hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)  # HWND_TOPMOST
            windll.user32.SetWindowPos(self.hwnd, -2, 0, 0, 0, 0, 0x0001 | 0x0002)  # HWND_NOTOPMOST
            windll.user32.SwitchToThisWindow(self.hwnd, True)
            return windll.user32.GetForegroundWindow() == self.hwnd

        except Exception as e:
            print(f"Błąd podczas ustawiania focusu: {e}")
            return False

    def click_relative(self, x, y):
        anch_x, anch_y = self.get_top_left_coordinates()
        self.get_focus()
        click_x = anch_x + x
        click_y = anch_y + y
        print(f"Kliknięcie w: ({click_x}, {click_y})")
        sleep(0.1)
        win32api.SetCursorPos((click_x, click_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        sleep(0.05)
        pyautogui.doubleClick(click_x, click_y)

    def click_relative_fast(self, x, y):
        self.get_focus()
        anch_x, anch_y = self.get_top_left_coordinates()
        click_x = anch_x + x
        click_y = anch_y + y
        win32api.SetCursorPos((click_x, click_y))
        sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def send_key_input(self, key):
        self.get_focus()
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
            '0': (0x30, 0x0B),
            'enter': 0x0D
        }

        value = special_keys.get(key, None)
        if value is None:
            raise ValueError(f"Nieobsługiwany klawisz: {key}")

        if isinstance(value, tuple):
            vk_code, scan_code = value
        else:
            vk_code = value
            scan_code = None
        sleep(0.1)
        win32api.keybd_event(vk_code, scan_code if scan_code is not None else 0, 0, 0)
        sleep(0.1)
        win32api.keybd_event(vk_code, scan_code if scan_code is not None else 0, win32con.KEYEVENTF_KEYUP, 0)
        sleep(0.2)

    def match_at_position(self, center, template_path, confidence=0.85):  # można ustawić niższy próg
        print(f"[INFO] Template path: {template_path}")
        template = cv2.imread(template_path)
        if template is None:
            print("[ERROR] Failed to load template.")
            return False
        h, w = template.shape[:2]
        anch_x, anch_y = self.get_top_left_coordinates()
        x_center, y_center = center
        x_center += anch_x
        y_center += anch_y
        x1 = int(x_center - w / 2)
        y1 = int(y_center - h / 2)
        screenshot = pyautogui.screenshot(region=(x1, y1, w, h))
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCORR_NORMED)
        max_val = cv2.minMaxLoc(result)[1]
        print(f"[DEBUG] Max match value: {max_val:.4f}")
        debug_path = os.path.join(os.path.dirname(template_path), "debug_image.png")
        cv2.imwrite(debug_path, screenshot)
        print(f"[INFO] Debug image saved to {debug_path}")

        return max_val >= confidence

    def place_mt2window(self, x, y, width, height):
        win32gui.SetWindowPos(
            self.hwnd,
            win32con.HWND_TOPMOST,
            x, y, width, height,
            win32con.SWP_NOACTIVATE
        )

    def find_fish(self):
        anch_x, anch_y = self.get_top_left_coordinates()
        left, top, right, bottom = self.config.circle_region
        center_x = anch_x + (left[0] + right[0]) // 2
        center_y = anch_y + (top[1] + bottom[1]) // 2
        radius = abs((right[0] - left[0]) // 2)
        x, y = center_x - radius, center_y - radius
        scan_size = radius * 2
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": scan_size, "height": scan_size}
            screenshot = sct.grab(monitor)
            image_np = np.array(screenshot)
        hsv = cv2.cvtColor(image_np, cv2.COLOR_BGRA2BGR)
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
        target_color_bgr = np.uint8([[[123, 88, 53]]])
        target_hsv = cv2.cvtColor(target_color_bgr, cv2.COLOR_BGR2HSV)[0][0]
        h, s, v = target_hsv
        delta_h, delta_s, delta_v = 20, 20, 20
        lower_bound = np.array([max(h - delta_h, 0), max(s - delta_s, 0), max(v - delta_v, 0)])
        upper_bound = np.array([min(h + delta_h, 179), min(s + delta_s, 255), min(v + delta_v, 255)])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        circle_mask = np.zeros(mask.shape, dtype=np.uint8)
        cv2.circle(circle_mask, (radius, radius), radius, 255, -1)
        masked_color = cv2.bitwise_and(mask, mask, mask=circle_mask)
        ys, xs = np.where(masked_color > 0)

        if xs.size == 0:
            return None
        mean_x = int(xs.mean())
        mean_y = int(ys.mean())
        screen_x = x + mean_x
        screen_y = y + mean_y
        fish_coords = (screen_x - anch_x, screen_y - anch_y)
        return fish_coords

    def find_fish_window(self):
        """Checks if a specified color exists in the region defined in find_fish."""
        anch_x, anch_y = self.get_top_left_coordinates()
        left, top, right, bottom = self.config.circle_region
        center_x = anch_x + (left[0] + right[0]) // 2
        center_y = anch_y + (top[1] + bottom[1]) // 2
        radius = abs((right[0] - left[0]) // 2)
        x, y = center_x - radius, center_y - radius
        scan_size = radius * 2
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": scan_size, "height": scan_size}
            screenshot = sct.grab(monitor)
            image_np = np.array(screenshot)
        hsv = cv2.cvtColor(image_np, cv2.COLOR_BGRA2BGR)
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
        target_color_bgr = np.uint8([[[216, 145, 49]]])  # Color #3191D8 in BGR
        target_hsv = cv2.cvtColor(target_color_bgr, cv2.COLOR_BGR2HSV)[0][0]
        h, s, v = target_hsv
        delta_h, delta_s, delta_v = 3, 3, 3
        lower_bound = np.array([max(h - delta_h, 0), max(s - delta_s, 0), max(v - delta_v, 0)])
        upper_bound = np.array([min(h + delta_h, 179), min(s + delta_s, 255), min(v + delta_v, 255)])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        return np.any(mask > 0)