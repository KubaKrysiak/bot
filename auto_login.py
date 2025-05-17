from time import sleep, time
from commands import ClickSafeCommand


class AutoLogin:
    def __init__(self, window_session, click_delay = 0.1):
        self.ws = window_session
        self.is_chosen_channel = False
        self.click_delay = click_delay

    def click_ch_button(self, nr):
        cmd = ClickSafeCommand(self.ws, *self.ws.config.ch[nr])
        self.ws.execute_command(cmd)

    def click_ok_button(self):
        cmd = ClickSafeCommand(self.ws, *self.ws.config.ch_ok)
        self.ws.execute_command(cmd)

    def click_play(self):
        cmd = ClickSafeCommand(self.ws, *self.ws.config.select_btn)
        self.ws.execute_command(cmd)

    def find_play_button(self):
        return self.ws.match_at_position(self.ws.config.select_btn, self.ws.config.stop_id)

    def click_play_button(self):
        cmd = ClickSafeCommand(self.ws, *self.ws.config.select_btn)
        self.ws.execute_command(cmd)

    def choose_channel(self):
        self.click_ch_button(4)
        sleep(self.click_delay)
        self.click_ok_button()
        sleep(self.click_delay)


    def do_auto_login_action(self):
        if self.find_play_button():
            self.click_play_button()
            return True
        else:
            if not self.is_chosen_channel:
                self.choose_channel()
                self.is_chosen_channel = True
                return False
