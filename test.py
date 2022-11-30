import cv2
import numpy as np
from matplotlib import pyplot as plt

KERNEL = np.ones((5, 5), np.uint8)
LOWER_BOUND, UPPER_BOUND = (28, 30, 40), (67, 228, 144)

def color_filter(image_bgr, lower_bound, upper_bound):
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    mask_ = cv2.inRange(hsv, lower_bound, upper_bound)
    return cv2.bitwise_and(image_bgr, image_bgr, mask=mask_)


def equalize_hist(image_bgr):
    """ Equalize histogram of the image, does it work ? """
    image_yuv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YUV)
    image_yuv[:, :, 0] = cv2.equalizeHist(image_yuv[:, :, 0])
    return cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)


def show_histogram(image_bgr):
    """ Show histogram of the given image """
    plt.hist(image_bgr.ravel(), 256, [0, 256])
    plt.show()


def mask_generator(image_bgr):
    green = color_filter(image_bgr,  LOWER_BOUND, UPPER_BOUND)
    thresh = np.where(green > 0, 255, 0).astype(np.uint8)
    tmp = cv2.dilate(thresh, KERNEL, iterations=1)
    tmp = cv2.erode(tmp, KERNEL, iterations=1)
    tmp = cv2.erode(tmp, KERNEL, iterations=1)
    green_mask = cv2.dilate(tmp, KERNEL, iterations=1)
    return green_mask, thresh, green


def isolate_largest_contour(mask):
    """ Isolate the largest contour in the mask """
    # Need to change the mask format !
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None
    return cv2.drawContours(mask, [max(contours, key=cv2.contourArea)], -1, (0, 255, 0), -1)

img = cv2.imread('./data/log1/001-rgb.png')
img = cv2.GaussianBlur(img, (3, 3), 0)
mask, thr, img_green = mask_generator(img)
# final_mask = isolate_largest_contour(mask)

cv2.imshow('frame', img)
cv2.imshow('green', img_green)
cv2.imshow('thresh', thr)
cv2.imshow('mask', mask)
# cv2.imshow('final_mask', final_mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
