import win32api


class Screen:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Screen, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.screen_width, self.screen_height = self.get_dimensions()
        self._initialized = True

    def get_dimensions(self):
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
        return screen_width, screen_height

    def __str__(self):
        return f"Monitor resolution: {self.screen_width}x{self.screen_height}"
