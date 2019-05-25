# # Compile code
# pyinstaller -y -i "C:/Users/Ben/PycharmProjects/OpenCV_Python/sausage.ico" --add-data "C:/Users/Ben/PycharmProjects/OpenCV_Python/referenceImage.png";"." "C:/Users/Ben/PycharmProjects/OpenCV_Python/main.py"

# import os
# os.system("pyuic5 mainwindow.ui > mainwindow.py")

import sys  # Forgot where I actually used this, but it's here
from PyQt5 import QtWidgets, QtGui, QtCore  # QT stuff
from mainwindow import Ui_PlateFinder  # Import UI
import cv2  # OpenCV
import processing
import importlib
import tkinter as tk  # For file dialog
from tkinter import filedialog


class MainPlotGui(Ui_PlateFinder):
    # The class variables which are used to pass things around
    filePath = "C:/Users/Ben/PycharmProjects/OpenCV_Python/photos/image (3).jpg"
    originImage = None  # To store the input image for on the fly processing

    imagePositions = []

    def __init__(self, dialog):  # Initialization function
        # Set up the GUI
        Ui_PlateFinder.__init__(self)
        self.setupUi(dialog)
        # Load the image and put onto the GUI
        self.originImage = cv2.imread(self.filePath)

        # Update timer to occasionally process the image
        self.checkThreadTimer = QtCore.QTimer()
        self.checkThreadTimer.setInterval(1000)  # 1 second

        self.checkThreadTimer.timeout.connect(self.process_image)
        self.checkThreadTimer.start(1000)

        # Connections to relate buttons to functions
        self.bLoad.pressed.connect(self.load_image)
        self.bClr.pressed.connect(self.clear_plates)

    def process_image(self):
        importlib.reload(processing)  # Reload the processing file to make testing easier
        box_image, plate_image = processing.process(self.originImage)  # Run the function

        self.disp_image(box_image, 0)  # Show final output
        self.disp_image(plate_image, 1)

    def disp_image(self, image, position):  # Display images on screen 0 top, 1 bottom  BGR IMAGE IS EXPECTED!
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        pix = QtGui.QPixmap(QtGui.QImage(image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped())
        # imgIn = QtGui.QImage((uchar *) img.data, img.cols, img.rows, img.step, QImage::Format_RGB888);
        # pix = QtGui.QPixmap(QtGui.QImage(image, image.shape[1], image.shape[0],
        #                                  image.shape[1] * 3, QtGui.QImage.Format_RGB888))
        if position:
            self.plateImg.setPixmap(pix)
        else:
            self.inImg.setPixmap(pix)

    def load_image(self):
        # Create tkinter window then hide
        root = tk.Tk()
        root.withdraw()

        # Get filename and check that it's valid
        user = filedialog.askopenfilename()
        if user[-3:].lower() == "jpg" or user[-3:].lower() == "png":
            self.filePath = user
            self.originImage = cv2.imread(self.filePath)
        else:
            print("No boueno")
            return

        print("Finished")

    def clear_plates(self):
        self.plateList.clear()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog(flags=(QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint |
                                      QtCore.Qt.WindowCloseButtonHint))

    prog = MainPlotGui(dialog)

    dialog.show()
    sys.exit(app.exec_())
