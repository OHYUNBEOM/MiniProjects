import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
import time

MAX=1000

class BackgroundWorker(QThread): #PyQt5 스레드를 위한 클래스 존재
    procChanged = pyqtSignal(int) # 커스텀 시그널 / Click같은 시그널을 사용자가 만드는것

    def __init__(self,count=0,parent=None)->None:
        super().__init__()
        self.main=parent
        self.working=False #스레드 동작여부 확인하는 변수
        self.count=count

    def run(self): # thread.start() 할 때 run이 돌아감
        while self.working:
            if self.count<=MAX:
                self.procChanged.emit(self.count) # self.count값을 호출한곳으로 내보냄(ex.procUpdated)
                self.count+=1 # 값 증가 처리만 함 // 업무프로세스 동작 위치
                time.sleep(0.001) # 0.00000001 정도로 주면 GUI처리를 제대로 못함
            else:
                self.working=False # MAX 값 넘어가면 False로 바뀌면서 while문 탈출

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyThread/threadApp.ui',self) #Qt Designer로 만든 ui 사용
        self.setWindowTitle('Thread 앱')
        self.pgbTask.setValue(0)

        self.btnStart.clicked.connect(self.btnStartClicked)
        # 스레드 초기화
        self.worker=BackgroundWorker(parent=self, count=0)
        # 백그라운드 worker의 시그널에 접근하여 처리하기 위한 슬롯 함수
        self.worker.procChanged.connect(self.procUpdated)

        self.pgbTask.setRange(0,MAX) #0~1000으로 범위설정

    def procUpdated(self,count):
        self.txbLog.append(f'스레드 출력 > {count}')
        self.pgbTask.setValue(count)
        print(f'스레드 출력 > {count}')

    def btnStartClicked(self):
        self.worker.start() # QThread 클래스 내부의 run() 실행
        self.worker.working = True
        self.worker.count=0 # 지정 범위 종료 후 스레드시작 버튼 다시 클릭 시 동작함

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())