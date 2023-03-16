import pygame

pygame.init() #초기화
win=pygame.display.set_mode((1000,500)) 

bg_img=pygame.image.load('./PyGame/Assets/background.png')
bg=pygame.transform.scale(bg_img,(1000,500)) # win에 맞춰서 사이즈 조정

pygame.display.set_caption('게임 만들기')
icon = pygame.image.load('./PyGame/game_icon.png')
pygame.display.set_icon(icon)

width=1000
loop=0
run=True
while run:
    win.fill((0,0,0))

    # 이벤트 = 시그널
    for event in pygame.event.get(): # 2. 이벤트 받기
        if event.type == pygame.QUIT:
            run = False # QUIT 일때 false로 만들고 탈출

    # 배경 그리기
    win.blit(bg,(loop,0))
    win.blit(bg,(width+loop,0))

    if loop==-width:
        loop=0

    loop-=1

    pygame.display.update()