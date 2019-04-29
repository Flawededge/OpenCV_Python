# The real imports
import sys
from PyQt5 import QtWidgets
from mainwindow import Ui_OpenCVThresholder


class MainPlotGui(Ui_OpenCVThresholder):
    currentImage = "example.png"

    def __init__(self, dialog):
        Ui_OpenCVThresholder.__init__(self)
        self.setupUi(dialog)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()

    prog = MainPlotGui(dialog)

    dialog.show()
    sys.exit(app.exec_())
