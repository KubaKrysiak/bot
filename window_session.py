from window_automation import WindowAutomation
from fish_area import FishArea
from commands import ClickSafeCommand, ClickFastCommand, KeyInputCommand
import time

class WindowSession:
    def __init__(self, config, window_automation, mouse_automation, keyboard_automation, bot_vision, fish_area):
        self.window_automation = window_automation
        self.mouse = mouse_automation
        self.keyboard = keyboard_automation
        self.vision = bot_vision
        self.config = config
        self.fish_area = fish_area
        """
        FishArea(
            anch_x=self.window_automation.get_corner_x(), anch_y=self.window_automation.get_corner_y(),
            cir_left=config.circle_region[0], cir_top=config.circle_region[1],
            cir_right=config.circle_region[2], cir_bottom=config.circle_region[3]
        ))
        """

    def place_window(self, x, y):
        self.window_automation.restore()
        self.window_automation.resize(self.config.width, self.config.height)
        self.window_automation.move(x, y)
        self.window_automation.set_topmost()

    def close(self):
        self.window_automation.close()

    def activate(self):
        self.window_automation.activate()

    def send_click_safe(self, x, y):
        self.window_automation.activate()
        self.mouse.click_safe(x + self.window_automation.get_corner_x(), y + self.window_automation.get_corner_y())

    def send_click_fast(self, x, y):
        self.window_automation.activate()
        self.mouse.click_fast(x + self.window_automation.get_corner_x(), y + self.window_automation.get_corner_y())

    def send_key_input(self, key):
        self.window_automation.activate()
        self.keyboard.send_key_input(key)

    def match_at_position(self, center, template_path):
        relative_center = [center[0] + self.window_automation.get_corner_x(),
                           center[1] + self.window_automation.get_corner_y()]
        return self.vision.match_at_position(relative_center, template_path)

    def find_color(self, bgr_target_color):
        return self.vision.find_color(self.fish_area, bgr_target_color)

    def find_color_mean(self, bgr_target_color):
        return self.vision.find_color_mean(self.fish_area, bgr_target_color)

    def click_fish(self):
        pos = self.find_fish()
        if pos:
            self.send_click_fast(*pos)

    def execute_command(self, command):
        command.execute()
