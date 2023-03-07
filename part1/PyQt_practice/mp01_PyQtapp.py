# PyQt 복습 - 직접 디자인 코딩
import sys
from PyQt5.QtWidgets import *

class qtApp(QWidget):
    def __init__(self)-> None:
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.lblMessage = QLabel('메시지: ',self)
        self.lblMessage.setGeometry(10,10,300,50)
        #버튼
        btnok=QPushButton('OK',self)
        btnok.setGeometry(280,250,100,40)
        #PyQt 이벤트 -> 이벤트핸들러가 처리 
        btnok.clicked.connect(self.btnok_clicked)
        #Form
        self.setGeometry(300,200,400,300)
        self.setWindowTitle('QFont')
        self.show()

    def btnok_clicked(self):
        #self.lblMessage.clear()
        self.lblMessage.setText('메시지: OK Clicked!')
        

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=qtApp() # 생성,생성자 호출되면서 initUI 호출
    sys.exit(app.exec_())