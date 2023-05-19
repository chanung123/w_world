# pylint: disable=C0114
import sys
import pygame

# Initialize the game engine
# pylint: disable=no-member
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
boxScale = 130
z = 100
r = 35

## 게임 창 설정 ##
screen = pygame.display.set_mode((1300, 720))
screen.fill(WHITE)  # 하얀색으로 배경 채우기
pygame.display.set_caption("움푸스 월드")  # 창 이름 설정


# 에셋 불러오기
def renderImage(src):
    return pygame.transform.scale(pygame.image.load(src), (boxScale, boxScale))


map_img = pygame.image.load("assets/map.png")
map_img = pygame.transform.scale(map_img, (670, 700))

fire_img = renderImage("assets/fire.png")
fire_img_up = pygame.transform.rotate(fire_img, 0)
fire_img_down = pygame.transform.rotate(fire_img, 180)
fire_img_left = pygame.transform.rotate(fire_img, 90)
fire_img_right = pygame.transform.rotate(fire_img, -90)

gold_img = renderImage("assets/gold in box.png")
wumpus_img = renderImage("assets/wumpus.png")
pitch_img = renderImage("assets/pitch.png")
pitch_img2 = renderImage("assets/pitch_rava.png")
player_img = renderImage("assets/player.png")
dark_img = renderImage("assets/dark.png")

player_posX = 0
player_posY = 0


def point(postionx, postiony):
    """플레이어 포지션 정하기"""
    if postionx >= 0 and postionx <= 3:
        if postiony >= 0 and postiony <= 3:
            return ((postionx * boxScale) + z, ((postiony) * boxScale) + z)

    if postionx > 3 or postiony > 3:
        return (((postionx) * boxScale) + z, ((postiony - 1) * boxScale) + z)


def dark():
    """검은화면으로 가리기"""
    for i in range(4):
        for j in range(4):
            if i != player_posX or j != player_posY:
                screen.blit(dark_img, (point(i, j)))


text_color = WHITE  # Black
font = pygame.font.Font("uhBeePuding.ttf", 28)

# text_surface = font.render("asdasdasdasd", True, text_color)
textArr = []


def textoutput(outtext):
    """텍스트 출력해주는 함수"""
    text_surface = font.render(outtext, True, text_color)
    textArr.append(text_surface)
    if len(textArr) > 10:
        del textArr[0]


while True:
    Clock.tick(FPS)

    for event in pygame.event.get():
        # # 게임을 종료시키는 함수
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            textoutput("아무고토 못하쥬?")
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_RIGHT and player_posX < 3:
                player_posX += 1
            if event.key == pygame.K_LEFT and player_posX > 0:
                player_posX -= 1
            if event.key == pygame.K_UP and player_posY > 0:
                player_posY -= 1
            if event.key == pygame.K_DOWN and player_posY < 3:
                player_posY += 1

    screen.fill(BLACK)

    screen.blit(map_img, (24, 10))
    screen.blit(fire_img, (boxScale + r, 0))
    screen.blit(fire_img, ((3 * boxScale) + r, 0))
    screen.blit(fire_img_down, (boxScale + r, boxScale * 4 + r * 2))
    screen.blit(fire_img_down, ((3 * boxScale) + 35, boxScale * 4 + r * 2))
    screen.blit(fire_img_left, (0, boxScale + r))
    screen.blit(fire_img_left, (0, (3 * boxScale) + r))
    screen.blit(fire_img_right, ((4 * boxScale) + r * 2, boxScale + r))
    screen.blit(fire_img_right, ((4 * boxScale) + r * 2, (3 * boxScale) + r))
    screen.blit(wumpus_img, (point(2, 2)))
    screen.blit(wumpus_img, (point(0, 2)))
    screen.blit(pitch_img, (point(2, 3)))
    screen.blit(pitch_img2, (point(1, 0)))
    screen.blit(gold_img, (point(3, 3)))
    screen.blit(player_img, (point(player_posX, player_posY)))

    dark()

    screen.blit(
        font.render(str(player_posX) + "," + str(player_posY), True, text_color),
        (800, 100),
    )
    for text in textArr:
        x = 30 * (textArr.index(text) + 1)
        screen.blit(text, (800, x + 100))

    pygame.display.update()
