import cv2
import numpy as np


def find_template_matches(image_path, template_path, scales=[0.5, 0.75, 1.0, 1.25, 1.5], threshold=0.8):
    # Wczytanie obrazu głównego i wzorca
    image = cv2.imread(image_path)
    template = cv2.imread(template_path)

    # Lista do przechowywania współrzędnych środków prostokątów
    centers = []

    for scale in scales:
        # Skalowanie obrazu referencyjnego
        resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

        # Dopasowanie wzorca
        result = cv2.matchTemplate(image, resized_template, cv2.TM_CCOEFF_NORMED)

        # Ustalenie progu dopasowania
        locations = np.where(result >= threshold)

        # Obliczanie współrzędnych środków prostokątów i dodawanie ich do listy
        for pt in zip(*locations[::-1]):
            center_x = pt[0] + resized_template.shape[1] // 2
            center_y = pt[1] + resized_template.shape[0] // 2
            centers.append([center_x, center_y])

    return centers


# Przykładowe użycie:
image_path = r"C:\Users\kurwa cholera jasna\Pictures\Screenshots\Zrzut ekranu 2024-08-27 164914.png"
template_path = r"C:\Users\kurwa cholera jasna\Pictures\Screenshots\Zrzut ekranu 2024-08-27 165025.png"
coordinates = find_template_matches(image_path, template_path)

# Wyświetlenie wyników
print(coordinates)
