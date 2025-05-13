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
# Parametry domyślne
WIDTH, HEIGHT = 800, 600

# Inicjalizacja
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("METIN2")

# Wczytywanie grafik
ch_imgs = [pygame.image.load(f'ch{i}.png').convert_alpha() for i in range(1, 7)]
ch_ok_img = pygame.image.load('ch_ok.png').convert_alpha()
postac_img = pygame.image.load('postac.png').convert_alpha()
popup_img = pygame.image.load('popup.png').convert_alpha()

# Fonty i wiadomości
font = pygame.font.SysFont('Arial', 24)
message = ''
hit_message = ''

# Zmienne stanu
state = 'wybor_ch'
selected_ch = None
selected_num = None
displayed_img = None
clicks = []
mouse_click_count = 0

# Parametry ryby
fish_color_bgr = np.uint8([[[123, 88, 53]]])
fish_color_hsv = cv2.cvtColor(fish_color_bgr, cv2.COLOR_BGR2HSV)[0][0]
fish_color_rgb = tuple(int(c) for c in fish_color_bgr[0][0][::-1])
fish_radius = 10
fish_pos = None
fish_dir = None
change_interval = 60
frame_counter = 0


def get_popup_rect():
    center = (WIDTH//2, HEIGHT//2)
    rect = popup_img.get_rect(center=center)
    return rect


def reset_display():
    global state, displayed_img, mouse_click_count, fish_pos, fish_dir, clicks, frame_counter, hit_message
    displayed_img = None
    mouse_click_count = 0
    clicks = []
    state = 'game'
    fish_pos = None
    fish_dir = None
    frame_counter = 0
    hit_message = ''
    return 'Odświeżenie. Wciśnij cyfrę i spację'


def update_positions():
    """Aktualizuje pozycje elementów na podstawie aktualnych wymiarów okna."""
    global ch_rects, ch_ok_rect, postac_rect, WIDTH, HEIGHT, start_y, x_center

    # Aktualizacja wymiarów
    WIDTH, HEIGHT = screen.get_size()

    # Pozycje kanałów
    total_height = sum(img.get_height() for img in ch_imgs)
    start_y = HEIGHT // 2 - total_height // 2
    ch_rects = []
    x_center = WIDTH // 2
    current_y = start_y
    for img in ch_imgs:
        rect = img.get_rect()
        rect.centerx = x_center
        rect.y = current_y
        ch_rects.append(rect)
        current_y += img.get_height()

    # Pozycja przycisku OK
    ch_ok_rect = ch_ok_img.get_rect()
    ch_ok_rect.centerx = WIDTH // 2
    ch_ok_rect.top = start_y + total_height + 50

    # Pozycja postaci
    postac_rect = postac_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))


# Wywołaj funkcję na początku, aby ustawić początkowe pozycje
update_positions()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            # Obsługa zmiany rozmiaru okna
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            update_positions()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Ignoruj kliknięcia gdy klawisz 's' jest wciśnięty
            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                continue

            mx, my = event.pos
            if state == 'wybor_ch':
                for idx, rect in enumerate(ch_rects, start=1):
                    if rect.collidepoint(mx, my):
                        selected_ch = idx
                        message = f"Wybrano kanał {idx}"
                        break
                if selected_ch and ch_ok_rect.collidepoint(mx, my):
                    state = 'wybor_postaci'
                    message = 'Wybór postaci'

            elif state == 'wybor_postaci':
                if postac_rect.collidepoint(mx, my):
                    state = 'game'
                    message = 'Wciśnij cyfrę 1-9, potem spację'

            elif state == 'display_image':
                mouse_click_count += 1
                clicks.append((mx, my))
                dist = np.hypot(mx - fish_pos[0], mx - fish_pos[1])
                hit_message = 'Trafiono!' if dist <= fish_radius else 'Nie trafiono'
                if mouse_click_count >= 3:
                    message = reset_display()

        elif event.type == pygame.KEYDOWN:
            if state == 'game':
                if event.unicode.isdigit() and '1' <= event.unicode <= '9':
                    selected_num = int(event.unicode)
                elif event.key == pygame.K_SPACE and selected_num:
                    displayed_img = popup_img
                    mouse_click_count = 0
                    clicks = []
                    state = 'display_image'
                    pr = get_popup_rect()
                    fish_pos = [random.randint(pr.left + fish_radius, pr.right - fish_radius),
                                random.randint(pr.top + fish_radius, pr.bottom - fish_radius)]
                    angle = random.uniform(0, 2 * np.pi)
                    fish_dir = [np.cos(angle), np.sin(angle)]
                    frame_counter = 0
                    message = 'Kliknij 3 razy, aby zamknąć'

            elif state == 'wybor_postaci' and event.key == pygame.K_RETURN:
                state = 'game'
                message = 'Wciśnij cyfrę 1-9, potem spację'

    # Ruch ryby
    if state == 'display_image':
        pr = get_popup_rect()
        frame_counter += 1
        fish_speed = 5
        if frame_counter >= change_interval:
            angle = random.uniform(0, 2 * np.pi)
            fish_dir = [np.cos(angle), np.sin(angle)]
            frame_counter = 0
        fish_pos[0] += fish_dir[0] * fish_speed
        fish_pos[1] += fish_dir[1] * fish_speed
        if fish_pos[0] - fish_radius <= pr.left or fish_pos[0] + fish_radius >= pr.right:
            fish_dir[0] *= -1
            fish_pos[0] = max(pr.left + fish_radius, min(pr.right - fish_radius, fish_pos[0]))
        if fish_pos[1] - fish_radius <= pr.top or fish_pos[1] + fish_radius >= pr.bottom:
            fish_dir[1] *= -1
            fish_pos[1] = max(pr.top + fish_radius, min(pr.bottom - fish_radius, fish_pos[1]))

    # Rysowanie
    screen.fill((0, 0, 0))
    if state == 'wybor_ch':
        for img, rect in zip(ch_imgs, ch_rects): screen.blit(img, rect)
        screen.blit(ch_ok_img, ch_ok_rect)
    elif state == 'wybor_postaci':
        screen.blit(postac_img, postac_rect)
    elif state == 'display_image':
        rect = popup_img.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(popup_img, rect)
        pygame.draw.circle(screen, fish_color_rgb, (int(fish_pos[0]), int(fish_pos[1])), fish_radius)
        for cx, cy in clicks:
            pygame.draw.circle(screen, (255, 0, 0), (cx, cy), 5)
    else:
        if displayed_img:
            rect = popup_img.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(popup_img, rect)

    # Komunikaty
    if message:
        text_surf = font.render(message, True, (255,255,255))
        text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT - 30))
        screen.blit(text_surf, text_rect)
    if hit_message:
        hit_surf = font.render(hit_message, True, (255, 255, 255))
        hit_rect = hit_surf.get_rect(center=(WIDTH//2, HEIGHT - 60))
        screen.blit(hit_surf, hit_rect)

    pygame.display.flip()
    clock.tick(60)
