import numpy as np
import cv2


class FieldDetector:
    # lower_bound = (28, 30, 40)
    # upper_bound = (67, 228, 144)
    # lower_bound = (24, 62, 31)
    # upper_bound = (63, 255, 208)
    # lower_bound = (27, 50, 31)
    # upper_bound = (64, 199, 129)
    # HSV equalized bounds :
    lower_bound = (26, 6, 30)
    upper_bound = (60, 240, 150)
    kernel = np.ones((5, 5), np.uint8)

    def __init__(self, image, debug=False):
        self.original = image
        self.image = image.copy()
        self.debug = debug
        self.mask = np.zeros(image.shape[:2], np.uint8)

    def show_image(self):
        if self.debug:
            cv2.imshow('original', self.original)
            cv2.moveWindow('original', 0, 0)
            cv2.imshow('current', self.image)
            cv2.moveWindow('current', 0, 1000)
            cv2.imshow('mask', self.mask)
            cv2.moveWindow('mask', 1000, 0)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def __pre_process(self):
        self.image = cv2.GaussianBlur(self.image, (3, 3), 0)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.image[:, :, 1] = cv2.equalizeHist(self.image[:, :, 1])
        self.image = cv2.cvtColor(self.image, cv2.COLOR_HSV2BGR)

    def __green_mask(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound)
        self.mask = cv2.dilate(self.mask, self.kernel, iterations=1)
        self.mask = cv2.erode(self.mask, self.kernel, iterations=1)
        self.mask = cv2.erode(self.mask, self.kernel, iterations=1)
        self.mask = cv2.dilate(self.mask, self.kernel, iterations=1)

    def __isolate_field(self):
        _, labels = cv2.connectedComponents(self.mask)
        largest_label = np.argmax(np.bincount(labels.flat)[1:]) + 1
        self.mask = np.where(labels == largest_label, 255, 0).astype(np.uint8)

    def get_mask(self):
        return self.mask

    def update(self, image):
        self.original = image
        self.image = image.copy()
        self.mask = np.zeros(image.shape[:2], np.uint8)

    def process(self):
        self.__pre_process()
        self.show_image()
        self.__green_mask()
        self.show_image()
        self.__isolate_field()
        self.show_image()
        return cv2.bitwise_and(self.original, self.original, mask=self.mask)

