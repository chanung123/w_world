# pylint: disable=C0114
import sys
import pygame
import random
import spritesheet



class Room:
    """방"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = "saferoom"
        self.view = False


class Player:
    """플레이어"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.arrows = 2

    def shoot_arrow(self, direction, currentroom):
        if self.arrows > 0:
            self.arrows -= 1
            if direction == "w":
                print("나이샷! 웜푸스가 뒤졌습니다!")
            else:
                print("어따쏘는거죠? 웜푸스를 놓쳤습니다.")

    def sense_wumpus(self, currentroom):
        """웜푸스 감지"""
        # TODO: 4가지 방향에 웜푸스가 있을경우 snetch
        if currentroom.status == "wumpus":
            print("You smell a Wumpus!")
        else:
            print("You don't smell a Wumpus.")

    def sense_pit(self, currentroom):
        """웅덩이 감지"""

    # TODO: 4가지 방향에 웅덩이가 있을경우 breeze
    # if currentroom.status == "pit":
    #     print("You feel a breeze!")
    # else:
    #     print("You don't feel a breeze.")


# Initialize the game engine
# pylint: disable=no-member
pygame.init()

## 초당 프레임 단위 설정 ##
FPS = 60
Clock = pygame.time.Clock()
pygame.key.set_repeat(300, 1)
FPSCLOCK = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spritesheets")

sprite_sheet_image = pygame.image.load("girl.png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)


BG = (0,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
WIDTH = 59.99
HEIGHT = 120

X=250
Y=250



#create animation list
animation_list = []
animation_steps = [8, 8, 8, 8]
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 100
frame = 0
step_counter = 0

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, WIDTH, HEIGHT,2,BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)

print(animation_list)

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

## 게임 창 설정 ##
screen = pygame.display.set_mode((1300, 720))
screen.fill(WHITE)  # 하얀색으로 배경 채우기
pygame.display.set_caption("움푸스 월드")  # 창 이름 설정


def renderimg(src):
    """에셋 불러오기"""
    return pygame.transform.scale(pygame.image.load(src), (BOXSCALE, BOXSCALE))


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


def point(postionx, postiony):
    """플레이어 포지션 정하기"""
    if postionx >= 0 and postionx <= 3:
        if postiony >= 0 and postiony <= 3:
            return ((postionx * BOXSCALE) + MARGIN, ((postiony) * BOXSCALE) + MARGIN)

    if postionx > 3 or postiony > 3:
        return (((postionx) * BOXSCALE) + MARGIN, ((postiony - 1) * BOXSCALE) + MARGIN)


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
def random_num(r):
    R = random.randint(0,r)
    return R

sample = 100 #표본개수

for x in range(4):
    for y in range(4):
        if x == 0 and y == 0:
            rooms[x][y].status = "none"
        elif x == 3 and y == 3:
            rooms[x][y].status = "gold"
        else:
            i = random_num(sample)
            if i <= 0.1*sample:
                rooms[x][y].status = "wumpus"
            elif i > 0.1*sample and i <= 0.15*sample:
                rooms[x][y].status = "pit"
            elif i > 0.15*sample and i <= 0.2*sample:
                rooms[x][y].status = "pit2"
            else:
                rooms[x][y].status = "none"




    
        # rooms[2][2].status = "wumpus"
        # rooms[0][1].status = "wumpus"
        # rooms[2][3].status = "pit"
        # rooms[3][1].status = "pit"
        # rooms[1][0].status = "pit2"
        # rooms[3][3].status = "gold"


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
    screen.blit(
        fire_img_down, (BOXSCALE + FIREPOSITION, BOXSCALE * 4 + FIREPOSITION * 2)
    )
    screen.blit(fire_img_down, ((3 * BOXSCALE) + 35, BOXSCALE * 4 + FIREPOSITION * 2))
    screen.blit(fire_img_left, (0, BOXSCALE + FIREPOSITION))
    screen.blit(fire_img_left, (0, (3 * BOXSCALE) + FIREPOSITION))
    screen.blit(
        fire_img_right, ((4 * BOXSCALE) + FIREPOSITION * 2, BOXSCALE + FIREPOSITION)
    )
    screen.blit(
        fire_img_right,
        ((4 * BOXSCALE) + FIREPOSITION * 2, (3 * BOXSCALE) + FIREPOSITION),
    )


while True:
    Clock.tick(FPS)
    
    #update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

    

    # 현재위치
    currentRoom = rooms[player.x][player.y]


    for event in pygame.event.get():
        # # 게임을 종료시키는 함수
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            textoutput("아무고토 못하쥬?")
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_RIGHT and player.x < 3:
                player.x += 1
                action = 2
            if event.key == pygame.K_LEFT and player.x > 0:
                player.x -= 1
                action = 1
            if event.key == pygame.K_UP and player.y > 0:
                player.y -= 1
                action = 3
            if event.key == pygame.K_DOWN and player.y < 3:
                player.y += 1
                action = 0
            rooms[player.x][player.y].view = True

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
                screen.blit(pit_img, (point(x, y)))
            elif rooms[x][y].status == "pit2":
                screen.blit(pit_img2, (point(x, y)))
            elif rooms[x][y].status == "gold":
                screen.blit(gold_img, (point(x, y)))
            # 지나간곳만 보임 (view가 false일떄)
            if not rooms[x][y].view:
                screen.blit(dark_img, (point(x, y)))
    # 플레이어 렌더링
    # screen.blit(player_img, ))

    #show frame image
    screen.blit(animation_list[action][frame], (point(player.x, player.y)))

    screen.blit(
        font.render(str(player.x) + "," + str(player.y), True, text_color),
        (800, 100),
    )
    for text in textArr:
        x = 30 * (textArr.index(text) + 1)
        screen.blit(text, (800, x + 100))

    pygame.display.update()