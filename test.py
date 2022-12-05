import field_detector as fd
import cv2
import numpy as np


def percentage_of_correspondance(image1, image2):
    """
    Returns the percentage of pixels that are the same in both images.
    """
    return np.sum(image1 == image2) / np.prod(image1.shape)


test = [10, 20, 25, 53, 62, 68, 79, 86, 95, 98, 103, 105, 109, 271, 279, 330]

detector = fd.FieldDetector(cv2.imread('bounds_test.png'), debug=False)
perc = np.zeros(len(test))
n = 0
for i in test:
    image = cv2.imread("data/log1/{:0>3}-rgb.png".format(i))
    target = cv2.imread("mask-field/log1/{:0>3}-rgb.png".format(i), 0)
    detector.update(image)
    detector.process()
    perc[n] = percentage_of_correspondance(detector.get_mask(), target)
    n += 1

print(perc)
print("Pourcentage de précision sur 16 images de test: {}".format(np.mean(perc)))
