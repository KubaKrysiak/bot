import psutil
import win32con
import win32gui

import win32process


class WindowAutomation:
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowpos

    def __init__(self, hwnd, anch_x, anch_y):
        self.hwnd = hwnd
        self.process = psutil.Process(win32process.GetWindowThreadProcessId(self.hwnd)[1])
        self.anch_x = anch_x
        self.anch_y = anch_y

    def get_corner_x(self):
        return self.anch_x

    def get_corner_y(self):
        return self.anch_y
    def restore(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWNOACTIVATE)

    def activate(self):
        win32gui.SetForegroundWindow(self.hwnd)

    def set_topmost(self):
        win32gui.SetWindowPos(
            self.hwnd,
            win32con.HWND_TOPMOST,
            0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
        )

    def move(self, x, y):
        win32gui.SetWindowPos(
            self.hwnd,
            0,
            x, y,
            0, 0,
            win32con.SWP_NOACTIVATE | win32con.SWP_NOSIZE | win32con.SWP_NOZORDER
        )

    def resize(self, width, height):
        win32gui.SetWindowPos(
            self.hwnd,
            0,
            0, 0,
            width, height,
            win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOZORDER
        )

    def close(self):
        self.process.terminate()
