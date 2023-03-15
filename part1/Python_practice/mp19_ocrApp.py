# 글자추출
# 이미지 처리 모듈 pip install pillow
# OCR 모듈 pip install pytesseract
# Tesseract-OCR 컴퓨터 설치
# https://github.com/tesseract-ocr/tessdata/blob/main/kor.traineddata 
# 위 링크에서 kor.traineddata 다운로드 후 C:\DEV\Tools\Tesseract-OCR\tessdata <- 경로에 붙여넣기
from PIL import Image
import pytesseract as tess

img_path='./Python_practice/한글이미지.png'
tess.pytesseract.tesseract_cmd = 'C:/DEV/Tools/Tesseract-OCR/tesseract.exe'

result = tess.image_to_string(Image.open(img_path), lang='kor')
print(result)