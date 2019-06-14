import cv2
import os
import numpy as np

dir = "C:/Users/Ben/Desktop/HAAR/N"
files = os.listdir(dir)
targetWidth = 600


for i in files:
    # print(f"{dir}/{i}")
    try:
        img = cv2.imread(f"{dir}/{i}")
        ratio = img.shape[0] / img.shape[1]
        cv2.resize(img, (600, int(600*ratio)))
        cv2.imwrite(f"{dir}/proc/{i}", img)
        print(f"{dir}/proc/{i}")
    except:
        print("Oh no!")