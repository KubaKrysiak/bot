from screen import Screen


class Config:
    # screen jest robiony podczas loadingu config
    def __init__(self, mt2_width, mt2_height, ch, ch_ok, select_btn, name, stop_id, circle_region):
        self.screen = Screen()
        self.screen_width = self.screen.screen_width
        self.screen_height = self.screen.screen_height
        self.mt2_width = mt2_width
        self.mt2_height = mt2_height
        self.ch = ch
        self.ch_ok = ch_ok
        self.select_btn = select_btn
        self.name = name
        self.stop_id = stop_id
        self.circle_region = circle_region

    def to_dict(self):
        return {
            'mt2_width': self.mt2_width,
            'mt2_height': self.mt2_height,
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
            mt2_width=data['mt2_width'],
            mt2_height=data['mt2_height'],
            ch=data['ch'],
            ch_ok=data['ch_ok'],
            select_btn=data['select_btn'],
            name=data['name'],
            stop_id=data['stop_id'],
            circle_region=data['circle_region']
        )
