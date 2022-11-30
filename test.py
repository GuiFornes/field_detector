import cv2
import numpy as np
from matplotlib import pyplot as plt

KERNEL = np.ones((5, 5), np.uint8)
LOWER_BOUND, UPPER_BOUND = (28, 30, 40), (67, 228, 144)


def color_filter(image_bgr, lower_bound, upper_bound):
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, lower_bound, upper_bound)


def equalize_hist(image_bgr):
    """ Equalize histogram of the image, does it work ? """
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    image_hsv[:, :, 0] = cv2.equalizeHist(image_hsv[:, :, 0])
    return cv2.cvtColor(image_hsv, cv2.COLOR_YUV2BGR)


def show_histogram(image_bgr):
    """ Show histogram of the given image """
    plt.hist(image_bgr.ravel(), 256, [0, 256])
    plt.show()


def mask_generator(image_bgr):
    mask = color_filter(image_bgr, LOWER_BOUND, UPPER_BOUND)
    tmp = cv2.dilate(mask, KERNEL, iterations=1)
    tmp = cv2.erode(tmp, KERNEL, iterations=1)
    tmp = cv2.erode(tmp, KERNEL, iterations=1)
    green_mask = cv2.dilate(tmp, KERNEL, iterations=1)
    return green_mask


def isolate_field(mask):
    """ Isolate the largest contour in the mask """
    # Need to change the mask format !
    _, labels = cv2.connectedComponents(mask)
    largest_label = np.argmax(np.bincount(labels.flat)[1:]) + 1
    return np.where(labels == largest_label, 255, 0).astype(np.uint8)


img = cv2.imread('./data/log1/001-rgb.png')
img = cv2.GaussianBlur(img, (3, 3), 0)
green_mask = mask_generator(img)
field_mask = isolate_field(green_mask)

cv2.imshow('frame', img)
cv2.imshow('mask', green_mask)
cv2.imshow('green', field_mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
