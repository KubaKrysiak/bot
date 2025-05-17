class Command:
    def execute(self):
        raise NotImplementedError

class ClickSafeCommand(Command):
    def __init__(self, session, x, y):
        self.session = session
        self.x = x
        self.y = y
    def execute(self):
        self.session.send_click_safe(self.x, self.y)

class ClickFastCommand(Command):
    def __init__(self, session, x, y):
        self.session = session
        self.x = x
        self.y = y
    def execute(self):
        self.session.send_click_fast(self.x, self.y)

class KeyInputCommand(Command):
    def __init__(self, session, key):
        self.session = session
        self.key = key
    def execute(self):
        self.session.send_key_input(self.key)