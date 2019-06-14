# This is here so it can be retroactively loaded
import cv2
import pytesseract
from PyQt5.QtGui import QGuiApplication
from numpy import arange
import itertools
import operator

from PIL import Image


def process(self, image):
    print("Process started → ", end='')  # Output for debug

    # pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\Tesseract.exe"  # Setup pytesseract

    print("Cascade → ", end='')  # Run the cascade classifier
    liPlate_cascade = cv2.CascadeClassifier('cascade.xml')  # Run the cascade
    pixWid = 1000
    scale = pixWid/image.shape[0]
    image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to greyscale for the cascade
    # print(scale, end='')
    liplates = liPlate_cascade.detectMultiScale(gray, 1.01, 7)  # Run the cascade

    print("Tesseract|", end="")  # Detect the contents of each detected region
    workingImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detected = []
    out_image = None
    # expandAmount = 0.03
    for expandAmount in arange(0.03, -0.01, -0.002):
        for (x, y, w, h) in liplates:
            x -= int(pixWid*expandAmount)
            y -= int(pixWid*expandAmount)
            w += int(pixWid*expandAmount*2)
            h += int(pixWid*expandAmount*2)
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            lic_image = workingImage[int(y):int(y + h), int(x):int(x + w)]  # Crop the current square
            lic_image = cv2.adaptiveThreshold(lic_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 2)

            cur = (pytesseract.image_to_string(lic_image))
            remove = "!@#$%^&*(){'`~}|\\[‘]=—-:;',./_ \n"
            for i in remove:
                cur = cur.replace(i, '')
            self.disp_image(cv2.cvtColor(lic_image, cv2.COLOR_GRAY2BGR), 1)
            self.disp_image(image, 0)  # Show final output
            QGuiApplication.processEvents()
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            if len(cur) < 3:
                continue
            print(f"{cur}|", end='')
            detected.append(cur)

    if len(detected) > 0:
        mostCommon = most_common(detected)
        print(f" → {mostCommon} → ", end='')
    else:
        print("→ Nothing found → ", end='')
    #     if len(detected) > 0:
    #         out_image = copy(workingImage[int(y):int(y + h), int(x):int(x + w)])
    #         break
    #
    # if out_image is None:
    #     x, y, w, h = liplates[0]
    #     out_image = copy(image[int(y):int(y + h), int(x):int(x + w)])

    # out_image = cv2.cvtColor(out_image, cv2.COLOR_GRAY2BGR)

    print(" Processing done!")
    return image

def most_common(L):
    # get an iterable of (item, iterable) pairs
    SL = sorted((x, i) for i, x in enumerate(L))
    # print 'SL:', SL
    groups = itertools.groupby(SL, key=operator.itemgetter(0))
    # auxiliary function to get "quality" for an item

    def _auxfun(g):
        item, iterable = g
        count = 0
        min_index = len(L)
        for _, where in iterable:
            count += 1
            min_index = min(min_index, where)
        # print 'item %r, count %r, minind %r' % (item, count, min_index)
        return count, -min_index
    # pick the highest-count/earliest item
    return max(groups, key=_auxfun)[0]