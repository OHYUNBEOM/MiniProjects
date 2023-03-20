#PyQT에 folium 지도 표시
import sys
import folium
import io 
import pandas as pd
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView #pip install PyQtWebEngine

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('전국대학교 위치')
        self.width,self.height=1000,800
        self.setMinimumSize(self.width,self.height)

        layout=QVBoxLayout()
        self.setLayout(layout)

        filePath='./Python_practice/university_locations.xlsx'
        df_excel=pd.read_excel(filePath,engine='openpyxl',header=None)
        df_excel.columns=['학교명','주소','lng','lat']

        name_list=df_excel['학교명'].to_list() # 학교명을 name_list에 다 담음
        addr_list=df_excel['주소'].to_list()
        lng_list=df_excel['lng'].to_list()
        lat_list=df_excel['lat'].to_list()

        
        m=folium.Map(location=[37.553175,126.989326],zoom_start=10)

        for i in range(len(name_list)):
            if lng_list[i] !=0:#위/경도 값이 0이 아니면
                marker=folium.Marker([lat_list[i],lng_list[i]],popup=name_list[i],
                                    icon=folium.Icon(color='blue'))
                marker.add_to(m)

        data=io.BytesIO()
        m.save(data,close_file=False)

        webView=QWebEngineView()
        webView.setHtml(data.getvalue().decode()) # 가져오는 데이터를 html로 저장
        layout.addWidget(webView)

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())