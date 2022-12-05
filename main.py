import time

import cv2
import field_detector as fd


# detector = fd.FieldDetector(cv2.imread('data/log1/001-rgb.png'), debug=True)
# masked = detector.process()
# cv2.imshow('masked', masked)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

for i in range(1, 375):
    image = cv2.imread("data/log1/{:0>3}-rgb.png".format(i))
    detector = fd.FieldDetector(image)
    masked = detector.process()
    cv2.imshow('mask', masked)
    cv2.waitKey(1)
    time.sleep(0.01)
cv2.destroyAllWindows()
