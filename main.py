# # Compile code
# pyinstaller -y -w -i "C:/Users/Ben/PycharmProjects/OpenCV_Python/example.ico" --add-data "C:/Users/Ben/PycharmProjects/OpenCV_Python/example.png";"." --add-data "C:/Users/Ben/PycharmProjects/OpenCV_Python/HSV.png";"." "C:/Users/Ben/PycharmProjects/OpenCV_Python/main.py"

import os
os.system("pyuic5 mainwindow.ui > mainwindow.py")

import importlib
import sys  # Forgot where I actually used this, but it's here
from PyQt5 import QtWidgets, QtGui, QtCore  # QT stuff
from mainwindow import Ui_OpenCVThresholder  # Import UI
from cv2 import *  # OpenCV
import tkinter as tk            # For file dialog
from tkinter import filedialog  # For file dialog
import processing
import numpy as np


class MainPlotGui(Ui_OpenCVThresholder):

    # The class variables which are used to pass things around
    currentFilename = "referenceImage.png"
    inputImage = None
    processedImage = None
    loading = 0
    path = None

    def __init__(self, dialog):  # Initialization function
        # Set up the GUI
        Ui_OpenCVThresholder.__init__(self)
        self.setupUi(dialog)
        # Load the image and put onto the GUI
        self.load_image()
        self.process_image()

        # Update timer to occasionally process the image
        self.checkThreadTimer = QtCore.QTimer()
        self.checkThreadTimer.setInterval(1000)  # .5 seconds

        self.checkThreadTimer.timeout.connect(self.process_image)
        self.checkThreadTimer.start(1000)

        # Connecting GUI elements to functions
        self.bLoad.pressed.connect(self.load_file)
        self.bSave.pressed.connect(self.save_file)

    def process_image(self):
        importlib.reload(processing)  # Reload the processing file to make testing easier
        self.processedImage, sausages = processing.process(self.inputImage)  # Run the function
        self.processedImage, self.path = processing.path(self.processedImage, sausages)
        self.disp_image(self.processedImage, 1)  # Show final output

    def load_image(self):  # Loads image from a filename
        if not (self.currentFilename.endswith('.png') or self.currentFilename.endswith('.jpg')):
            print("Incorrect file type!")
            return
        print(f"Loading '{self.currentFilename}'")
        self.inputImage = imread(self.currentFilename, IMREAD_COLOR)  # Load the image
        self.disp_image(cvtColor(self.inputImage, COLOR_BGR2RGB), 0)  # Display the image on the left side
        self.process_image()  # Process the image, which displays it on the right

    def disp_image(self, image, window):  # Shows the given image on 0 (input) or 1 (output)
        pix = QtGui.QPixmap(QtGui.QImage(image, image.shape[1], image.shape[0],
                                         image.shape[1] * 3, QtGui.QImage.Format_RGB888))
        if window:
            self.outImage.setPixmap(pix)
        else:
            self.inImage.setPixmap(pix)

    def load_file(self):  # Opens a file dialog to get a filename
        if self.loading:
            return
        self.loading = 1

        root = tk.Tk()
        root.withdraw()
        self.currentFilename = filedialog.askopenfilename()
        self.load_image()
        self.loading = 0

    def save_file(self):  # Saves the processedImage to output.png
        imwrite("output.png", self.processedImage)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog(flags=(QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint |
                                      QtCore.Qt.WindowCloseButtonHint))

    prog = MainPlotGui(dialog)

    dialog.show()
    sys.exit(app.exec_())
