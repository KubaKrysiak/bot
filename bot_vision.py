import numpy as np
import cv2
import mss
import pyautogui
import os
from fish_area import FishArea


class BotVision:
    def match_at_position(self, center, template_path, confidence=0.85):  # można ustawić niższy próg
        template = cv2.imread(template_path)
        h, w = template.shape[:2]
        x_center, y_center = center
        x1 = int(x_center - w / 2)
        y1 = int(y_center - h / 2)
        screenshot = pyautogui.screenshot(region=(x1, y1, w, h))
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCORR_NORMED)
        max_val = cv2.minMaxLoc(result)[1]

        return max_val >= confidence

    def find_color_mean(self, area: FishArea, bgr_target_color):
        center_x, center_y, radius = area.get_scan_center_and_radius()
        x, y = center_x - radius, center_y - radius
        scan_size = radius * 2

        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": scan_size, "height": scan_size}
            screenshot = sct.grab(monitor)
            image_np = np.array(screenshot)

        hsv = cv2.cvtColor(image_np, cv2.COLOR_BGRA2BGR)
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)

        target_color_bgr = np.uint8([[bgr_target_color]])
        target_hsv = cv2.cvtColor(target_color_bgr, cv2.COLOR_BGR2HSV)[0][0]
        h, s, v = target_hsv

        delta_h, delta_s, delta_v = 20, 20, 20
        lower = np.array([max(h - delta_h, 0), max(s - delta_s, 0), max(v - delta_v, 0)])
        upper = np.array([min(h + delta_h, 179), min(s + delta_s, 255), min(v + delta_v, 255)])

        mask = cv2.inRange(hsv, lower, upper)
        circle_mask = np.zeros(mask.shape, dtype=np.uint8)
        cv2.circle(circle_mask, (radius, radius), radius, 255, -1)

        masked = cv2.bitwise_and(mask, mask, mask=circle_mask)
        ys, xs = np.where(masked > 0)

        if xs.size == 0:
            return None

        mean_x = int(xs.mean())
        mean_y = int(ys.mean())

        screen_x = x + mean_x
        screen_y = y + mean_y

        return screen_x - area.anch_x, screen_y - area.anch_y

    def find_color(self, area: FishArea, bgr_target_color):
        center_x, center_y, radius = area.get_scan_center_and_radius()
        x, y = center_x - radius, center_y - radius
        scan_size = radius * 2

        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": scan_size, "height": scan_size}
            screenshot = sct.grab(monitor)
            image_np = np.array(screenshot)

        hsv = cv2.cvtColor(image_np, cv2.COLOR_BGRA2BGR)
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)

        target_color_bgr = np.uint8([[bgr_target_color]])
        target_hsv = cv2.cvtColor(target_color_bgr, cv2.COLOR_BGR2HSV)[0][0]
        h, s, v = target_hsv
        delta = 3

        lower = np.array([max(h - delta, 0), max(s - delta, 0), max(v - delta, 0)])
        upper = np.array([min(h + delta, 179), min(s + delta, 255), min(v + delta, 255)])

        mask = cv2.inRange(hsv, lower, upper)

        circle_mask = np.zeros(mask.shape, dtype=np.uint8)
        cv2.circle(circle_mask, (radius, radius), radius, 255, -1)
        masked_color = cv2.bitwise_and(mask, mask, mask=circle_mask)

        return np.any(masked_color > 0)
