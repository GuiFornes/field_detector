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

    def __init__(self, image=None, debug=False):
        self.original = None
        self.image = None
        self.mask = None
        if image is not None:
            self.update(image)
        self.debug = debug

    def show_image(self):
        """ display different steps of the process """
        cv2.imshow('original', self.original)
        cv2.moveWindow('original', 0, 0)
        cv2.imshow('current', self.image)
        cv2.moveWindow('current', 0, 1000)
        cv2.imshow('mask', self.mask)
        cv2.moveWindow('mask', 1000, 0)

    def __show_image(self):
        """ private method tho show image when debug is True """
        if self.debug:
            self.show_image()
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def __pre_process(self):
        """ apply preprocessing to the image"""
        self.image = cv2.GaussianBlur(self.image, (3, 3), 0)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.image[:, :, 1] = cv2.equalizeHist(self.image[:, :, 1])
        self.image = cv2.cvtColor(self.image, cv2.COLOR_HSV2BGR)

    def __green_mask(self):
        """ threshold the image to keep only green pixels """
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound)
        self.mask = cv2.dilate(self.mask, self.kernel, iterations=1)
        self.mask = cv2.erode(self.mask, self.kernel, iterations=1)
        self.mask = cv2.erode(self.mask, self.kernel, iterations=2)
        self.mask = cv2.dilate(self.mask, self.kernel, iterations=2)

        # filling holes totally surrounded by the detected field.
        # tmp = cv2.copyMakeBorder(self.mask, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
        # tmp = cv2.floodFill(tmp, None, (0, 0), 255)[1]
        # tmp_inv = cv2.bitwise_not(tmp)
        # self.mask = self.mask | tmp_inv[1:-1, 1:-1]

    def __isolate_field(self):
        """ isolate the field from the image """
        _, labels = cv2.connectedComponents(self.mask)

        # find the biggest connected component
        largest_label = np.argmax(np.bincount(labels.flat)[1:]) + 1
        self.mask = np.where(labels == largest_label, 255, 0).astype(np.uint8)

        # find the second biggest and select it too if it is big enough
        if len(np.unique(labels)) > 2:
            areas = np.bincount(labels.flatten())
            areas[0] = 0
            second_biggest = np.argsort(areas)[-2]
            if areas[second_biggest] > 5000:
                self.mask = np.where(labels == second_biggest, 255, self.mask).astype(np.uint8)
                # draw a straight line between the two biggest areas

        # find and fill the convexe hull of the field
        hull_list = []
        contours, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            hull_list.append(cv2.convexHull(contours[i]))
        cv2.drawContours(self.mask, hull_list, -1, 255, -1)

        # if 2 convex hulls have common points, it will join them into new complete convex hull
        if len(contours) > 1:
            contours, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # find moment of 2 biggest areas
            moments = [cv2.moments(contours[i]) for i in range(len(contours))]
            # draw a line between the 2 points
            for i in range(len(contours)):
                for j in range(i + 1, len(contours)):
                    # find the center of each area
                    center_i = (int(moments[i]['m10'] / moments[i]['m00']),
                                int(moments[i]['m01'] / moments[i]['m00']))
                    center_j = (int(moments[j]['m10'] / moments[j]['m00']),
                                int(moments[j]['m01'] / moments[j]['m00']))
                    # draw a line between the 2 centers
                    cv2.line(self.mask, center_i, center_j, 255, 5)

            contours, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            hull = cv2.convexHull(contours[0])
            cv2.drawContours(self.mask, [hull], -1, 255, -1)

    def get_mask(self):
        return self.mask

    def update(self, image):
        self.original = image
        self.image = image.copy()
        self.mask = np.zeros(image.shape[:2], np.uint8)

    def process(self):
        if self.debug:
            print("Pre-processing...")
        self.__pre_process()
        if self.debug:
            self.__show_image()
            print("Thresholding green color...")
        self.__green_mask()
        if self.debug:
            self.__show_image()
            print("Isolating football field...")
        self.__isolate_field()
        # self.__show_image()
        return cv2.bitwise_and(self.original, self.original, mask=self.mask)

