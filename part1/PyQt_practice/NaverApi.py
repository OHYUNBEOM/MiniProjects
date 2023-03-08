#NaverApi 클래스 - OpenApi : 인터넷을 통해 데이터 전달받음
from urllib.request import Request,urlopen
from urllib.parse import quote
import datetime
import json
class NaverApi:
    # 생성자
    def __init__(self) -> None:
        print(f'[{datetime.datetime.now()}] Naver API Search 생성')

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