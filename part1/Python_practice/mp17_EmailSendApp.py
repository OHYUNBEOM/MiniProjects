# 이메일 보내기 앱
import smtplib # 메일 전송 프로토콜 
from email.mime.text import MIMEText

send_email='@naver.com' #실제 구동 시 제대로된 이메일 작성
send_pass='!!' # 실제 구동 시 해당 이메일의 실제 패스워드 작성

recv_email='@naver.com' #실제 구동 시 제대로된 이메일 작성

smtp_name='smtp.naver.com'
smtp_port = 587 # 포트번호 정해져있음

text = '''메일 내용
긴급 빨리 연락바람'''

msg=MIMEText(text)
msg['Subject'] = '메일 제목입니다'
msg['From'] = send_email # 보내는 메일
msg['To'] = recv_email # 받는 메일

#print(msg.as_string())

mail=smtplib.SMTP(smtp_name,smtp_port) # SMTP 객체생성
mail.starttls() #전송계층 보안시작
mail.login(send_email,send_pass)
mail.sendmail(send_email,recv_email,msg=msg.as_string())
mail.quit()
print('전송완료!')