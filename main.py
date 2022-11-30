import pretreatment as pt
import matplotlib as plt
import cv2 as cv


img = cv.imread('./images/test.png')
pre_traited_image = pt.init_treatment(cv.imread('./images/test.png'))
objects = pt.extract_object(pre_traited_image,img)
k = pt.main_contour(objects)
cv.imshow("img", pre_traited_image)
cv.waitKey(0)
