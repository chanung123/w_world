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
FRAMSCALE = 265
MOVE = False
CLICK = False

MX = 0
MY = 0
COLUMN_COUNT = 4
ROW_COUNT = 4
MOUS_X = 0
MOUS_Y = 0

column_index1 = 0
row_index1 = 0
column_index2 = 0
row_index2 = 0

frame_img = pygame.image.load("assets/frame.png")
frame_img = pygame.transform.scale(frame_img, (FRAMSCALE, FRAMSCALE))
frame_img_Rect = frame_img.get_rect()

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
for i in range(COLUMN_COUNT):
    for j in range(ROW_COUNT):
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
        if event.type == pygame.KEYDOWN:
            textoutput("키보드 이동")
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

            # 마우스 버튼이 눌렸을 때
        if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos

                column_index1 = mouse_pos_x(x1)
                row_index1 = mouse_pos_y(y1)

                rooms[column_index1][row_index1].view =True

                screen.blit(frame_img, (point_core(column_index1, row_index1, BOXSCALE, FRAMSCALE)))

                CLICK = not CLICK
                MOVE = True
            
                M_icon(CLICK)
               
                player.x = column_index1
                player.y = row_index1

                textoutput("마우스 이동")

                

            # if CLICK == 0:
            #     x2, y2 = event.pos

            #     column_index2 = mouse_pos_x(x2)
            #     row_index2 = mouse_pos_y(y2)

            #     screen.blit(frame_img, (point_core(column_index2, row_index2, BOXSCALE, FRAMSCALE)))

            #     CLICK = not CLICK
            #     MOVE = True
            
            #     M_icon(CLICK)
                
            #     player.x = column_index2
            #     player.y = row_index2



        # # 마우스 버튼이 올라갔을 때
        # if event.type == pygame.MOUSEBUTTONUP:
        # # Image가 이동하면 안되므로 MOVE는 False로
        #     MOVE = False

        #     # 마우스 커서의 모양을 기본값인 화살표 모양으로 변경
        #     M_icon(CLICK)
        #     # pygame.mouse.set_cursor(*pygame.cursors.arrow)


           

        
                                    

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
              

    
    screen.blit(frame_img, (point_core(column_index1, row_index1, BOXSCALE, FRAMSCALE)))

    if CLICK:
        # 플레이어 렌더링
        screen.blit(player_img, (point(player.x, player.y)))

        
    
    # 플레이어 렌더링
    screen.blit(player_img, (point(player.x, player.y)))

    x1, y1 = pygame.mouse.get_pos()
    column_index1 = mouse_pos_x(x1)
    row_index1 = mouse_pos_y(y1)
    screen.blit(frame_img, (point_core(column_index1, row_index1, BOXSCALE, FRAMSCALE)))


    screen.blit(font.render(str(player.x) + "," + str(player.y), True, text_color),(800, 100))

    
    for text in textArr:
        x = 30 * (textArr.index(text) + 1)
        screen.blit(text, (800, x + 100))


    

    pygame.display.update()