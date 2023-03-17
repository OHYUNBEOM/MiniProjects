# DinoRun / 공룡 달리기(크롬)
import pygame
import os
import random # 구름 생성 시 필요했음

pygame.init()

ASSETS='./PyGame/Assets/' #경로 계속 적기 귀찮으니까 하나의 변수로 지정
SCREEN_WIDTH=1100 # 게임 윈도우 넓이 
SCREEN=pygame.display.set_mode((SCREEN_WIDTH,600))

# form 상단에 나오는 이름 / 이미지 출력
pygame.display.set_caption('다이노 런')
icon = pygame.image.load('./PyGame/dinoRun.png')
pygame.display.set_icon(icon)

bg=pygame.image.load(os.path.join(f'{ASSETS}Other','Track.png'))

#뛰는 모션 / 애니메이션
RUNNING = [pygame.image.load(f'{ASSETS}Dino/DinoRun1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoRun2.png')]

#숙이는 모션
DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png')]

#점프 모션
JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png') # 점프는 사진 하나라 배열로 선언X

#구름이미지
CLOUD = pygame.image.load(f'{ASSETS}Other/Cloud.png')

#익룡이미지
BIRD = [pygame.image.load(f'{ASSETS}Bird/Bird1.png'),
        pygame.image.load(f'{ASSETS}Bird/Bird2.png')]

#선인장 이미지 / 애니메이션이 아니고 선인장 종류가 세개임
LARGE_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/LargeCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus3.png')]

SMALL_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/SmallCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus3.png')]

# 공룡 클래스
class Dino: 
    X_POS=80 ; Y_POS = 310 ; Y_POS_DUCK = 340 ; JUMP_VEL = 9.0

    def __init__(self) -> None:
        self.run_img=RUNNING
        self.duck_img=DUCKING
        self.jump_img=JUMPING

        self.dino_run=True
        self.dino_duck=False
        self.dino_jump=False

        self.step_index=0
        self.jump_vel=self.JUMP_VEL # 점프 초기값 9.0
        self.image=self.run_img[0]
        self.dino_rect=self.image.get_rect() # 이미지 사각형 정보
        self.dino_rect.x=self.X_POS
        self.dino_rect.y=self.Y_POS
        

    def update(self,userInput) -> None:
        if self.dino_run:
            self.run()
        elif self.dino_duck:
            self.duck()
        elif self.dino_jump:
            self.jump()
        
        if self.step_index>=10 : self.step_index=0 # 애니메이션 스텝을 위해서 씀

        if userInput[pygame.K_UP] and not self.dino_jump : #점프
            self.dino_run=False
            self.dino_duck=False
            self.dino_jump=True
            self.dino_rect.y=self.Y_POS # 점프 할때마다 올라가는거 방지
        elif userInput[pygame.K_DOWN] and not self.dino_jump: #숙이기
            self.dino_run=False
            self.dino_duck=True
            self.dino_jump=False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]): # 달리기
            self.dino_run=True
            self.dino_duck=False
            self.dino_jump=False
        
    # 공룡 달리는 부분
    def run(self): 
        self.image=self.run_img[self.step_index//5]  # run_img
        self.dino_rect=self.image.get_rect() # 이미지 사각형 정보
        self.dino_rect.x=self.X_POS
        self.dino_rect.y=self.Y_POS
        self.step_index+=1

    # 공룡 숙이는 부분
    def duck(self):
        self.image=self.duck_img[self.step_index//5] # duck_img
        self.dino_rect=self.image.get_rect() # 이미지 사각형 정보
        self.dino_rect.x=self.X_POS
        self.dino_rect.y=self.Y_POS_DUCK # 이미지 높이 따로 설정
        self.step_index+=1

    # 공룡 점프하는 부분
    def jump(self):
        self.image=self.jump_img
        if self.dino_jump:
            self.dino_rect.y-=self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel<-self.JUMP_VEL: # 초기에 설정해둔 9.0이 되버리면 점프 중단
            self.dino_jump=False
            self.jump_vel=self.JUMP_VEL # 9.0으로 다시 초기화


    def draw(self,SCREEN) -> None:
        SCREEN.blit(self.image,(self.dino_rect.x,self.dino_rect.y))

#구름 클래스
class Cloud: 
    def __init__(self) -> None:
        self.x = SCREEN_WIDTH + random.randint(300,500)
        self.y = random.randint(50,100)
        self.image=CLOUD
        self.width=self.image.get_width()

    def update(self) -> None:
        self.x-=game_speed
        if self.x < -self.width: #화면밖으로 벗어나면
            self.x=SCREEN_WIDTH + random.randint(1300,2000)
            self.y=random.randint(50,100)

    def draw(self,SCREEN) -> None:
        SCREEN.blit(self.image, (self.x,self.y))

#장애물 클래스(부모 클래스)
class Obstacle:
    def __init__(self,image,type) -> None:
        self.image=image
        self.type=type
        self.rect=self.image[self.type].get_rect()
        self.rect.x=SCREEN_WIDTH #1100
        
    def update(self)->None:
        self.rect.x-=game_speed
        if self.rect.x<=-self.rect.width: # 왼쪽 화면 밖으로 벗어나면
            obstacles.pop() # 장애물(배열) 에서 값들을 하나씩 빼옴


    def draw(self,SCREEN)->None:
        SCREEN.blit(self.image[self.type],self.rect)

class Bird(Obstacle): #장애물 클래스 상속클래스
    def __init__(self, image) -> None:
        self.type=0 # 새는 0
        super().__init__(image,self.type)
        self.rect.y=250 # 새라서 하늘에 그림그려야하니까 y좌표 올림
        self.index=0 #0이미지로 시작

    def draw(self,SCREEN)->None:#draw 재정의
        if self.index >= 9:
            self.index=0
        SCREEN.blit(self.image[self.index//5],self.rect)
        self.index+=1

class LargeCactus(Obstacle):
    def __init__(self, image) -> None:
        self.type=random.randint(0,2) # 큰 선인장 세가지 종류
        super().__init__(image, self.type)
        self.rect.y=300

class SmallCactus(Obstacle):
    def __init__(self, image) -> None:
        self.type=random.randint(0,2) # 작은 선인장 세가지 종류
        super().__init__(image, self.type)
        self.rect.y=325

def main():
    global game_speed, x_pos_bg , y_pos_bg, points , obstacles
    x_pos_bg = 0
    y_pos_bg = 380
    points=0 # 게임 점수
    run=True
    clock=pygame.time.Clock()
    dino=Dino() # 공룡 객체 생성
    cloud = Cloud() # 구름 객체 생성
    game_speed = 14
    obstacles=[]

    font=pygame.font.Font(f'{ASSETS}NanumGothicBold.ttf',size=20)

    def background(): # 함수 내 함수 즉 main 함수에서만 사용, 땅바닥 update와 draw 동시에 해주는 함수
        global x_pos_bg, y_pos_bg 
        image_width=bg.get_width() # track 이미지 2404쯤됨
        SCREEN.blit(bg,(x_pos_bg,y_pos_bg)) # 0,300 먼저 그림
        SCREEN.blit(bg,(image_width+x_pos_bg,y_pos_bg)) # 2404+ 0,380

        if x_pos_bg<=-image_width:
            #SCREEN_WIDTH.blit(bg,(image_width+x_pos_bg,y_pos_bg))
            x_pos_bg=0
        
        x_pos_bg-=game_speed

    def score(): # main 함수에서만 사용가능한 함수 내 함수 / 점수 표시
        global points, game_speed
        points+=1
        if points % 100==0: #100,200,300... 
            game_speed +=1 #점수가 높아질수록 게임 속도가 빠르게
        
        txtScore=font.render(f'SCORE : {points}', True , (83,83,83)) #공룡과 색 맞춤(회색)
        txtRect=txtScore.get_rect()
        txtRect.center = (1000,40)
        SCREEN.blit(txtScore,txtRect)

    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        
        SCREEN.fill((255,255,255)) # 배경 흰색
        userInput=pygame.key.get_pressed() #키보드입력

        background()
        score()

        cloud.draw(SCREEN) # 구름이 애니메이션
        cloud.update() # 구름이 공룡보다 먼저 그려져야됨

        dino.draw(SCREEN) # 공룡 그리기
        dino.update(userInput)

        if len(obstacles)==0:
            if random.randint(0,2)==0:#작은선인장
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0,2)==1:#큰선인장
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0,2)==2:#새
                obstacles.append(Bird(BIRD))
        
        for obs in obstacles:
            obs.draw(SCREEN)
            obs.update()
            #Collision Detection
            if dino.dino_rect.colliderect(obs.rect): # 장애물에 부딪히면 표시
                pygame.draw.rect(SCREEN,(255,0,0),dino.dino_rect,3)

        clock.tick(30)
        pygame.display.update() # 초당 30번 update 수행함

if __name__=='__main__':
    main()