import pandas as pd
import folium #pip install folium

filePath='./Python_practice/university_locations.xlsx'
df_excel=pd.read_excel(filePath,engine='openpyxl',header=None)
df_excel.columns=['학교명','주소','lng','lat']

name_list=df_excel['학교명'].to_list() # 학교명을 name_list에 다 담음
addr_list=df_excel['주소'].to_list()
lng_list=df_excel['lng'].to_list()
lat_list=df_excel['lat'].to_list()

fMap=folium.Map(location=[37.553175,126.989326],zoom_start=10)

for i in range(len(name_list)):
    if lng_list[i] !=0:#위/경도 값이 0이 아니면
        marker=folium.Marker([lat_list[i],lng_list[i]],popup=name_list[i],
                             icon=folium.Icon(color='blue'))
        marker.add_to(fMap)

fMap.save('./Python_practice/Korea_universites.html')
