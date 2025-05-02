import win32gui
import win32con
import pyautogui
import numpy as np
import cv2
from time import sleep
from PIL import ImageGrab
from ctypes import windll, Structure, c_ushort, c_ulong, c_long, POINTER, sizeof
import win32api

class KEYBDINPUT(Structure):
    _fields_ = [("wVk", c_ushort),
                ("wScan", c_ushort),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", POINTER(c_ulong))]

class INPUT(Structure):
    _fields_ = [("type", c_ulong),
                ("ki", KEYBDINPUT)]

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
        win32api.SetCursorPos((click_x, click_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def send_key_input(self, key):
        sleep(0.2)
        self.get_focus()
        print(f"Wysyłanie klawisza: {key}")

        key_map = {
            '1': 0x31,
            '2': 0x32,
            '3': 0x33,
            '4': 0x34,
            '5': 0x35,
            '6': 0x36,
            '7': 0x37,
            '8': 0x38,
            ' ': 0x20
        }

        vk_code = key_map.get(key.lower())
        if vk_code is None:
            print(f"Nieobsługiwany klawisz: {key}")
            return
        input_structure = INPUT()
        input_structure.type = 1
        input_structure.ki = KEYBDINPUT(wVk=vk_code, wScan=0, dwFlags=0, time=0, dwExtraInfo=None)
        windll.user32.SendInput(1, POINTER(INPUT)(input_structure), sizeof(INPUT))
        input_structure.ki.dwFlags = 2  # KEYEVENTF_KEYUP
        windll.user32.SendInput(1, POINTER(INPUT)(input_structure), sizeof(INPUT))

    def match_at_position(self, center, template_path, confidence=0.95):
        template = cv2.imread(template_path)
        h, w = template.shape[:2]
        anch_x, anch_y = self.get_top_left_coordinates()
        x_center, y_center = center
        x_center += anch_x
        y_center += anch_y
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

    def find_fish(self):
        anch_x, anch_y = self.get_top_left_coordinates()
        left, top, right, bottom = self.config.circle_region
        left = (left[0] + anch_x, left[1] + anch_y)
        top = (top[0] + anch_x, top[1] + anch_y)
        right = (right[0] + anch_x, right[1] + anch_y)
        bottom = (bottom[0] + anch_x, bottom[1] + anch_y)
        center_x = (left[0] + right[0]) // 2
        center_y = (top[1] + bottom[1]) // 2
        radius = abs(center_x - left[0])
        x = center_x - radius
        y = center_y - radius
        width = height = radius * 2

        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        image_np = np.array(screenshot)
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Convert to HSV
        hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

        # Get center color (approx. background color)
        center_color = hsv[radius, radius]

        # Compute color difference mask
        diff = cv2.absdiff(hsv, center_color)
        mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Threshold the difference
        _, thresh = cv2.threshold(mask, 30, 255, cv2.THRESH_BINARY)

        # Clean up
        thresh = cv2.medianBlur(thresh, 5)

        # Mask circle
        circle_mask = np.zeros((height, width), dtype=np.uint8)
        cv2.circle(circle_mask, (radius, radius), radius, 255, -1)
        thresh = cv2.bitwise_and(thresh, thresh, mask=circle_mask)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        fish_coords = None
        if contours:
            largest = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                dist = ((cx - radius) ** 2 + (cy - radius) ** 2) ** 0.5
                if dist < radius:
                    fish_coords = (x + cx, y + cy)
                    cv2.circle(image_bgr, (cx, cy), 5, (0, 0, 255), -1)
        if fish_coords!= None:
            fish_coords = (x + cx - anch_x, y + cy - anch_y)
        return fish_coords