# This is here so it can be retroactively loaded
import cv2
from copy import deepcopy
from copy import copy
import pytesseract
from PIL import Image


def process(img):
    img = copy(img)
    liPlate_cascade = cv2.CascadeClassifier('cascade.xml')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    liplates = liPlate_cascade.detectMultiScale(gray, 1.01, 7)

    for (x, y, w, h) in liplates:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    r = liplates[0]
    lic_image = deepcopy(img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])])
    # lic_image = cv2.cvtColor(lic_image, cv2.COLOR_BGR2GRAY)



    # frame_hsl = cv2.cvtColor(box_image, cv2.COLOR_BGR2HLS)
    # frame_threshold = cv2.inRange(frame_hsl, (0, 136, 0), (255, 221, 255))

    # final_image = cv2.cvtColor(, cv2.COLOR_GRAY2BGR)  # done when licence plate has been found
    box_image = img

    liplate_detect = pytesseract.image_to_string(lic_image)

    print(liplate_detect)

    return box_image, lic_image
