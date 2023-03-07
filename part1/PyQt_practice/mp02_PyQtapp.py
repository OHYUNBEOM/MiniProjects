# Qt Designer 디자인 사용
import sys
from PyQt5 import QtGui,uic,QtWidgets
from PyQt5.QtWidgets import *
class qtApp(QWidget):

    count=0#버튼클릭횟수

    def __init__(self):
        super().__init__()
        uic.loadUi('./PyQt_Practice/mainApp.ui',self)

        #Qt Designer에서 구상한 위젯 시그널 만듬
        self.btnok.clicked.connect(self.btnokClicked)
        self.btnpop.clicked.connect(self.btnpopClicked)
    
    def btnokClicked(self) : #슬롯함수
        self.count+=1
        self.lblMessage.clear()
        self.lblMessage.setText(f'메시지: OK Clicked! 버튼클릭횟수: {self.count}')
    
    def btnpopClicked(self):
        QMessageBox.about(self,'popup','까꿍')

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())