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


## 게임 창 설정 ##
screen = pygame.display.set_mode((1300, 700))
screen.fill(WHITE)  # 하얀색으로 배경 채우기
pygame.display.set_caption("움푸스 월드")  # 창 이름 설정

img = pygame.image.load("player.png")
img = pygame.transform.scale(img, (150, 150))

player_posX = 0
player_posY = 0


def point(postionX, postionY):
    return ((postionX * 150), ((postionY) * 150))


text_color = (0, 0, 0)  # Black
font = pygame.font.Font("uhBeePuding.ttf", 26)

# text_surface = font.render("asdasdasdasd", True, text_color)

textArr = []


def textOutput(text):
    text_surface = font.render(text, True, text_color)
    textArr.append(text_surface)
    if len(textArr) > 10:
        del textArr[0]


while True:
    Clock.tick(FPS)
    # Create a text surface
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            textOutput("멍충한 놈~")
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_RIGHT:
                player_posX += 1
            if event.key == pygame.K_LEFT:
                player_posX -= 1
            if event.key == pygame.K_UP:
                player_posY -= 1
            if event.key == pygame.K_DOWN:
                player_posY += 1

    screen.fill(WHITE)

    # 격자만들기(가로)
    x = 0  # (0,0)
    y = 150
    for i in range(5):
        pygame.draw.line(screen, BLACK, (x, 0), (x, y * 4), width=3)
        pygame.draw.line(screen, BLACK, (0, x), (y * 4, x), width=3)
        x += y

    screen.blit(img, (point(player_posX, player_posY)))

    screen.blit(
        font.render(str(player_posX) + "," + str(player_posY), True, text_color),
        (800, 100),
    )
    for text in textArr:
        x = 40 * (textArr.index(text) + 1)
        screen.blit(text, (800, x + 100))

    # # 게임을 종료시키는 함수
    pygame.display.update()
