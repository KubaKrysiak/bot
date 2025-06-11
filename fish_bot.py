from time import time
from commands import KeyInputCommand, ClickFastCommand


class FishBot:
    def __init__(self, window_session):
        self.ws = window_session
        self.worms_count = 400 * 8
        self.action = 0
        self.time_acc = 0
        self.time_counter = 0

    def take_worm(self):
        cmd = KeyInputCommand(self.ws, str(8 - (self.worms_count // 400) + 1))
        self.ws.execute_command(cmd)

    def cast_the_fishing_rod(self):
        cmd = KeyInputCommand(self.ws, "space")
        self.ws.execute_command(cmd)

    def find_fish_window(self):
        return self.ws.find_color((216, 145, 49))

    def find_fish(self):
        return self.ws.find_color_mean((123, 88, 53))

    def click_fish(self):
        pos = self.find_fish()
        if pos:
            cmd = ClickFastCommand(self.ws, *pos)
            self.ws.execute_command(cmd)
            return True
        return False

    def wait(self, timee):
        self.time_counter = time()
        self.time_acc = timee
        self.action += 1

    def do_fishing_action(self):
        if self.action == 0:
            self.take_worm()
            self.wait(1)
            print("Wziąłem robaka", self.time_counter)
        elif self.action == 1 and time() - self.time_counter > self.time_acc:
            self.cast_the_fishing_rod()
            self.wait(1)
            print("Wziąłem robaka", self.time_counter)
        elif self.action == 2:
            if self.find_fish_window():
                self.action = 3
        elif self.action == 3:
            if self.find_fish_window():
                if time() - self.time_counter > self.time_acc:
                    if self.click_fish():
                        gizmo = self.action
                        self.wait(1)
                        self.action = gizmo
            else:
                self.worms_count -= 1
                if self.worms_count == 0:
                    return True
                self.wait(4)
        elif self.action == 4 and time() - self.time_counter > self.time_acc:
            self.action = 0
