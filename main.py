# pylint: disable=C0114
import sys
import os
import pygame
from classes.Player import Player
from classes.Room import Room
from classes.fireball import Fireball
from position import (
    BOXSCALE,
    RenderMap,
    mouse_pos_x,
    mouse_pos_y,
    point,
    point_core,
    point_fireball,
)
import random

from wumpus_ai import Action

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

pygame.mouse.set_cursor(
    (8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0)
)
# pygame.mouse.set_visible(False)

BGM = pygame.mixer.Sound("assets/music/bgm.mp3")
BGM.set_volume(0.05)

feet_sound = pygame.mixer.Sound("assets/music/feet.mp3")
feet_sound.set_volume(0.5)

clear_sound = pygame.mixer.Sound("assets/music/clear.mp3")
clear_sound.set_volume(0.1)

start_sound = pygame.mixer.Sound("assets/music/start.mp3")
start_sound.set_volume(0.4)

fireball_sound = pygame.mixer.Sound("assets/music/fire.mp3")
fireball_sound.set_volume(0.4)

wumpus_sound = pygame.mixer.Sound("assets/music/wumpus.mp3")
wumpus_sound.set_volume(0.6)


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


frame_img = renderimg("assets/image/frame.png", FRAMSCALE)

map_img = pygame.image.load("assets/image/map.png")
map_img = pygame.transform.scale(map_img, (670, 700))

clear_img = pygame.image.load("assets/image/congratulations.png")
# clear_img =pygame.transform.scale(clear_img, (670, 700))

fire_img = renderimg("assets/image/fire.png")
fire_img_up = pygame.transform.rotate(fire_img, 0)
fire_img_down = pygame.transform.rotate(fire_img, 180)
fire_img_left = pygame.transform.rotate(fire_img, 90)
fire_img_right = pygame.transform.rotate(fire_img, -90)

gold_img = renderimg("assets/image/gold in box.png")
wumpus_img = renderimg("assets/image/wumpus.png")
pit_img = renderimg("assets/image/pitch_rava.png")
player_img = renderimg("assets/image/player.png")
dark_img = renderimg("assets/image/dark.png")

cursor_img_on = pygame.image.load("assets/image/curcor_on.png")
cursor_img_on = pygame.transform.scale(cursor_img_on, (50, 50))
cursor_img_off = pygame.image.load("assets/image/curcor_off.png")
cursor_img_off = pygame.transform.scale(cursor_img_off, (50, 50))

click = False


text_color = WHITE  # Black
font = pygame.font.Font("uhBeePuding.ttf", 28)
textArr = []


def textoutput(outtext):
    """텍스트 출력해주는 함수"""
    text_surface = font.render(outtext, True, text_color)
    textArr.append(text_surface)
    if len(textArr) > 10:
        del textArr[0]


def textoutput_sensor(outtext, x, y):
    """감지텍스트출력"""
    text_surface = font.render(outtext, True, text_color)
    screen.blit(text_surface, (x, y))


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
for i in range(100):
    R1 = random.randrange(0, 30)
    R2 = random.randrange(0, 30)
    if R1 <= 3 and R2 <= 3:
        if not (R1 + R2) == 0:
            rooms[R1][R2].status = "wumpus"

for i in range(100):
    R1 = random.randrange(0, 30)
    R2 = random.randrange(0, 30)
    if R1 <= 3 and R2 <= 3:
        if not (R1 + R2) == 0:
            rooms[R1][R2].status = "pit"

R1 = random.randint(2, 3)
R2 = random.randint(2, 3)
if not (R1 + R2) == 0:
    rooms[R1][R2].status = "gold"


# 파이어볼

# fireball 추출된 sprite 이미지 담을 리스트
fireball_images = [[], [], [], []]
fireball_eachway_image = ["up", "down", "left", "right"]
# 추출할 각각의 sprite 이미지 크기
sprite_width = 64
sprite_height = 64


# 파이어볼 로드(이미지 불러오기)
def fireball_load(idx, image):
    # Spritesheet 이미지 로드
    fireball_spritesheet = pygame.image.load(os.path.join("assets", "sprites", image))
    for i in range(0, fireball_spritesheet.get_width(), sprite_width):
        # (i, 0) 위치부터 sprite_width x sprite_height 크기로 이미지 추출
        sprite_rect = pygame.Rect((i, 0), (sprite_width, sprite_height))
        sprite_image = pygame.Surface(sprite_rect.size, pygame.SRCALPHA)
        sprite_image.blit(fireball_spritesheet, (0, 0), sprite_rect)
        fireball_images[idx].append(sprite_image)


# 상하좌우로딩
for idx, val in enumerate(fireball_eachway_image):
    val = f"FireBall_64x64_{val}.png"
    fireball_load(idx, val)


def fireball_render(
    x,
    y,
    direction,
):
    """파이어볼 렌더링"""
    speed = 10
    vel = (x * speed, y * speed)
    fireball = Fireball(
        point_fireball(player.x, player.y),
        vel,
        fireball_images[direction],
    )
    all_sprites.add(fireball)


# 스프라이트 그룹 생성
all_sprites = pygame.sprite.Group()
player_rect = player_img.get_rect()


# 배경음
BGM.play()


# 인게임
def shoot_arrow(target):
    if player.arrows > 0:
        fireball_sound.play()
        fireball_sound.fadeout(500)
        player.arrows -= 1
        X, Y = target

        if player.y > Y:
            # up
            fireball_render(0, -1, 0)
        elif player.y < Y:
            # down
            fireball_render(0, 1, 1)
        elif player.x > X:
            # left
            fireball_render(-1, 0, 2)
        elif player.x < X:
            # right
            fireball_render(1, 0, 3)

        if rooms[X][Y].canmove and rooms[X][Y].status == "wumpus":
            # 애니메이션
            rooms[X][Y].status = "saferoom"
            textoutput(' "끼엑!!" 움푸스가 뒈졋습니다.')
            wumpus_sound.play()


action = Action()

gameover_count = 0


def move(target):
    global gameover_count
    X, Y = target
    if abs(player.x - X) == 1 or abs(player.y - Y) == 1:
        # if rooms[X][Y].canmove:
        #     rooms[X][Y].canmove = False
        player.x = X
        player.y = Y
        rooms[player.x][player.y].view = True
        # 게임오버 and 클리어
    if not rooms[player.x][player.y].status == "saferoom":
        # 클리어
        if rooms[player.x][player.y].status == "gold":
            screen.blit(clear_img, ((1300 - 920) / 2, 0))
            textoutput_sensor("축하합니다! 성공입니다!", 500, 610)
            clear_sound.play()
            # 게임오버
        else:
            player.x = 0
            player.y = 0
            player.arrows = 2
            gameover_count += 1
            textoutput("당신은 죽었습니다.")
            textoutput(f"지금까지 죽은 횟수: {gameover_count}")
            start_sound.play()


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
            # x1, y1 = pygame.mouse.get_pos()
            # shoot_arrow((mouse_pos_x(x1), mouse_pos_y(y1)))
            move((1, 0))

        # 히히 화살발사
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.quit()
            if event.key == pygame.K_SPACE:
                action.move(player, "down")
                # x1, y1 = pygame.mouse.get_pos()
                # shoot_arrow((mouse_pos_x(x1), mouse_pos_y(y1)))

    # 맵 렌더링 background, toach, object(status), view
    all_sprites.update()

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
                screen.blit(pit_img, (point(x, y)))
            elif rooms[x][y].status == "gold":
                screen.blit(gold_img, (point(x, y)))
            # 지나간곳만 보임 (view가 false일떄)
            if not rooms[x][y].view:
                screen.blit(dark_img, (point(x, y)))

    all_sprites.draw(screen)

    # 이동할 수 있는 곳 밝은 프레임으로 감싸기
    framePos = [-1, 0], [1, 0], [0, -1], [0, 1]
    for pos_box in framePos:
        x = player.x + pos_box[0]
        y = player.y + pos_box[1]
        x1, y1 = pygame.mouse.get_pos()
        if abs(pos_box[0] + pos_box[1]) == 1:
            if (0 <= x <= 3) and (0 <= y <= 3):
                if mouse_pos_x(x1) == x and mouse_pos_y(y1) == y:
                    rooms[x][y].canmove = True
                    screen.blit(frame_img, (point_core(x, y, FRAMSCALE)))
    # 감지
    for pos_box in framePos:
        x = player.x + pos_box[0]
        y = player.y + pos_box[1]

        if abs(pos_box[0] + pos_box[1]) == 1:
            if (0 <= x <= 3) and (0 <= y <= 3):
                if rooms[x][y].status == "wumpus":
                    if not "w" in rooms[x][y].sensor:
                        rooms[x][y].sensor.append("w")
                    textoutput_sensor("웜프스의 냄새가 납니다!", 800, 600)
                if rooms[x][y].status == "pit":
                    if not "p" in rooms[x][y].sensor:
                        rooms[x][y].sensor.append("p")
                    textoutput_sensor("주위가 뜨겁습니다!", 800, 630)

    # 플레이어 렌더링
    screen.blit(player_img, (point(player.x, player.y)))
    # 현재위치
    screen.blit(
        font.render(str(player.x) + "," + str(player.y), True, text_color), (800, 100)
    )
    # 화살수
    screen.blit(
        font.render("화살: " + str(player.arrows) + "개", True, text_color), (850, 100)
    )

    for text in textArr:
        x = 30 * (textArr.index(text) + 1)
        screen.blit(text, (800, x + 100))

    if click == True:
        mx, my = pygame.mouse.get_pos()
        screen.blit(cursor_img_on, (mx - 20, my - 20))

    if click == False:
        mx, my = pygame.mouse.get_pos()
        screen.blit(cursor_img_off, (mx - 20, my - 20))

    pygame.display.update()
