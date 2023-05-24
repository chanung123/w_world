# pylint: disable=C0114
import sys
import pygame


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
font = pygame.font.Font(None, 36)
>>>>>>>>> Temporary merge branch 2

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
    # 현재위치
    currentRoom = rooms[player.x][player.y]

    for event in pygame.event.get():
        # # 게임을 종료시키는 함수
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            textOutput("아무고토 못하쥬?")
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_RIGHT and player.x < 3:
                player.x += 1
            if event.key == pygame.K_LEFT and player.x > 0:
                player.x -= 1
            if event.key == pygame.K_UP and player.y > 0:
                player.y -= 1
            if event.key == pygame.K_DOWN and player.y < 3:
                player.y += 1
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
                screen.blit(pit_img, (point(2, 3)))
            elif rooms[x][y].status == "gold":
                screen.blit(gold_img, (point(3, 3)))
            # 지나간곳만 보임 (view가 false일떄)
            if not rooms[x][y].view:
                screen.blit(dark_img, (point(x, y)))
    # 플레이어 렌더링
    screen.blit(player_img, (point(player.x, player.y)))

    screen.blit(
        font.render(str(player.x) + "," + str(player.y), True, text_color),
        (800, 100),
    )
    for text in textArr:
<<<<<<<<< Temporary merge branch 1
        x = 40 * (textArr.index(text) + 1)
=========
        x = 20 * (textArr.index(text) + 1)
>>>>>>>>> Temporary merge branch 2
        screen.blit(text, (800, x + 100))

    pygame.display.update()
<<<<<<<<< Temporary merge branch 1
=========

    # ------------------------------------------

    # # Print the player's location
    # currentRoom = rooms[player.x][player.y]
    # # TODO: Gameover
    # if currentRoom.status == "wumpus":
    #     print("으악! 웜푸스한테 잡아먹혔습니다. YOU DIE")
    # elif currentRoom.status == "pit":
    #     print("읍...웅덩이에 빠져죽었습니다. YOU DIE")
    # # Check if the player has won or lost
    # elif currentRoom.status == "gold":
    #     print("이겼다!")
    #     break

    # print("현재위치 {}.".format((player.x, player.y)))

    # # Let the player sense the Wumpus and the pit
    # snetch = player.sense_wumpus(currentRoom, rooms)
    # breeze = player.sense_pit(currentRoom)
    # if snetch:
    #     print("웜푸스 냄새가 납니다.")
    # if breeze:
    #     print("바람소리가 들립니다.")

    # # 화살쏘기
    # if player.arrows > 0:
    #     shoot = input("화살쏠거? (y/n): ")
    #     if shoot == "y":
    #         # TODO: 화살을 어디로 쏠거냐???
    #         direction = int(input("어디로 쏠래? (w,a,s,d)"))
    #         player.shoot_arrow(direction, snetch)

    # ------------------------------------------
>>>>>>>>> Temporary merge branch 2
