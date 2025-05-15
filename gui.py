import sys
import customtkinter as ctk
import os
import threading
import keyboard
import json
import subprocess

from tkinter import simpledialog
from configurator import Configurator
from windows_manager import WindowsManager

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

STATE_FILE = "gui_state.json"

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, s):
        self.text_widget.configure(state='normal')
        self.text_widget.insert("end", s)
        self.text_widget.see("end")
        self.text_widget.configure(state='disabled')

    def flush(self):
        pass

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FinalBot GUI")
        self.selected_config = None
        self.fishing_time = None
        self.window_title = None
        self.load_state()
        self.create_widgets()

        # Przechwyć sys.stdout i sys.stderr
        sys.stdout = TextRedirector(self.log_text)
        sys.stderr = TextRedirector(self.log_text)

        # Skróty klawiszowe: ESC+S = wyjdź, S+R = restart
        threading.Thread(target=self._keyboard_shortcuts, daemon=True).start()

    def _keyboard_shortcuts(self):
        while True:
            # ESC + S (niezależnie od kolejności)
            if keyboard.is_pressed('esc') and keyboard.is_pressed('s'):
                self.root.quit()
                break
            # S + R (niezależnie od kolejności)
            if keyboard.is_pressed('s') and keyboard.is_pressed('r'):
                self.root.after(0, self.restart_gui)
                break
            # Odświeżanie co 0.1s
            import time
            time.sleep(0.1)

    def save_state(self):
        state = {
            "selected_config": self.selected_config,
            "fishing_time": self.fishing_time,
            "window_title": self.window_title  # <-- zapisz tytuł okna
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f)

    def load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    self.selected_config = state.get("selected_config")
                    self.fishing_time = state.get("fishing_time")
                    self.window_title = state.get("window_title")  # <-- wczytaj tytuł okna
            except Exception:
                self.selected_config = None
                self.fishing_time = None
                self.window_title = None

    def update_info_label(self):
        text = (
            f"Wybrana konfiguracja: {self.selected_config or 'Brak'}\n"
            f"Czas łowienia: {self.fishing_time or 'Brak'}\n"
            f"Tytuł okna: {self.window_title or 'Brak'}"
        )
        self.info_label.configure(text=text)

    def restart_gui(self):
        print("Restartuję GUI i przerywam wszystkie akcje...")
        self.root.after(100, self._do_restart)

    def _do_restart(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def create_widgets(self):
        # Układ z ramką na lewą część (przyciski) i prawą (konsola)
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Lewy panel (przyciski)
        self.left_panel = ctk.CTkFrame(self.main_frame)
        self.left_panel.pack(side='left', fill='y', padx=(0, 10), pady=0, expand=False)

        self.info_label = ctk.CTkLabel(self.left_panel, text="", font=("Segoe UI", 14, "bold"))
        self.info_label.pack(fill='x', pady=(10, 15))
        self.update_info_label()

        ctk.CTkButton(self.left_panel, text="Wybierz konfigurację", command=self.choose_config).pack(fill='x', padx=30, pady=5)
        ctk.CTkButton(self.left_panel, text="Ustaw czas łowienia", command=self.choose_fishing_time).pack(fill='x', padx=30, pady=5)
        ctk.CTkButton(self.left_panel, text="Ustaw tytuł okna", command=self.choose_window_title).pack(fill='x', padx=30, pady=5)
        ctk.CTkButton(self.left_panel, text="1. Stwórz konfigurację", command=self.create_configuration).pack(fill='x', padx=30, pady=5)
        ctk.CTkButton(self.left_panel, text="2. Usuń konfigurację", command=self.delete_configuration).pack(fill='x', padx=30, pady=5)
        ctk.CTkButton(self.left_panel, text="3. Uruchom test.py", command=self.run_test_script).pack(fill='x', padx=30, pady=5)
        ctk.CTkButton(self.left_panel, text="4. Autologin", command=self.auto_login).pack(fill='x', padx=30, pady=5)
        ctk.CTkButton(self.left_panel, text="5. Włącz fishbota", command=self.launch_fishbots).pack(fill='x', padx=30, pady=5)
        ctk.CTkButton(self.left_panel, text="6. Zamknij okna", command=self.close_all_windows).pack(fill='x', padx=30, pady=5)
        ctk.CTkButton(self.left_panel, text="Restart", command=self.restart_gui).pack(fill='x', padx=30, pady=5)
        ctk.CTkButton(self.left_panel, text="Wyjdź (escape)", command=self.root.quit).pack(fill='x', padx=30, pady=5)

        # Prawy panel (konsola/logi)
        self.right_panel = ctk.CTkFrame(self.main_frame)
        self.right_panel.pack(side='left', fill='both', expand=True, padx=(0, 0), pady=0)

        self.log_text = ctk.CTkTextbox(self.right_panel, height=200, font=("Consolas", 13))
        self.log_text.pack(fill='both', expand=True, padx=20, pady=(10, 20))
    
    def create_configuration(self):
        def worker():
            Configurator.configure(window_title=self.window_title)
            input("Naciśnij Enter, aby zamknąć...")
            print("Zakończono konfigurację (sprawdź logi i pliki).")
        threading.Thread(target=worker, daemon=True).start()

    def delete_configuration(self):
        directory_path = os.getcwd()
        folders = [f for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))]
        if not folders:
            print("Brak konfiguracji do usunięcia.")
            return
        conf = simpledialog.askstring("Usuń konfigurację", f"Wybierz do usunięcia:\n{', '.join(folders)}")
        if conf:
            def worker():
                try:
                    Configurator.delete_config(conf)
                    print(f"Usunięto {conf}")
                    if self.selected_config == conf:
                        self.selected_config = None
                        self.save_state()
                        self.update_info_label()
                except Exception as e:
                    print(f"Nie udało się usunąć: {e}")
            threading.Thread(target=worker, daemon=True).start()
        else:
            print("Nie wybrano konfiguracji do usunięcia.")

    def load_configuration(self):
        directory_path = os.getcwd()
        folders = [f for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))]
        if not folders:
            print("Brak konfiguracji do wyboru.")
            return None
        conf = simpledialog.askstring("Wczytaj konfigurację", f"Wybierz konfigurację:\n{', '.join(folders)}")
        if conf:
            self.selected_config = conf
            self.save_state()
            self.update_info_label()
            return Configurator.load_config(conf)
        return None

    def choose_config(self):
        if self.selected_config:
            return True
        directory_path = os.getcwd()
        folders = [f for f in os.listdir(directory_path)
                   if os.path.isdir(os.path.join(directory_path, f)) and not f.startswith('.') and not f.startswith('_')]
        if not folders:
            print("Brak konfiguracji do wyboru.")
            return False
        numbered_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(folders)])
        num = simpledialog.askinteger(
            "Wybierz konfigurację",
            f"Wybierz numer konfiguracji:\n{numbered_list}"
        )
        if num and 1 <= num <= len(folders):
            conf = folders[num - 1]
            self.selected_config = conf
            self.save_state()
            self.update_info_label()
            print(f"Wybrano konfigurację: {conf}")
            return True
        else:
            print("Nie wybrano konfiguracji.")
            return False

    def choose_fishing_time(self):
        if self.fishing_time:
            return True
        tim = simpledialog.askinteger("Czas łowienia", "Podaj czas łowienia w sekundach:")
        if tim:
            self.fishing_time = tim
            self.save_state()
            self.update_info_label()
            print(f"Ustawiono czas łowienia: {tim} s")
            return True
        else:
            print("Nie podano czasu łowienia.")
            return False

    def choose_window_title(self):
        title = simpledialog.askstring("Tytuł okna", "Podaj tytuł okna aplikacji (np. Metin2):")
        if title:
            self.window_title = title
            self.save_state()
            self.update_info_label()
            print(f"Ustawiono tytuł okna: {title}")
            return True
        else:
            print("Nie podano tytułu okna.")
            return False

    # Przed uruchomieniem automatyzacji, wymuś wybór tytułu okna:
    def auto_login(self):
        if not self.choose_config():
            return
        if not self.window_title:
            if not self.choose_window_title():
                return
        cfg = Configurator.load_config(self.selected_config)
        if cfg:
            def worker():
                wm = WindowsManager(cfg, self.window_title)
                wm.place_all_windows()
                wm.automatic_login()
                print("Autologin uruchomiony!")
            threading.Thread(target=worker, daemon=True).start()

    def launch_fishbots(self):
        if not self.choose_config():
            return
        if not self.choose_fishing_time():
            return
        if not self.window_title:
            if not self.choose_window_title():
                return
        cfg = Configurator.load_config(self.selected_config)
        tim = self.fishing_time
        def worker():
            wm = WindowsManager(cfg, self.window_title)
            wm.place_all_windows()
            wm.start_fishing(tim)
            print("Fishbot uruchomiony!")
        threading.Thread(target=worker, daemon=True).start()

    def run_test_script(self):
        test_script_path = os.path.join(os.getcwd(), "test", "test.py")
        test_dir = os.path.join(os.getcwd(), "test")
        if os.path.exists(test_script_path):
            def reader():
                import subprocess
                proc = subprocess.Popen(
                    ["python", "test.py"],
                    cwd=test_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                for line in proc.stdout:
                    print("[test.py]", line, end="")
            threading.Thread(target=reader, daemon=True).start()
            print("test.py uruchomiony w tle")
        else:
            print("Nie znaleziono test/test.py")

    def close_all_windows(self):
        if not self.choose_config():
            return
        if not self.window_title:
            if not self.choose_window_title():
                return
        cfg = Configurator.load_config(self.selected_config)
        if cfg:
            def worker():
                wm = WindowsManager(cfg, self.window_title)
                wm.place_all_windows()
                try:
                    wm.close_all_windows()
                    print("Wszystkie okna zostały zamknięte.")
                except Exception as e:
                    print(f"Nie udało się zamknąć okien: {e}")
            threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    root = ctk.CTk()
    gui = GUI(root)
    root.mainloop()