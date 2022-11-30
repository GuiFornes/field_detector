import cv2
import numpy as np
from matplotlib import pyplot as plt

kernel = np.ones((5, 5), np.uint8)


def color_filter(image, lower_bound, upper_bound):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    return cv2.bitwise_and(image, image, mask=mask)


img = cv2.imread('./data/log1/001-rgb.png')
img = cv2.GaussianBlur(img, (3, 3), 0)

# Equalizing histogramme, does it work ?
# cv2.imshow('frame', img)
# plt.hist(img.ravel(), 256, [0, 256])
# plt.show()
# img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
# print(img[1:10, 1:10, 0])
# channels = cv2.split(img)
# cv2.equalizeHist(channels[0])
# img = cv2.merge(channels)
# print(img[1:10, 1:10, 0])

# img = cv2.cvtColor(img, cv2.COLOR_YCrCb2BGR)
# plt.hist(img.ravel(), 256, [0, 256])
# plt.show()
# cv2.imshow('frame equalized', img)
# cv2.waitKey(0)


green = color_filter(img, (28, 30, 40), (67, 228, 144))
thresh = np.where(green > 0, 255, 0).astype(np.uint8)
tmp = cv2.dilate(thresh, kernel, iterations=1)
tmp = cv2.erode(tmp, kernel, iterations=1)
tmp = cv2.erode(tmp, kernel, iterations=1)
mask = cv2.dilate(tmp, kernel, iterations=1)
print(type(mask[0][0]))
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# cv2.drawContours(mask, [max(contours, key=cv2.contourArea)], -1, (0, 255, 0), -1)
cv2.imshow('frame', img)
cv2.imshow('green', green)
cv2.imshow('thresh', thresh)
cv2.imshow('final_mask', mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
