# Qt Designer 디자인 사용
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from NaverApi import * #만들어둔 NaverApi 클래스 사용
import webbrowser #웹브라우저 모듈(링크연결 등)
from PyQt5.QtGui import *
from urllib.request import urlopen # 빠른 이미지 다운(포스터)

# NaverApiSearch.ui의 동작을 설정하는것

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./PyQt_Practice/NaverApiMovie.ui',self)
        self.setWindowIcon(QIcon('./PyQt_practice/newspaper.png'))
        # 검색버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 텍스트박스에 검색어 입력 후 엔터 처리
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        # 링크 더블클릭
        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked) 
    
    def tblResultDoubleClicked(self): #링크 더블클릭
        selected=self.tblResult.currentRow() #선택한 영화 행
        url=self.tblResult.item(selected,5).text() #네이버 영화 링크 뽑아냄 
        webbrowser.open(url) #해당 링크 연결

    def txtSearchReturned(self): # 검색어 입력 후 엔터쳤을 때 처리 부분
        self.btnSearchClicked()

    def btnSearchClicked(self):
        search=self.txtSearch.text()

        if search=='':
            QMessageBox.warning(self,'경고','영화명을 입력하세요')
            return
        else:
            api=NaverApi() # NaverApi 클래스 객체 생성
            node='movie'
            display=100 #검색결과 100개만 뽑아오겠다는 의미

            result=api.getNaverSearch(node,search,1,display)
            #print(result)

            #QTableWidget에 출력하기
            items=result['items'] # json전체 결과 중 items 아래 배열만 잘라오는 의미 
            self.makeTable(items) # 테이블위젯에 데이터들을 할당한다


    # 테이블 위젯에 데이터 표시 --> 네이버 영화 결과에 맞춰 변경
    def makeTable(self,items) -> None:
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)# 단일선택모드
        self.tblResult.setColumnCount(7) 
        self.tblResult.setRowCount(len(items)) #display값으로 설정하여 나온 결과값 100개 행 생성
        self.tblResult.setHorizontalHeaderLabels(['영화제목','개봉년도','감독',
                                                  '출연진','평점','링크','포스터']) #행 제목 변경
        self.tblResult.setColumnWidth(0,150)
        self.tblResult.setColumnWidth(1,60) #개봉년도
        self.tblResult.setColumnWidth(4,50)
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers) #컬럼데이터 수정금지

        for i,post in enumerate(items): #0,영화
            title=self.replaceHtmlTab(post['title']) # HTMl 특수문자 변환
            pubDate=post['pubDate']
            director = post['director']
            actor = post['actor']
            userRating=post['userRating']
            link=post['link']
            #image=QImage(requests.get(post['image'], stream=True))
            #영화 포스터 넣기
            # imgData=urlopen(post['image']).read()
            # image = QPixmap()
            # image.loadFromData(imgData)
            # imgLabel=QLabel()
            # imgLabel.setPixmap(image)
            # imgLabel.setGeometry(0,0,60,100)
            # imgLabel.resize(60,100)
            #setItem(행,열,넣을데이터)
            self.tblResult.setItem(i,0,QTableWidgetItem(title))
            self.tblResult.setItem(i,1,QTableWidgetItem(pubDate))
            self.tblResult.setItem(i,2,QTableWidgetItem(director))
            self.tblResult.setItem(i,3,QTableWidgetItem(actor))
            self.tblResult.setItem(i,4,QTableWidgetItem(userRating))
            self.tblResult.setItem(i,5,QTableWidgetItem(link))
            # self.tblResult.setCellWidget(i,6,imgLabel)


    # HTMl 특수문자 변환하는 함수
    def replaceHtmlTab(self,sentence) -> str: #->str :함수 끝에서 str을 반환한다는뜻
        #제목에 그대로 출력되는 HTML 기호들을 가독성 좋게 변환
        result=sentence.replace('&lt;', '<').replace('&gt;', '>').replace('<b>', 
        '').replace('</b>', '').replace('&apos;', "'").replace('&quot;', '"') 
        return result

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())