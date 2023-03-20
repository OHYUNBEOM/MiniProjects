#전국대학교 리스트
# pandas 모듈 사용 / pip install pandas
import pandas as pd
filePath='./Python_practice/university_list_2020.xlsx'
df_excel=pd.read_excel(filePath,engine='openpyxl')

df_excel.columns = df_excel.loc[4].tolist()
df_excel=df_excel.drop(index=list(range(0,5))) # 실ㅈ ㅔ데이터 이외 행 날림

print(df_excel.head()) #상위 5개만

print(df_excel['학교명'].values) #학교명만 출력
print(df_excel['주소'].values) #주소만 출력