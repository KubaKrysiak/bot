import cv2
import numpy as np


def znajdz_okrag(image_path):
    """
    Find the first circle in the image and return its coordinates as standard integers.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot load image from {image_path}")

    red_channel = image[:, :, 2]
    _, thresh = cv2.threshold(red_channel, 240, 255, cv2.THRESH_BINARY)
    circles = cv2.HoughCircles(
        thresh,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=20,
        param1=50,
        param2=30,
        minRadius=20,
        maxRadius=100
    )

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        okrag = circles[0]
        x, y, r = okrag
        return [int(x), int(y), int(r)]

    return None


def draw_circle_on_image(image_path, output_path):
    """
    Draw a circle on the image based on the coordinates returned by znajdz_okrag function.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path to save the output image with the circle drawn.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot load image from {image_path}")

    # Find the circle
    circle_info = znajdz_okrag(image_path)

    if circle_info is not None:
        x, y, r = circle_info
        # Draw the circle on the image
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)  # Green circle with thickness 2
        cv2.circle(image, (x, y), 2, (0, 0, 255), 3)  # Red center with thickness 3

        # Save or display the result
        cv2.imwrite(output_path, image)
        cv2.imshow("Detected Circle", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No circle was detected.")


# Example usage
input_image_path = r"C:\Users\kurwa cholera jasna\Pictures\Screenshots\Zrzut ekranu 2024-08-27 021909.png"
output_image_path = r"C:\Users\kurwa cholera jasna\Pictures\Screenshots\output_image_with_circle.png"
draw_circle_on_image(input_image_path, output_image_path)
