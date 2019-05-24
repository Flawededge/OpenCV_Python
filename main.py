# # Compile code
# pyinstaller -y -i "C:/Users/Ben/PycharmProjects/OpenCV_Python/sausage.ico" --add-data "C:/Users/Ben/PycharmProjects/OpenCV_Python/referenceImage.png";"." "C:/Users/Ben/PycharmProjects/OpenCV_Python/main.py"

# import os
# os.system("pyuic5 mainwindow.ui > mainwindow.py")

import sys  # Forgot where I actually used this, but it's here
from PyQt5 import QtWidgets, QtGui, QtCore  # QT stuff
from mainwindow import Ui_OpenCVThresholder  # Import UI
from cv2 import *  # OpenCV
import processing


class MainPlotGui(Ui_OpenCVThresholder):

    # The class variables which are used to pass things around

    def __init__(self, dialog):  # Initialization function
        # Set up the GUI
        Ui_OpenCVThresholder.__init__(self)
        self.setupUi(dialog)
        # Load the image and put onto the GUI
        # self.process_image()

        # Update timer to occasionally process the image
        self.checkThreadTimer = QtCore.QTimer()
        self.checkThreadTimer.setInterval(1000)  # .5 seconds

        self.checkThreadTimer.timeout.connect(self.process_image)
        self.checkThreadTimer.start(1000)


    def process_image(self):
        importlib.reload(processing)  # Reload the processing file to make testing easier
        self.processedImage, sausages = processing.process(self.inputImage)  # Run the function
        self.processedImage, self.path = processing.path(self.processedImage, sausages)
        self.disp_image(self.processedImage)  # Show final output



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog(flags=(QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint |
                                      QtCore.Qt.WindowCloseButtonHint))

    prog = MainPlotGui(dialog)

    dialog.show()
    sys.exit(app.exec_())
