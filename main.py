# # Compile code
# pyinstaller -y -w -i "C:/Users/Ben/PycharmProjects/OpenCV_Python/example.ico" --add-data "C:/Users/Ben/PycharmProjects/OpenCV_Python/example.png";"." --add-data "C:/Users/Ben/PycharmProjects/OpenCV_Python/HSV.png";"." "C:/Users/Ben/PycharmProjects/OpenCV_Python/main.py"

import sys  # Forgot where I actually used this, but it's here
from PyQt5 import QtWidgets, QtGui  # QT stuff
from mainwindow import Ui_OpenCVThresholder  # Import UI
import cv2  # OpenCV
import tkinter as tk            # For file dialog
from tkinter import filedialog  # For file dialog


class MainPlotGui(Ui_OpenCVThresholder):

    # The class variables which are used to pass things around
    currentImage = "example.png"
    curFileImage = None
    mask = None
    loading = 0

    def __init__(self, dialog):
        Ui_OpenCVThresholder.__init__(self)  # Set up the GUI
        self.setupUi(dialog)

        self.lColorBar.setPixmap(QtGui.QPixmap("HSV.png"))  # For the pretty bar in the middle of the interface

        self.load_image()  # Load the image and put onto the GUI
        self.update_outline()

        # Connecting GUI elements to functions
        self.sLower.sliderMoved.connect(self.upper_slider)  # Attach sliders to update the input image
        self.sUpper.sliderMoved.connect(self.lower_slider)
        self.bClear.pressed.connect(self.clear_mask)  # Attach clearing
        self.bAdd.pressed.connect(self.add_mask)
        self.bLoad.pressed.connect(self.load_file)
        self.bSave.pressed.connect(self.save_file)

    def load_image(self):  # Loads image from a filename
        if not (self.currentImage.endswith('.png') or self.currentImage.endswith('.jpg')):
            print("Incorrect file type!")
            return
        print(f"Loading '{self.currentImage}'")
        self.curFileImage = cv2.imread(self.currentImage)  # Load the image
        self.mask = None
        self.curFileImage = cv2.cvtColor(self.curFileImage, cv2.COLOR_BGR2HSV)  # Convert to HSV
        self.disp_image(self.curFileImage, 0)  # Display the image on the left side

    def disp_image(self, image, window):  # Shows the given image on 0 (input) or 1 (output)
        image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)  # Convert to RGB to display
        pix = QtGui.QPixmap(QtGui.QImage(image, image.shape[1], image.shape[0],
                                         image.shape[1] * 3, QtGui.QImage.Format_RGB888))
        if window:
            self.outImage.setPixmap(pix)
        else:
            self.inImage.setPixmap(pix)

    def upper_slider(self):  # Function to keep the slider values consistent
        if self.sLower.value() > self.sUpper.value():
            self.sUpper.setValue(self.sLower.value())
        self.update_outline()

    def lower_slider(self):  # Function to keep the slider values consistent
        if self.sLower.value() > self.sUpper.value():
            self.sLower.setValue(self.sUpper.value())
        self.update_outline()

    def update_outline(self, update_global=0):
        thresh = cv2.inRange(self.curFileImage, (self.sLower.value(), 0, 0), (self.sUpper.value(), 255, 255))  # Threshold image

        if update_global:  # If add button was pressed
            if update_global == 1:
                if self.mask is None:  # If no global mask currently exists
                    self.mask = thresh  # Set global mask
                else:  # If there is a global mask
                    self.mask = cv2.bitwise_or(thresh, self.mask)  # Do a bitwise or to add the current mask to the global one

            tmp = cv2.bitwise_and(self.curFileImage, self.curFileImage, mask=self.mask)  # Use the global mask to generate image
            self.disp_image(tmp, 1)  # Display the image on the output panel

        tmp = cv2.bitwise_and(self.curFileImage, self.curFileImage, mask=thresh)  # Use the current mask to generate image
        self.disp_image(tmp, 0)  # Display the image on the input panel

    def clear_mask(self):
        self.mask.fill(0)
        self.update_outline(2)

    def add_mask(self):
        self.update_outline(1)

    def load_file(self):
        if self.loading:
            return
        self.loading = 1

        root = tk.Tk()
        root.withdraw()
        self.currentImage = filedialog.askopenfilename()
        self.load_image()
        self.loading = 0

    def save_file(self):
        tmp = cv2.bitwise_and(self.curFileImage, self.curFileImage, mask=self.mask)
        tmp = cv2.cvtColor(tmp, cv2.COLOR_HSV2BGR)  # Convert to RGB to save
        cv2.imwrite("output.png", tmp)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()

    prog = MainPlotGui(dialog)

    dialog.show()
    sys.exit(app.exec_())
