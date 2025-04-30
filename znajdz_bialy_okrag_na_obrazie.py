import cv2
import numpy as np

def znajdz_okrag(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot load image from {image_path}")
    red_channel = image[:, :, 2]
    _, thresh = cv2.threshold(red_channel, 240, 255, cv2.THRESH_BINARY)
    circles = cv2.HoughCircles(thresh,cv2.HOUGH_GRADIENT,dp=1.2,minDist=20,param1=50,param2=30,minRadius=20,maxRadius=100)
    okrag = np.round(circles[0, :]).astype("int")[0]
    x,y,r=okrag
    return [int(x),int(y),int(r)]

