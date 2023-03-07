#NaverApi 클래스 - OpenApi : 인터넷을 통해 데이터 전달받음
import os
import sys
from urllib.request import Request,urlopen
from urllib.parse import quote
import datetime
import time
import json
class NaverApi:
    # 생성자
    def __init__(self) -> None:
        print('Naver API Search 생성')

    # NaverAPI를 요청
    def getRequestUrl(self,url):
        req=Request(url)
        #NaverAPI 개인 인증
        req.add_header('X-Naver-Client-ID','kflq_q32Q1Q3tf46AKDF')
        req.add_header('X-Naver-Client-Secret','kpYx2Ai7O5')
        try:
            res = urlopen(req) #요청결과 바로 반환
            if res.getcode() ==200: # reponse OK
                print(f'[{datetime.datetime.now()}] NaverAPI 요청 성공')
                return res.read().decode('utf-8') #사용자가 알아볼 수 있게 반환
            else:
                print(f'[{datetime.datetime.now()}]NaverAPI 요청 실패')
                return None

        except Exception as e:
            print(f'[{datetime.datetime.now()}] 예외발생 : {e}')
            return None

    # 호출
    def getNaverSearch(self,node,search,start,display):
        base_url='https://openapi.naver.com/v1/search'
        node_url=f'/{node}.json'
        params=f'?query={quote(search)}&start={start}&display={display}'

        url=base_url+node_url+params #전체 url
        
        retData=self.getRequestUrl(url)

        if retData==None : return None
        else : return json.loads(retData) # json 으로 return

    # json으로 받은 데이터-->list로 바꿔주는 역할
    def getPostData(self,post,outputs):
        title=post['title']
        description = post['description']
        originallink=post['originallink']
        link=post['link']

        #'Tue,07 Mar 2023 17:04:00 +0900' 과 같이 들어온걸 날짜형으로 변환해주는역할
        pDate=datetime.datetime.strptime(post['pubDate'],'%a, %d %b %Y %H:%M:%S +0900')
        pubDate=pDate.strftime('%Y-%m-%d %H:%M:%S') # 우리가 쓰는 형태로 다시 변환 ex)2023-03-07 17:04:00 변경
