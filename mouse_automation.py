import win32con
from win32api import mouse_event, SetCursorPos
from time import sleep


class MouseAutomation:
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mouse_event

    def __init__(self, fast_delay=0.01):
        self.fast_delay = fast_delay

    def click_safe(self, x, y):
        SetCursorPos((x, y))
        sleep(0.1)
        mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
        sleep(0.1)
        mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y)

    def click_fast(self, x, y):
        SetCursorPos((x, y))
        sleep(self.fast_delay)
        mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
        sleep(self.fast_delay)
        mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y)
