import cv2
import field_detector as fd
import time
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("Usage: python3 main.py <image_path>\ntaking data/log1/001-rgb.png as default")
    filename = 'data/log4/031-rgb.png'

detector = fd.FieldDetector(cv2.imread(filename), debug=True)
masked = detector.process()
detector.show_image()
cv2.imshow('masked', masked)
cv2.waitKey(0)
cv2.destroyAllWindows()
