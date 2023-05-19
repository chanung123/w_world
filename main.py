import sys
import pygame
from pygame.locals import *

# Initialize the game engine
pygame.init()


## 초당 프레임 단위 설정 ##
FPS = 60
Clock = pygame.time.Clock()

## 컬러 세팅 ##
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 격자만들기(가로)
x = 0  # (0,0)
y = 130
z = 100
r = 35


## 게임 창 설정 ##
screen = pygame.display.set_mode((1300, 720))
screen.fill(WHITE)  # 하얀색으로 배경 채우기
pygame.display.set_caption("움푸스 월드")  # 창 이름 설정

# 에셋 불러오기
map_img = pygame.image.load("assets/map.png")
map_img = pygame.transform.scale(map_img, (670, 700))

fire_img = pygame.image.load("assets/fire.png")
fire_img = pygame.transform.scale(fire_img, (y, y))
fire_img_u = pygame.transform.rotate(fire_img, 0)
fire_img_d = pygame.transform.rotate(fire_img, 180)
fire_img_l = pygame.transform.rotate(fire_img, 90)
fire_img_r = pygame.transform.rotate(fire_img, -90)


gold_img = pygame.image.load("assets/gold in box.png")
gold_img = pygame.transform.scale(gold_img, (y, y))

wumpus_img = pygame.image.load("assets/wumpus.png")
wumpus_img = pygame.transform.scale(wumpus_img, (y, y))

pitch_img = pygame.image.load("assets/pitch.png")
pitch_img = pygame.transform.scale(pitch_img, (y, y))

pitch_img2 = pygame.image.load("assets/pitch_rava.png")
pitch_img2 = pygame.transform.scale(pitch_img2, (y, y))

player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (y, y))

dark_img = pygame.image.load("assets/dark.png")
dark_img = pygame.transform.scale(dark_img, (y, y))

player_posX = 0
player_posY = 0

# def rand_point(x , y):


def point(postionX, postionY):
    if postionX >= 0 and postionX <= 3:
        if postionY >= 0 and postionY <= 3:
            return ((postionX * y) + z, ((postionY) * y) + z)

    if postionX > 3 or postionY > 3:
        return (((postionX) * y) + z, ((postionY - 1) * y) + z)


# def light():


def dark():
    for i in range(4):
        for j in range(4):
            if i != player_posX or j != player_posY:
                screen.blit(dark_img, (point(i, j)))


text_color = WHITE  # Black
font = pygame.font.Font("uhBeePuding.ttf", 28)

# text_surface = font.render("asdasdasdasd", True, text_color)
textArr = []


def textOutput(text):
    text_surface = font.render(text, True, text_color)
    textArr.append(text_surface)
    if len(textArr) > 10:
        del textArr[0]


while True:
    Clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            textOutput("아무고토 못하쥬?")
            if event.key == pygame.K_ESCAPE:
                sys.exit()
                pygame.quit()
            if event.key == pygame.K_RIGHT:
                player_posX += 1
            if event.key == pygame.K_LEFT:
                player_posX -= 1
            if event.key == pygame.K_UP:
                player_posY -= 1
            if event.key == pygame.K_DOWN:
                player_posY += 1

    screen.fill(BLACK)

    screen.blit(map_img, (24, 10))

    screen.blit(fire_img, (y + r, 0))
    screen.blit(fire_img, ((3 * y) + r, 0))

    screen.blit(fire_img_d, (y + r, y * 4 + r * 2))
    screen.blit(fire_img_d, ((3 * y) + 35, y * 4 + r * 2))

    screen.blit(fire_img_l, (0, y + r))
    screen.blit(fire_img_l, (0, (3 * y) + r))

    screen.blit(fire_img_r, ((4 * y) + r * 2, y + r))
    screen.blit(fire_img_r, ((4 * y) + r * 2, (3 * y) + r))

    screen.blit(wumpus_img, (point(2, 2)))

    screen.blit(wumpus_img, (point(0, 2)))

    screen.blit(pitch_img, (point(2, 3)))

    screen.blit(pitch_img2, (point(1, 0)))

    screen.blit(gold_img, (point(3, 3)))
    # 격자만들기(가로)
    x = 0  # (0,0)
    y = 130
    z = 100

    for i in range(5):
        pygame.draw.line(screen, BLACK, (x + z, 0 + z), (x + z, (y * 4) + z), width=3)
        pygame.draw.line(screen, BLACK, (0 + z, x + z), ((y * 4) + z, x + z), width=3)
        x += y

    screen.blit(player_img, (point(player_posX, player_posY)))

    dark()

    screen.blit(
        font.render(str(player_posX) + "," + str(player_posY), True, text_color),
        (800, 100),
    )
    for text in textArr:
        x = 30 * (textArr.index(text) + 1)
        screen.blit(text, (800, x + 100))

    # # 게임을 종료시키는 함수
    pygame.display.update()
