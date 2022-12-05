import cv2 as cv
import numpy as np

kernel = np.ones((2, 2), np.uint8)

#Traitement initiale de l'image
def init_treatment(image):
    # image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) # image in gray levels
    image_blured = cv.GaussianBlur(image, (3, 3), 0)  # image blured
    green_channel = image_blured[:, :, 2]
    green_channel = cv.equalizeHist(green_channel)
    _, treshed = cv.threshold(green_channel, 160, 255, cv.THRESH_BINARY_INV)
    eroded = cv.erode(treshed, kernel, iterations=1)
    dilated = cv.dilate(eroded, kernel, iterations=1)
    return dilated


#Extrait tous les objets blancs de l'image
def extract_object(th, image):
    objects = []
    contours, _ = cv.findContours(th,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    for i in range (0, len(contours)) :
        mask_BB_i = np.zeros((len(th),len(th[0])), np.uint8)
        x,y,w,h = cv.boundingRect(contours[i])
        cv.drawContours(mask_BB_i, contours, i, (255,255,255), -1)
        BB_i=cv.bitwise_and(image,image,mask=mask_BB_i)
        if h >15 and w>15 :
            BB_i=BB_i[y:y+h,x:x+w]
            objects.append(BB_i)
            cv.imwrite("./obj/BB_"+str(i)+".png",BB_i)
    return objects

#Selectionne le plus gros contour
def main_contour(objects):
    index = 0
    sizes = []
    for k in objects:
        size = k.shape[0]*k.shape[1]
        sizes.append(size)
    index = max(sizes)
    return objects[index]