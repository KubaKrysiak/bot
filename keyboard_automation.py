from win32api import keybd_event
from time import sleep
from win32con import KEYEVENTF_KEYUP, VK_SPACE
import pyautogui

class KeyboardAutomation:
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-keybd_event

 def send_key_input(self, key):
        special_keys = {
            'space': (VK_SPACE, 0x39),
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

        sleep(0.01)
        keybd_event(vk_code, scan_code if scan_code is not None else 0, 0, 0)
        sleep(0.01)
        if key == "space":
            pyautogui.press('space')
        keybd_event(vk_code, scan_code if scan_code is not None else 0, KEYEVENTF_KEYUP, 0)

