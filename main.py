# pylint: disable=C0114
import sys
import os
import pygame
from classes.Player import Player
from classes.Room import Room
from classes.fireball import Fireball
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

# 파이어볼

# Spritesheet 이미지 로드
fireball_spritesheet_down = pygame.image.load(os.path.join("assets", "sprites", "FireBall_64x64_down.png"))
fireball_spritesheet_up = pygame.image.load(os.path.join("assets", "sprites", "FireBall_64x64_up.png"))
fireball_spritesheet_left = pygame.image.load(os.path.join("assets", "sprites", "FireBall_64x64_left.png"))
fireball_spritesheet_right = pygame.image.load(os.path.join("assets", "sprites", "FireBall_64x64_right.png"))


# fireball 추출된 sprite 이미지 담을 리스트
fireball_images_up = []
fireball_images_down = []
fireball_images_left = []
fireball_images_right = []


# 추출할 각각의 sprite 이미지 크기 
sprite_width = 64
sprite_height = 64

for i in range(0, fireball_spritesheet_up.get_width(), sprite_width):
    # (i, 0) 위치부터 sprite_width x sprite_height 크기로 이미지 추출
    sprite_rect = pygame.Rect((i, 0), (sprite_width, sprite_height))
    sprite_image = pygame.Surface(sprite_rect.size, pygame.SRCALPHA)
    sprite_image.blit(fireball_spritesheet_up, (0, 0), sprite_rect)
    fireball_images_up.append(sprite_image)

for i in range(0, fireball_spritesheet_down.get_width(), sprite_width):
    # (i, 0) 위치부터 sprite_width x sprite_height 크기로 이미지 추출
    sprite_rect = pygame.Rect((i, 0), (sprite_width, sprite_height))
    sprite_image = pygame.Surface(sprite_rect.size, pygame.SRCALPHA)
    sprite_image.blit(fireball_spritesheet_down, (0, 0), sprite_rect)
    fireball_images_down.append(sprite_image)

for i in range(0, fireball_spritesheet_left.get_width(), sprite_width):
    # (i, 0) 위치부터 sprite_width x sprite_height 크기로 이미지 추출
    sprite_rect = pygame.Rect((i, 0), (sprite_width, sprite_height))
    sprite_image = pygame.Surface(sprite_rect.size, pygame.SRCALPHA)
    sprite_image.blit(fireball_spritesheet_left, (0, 0), sprite_rect)
    fireball_images_left.append(sprite_image)

for i in range(0, fireball_spritesheet_right.get_width(), sprite_width):
    # (i, 0) 위치부터 sprite_width x sprite_height 크기로 이미지 추출
    sprite_rect = pygame.Rect((i, 0), (sprite_width, sprite_height))
    sprite_image = pygame.Surface(sprite_rect.size, pygame.SRCALPHA)
    sprite_image.blit(fireball_spritesheet_right, (0, 0), sprite_rect)
    fireball_images_right.append(sprite_image)
    
# fireball_up = Fireball((0, 0), (0, 0), fireball_images_up)
# fireball_down = Fireball((0, 0), (0, 0), fireball_images_down)
# fireball_left = Fireball((0, 0), (0, 0), fireball_images_left)
# fireball_right = Fireball((0, 0), (0, 0), fireball_images_right)

# 스프라이트 그룹 생성
all_sprites = pygame.sprite.Group()
# all_sprites.add(fireball_up)
# all_sprites.add(fireball_down)
# all_sprites.add(fireball_left)
# all_sprites.add(fireball_right)

player_rect = player_img.get_rect()

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
                rooms[player.x][player.y].view = True
                # 감지 - breeze, snatch
                # 사망

        # 히히 화살발사
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.arrows -= 1
                x1, y1 = pygame.mouse.get_pos()
                X = mouse_pos_x(x1)
                Y = mouse_pos_y(y1)
                SPEED = 0.05 
                vel = (x1 * SPEED, y1 * SPEED) 
                fireball_up = Fireball(point(player.x+0.5, player.y+0.5), vel, fireball_images_up)
                fireball_down = Fireball(point(player.x+0.5, player.y+0.5), vel, fireball_images_down)
                fireball_left = Fireball(point(player.x+0.5, player.y+0.5), vel, fireball_images_left)
                fireball_right = Fireball(point(player.x+0.5, player.y+0.5), vel, fireball_images_right)

                all_sprites.add(fireball_up)
                all_sprites.add(fireball_down)
                all_sprites.add(fireball_left)
                all_sprites.add(fireball_right)

                if rooms[X][Y].canmove and rooms[X][Y].status == "wumpus":
                    # 애니메이션
                    rooms[X][Y].status = "saferoom"
                    textoutput("움푸스가 뒈졋습니다.")

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
                screen.blit(pit_img, (point(2, 3)))
            elif rooms[x][y].status == "gold":
                screen.blit(gold_img, (point(3, 3)))
            # 지나간곳만 보임 (view가 false일떄)
            if not rooms[x][y].view:
                screen.blit(dark_img, (point(x, y)))

    all_sprites.draw(screen)

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

    # rec1=Fireball.rect
    # print(rec1)


    pygame.display.update()
