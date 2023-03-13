# PyQT와 QR을 활용한 앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * #Qt.white 사용하기 위함
import qrcode #qr코드 사용

# QRCode 커스터마이징 클래스
class Image(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size) -> None:
        self.border=border
        self.width=width
        self.box_size=box_size
        # size 생성
        size = (width+border*2) * box_size

        self._image = QImage(size,size,QImage.Format_RGB8)
        self._image.fill(Qt.white)

    def pixmap(self):
        return QPixmap.fromImage(self._image)

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Python_practice/QrCodeApp.ui',self) #Qt Designer로 만든 ui 사용
        self.setWindowTitle('QrCode 생성앱')
        self.setWindowIcon(QIcon('./Python_practice/qrIcon.png'))

        # 시그널/슬롯
        self.btnQrGen.clicked.connect(self.btnQrGenClicked)
        # 엔터 쳤을때 만들어지게 하기
        self.txtQrData.returnPressed.connect(self.btnQrGenClicked)

    #QR생성하기 버튼 클릭 함수
    def btnQrGenClicked(self):
        data = self.txtQrData.text()

        if data=='': 
            QMessageBox.warning(self,'경고','데이터를 입력하세요') 
            return
        else : 
            qr_img=qrcode.make(data)
            qr_img.save('./Python_practice/site.png')

            img=QPixmap('./Python_practice/site.png')
            self.lblQrCode.setPixmap(QPixmap(img).scaledToWidth(300))


if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())