import sys
import numpy as np
import cv2
import random
import win32gui
import win32con
import os
import contextlib
with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    import pygame
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class TestGame:
    def __init__(self):
        # Parametry domyślne
        self.WIDTH, self.HEIGHT = 800, 600

        # Inicjalizacja
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Test")

        # Wczytywanie grafik
        self.ch_imgs = [pygame.image.load(f'test_assets/ch{i}.png').convert_alpha() for i in range(1, 7)]
        self.ch_ok_img = pygame.image.load('test_assets/ch_ok.png').convert_alpha()
        self.postac_img = pygame.image.load('test_assets/postac.png').convert_alpha()
        self.popup_img = pygame.image.load('test_assets/popup.png').convert_alpha()

        # Fonty i wiadomości
        self.font = pygame.font.SysFont('Arial', 24)
        self.message = ''
        self.hit_message = ''

        # Zmienne stanu
        self.state = 'wybor_ch'
        self.selected_ch = None
        self.selected_num = None
        self.displayed_img = None
        self.clicks = []
        self.mouse_click_count = 0

        # Parametry ryby
        fish_color_bgr = np.uint8([[[123, 88, 53]]])
        self.fish_color_hsv = cv2.cvtColor(fish_color_bgr, cv2.COLOR_BGR2HSV)[0][0]
        self.fish_color_rgb = tuple(int(c) for c in fish_color_bgr[0][0][::-1])
        self.fish_radius = 10
        self.fish_pos = None
        self.fish_dir = None
        self.change_interval = 60
        self.frame_counter = 0

        self.clock = pygame.time.Clock()
        self.update_positions()

    def get_popup_rect(self):
        center = (self.WIDTH // 2, self.HEIGHT // 2)
        rect = self.popup_img.get_rect(center=center)
        return rect

    def reset_display(self):
        self.displayed_img = None
        self.mouse_click_count = 0
        self.clicks = []
        self.state = 'game'
        self.fish_pos = None
        self.fish_dir = None
        self.frame_counter = 0
        self.hit_message = ''
        return 'Odświeżenie. Wciśnij cyfrę i spację'

    def update_positions(self):
        # Aktualizacja wymiarów
        self.WIDTH, self.HEIGHT = self.screen.get_size()

        # Pozycje kanałów
        total_height = sum(img.get_height() for img in self.ch_imgs)
        start_y = self.HEIGHT // 2 - total_height // 2
        self.ch_rects = []
        x_center = self.WIDTH // 2
        current_y = start_y
        for img in self.ch_imgs:
            rect = img.get_rect()
            rect.centerx = x_center
            rect.y = current_y
            self.ch_rects.append(rect)
            current_y += img.get_height()

        # Pozycja przycisku OK
        self.ch_ok_rect = self.ch_ok_img.get_rect()
        self.ch_ok_rect.centerx = self.WIDTH // 2
        self.ch_ok_rect.top = start_y + total_height + 50

        # Pozycja postaci
        self.postac_rect = self.postac_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            self.update_positions()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                return

            mx, my = event.pos
            if self.state == 'wybor_ch':
                for idx, rect in enumerate(self.ch_rects, start=1):
                    if rect.collidepoint(mx, my):
                        self.selected_ch = idx
                        self.message = f"Wybrano kanał {idx}"
                        break
                if self.selected_ch and self.ch_ok_rect.collidepoint(mx, my):
                    self.state = 'wybor_postaci'
                    self.message = 'Wybór postaci'

            elif self.state == 'wybor_postaci':
                if self.postac_rect.collidepoint(mx, my):
                    self.state = 'game'
                    self.message = 'Wciśnij cyfrę 1-9, potem spację'

            elif self.state == 'display_image':
                self.mouse_click_count += 1
                self.clicks.append((mx, my))
                hitbox_radius = self.fish_radius + 15
                fish_x, fish_y = int(self.fish_pos[0]), int(self.fish_pos[1])
                dx = mx - fish_x
                dy = my - fish_y
                dist = np.hypot(dx, dy)
                print(f"Kliknięcie: ({mx}, {my}), Pozycja ryby: ({fish_x}, {fish_y}), dx: {dx}, dy: {dy}, Odległość: {dist}, Hitbox: {hitbox_radius}")
                self.hit_message = 'Trafiono!' if dist <= hitbox_radius else 'Nie trafiono'

                if self.mouse_click_count >= 3:
                    self.message = self.reset_display()

        elif event.type == pygame.KEYDOWN:
            if self.state == 'game':
                if event.unicode.isdigit() and '1' <= event.unicode <= '9':
                    self.selected_num = int(event.unicode)
                elif event.key == pygame.K_SPACE and self.selected_num:
                    self.displayed_img = self.popup_img
                    self.mouse_click_count = 0
                    self.clicks = []
                    self.state = 'display_image'
                    pr = self.get_popup_rect()
                    self.fish_pos = [
                        random.randint(pr.left + self.fish_radius, pr.right - self.fish_radius),
                        random.randint(pr.top + self.fish_radius, pr.bottom - self.fish_radius)
                    ]
                    angle = random.uniform(0, 2 * np.pi)
                    self.fish_dir = [np.cos(angle), np.sin(angle)]
                    self.frame_counter = 0
                    self.message = 'Kliknij 3 razy, aby zamknąć'

            elif self.state == 'wybor_postaci' and event.key == pygame.K_RETURN:
                self.state = 'game'
                self.message = 'Wciśnij cyfrę 1-9, potem spację'

    def update_fish(self):
        if self.state == 'display_image':
            pr = self.get_popup_rect()
            self.frame_counter += 1
            fish_speed = 3
            if self.frame_counter >= self.change_interval:
                center_x, center_y = self.WIDTH // 2, self.HEIGHT // 2
                vector_to_center = [center_x - self.fish_pos[0], center_y - self.fish_pos[1]]
                magnitude = np.hypot(vector_to_center[0], vector_to_center[1])
                vector_to_center = [vector_to_center[0] / magnitude, vector_to_center[1] / magnitude]

                bias = 0.7
                if random.random() < bias:
                    self.fish_dir = vector_to_center
                else:
                    angle = random.uniform(0, 2 * np.pi)
                    self.fish_dir = [np.cos(angle), np.sin(angle)]

                self.frame_counter = 0
            self.fish_pos[0] += self.fish_dir[0] * fish_speed
            self.fish_pos[1] += self.fish_dir[1] * fish_speed
            if self.fish_pos[0] - self.fish_radius <= pr.left or self.fish_pos[0] + self.fish_radius >= pr.right:
                self.fish_dir[0] *= -1
                self.fish_pos[0] = max(pr.left + self.fish_radius, min(pr.right - self.fish_radius, self.fish_pos[0]))
            if self.fish_pos[1] - self.fish_radius <= pr.top or self.fish_pos[1] + self.fish_radius >= pr.bottom:
                self.fish_dir[1] *= -1
                self.fish_pos[1] = max(pr.top + self.fish_radius, min(pr.bottom - self.fish_radius, self.fish_pos[1]))

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.state == 'wybor_ch':
            for img, rect in zip(self.ch_imgs, self.ch_rects):
                self.screen.blit(img, rect)
            self.screen.blit(self.ch_ok_img, self.ch_ok_rect)
        elif self.state == 'wybor_postaci':
            self.screen.blit(self.postac_img, self.postac_rect)
        elif self.state == 'display_image':
            rect = self.popup_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(self.popup_img, rect)
            pygame.draw.circle(self.screen, self.fish_color_rgb, (int(self.fish_pos[0]), int(self.fish_pos[1])), self.fish_radius)
            for cx, cy in self.clicks:
                pygame.draw.circle(self.screen, (255, 0, 0), (cx, cy), 5)
        else:
            if self.displayed_img:
                rect = self.popup_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                self.screen.blit(self.popup_img, rect)

        # Komunikaty
        if self.message:
            text_surf = self.font.render(self.message, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 30))
            self.screen.blit(text_surf, text_rect)
        if self.hit_message:
            hit_surf = self.font.render(self.hit_message, True, (255, 255, 255))
            hit_rect = hit_surf.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 60))
            self.screen.blit(hit_surf, hit_rect)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                self.handle_event(event)
            self.update_fish()
            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    game = TestGame()
    game.run()
