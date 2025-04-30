import win32gui
import win32con
import win32api
from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui
import time
def enum_windows_callback(hwnd, windows):
    # Sprawdź, czy okno jest widoczne i ma tytuł "Metin 2"
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == "METIN2":
        windows.append(hwnd)


def get_top_right_coordinates(hwnd):
    # Pobierz prostokąt okna (left, top, right, bottom)
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect

    # Współrzędne prawego górnego rogu
    top_right_x = right
    top_right_y = top

    return top_right_x, top_right_y
def find_windows_by_title(title):
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows
def restore_window(hwnd):
    # Przywróć okno, jeśli jest zminimalizowane
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
def get_window_size(hwnd):
    # Pobranie prostokąta okna
    rect = win32gui.GetWindowRect(hwnd)
    # Obliczenie szerokości i wysokości
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    return width,height


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


def get_screen_size():
    # Pobranie rozmiaru ekranu
    width = win32api.GetSystemMetrics(0)  # SM_CXSCREEN
    height = win32api.GetSystemMetrics(1) # SM_CYSCREEN
    return width, height
def move_and_activate_window(hwnd, x, y,width,height):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, width, height, win32con.SWP_NOACTIVATE)
if __name__ == "__main__":
    title_to_find = "METIN2"
    windows = find_windows_by_title(title_to_find)
    print(f"Znalezione okna o tytule '{title_to_find}':")
    for hwnd in windows:
        print(f"Okno HWND: {hwnd}")
        restore_window(hwnd)
"""
wiersze=1
widths, heights = get_screen_size()
width, height = get_window_size(windows[0])
wsp = heights / wiersze / height
height = int(height * wsp)
width = int(width * wsp)
"""
width=800
height=600
widths=1960
heights=1080
move_and_activate_window(windows[0],0,0,width,height)
print(f"Width: {width}, Height: {height}")
i=0
setx,sety=0,0
while i<len(windows):
    restore_window(windows[i])
    move_and_activate_window(windows[i],setx,sety,width,height)
    if setx+width>widths:
        setx=0
        sety+=height
        if sety>heights:
            print("za duzo okien usun")
            break
    else:
        setx+=width
    i+=1
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
