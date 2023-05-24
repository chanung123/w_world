# pylint: disable=C0114
import sys
import pygame
from classes.Player import Player
from classes.Room import Room

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
EDGE = 0  # (0,0)
BOXSCALE = 130
MARGIN = 100
FIREPOSITION = 35
FRAMSCALE = 265

def M_icon(click):
    if click == 0:
        # 마우스 커서 기본
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
    if click == 1:
        # x표시
        pygame.mouse.set_cursor(*pygame.cursors.diamond)


## 게임 창 설정 ##
screen = pygame.display.set_mode((1300, 720))
screen.fill(WHITE)  # 하얀색으로 배경 채우기
pygame.display.set_caption("움푸스 월드")  # 창 이름 설정


def renderimg(src, rscale=BOXSCALE):
    """에셋 불러오기"""
    return pygame.transform.scale(pygame.image.load(src), (rscale, rscale))

frame_img = renderimg("assets/frame.png",FRAMSCALE)

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


#격자 스케일(이미지 정렬)
def point_core(postionx, postiony, box_scale, scale):
    #중심을 기준으로 포지션
    if box_scale < scale:
        if postionx >= 0 and postionx <= 3:
            if postiony >= 0 and postiony <= 3:
                return ((postionx * BOXSCALE) + MARGIN - (scale-box_scale)/2, ((postiony) * BOXSCALE) + MARGIN -(scale-box_scale)/2)

        if postionx > 3 or postiony > 3:
            return ((postionx * BOXSCALE) + MARGIN - (scale-box_scale)/2, ((postiony-1) * BOXSCALE) + MARGIN - (scale-box_scale)/2)
    if box_scale == scale:
        if postionx >= 0 and postionx <= 3:
            if postiony >= 0 and postiony <= 3:
                return ((postionx * BOXSCALE) + MARGIN, ((postiony) * BOXSCALE) + MARGIN)

        if postionx > 3 or postiony > 3:
            return (((postionx) * BOXSCALE) + MARGIN, ((postiony - 1) * BOXSCALE) + MARGIN)
    if box_scale > scale:
        if postionx >= 0 and postionx <= 3:
            if postiony >= 0 and postiony <= 3:
                return ((postionx * BOXSCALE) + MARGIN + (box_scale-scale)/2, ((postiony) * BOXSCALE) + MARGIN + (box_scale-scale)/2)

        if postionx > 3 or postiony > 3:
            return ((postionx * BOXSCALE) + MARGIN + (box_scale-scale)/2, ((postiony-1) * BOXSCALE) + MARGIN + (box_scale-scale)/2)
            

#마우스 격자
def mouse_pos_x(pos_x):
    if pos_x >= MARGIN and pos_x < MARGIN + BOXSCALE:
        return 0
    if pos_x >= MARGIN + BOXSCALE and pos_x < MARGIN + (BOXSCALE*2):
        return 1
    if pos_x >= MARGIN + (BOXSCALE*2) and pos_x < MARGIN + (BOXSCALE*3):
        return 2
    if pos_x >= MARGIN + (BOXSCALE*3) and pos_x < MARGIN + (BOXSCALE*4):
        return 3
    else:
        return 0

def mouse_pos_y(pos_y):
    if pos_y >= MARGIN and pos_y < MARGIN + BOXSCALE:
        return 0
    if pos_y >= MARGIN + BOXSCALE and pos_y < MARGIN + (BOXSCALE*2):
        return 1
    if pos_y >= MARGIN + (BOXSCALE*2) and pos_y < MARGIN + (BOXSCALE*3):
        return 2
    if pos_y >= MARGIN + (BOXSCALE*3) and pos_y < MARGIN + (BOXSCALE*4):
        return 3
    else:
        return 0

def point(postionx, postiony):
    """플레이어 포지션 정하기"""
    if postionx >= 0 and postionx <= 3:
        if postiony >= 0 and postiony <= 3:
            return ((postionx * BOXSCALE) + MARGIN, ((postiony) * BOXSCALE) + MARGIN)

    if postionx > 3 or postiony > 3:
        return (((postionx) * BOXSCALE) + MARGIN, ((postiony - 1) * BOXSCALE) + MARGIN)


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


def RenderMap(
    BOXSCALE,
    FIREPOSITION,
    screen,
    map_img,
    fire_img,
    fire_img_down,
    fire_img_left,
    fire_img_right,
):
    screen.blit(map_img, (24, 10))
    screen.blit(fire_img, (BOXSCALE + FIREPOSITION, 0))
    screen.blit(fire_img, ((3 * BOXSCALE) + FIREPOSITION, 0))
    screen.blit(fire_img_down, (BOXSCALE + FIREPOSITION, BOXSCALE * 4 + FIREPOSITION * 2))
    screen.blit(fire_img_down, ((3 * BOXSCALE) + 35, BOXSCALE * 4 + FIREPOSITION * 2))
    screen.blit(fire_img_left, (0, BOXSCALE + FIREPOSITION))
    screen.blit(fire_img_left, (0, (3 * BOXSCALE) + FIREPOSITION))
    screen.blit(fire_img_right, ((4 * BOXSCALE) + FIREPOSITION * 2, BOXSCALE + FIREPOSITION))
    screen.blit(fire_img_right,((4 * BOXSCALE) + FIREPOSITION * 2, (3 * BOXSCALE) + FIREPOSITION),)


while True:
    Clock.tick(FPS)
    # 현재위치
    currentRoom = rooms[player.x][player.y]

    for event in pygame.event.get():
        # # 게임을 종료시키는 함수
        if event.type == pygame.QUIT:
            sys.exit()
        #캐릭터 이동
        if event.type == pygame.MOUSEBUTTONDOWN:
            x1, y1 = event.pos
            x = mouse_pos_x(x1)
            y = mouse_pos_y(y1)
            if rooms[x][y].canmove:
                rooms[x][y].canmove = False
                player.x = x
                player.y = y
                textoutput("마우스 이동")

                rooms[player.x][player.y].view = True
        
        # if event.type == pygame.KEYDOWN:
        #     textoutput("키보드 이동")
        #     if event.key == pygame.K_ESCAPE:
        #         sys.exit()
        #     if event.key == pygame.K_RIGHT and player.x < 3:
        #         player.x += 1
        #     if event.key == pygame.K_LEFT and player.x > 0:
        #         player.x -= 1
        #     if event.key == pygame.K_UP and player.y > 0:
        #         player.y -= 1
        #     if event.key == pygame.K_DOWN and player.y < 3:
        #         player.y += 1
        #         # 이동(마우스 버튼)
        #     rooms[player.x][player.y].view = True



    screen.fill(BLACK)

    RenderMap(
        BOXSCALE,
        FIREPOSITION,
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

    #이동할 수 있는 곳 밝은 프레임으로 감싸기
    framePos = [-1,0],[1,0],[0,-1],[0,1]
    for pos_box in framePos:
        x = player.x+pos_box[0]
        y = player.y+pos_box[1]
        if (0 <= x <= 3) and (0 <= y <= 3):
            x1, y1 = pygame.mouse.get_pos()
            if mouse_pos_x(x1) == x and mouse_pos_y(y1) == y:
                rooms[x][y].canmove = True
                screen.blit(frame_img, (point_core(x, y, BOXSCALE, FRAMSCALE)))

    # 플레이어 렌더링
    screen.blit(player_img, (point(player.x, player.y)))
    screen.blit(font.render(str(player.x) + "," + str(player.y), True, text_color),(800, 100))

    for text in textArr:
        x = 30 * (textArr.index(text) + 1)
        screen.blit(text, (800, x + 100))


    

    pygame.display.update()