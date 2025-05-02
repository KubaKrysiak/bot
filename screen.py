import win32api


class Screen:
    def __init__(self):
        self.screen_width, self.screen_height = self.get_dimensions()

    def get_dimensions(self):
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
        return screen_width, screen_height

    def __str__(self):
        return f"Monitor resolution: {self.screen_width}x{self.screen_height}"
