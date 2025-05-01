import win32gui
import win32con
import win32api
from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui
import time

class ScreenProperties:
    def __init__(self):
        self.screenWidth, self.screenHeight = self.get_screen_size()
        self.mt2width = 800
        self.mt2height = 600

    def get_screen_size(self):
        """
        zwraca rozdzielczosc monitora
        """
        width = win32api.GetSystemMetrics(0)
        height = win32api.GetSystemMetrics(1)
        return width, height

    def enum_windows_callback(hwnd, windows):
        """
        funkcja pomocnicza
        """
        # chyba bez is Window Visible
        if win32gui.GetWindowText(hwnd) == "METIN2":
            windows.append(hwnd)

    def update_METIN2_windows(self):
        """
        zwraca tablice obiektow MT2window gdzie kazdy obiekt to okienko z zakotwiczonym uchwytem hwnd
        """
        #niefajnie 2 windowsy i windows_object
        windows = []
        win32gui.EnumWindows(self.enum_windows_callback, windows)
        windows_objects = []
        print(f"Znalezione okna o tytule METIN2:")
        for hwnd in windows:
            print(f"Okno HWND: {hwnd}")
            windows_objects.append(Mt2Window(hwnd))
        return windows_objects

    def get_window_size(self):
        """
        zwraca rozmiary pojedynczego okna
        """
        rect = win32gui.GetWindowRect(self.hwnd)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        return width,height

class WindowsManager:
    def __init__(self):
        self.screen = ScreenProperties()
        self.windows = self.screen.update_METIN2_windows()

    def calc_win_pos(self):
        setx, sety = 0, 0
        for window in windows:
            restore_window(window)
            move_and_activate_window(windows[i], setx, sety, width, height)
            if setx + width > widths:
                setx = 0
                sety += height
                if sety > heights:
                    print("za duzo okien usun")
                    break
            else:
                setx += width
            i += 1

    def notify(self, action : str, context : dict):
        for window in self.windows:
            window.update(action)

class Mt2Window:
    def __init__(self, hwnd):
        self.hwnd = hwnd
    def get_top_right_coordinates(self):
        """
        zwraca gorny prawy rog wspolrzedne
        """
        # rect prostokąt okna (left, top, right, bottom)
        rect = win32gui.GetWindowRect(self.hwnd)
        left, top, right, bottom = rect
        top_right_x = right
        top_right_y = top
        return top_right_x, top_right_y

    def restore_window(self):
        """
        maksymalizuje okno jesli jest ukryte
        """
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)

    def place_mt2window(hwnd, x, y, width, height):
        """
        ustawia: rozmiar, focus i pozycje
        """
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, width, height, win32con.SWP_NOACTIVATE)
    def update(self, action):
        """
        gdy observer dostanie powiadomienie to wykonuje akcje
        """
        if action == "restore_window":
            self.restore_window()
        if action == "setup_mt2window_on_screen":
            self.setup_mt2window_on_screen()




def find_image_on_screen(template_path, area, threshold=0.9):
    # Przechwyć obraz z ekranu w określonym obszarze
    left, top, right, bottom = area
    screen_image = ImageGrab.grab(bbox=(left, top, right, bottom))
    screen_image_np = np.array(screen_image)

    # Wczytaj obraz wzorcowy
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    screen_gray = cv2.cvtColor(screen_image_np, cv2.COLOR_BGR2GRAY)

    # Wykonaj dopasowanie wzorca
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)

    # Zwróć współrzędne dopasowania
    coordinates = []
    for pt in zip(*locations[::-1]):
        coordinates.append(pt)

    return coordinates
if __name__ == "__main__":

"""
wiersze=1
widths, heights = get_screen_size()
width, height = get_window_size(windows[0])
wsp = heights / wiersze / height
height = int(height * wsp)
width = int(width * wsp)
"""

print(get_top_right_coordinates(windows[0]))
print(get_top_right_coordinates(windows[1]))
print(get_window_size(windows[0]))
time.sleep(1)
cords1=find_image_on_screen(r"C:\Users\kurwa cholera jasna\Pictures\Screenshots\Zrzut ekranu 2024-08-27 071953.png",(0,0,width,height),0.9)
x1,y1=cords1[0]
y1=int(y1)
x1=int(x1)
pyautogui.click(x1,y1)
cords2=find_image_on_screen(r"C:\Users\kurwa cholera jasna\Pictures\Screenshots\Zrzut ekranu 2024-08-27 072328.png",(0,0,width,height),0.9)
x2,y2=cords2[0]
y2=int(y2)
x2=int(x2)
pyautogui.click(x2,y2)
time.sleep(8)
cords3=find_image_on_screen(r"C:\Users\kurwa cholera jasna\Pictures\Screenshots\Zrzut ekranu 2024-08-27 072601.png",(0,0,width,height),0.98)
x3,y3=cords3[0]
y3=int(y3)
x3=int(x3)
pyautogui.click(x3,y3)
"""
width,height = Image.open(image_path).size
anti-logout=funkcja log in w przypadku log outa
informacja poczatkowa - jaka ma byc pierwsza strona ekwipunku, a moze robaki w umiejetnosciach, oraz informacja ze mozna wlaczyc dodatkowe pulpity, oraz
ze max mozna 4 rybaki na raz start, wlaczanie autologa lub nie autolog dziala ze loguje sie na pierwszego slota, otwieranie ekwipunku 
"""
