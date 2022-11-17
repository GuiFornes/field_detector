import pretreatment as pt
import matplotlib as plt
import cv2 as cv

image = pt.init_treatment(cv.imread('./images/test.png'))
cv.imshow("img", image)
cv.waitKey(0)