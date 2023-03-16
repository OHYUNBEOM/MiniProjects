#Python으로 게임 만들기 - PyGame Game Framework 사용
#pip install pygame
import pygame

pygame.init() # 1. 게임 초기화 / 필수

width,height=500,500
win=pygame.display.set_mode((width,height)) #윈도우 사이즈 설정 / tuple 이라 괄호 한번 더 사용
pygame.display.set_caption('게임 만들기')
icon = pygame.image.load('./PyGame/game_icon.png')
pygame.display.set_icon(icon)

# object 설정
x,y=250,250
radius=10
vel_x=10
vel_y=10
jump=False

run=True

while run:
    win.fill((0,0,0)) # 사용자가 원하는대로 display.update 해주고 다시 윈도우를 검은색으로 초기화
    pygame.draw.circle(win,(255,255,255), (x,y), radius)

    #이벤트 = 시그널
    for event in pygame.event.get(): # 2. 이벤트 받기
        if event.type == pygame.QUIT:
            run = False # QUIT 일때 false로 만들고 탈출

    # 객체이동
    userInput=pygame.key.get_pressed()
    if userInput[pygame.K_LEFT] and x>10:
        x-=vel_x #왼쪽으로 10씩 
    if userInput[pygame.K_RIGHT] and x<width-10:
        x+=vel_x
    # if userInput[pygame.K_UP] and y>10:
    #     y-=vel_x # y좌표는 빼줘야 위로 올라감 주의
    # if userInput[pygame.K_DOWN]and y<height-10:
    #     y+=vel_x
    
    # 객체점프
    if jump == False and userInput[pygame.K_SPACE]:
        jump = True 
        
    if jump==True:
        y -= vel_y * 2
        vel_y -= 1
        if vel_y<-10:
            jump=False
            vel_y=10

    pygame.time.delay(10)    
    pygame.display.update() # 3.화면 업데이트(전환)
