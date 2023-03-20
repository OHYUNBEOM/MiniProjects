import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class qtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./PyQt_Practice/calculator.ui',self)


if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())