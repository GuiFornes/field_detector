#niveau de gris
#flou
#seuillage par couleur
import cv2 as cv
import numpy as np

kernel = np.ones((2,2),np.uint8)
kernel1 = np.ones((5,5),np.uint8)
def init_treatment(image):
    #image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) # image in gray levels
    #img = cv.cvtColor(image,cv.COLOR_BGR2HSV)

    image_blured = cv.GaussianBlur(image,(5,5),0) # image blured
    green_channel = image_blured[:,:,2]
    green_channel = cv.equalizeHist(green_channel)
    _, treshed = cv.threshold(green_channel, 160, 255, cv.THRESH_BINARY_INV)
    dilated = cv.dilate(treshed,kernel, iterations=1)
    eroded = cv.erode(dilated,kernel, iterations=1)
    # eroded = cv.erode(treshed,kernel1, iterations=1)
    # dilated = cv.dilate(eroded,kernel1, iterations=1)
   

    return eroded
    
