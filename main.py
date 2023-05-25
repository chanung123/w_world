# pylint: disable=C0114
import sys
import pygame
from classes.Player import Player
from classes.Room import Room
from position import BOXSCALE, RenderMap, mouse_pos_x, mouse_pos_y, point, point_core

# Initialize the game engine
# pylint: disable=no-member
pygame.init()

## 초당 프레임 단위 설정 ##
FPS = 60
Clock = pygame.time.Clock()

## 컬러 세팅 ##
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 격자만들기(가로)
EDGE = 0  # (0,0)

FRAMSCALE = 265


def cursoricon(cursor):
    """칸에 커서올라가면 마우스 변경"""
    if cursor:  # 마우스 커서 on
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
    else:  # 마우스 커서 off
        pygame.mouse.set_cursor(*pygame.cursors.arrow)


## 게임 창 설정 ##
screen = pygame.display.set_mode((1300, 720))
pygame.display.set_caption("움푸스 월드")  # 창 이름 설정


def renderimg(src, rscale=BOXSCALE):
    """에셋 불러오기"""
    return pygame.transform.scale(pygame.image.load(src), (rscale, rscale))


frame_img = renderimg("assets/frame.png", FRAMSCALE)

map_img = pygame.image.load("assets/map.png")
map_img = pygame.transform.scale(map_img, (670, 700))

fire_img = renderimg("assets/fire.png")
fire_img_up = pygame.transform.rotate(fire_img, 0)
fire_img_down = pygame.transform.rotate(fire_img, 180)
fire_img_left = pygame.transform.rotate(fire_img, 90)
fire_img_right = pygame.transform.rotate(fire_img, -90)

gold_img = renderimg("assets/gold in box.png")
wumpus_img = renderimg("assets/wumpus.png")
pit_img = renderimg("assets/pitch_rava.png")
player_img = renderimg("assets/player.png")
dark_img = renderimg("assets/dark.png")


text_color = WHITE  # Black
font = pygame.font.Font("uhBeePuding.ttf", 28)
textArr = []


def textoutput(outtext):
    """텍스트 출력해주는 함수"""
    text_surface = font.render(outtext, True, text_color)
    textArr.append(text_surface)
    if len(textArr) > 10:
        del textArr[0]


##초기화

# 룸생성
rooms = [[], [], [], []]
for i in range(4):
    for j in range(4):
        rooms[i].append(Room(i, j))

# 0,0초기화
rooms[0][0].view = True

# 플레이어 초기화
player = Player(0, 0)

# 장애물 설정
rooms[2][2].status = "wumpus"
rooms[2][3].status = "pit"
rooms[3][3].status = "gold"

# 인게임
while True:
    Clock.tick(FPS)
    # 현재위치
    currentRoom = rooms[player.x][player.y]
    for event in pygame.event.get():
        # # 게임을 종료시키는 함수
        if event.type == pygame.QUIT:
            sys.exit()
        # 캐릭터 이동
        if event.type == pygame.MOUSEBUTTONDOWN:
            x1, y1 = event.pos
            X = mouse_pos_x(x1)
            Y = mouse_pos_y(y1)
            if rooms[X][Y].canmove:
                rooms[X][Y].canmove = False
                player.x = X
                player.y = Y
                textoutput("마우스 이동")
                rooms[player.x][player.y].view = True

    # 맵 렌더링 background, toach, object(status), view
    screen.fill(BLACK)
    RenderMap(
        screen,
        map_img,
        fire_img,
        fire_img_down,
        fire_img_left,
        fire_img_right,
    )
    for x in range(4):
        # 룸의 상태에 따라 오브젝트 생성. 변경은 위에서 하면 된다. 여긴 안건드려도 됨
        for y in range(4):
            if rooms[x][y].status == "wumpus":
                screen.blit(wumpus_img, (point(x, y)))
            elif rooms[x][y].status == "pit":
                screen.blit(pit_img, (point(2, 3)))
            elif rooms[x][y].status == "gold":
                screen.blit(gold_img, (point(3, 3)))
            # 지나간곳만 보임 (view가 false일떄)
            if not rooms[x][y].view:
                screen.blit(dark_img, (point(x, y)))

    # 이동할 수 있는 곳 밝은 프레임으로 감싸기
    framePos = [-1, 0], [1, 0], [0, -1], [0, 1]
    for pos_box in framePos:
        x = player.x + pos_box[0]
        y = player.y + pos_box[1]
        if (0 <= x <= 3) and (0 <= y <= 3):
            x1, y1 = pygame.mouse.get_pos()
            if mouse_pos_x(x1) == x and mouse_pos_y(y1) == y:
                rooms[x][y].canmove = True
                screen.blit(frame_img, (point_core(x, y, BOXSCALE, FRAMSCALE)))

    # 플레이어 렌더링
    screen.blit(player_img, (point(player.x, player.y)))
    screen.blit(
        font.render(str(player.x) + "," + str(player.y), True, text_color), (800, 100)
    )

    for text in textArr:
        x = 30 * (textArr.index(text) + 1)
        screen.blit(text, (800, x + 100))

    pygame.display.update()
