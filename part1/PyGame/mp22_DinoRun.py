# DinoRun / 공룡 달리기(크롬)
import pygame
import os

pygame.init()

ASSETS='./PyGame/Assets/' #경로 계속 적기 귀찮으니까 하나의 변수로 지정
SCREEN=pygame.display.set_mode((1100,600))

# form 상단에 나오는 이름 / 이미지 출력
pygame.display.set_caption('다이노 런')
icon = pygame.image.load('./PyGame/dinoRun.png')
pygame.display.set_icon(icon)

bg=pygame.image.load(os.path.join(f'{ASSETS}Other','Track.png'))

#뛰는 모션
RUNNING = [pygame.image.load(f'{ASSETS}Dino/DinoRun1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoRun2.png'),]

#숙이는 모션
DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'),]

#점프 모션
JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png') # 점프는 사진 하나라 배열로 선언X

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


def main():
    run=True
    clock=pygame.time.Clock()
    dino=Dino() # 공룡 객체 생성

    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        
        SCREEN.fill((255,255,255)) # 배경 흰색
        userInput=pygame.key.get_pressed() #키보드입력

        dino.draw(SCREEN) # 공룡 그리기
        dino.update(userInput)

        clock.tick(30)
        pygame.display.update() # 초당 30번 update 수행함

if __name__=='__main__':
    main()