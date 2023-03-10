# 주소록 GUI 프로그램 - MySQL 연동
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymysql

class qtApp(QMainWindow):
    conn=None
    curIdx = 0 # 고유 키 값(PK)을 담을 변수

    def __init__(self):
        super().__init__()
        uic.loadUi('./PyQt_Practice/addressBook.ui',self)
        self.setWindowIcon(QIcon('./PyQt_practice/address-book.png'))

        self.initDB() #DB 초기화
        
        #버튼 시그널/슬롯함수 작성
        self.btnNew.clicked.connect(self.btnNewClicked) # 신규 버튼 처리하는 함수 
        self.btnSave.clicked.connect(self.btnSaveClicked) # 저장 버튼 처리하는 함수
        self.tblAddress.doubleClicked.connect(self.tblAddressDoubleClicked) # 주소록 클릭 시 처리되는 함수
        self.btnDel.clicked.connect(self.btnDelClicked)

    # 신규 버튼 누름
    def btnNewClicked(self):
        #LineEdit 내용 삭제 후 이름에 포커스
        self.txtName.setText('')
        self.txtPhone.setText('')
        self.txtEmail.setText('')
        self.txtAddress.setText('')
        self.txtName.setFocus()
        self.curIdx =0 # 신규 등록

    # 저장 버튼 누름
    def btnSaveClicked(self):
        fullName=self.txtName.text()
        phoneNum = self.txtPhone.text()
        email=self.txtEmail.text()
        address=self.txtAddress.text()
        # 이름/전화번호 : not null이기에 입려하지 않으면 경고
        if fullName=='' or phoneNum=='':
            QMessageBox.warning(self,'주의','이름과 휴대폰 번호를 입력하세요')
            return # 진행불가
        else:
            #DB 사용
            self.conn=pymysql.connect(host='localhost',user='root',password='12345',
                                  db='miniproject',charset='utf8')
            
            if self.curIdx ==0: #신규 입력인 경우의 처리
            # lineEdit에 사용자가 입력하는값 받아서 쿼리문으로 DB에 INSERT
                query = '''
                INSERT INTO addressbook (FullName,PhoneNum,Email,Address)
                                VALUES(%s,%s,%s,%s)
                '''
            else:
                query = ''' UPDATE addressbook
                            SET FullName = %s
                                , PhoneNum = %s
                                , Email = %s
                                , Address = %s
                            WHERE idx = %s '''
                         # UPDATE 쿼리문

            cur=self.conn.cursor()

            if self.curIdx==0: #신규 등록인 경우 원래대로 
                cur.execute(query,(fullName,phoneNum,email,address))
            else: #업데이트의 경우 행의 고유 키값 curIdx 받아와야함
                cur.execute(query,(fullName,phoneNum,email,address,self.curIdx))

            self.conn.commit()
            self.conn.close()

            #저장 성공 메시지
            if self.curIdx==0:
                QMessageBox.about(self,'성공','INSERT Completed')
            else:
                QMessageBox.about(self,'성공','Update Completed')
            # QTableWidget에 Insert 된 데이터 출력
            self.initDB()
            # textbox 입력창 내용 지우기
            self.btnNewClicked()


    # 주소록 내용 더블 클릭시 해당 내용이 textbox에도 들어갈 수 있도록
    def tblAddressDoubleClicked(self):
            rowIndex=self.tblAddress.currentRow() #행번호
            self.txtName.setText(self.tblAddress.item(rowIndex,1).text())
            self.txtPhone.setText(self.tblAddress.item(rowIndex,2).text())
            self.txtEmail.setText(self.tblAddress.item(rowIndex,3).text())
            self.txtAddress.setText(self.tblAddress.item(rowIndex,4).text())
            self.curIdx = int(self.tblAddress.item(rowIndex,0).text()) #curIdx - 주소록 특정 행의 고유 키값 받아옴

    # 삭제 버튼 클릭 시 
    def btnDelClicked(self):
        if self.curIdx ==0:
            QMessageBox.warning(self,'경고','삭제할 데이터를 선택하세요')
        else:
            reply=QMessageBox.question(self,'확인','정말로 삭제하시겠습니까?',QMessageBox.Yes|QMessageBox.No,
                                       QMessageBox.Yes) # 삭제 확인
            
            if reply==QMessageBox.No:
                return # 탈출
            

            self.conn=pymysql.connect(host='localhost',user='root',password='12345',
                                  db='miniproject',charset='utf8')
            query='DELETE FROM addressbook WHERE idx=%s'
            cur=self.conn.cursor()
            cur.execute(query,(self.curIdx))

            self.conn.commit()
            self.conn.close()
            
            QMessageBox.about(self,'성공','Delete Completed')

            self.initDB()
            self.btnNewClicked()

        
    def initDB(self):
        self.conn=pymysql.connect(host='localhost',user='root',password='12345',
                                  db='miniproject',charset='utf8')
        cur=self.conn.cursor() #커서
        query='''
        SELECT idx
	        , FullName
            , PhoneNum
            , Email
            , Address
        FROM addressbook
        '''
        cur.execute(query)
        rows=cur.fetchall() 

        #print(rows)
        self.makeTable(rows)
        self.conn.close() #프로그램 종료

    #Qt Designer에서 만든 ui에 db에 저장된 정보 뿌려주기
    def makeTable(self,rows):
        self.tblAddress.setColumnCount(5)#열갯수
        self.tblAddress.setRowCount(len(rows))#행갯수
        self.tblAddress.setSelectionMode(QAbstractItemView.SingleSelection)#단일선택
        self.tblAddress.setHorizontalHeaderLabels(['번호','이름','휴대폰','이메일','주소'])
        self.tblAddress.setColumnWidth(0,0) # 번호는 숨김
        self.tblAddress.setColumnWidth(1,70) # 이름 열 사이즈 70
        self.tblAddress.setColumnWidth(2,105) # 핸드폰 열 사이즈 105
        self.tblAddress.setColumnWidth(3,175) # 이메일 열 사이즈 175
        self.tblAddress.setColumnWidth(4,200) # 주소 열 사이즈 200
        self.tblAddress.setEditTriggers(QAbstractItemView.NoEditTriggers) # 컬럼 수정 금지
        

        for i,row in enumerate(rows):
            idx=row[0]
            fullName=row[1]
            phoneNum=row[2]
            email=row[3]
            address=row[4]

            self.tblAddress.setItem(i,0,QTableWidgetItem(str(idx)))
            self.tblAddress.setItem(i,1,QTableWidgetItem(fullName))
            self.tblAddress.setItem(i,2,QTableWidgetItem(phoneNum))
            self.tblAddress.setItem(i,3,QTableWidgetItem(email))
            self.tblAddress.setItem(i,4,QTableWidgetItem(address))
        
        self.stbCurrent.showMessage(f'전체 주소록 : {len(rows)}개')

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())