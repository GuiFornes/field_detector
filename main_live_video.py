import cv2
import field_detector as fd
import time
import sys
import os

if len(sys.argv) > 1:
    folder = sys.argv[1]
else:
    print("Usage: python3 main_live_video.py <path_to_image_folder>\ntaking data/log1/ as default")
    folder = 'data/log1/'

# number of images in folder
num_images = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])

# processing each images in folder
for i in range(1, num_images):
    image = cv2.imread(folder + "/{:0>3}-rgb.png".format(i))
    detector = fd.FieldDetector(image)
    masked = detector.process()
    cv2.imshow('mask', masked)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quitting... image number {}".format(i))
        break
    time.sleep(0.1)
cv2.destroyAllWindows()
