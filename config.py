from screen import Screen


class Config:
    # screen jest robiony podczas loadingu config
    def __init__(self, width, height, ch, ch_ok, select_btn, name, stop_id, circle_region):
        self.screen = Screen()
        self.screen_width = self.screen.screen_width
        self.screen_height = self.screen.screen_height
        self.width = width
        self.height = height

        self.ch_ok = ch_ok
        self.ch = ch
        # srodek select btn
        self.select_btn = select_btn
        self.name = name
        # path do sleect btn
        self.stop_id = stop_id
        # krotka left top right, bottom
        self.circle_region = circle_region

    def to_dict(self):
        return {
            'width': self.width,
            'height': self.height,
            'ch': self.ch,
            'ch_ok': self.ch_ok,
            'select_btn': self.select_btn,
            'name': self.name,
            'stop_id': self.stop_id,
            'circle_region': self.circle_region
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            width=data['width'],
            height=data['height'],
            ch=data['ch'],
            ch_ok=data['ch_ok'],
            select_btn=data['select_btn'],
            name=data['name'],
            stop_id=data['stop_id'],
            circle_region=data['circle_region']
        )
