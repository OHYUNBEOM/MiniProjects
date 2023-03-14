# 암호 해제 앱
import itertools
import time
import zipfile

pwd_string='0123456789' # 패스워드에 영문자도 들어있으면 9 뒤에 영어 소/대문자 다 넣어야함

file=zipfile.ZipFile('./Python_practice/암호는.zip')
isFind = False #암호를 찾았는지

for i in range(1,5):
    attempts=itertools.product(pwd_string, repeat=i)
    for attempt in attempts:
        try_pass=''.join(attempt)
        print(try_pass)
        #time.sleep(0.01)
        try:
            file.extractall(pwd=try_pass.encode(encoding='utf-8'))
            print(f'암호는 {try_pass} 입니다')
            isFind=True; break # 암호를 찾으면 break
        except:
            pass

    if isFind==True : break