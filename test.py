import field_detector as fd
import cv2
import numpy as np


def percentage_of_correspondance(image1, image2):
    """
    Returns the percentage of pixels that are the same in both images.
    """
    return np.sum(image1 == image2) / np.prod(image1.shape)


def intersection_on_union(image1, image2):
    """
    Returns the percentage of pixels that are the same in both images.
    """
    return np.sum(np.logical_and(image1, image2)) / np.sum(np.logical_or(image1, image2))


test = [[10, 20, 25, 53, 62, 68, 79, 86, 95, 98, 103, 105, 109, 271, 279, 330],
        [18, 33, 37, 43, 53, 55, 89, 154, 193, 201, 236],
        [1, 11, 15, 72, 96, 150, 163, 167, 208, 217],
        [22, 24, 31, 35]]

detector = fd.FieldDetector(debug=False)
percentages = np.zeros(len(test[0])+len(test[1])+len(test[2])+len(test[3]))
n = 0
for i in range(len(test)):
    for j in test[i]:
        image = cv2.imread("data/log{}/{:0>3}-rgb.png".format(i+1, j))
        target = cv2.imread("mask-field/log{}/{:0>3}-rgb.png".format(i+1, j), 0)
        detector.update(image)
        detector.process()
        percentages[n] = intersection_on_union(detector.get_mask(), target)
        if percentages[n] > 1:
            detector.show_image()
            cv2.imshow('target', target)
            cv2.waitKey(0)
        n += 1



print(percentages)
print("Pourcentage de précision sur {} images de test: {:<3}%".format(n-1, np.mean(percentages)*100))
