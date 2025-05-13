from time import sleep, time

import win32gui

from fish_bot import FishBot
from mt2_window import Mt2Window


class WindowsManager:
    def __init__(self, config):
        self.config = config
        self.windows = self.update_METIN2_windows()
        self.mt2_width = config.mt2_width
        self.mt2_height = config.mt2_height
        self.screen_width = config.screen_width
        self.screen_height = config.screen_height
        self.max_catches = 400

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
        for idx, window in enumerate(self.windows):
            if sety + self.mt2_height > self.screen_height:
                break
            if setx + self.mt2_width > self.screen_width:
                setx = 0
                sety += self.mt2_height
                if sety + self.mt2_height > self.screen_height:
                    break
            window.restore_window()
            window.place_mt2window(setx, sety, self.mt2_width, self.mt2_height)
            setx += self.mt2_width
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
                sleep(0.5)
                window.click_relative(*self.config.ch[i % 6])
                i += 1
                sleep(0.5)
                window.click_relative(*self.config.ch_ok)
                if window.match_at_position(self.config.select_btn, self.config.stop_id):
                    launched_counter += 1
                    sleep(0.1)
                    window.send_key_input("enter")
                    sleep(0.1)
                    window.send_key_input(" ")
                    window.click_relative(*self.config.select_btn)

    def start_fishing(self, timee):
        fish_bots = []
        for window in self.windows:
            bot = FishBot(window)
            fish_bots.append(bot)
        start_time = time()
        while time() - start_time < timee:
            # 1 focus
            # 2 sleep 0.1
            # 3 take worm
            # 4 sleep 1
            # 5 get focus
            # 6 sleep 0.1
            # 7 cast the fishing rod
            # 8 czekaj az nie bedzie okienka z rybą
            # 9 dopoki okienko z rybką nie zniknie klikaj rybe
            # 10 sleep 2
            bot.get_focus()
            for bot in fish_bots:
                if bot.action == 0:
                    bot.get_focus()
                    sleep(0.1)
                    bot.take_worm()
                    bot.wait(1)
                elif bot.action == 1 and time() - bot.time_counter > bot.time_acc:
                    bot.get_focus()
                    sleep(0.1)
                    bot.cast_the_fishing_rod()
                    bot.wait(1)
                elif bot.action == 2:
                    if not bot.mt2_window.find_fish_window():
                        sleep(0.1)
                    else:
                        bot.action = 3
                elif bot.action == 3:
                    if bot.mt2_window.find_fish_window():
                        if time() - bot.time_counter > bot.time_acc:
                            pos = bot.find_fish()
                            if pos != None:
                                bot.get_focus()
                                sleep(0.01)
                                bot.click(pos)
                                gizmo = bot.action
                                bot.wait(1)
                                bot.action = gizmo
                    else:
                        bot.zlowione += 1
                        if bot.zlowione == 400:
                            # na potem
                            return 0
                        bot.wait(2)
                elif bot.action == 4 and time() - bot.time_counter > bot.time_acc:
                    bot.action = 0

    def close_all_windows(self):
        """Zamyka wszystkie okna METIN2 znalezione przez WindowsManager."""
        for window in self.windows:
            try:
                window.close_window()
            except Exception as e:
                print(f"Nie udało się zamknąć okna {window}: {e}")


"""
            wojtaczek1237170@gmail.com
            KochamBbe123!
            1. Pierwsza wersja (action-owa, z wait i action)
Sterowanie stanem: Każdy bot ma własny stan (action), który decyduje, co ma robić w danym momencie.
Czas oczekiwania: Używasz bot.wait(x), które ustawia bot.time_counter i bot.time_acc, a potem sprawdzasz if time() - bot.time_counter > bot.time_acc:. To oznacza, że przejście do kolejnej akcji zależy od upływu czasu od ostatniego wait.
Wielookienkowość: Wszystkie boty są obsługiwane w jednej pętli, ale każdy bot może być w innym stanie (action), więc mogą się rozjeżdżać w czasie.
W każdej iteracji pętli: Najpierw bot.get_focus() dla jednego bota, potem pętla po wszystkich botach i ich akcje.
import threading

def bot_fishing(bot, timee):
    start_time = time()
    while time() - start_time < timee:
        bot.get_focus()
        bot.take_worm()
        sleep(1)
        bot.cast_the_fishing_rod()
        while not bot.mt2_window.find_fish_window():
            sleep(0.1)
        while bot.mt2_window.find_fish_window():
            pos = bot.find_fish()
            if pos is not None:
                bot.click(pos)
                sleep(1)
        bot.zlowione += 1
        if bot.zlowione == 400:
            return
        sleep(2)

def start_fishing(self, timee):
    fish_bots = [FishBot(window) for window in self.windows]
    threads = []
    for bot in fish_bots:
        t = threading.Thread(target=bot_fishing, args=(bot, timee))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

Dokładnie – i bardzo trafnie zauważyłeś klasyczny problem współdzielenia zasobów w środowisku GUI: fokus okna jest współdzielony globalnie, więc tylko jedno okno może mieć fokus na raz. Jeśli boty będą działać jednocześnie (czy to przez asyncio, czy wątki), mogą sobie ten fokus nadpisywać, co sprawia, że np. kliknięcia trafią nie tam, gdzie trzeba. Dlatego Twoje podejście quasi-asynchroniczne ma sens w tym kontekście.
pewnie mozna inaczej z multithread

"""
