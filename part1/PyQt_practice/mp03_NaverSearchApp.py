# Qt Designer 디자인 사용
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from NaverApi import * #만들어둔 NaverApi 클래스 사용

# NaverApiSearch.ui의 동작을 설정하는것

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./PyQt_Practice/NaverApiSearch.ui',self)
        # 검색버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 텍스트박스에 검색어 입력 후 엔터를 치면 처리하는 부분
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)

    
    def btnSearchClicked(self):
        search=self.txtSearch.text()

        if search=='':
            QMessageBox.warning(self,'경고','검색어를 입력하세요')
            return
        else:
            api=NaverApi() # NaverApi 클래스 객체 생성
            node='news'
            outputs=[] # 검색 후 결과를 담을 리스트 변수
            display=100

            result=api.getNaverSearch(node,search,1,display)
            #print(result)

            #listView에 출력하기
            while result != None and result['display']!=0:
                for post in result['items']: #사용자가 입력하는 검색어의 결과의 items부분만큼
                    api.getPostData(post,outputs) #NaverApi Class에서 받아서 처리함
    

    def txtSearchReturned(self): # 검색어 입력 후 엔터쳤을 때 처리 부분
        self.btnSearchClicked()

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())