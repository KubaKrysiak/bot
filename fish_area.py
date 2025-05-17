class FishArea:
    def __init__(self, anch_x, anch_y, cir_left, cir_top, cir_right, cir_bottom):
        self.anch_x = anch_x
        self.anch_y = anch_y
        self.cir_left = cir_left
        self.cir_top = cir_top
        self.cir_right = cir_right
        self.cir_bottom = cir_bottom

    def get_scan_center_and_radius(self):
        center_x = self.anch_x + (self.cir_left[0] + self.cir_right[0]) // 2
        center_y = self.anch_y + (self.cir_top[1] + self.cir_bottom[1]) // 2
        radius = abs((self.cir_right[0] - self.cir_left[0]) // 2)
        return center_x, center_y, radius