# TTS(Text To Speech)
# pip install gTTs (PyPi 사이트 참조하여 설치)
# pip install playsound
from gtts import gTTS
from playsound import playsound

text='안녕하세요, 오윤범입니다.'

tts=gTTS(text=text, lang='ko')
tts.save('./Python_practice/output/hi.mp3')
print('생성 완료!')

playsound('././Python_practice/output/hi.mp3')
print('음성출력 완료!')