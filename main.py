# pylint: disable=C0114
import sys
import os
import pygame
from classes.Player import Player
from classes.Room import Room
from classes.fireball import Fireball
from position import BOXSCALE, RenderMap, mouse_pos_x, mouse_pos_y, point, point_core, point_fireball
import random
import time
import Mixer
import spritesheet
import threading



# Initialize the game engine
# pylint: disable=no-member
pygame.init()

## 게임 창 설정 ##
screen = pygame.display.set_mode((1300, 720))
pygame.display.set_caption("움푸스 월드")  # 창 이름 설정

## 초당 프레임 단위 설정 ## 
FPS = 60
Clock = pygame.time.Clock()

## 컬러 세팅 ##
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 격자만들기(가로)
EDGE = 0  # (0,0)
FRAMSCALE = 265

sprite_sheet_image = pygame.image.load("assets\sprites\wizard.png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)


#create animation list
animation_list = []
animation_steps = [8,7, 6, 8, 8, 6, 3, 7]
action = 1
last_update = pygame.time.get_ticks()
animation_cooldown = 120
frame = 0
step_counter = 0

WIDTH=128
HEIGHT=128

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, WIDTH, HEIGHT, 1.3 ,BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)


pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))



def cursoricon(cursor):
    """칸에 커서올라가면 마우스 변경"""
    if cursor:  # 마우스 커서 on
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
    else:  # 마우스 커서 off
        pygame.mouse.set_cursor(*pygame.cursors.arrow)



def renderimg(src, rscale=BOXSCALE):
    """에셋 불러오기"""
    return pygame.transform.scale(pygame.image.load(src), (rscale, rscale))


frame_img = renderimg("assets/image/frame.png", FRAMSCALE)

map_img = pygame.image.load("assets/image/map.png")
map_img = pygame.transform.scale(map_img, (668, 700))


BG_img = pygame.image.load("assets\image\BG.jpg")
BG_img = pygame.transform.scale(BG_img, (2807, 720))

clear_img = pygame.image.load("assets/image/congratulations.png")
# clear_img =pygame.transform.scale(clear_img, (670, 700))

fire_img = renderimg("assets/image/fire.png")
fire_img_up = pygame.transform.rotate(fire_img, 0)
fire_img_down = pygame.transform.rotate(fire_img, 180)
fire_img_left = pygame.transform.rotate(fire_img, 90)
fire_img_right = pygame.transform.rotate(fire_img, -90)

gold_img = renderimg("assets\image\GEM.png")
wumpus_img = renderimg("assets\image\ork.png")
pit_img = renderimg("assets\image\pitch_rava_.png")
player_img = renderimg("assets/image/player.png")
dark_img = renderimg("assets/image/dark.png")
fog_img = renderimg("assets/image/fog.png")
magic_circle_img = renderimg("assets\image\magic_circle.png")


cursor_img_on = pygame.image.load("assets/image/curcor_on.png")
cursor_img_on = pygame.transform.scale(cursor_img_on, (50,50))
cursor_img_off = pygame.image.load("assets/image/curcor_off.png")
cursor_img_off = pygame.transform.scale(cursor_img_off, (50,50))

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

def textoutput_sensor_wumpus(outtext2):
    """텍스트 출력해주는 함수"""
    text_surface = font.render(outtext2, True, text_color)
    screen.blit(text_surface, (800, 600))

def textoutput_sensor_pitch(outtext2):
    """텍스트 출력해주는 함수"""
    text_surface = font.render(outtext2, True, text_color)
    screen.blit(text_surface, (800, 630))

def textoutput_sensor_gold(outtext2):   
    """텍스트 출력해주는 함수"""
    text_surface = font.render(outtext2, True, text_color)
    screen.blit(text_surface, (550, 610))
    




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
    R1 = random.randrange(0,30)
    R2 = random.randrange(0,30)
    if R1 <= 3 and R2 <= 3 :
        if not (R1 + R2) == 0:
            rooms[R1][R2].status = "wumpus"

for i in range(100):
    R1 = random.randrange(0,30)
    R2 = random.randrange(0,30)
    if R1 <= 3 and R2 <= 3 :
        if not (R1 + R2) == 0:
            rooms[R1][R2].status = "pit"
            
R1 = random.randint(2,3)
R2 = random.randint(2,3)
if not (R1 + R2) == 0:      
    rooms[R1][R2].status = "gold"


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

Gameover_count = 0 


#배경음
# BGM.play()
Mixer.playmusic("assets/music/bgm.mp3", 0.1)    
    
MOVE_right = False
MOVE_left = False
MOVE_up = False
MOVE_down = False

fireball = False

pos_X = (player.x)*130+100
pos_Y = (player.y)*130+40

MOVE = False
GAMEOVER = False

cnt = 0


# 인게임
while True:

    
    
    if fireball:
            action = 3
            cnt += 1
            if cnt == 48:
                fireball = False 
                cnt = 0
                frame = 0
                action = 1 
                MOVE = False
            elif cnt > 48:
                cnt = 0
            
     

    elif MOVE_right:
        MOVE = True
        action = 4
        pos_X += 1
        if (pos_X-100)/130 == player.x:
            MOVE_right = False
            pos_X = 0
            pos_y = 0
            pos_X = (player.x)*130+100
            pos_Y = (player.y)*130+40   
            frame = 0
            action = 1 
            MOVE = False

    elif MOVE_left:
        MOVE = True
        action = 0
        pos_X -= 1
        if (pos_X-100)/130 == player.x:
            MOVE_left = False
            pos_X = 0
            pos_Y = 0
            pos_X = (player.x)*130+100
            pos_Y = (player.y)*130+40 
            frame = 0
            action = 1 
            MOVE = False

    elif MOVE_up:
        MOVE = True
        action = 5
        pos_Y += 1
        if (pos_Y-40)/130 == player.y:
            MOVE_up = False
            pos_X = 0
            pos_y = 0
            pos_X = (player.x)*130+100
            pos_Y = (player.y)*130+40
            frame = 0 
            action = 1 
            MOVE = False

    elif MOVE_down:
        MOVE = True
        action = 5
        pos_Y -= 1
        if (pos_Y-40)/130 == player.y:
            MOVE_down = False
            pos_X = 0
            pos_y = 0
            pos_X = (player.x)*130+100
            pos_Y = (player.y)*130+40 
            frame = 0
            action = 1
            MOVE = False

    

    Clock.tick(FPS)
    
    # 현재위치
    currentRoom = rooms[player.x][player.y]
    if not MOVE:
        for event in pygame.event.get():
            # # 게임을 종료시키는 함수
            if event.type == pygame.QUIT:
                sys.exit()
            # 캐릭터 이동
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                start_pos_X = 0
                start_pos_Y = 0  
                start_pos_X = player.x
                start_pos_Y = player.y

                x1, y1 = pygame.mouse.get_pos()
                X = mouse_pos_x(x1)
                Y = mouse_pos_y(y1)
                if rooms[X][Y].canmove == True:
                    if start_pos_X < X:
                        MOVE_right = True
                    elif start_pos_X > X:
                        MOVE_left = True
                    elif start_pos_Y < Y:
                        MOVE_up = True
                    elif start_pos_Y > Y:
                        MOVE_down = True         
               
                    if abs(player.x - X)==1 or abs(player.y-Y)==1:
                        if rooms[X][Y].canmove:
                            rooms[X][Y].canmove = False
                            player.x = X 
                            player.y = Y
                            rooms[player.x][player.y].view = True
                            Mixer.playsound("assets/music/feet.mp3", 0.5)
                      
                            
                        
            if event.type == pygame.MOUSEBUTTONUP:
                click = False
            
            


            # 히히 화살발사
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.quit()
                if event.key == pygame.K_SPACE:
                    if player.arrows > 0:
                        Mixer.playsound("assets/music/fire.mp3", 0.5)
                        fireball = True

                        player.arrows -= 1
                        x1, y1 = pygame.mouse.get_pos()
                        X = mouse_pos_x(x1)
                        Y = mouse_pos_y(y1)
                        SPEED = 10  
                        vel = (x1 * SPEED, y1 * SPEED) 
                        if player.y > Y:
                            fireball_up = Fireball(point_fireball(player.x, player.y), (0*SPEED,-1*SPEED), fireball_images_up)
                            all_sprites.add(fireball_up)
                        elif player.y < Y: 
                            fireball_down = Fireball(point_fireball(player.x, player.y), (0*SPEED,1*SPEED), fireball_images_down)
                            all_sprites.add(fireball_down)
                        elif player.x > X: 
                            fireball_left = Fireball(point_fireball(player.x, player.y), (-1*SPEED,0*SPEED), fireball_images_left)
                            all_sprites.add(fireball_left)
                        elif player.x < X: 
                            fireball_right = Fireball(point_fireball(player.x, player.y), (1*SPEED,0*SPEED), fireball_images_right)
                            all_sprites.add(fireball_right)
                    
                        if rooms[X][Y].canmove and rooms[X][Y].status == "wumpus":
                            # 애니메이션
                            rooms[X][Y].status = "saferoom"
                            textoutput("움푸스가 뒈졋습니다.")
                            Mixer.playsound("assets\music\wumpus.mp3", 0.5)
                            fireball = False
                
                 

    # 맵 렌더링 background, toach, object(status), view
    all_sprites.update() 

    screen.fill(BLACK)
    screen.blit(BG_img,(0,0))
    

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
                # screen.blit(fog_img, (point(x, y)))


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
    framePos = [-1, 0], [1, 0], [0, -1], [0, 1]
    for pos_box in framePos:
        x = player.x + pos_box[0]
        y = player.y + pos_box[1]
        
        if abs(pos_box[0] + pos_box[1]) == 1:
            if (0 <= x <= 3) and (0 <= y <= 3):
                if rooms[x][y].status == "wumpus":
                    textoutput_sensor_wumpus("웜프스의 냄새가 납니다!")
                if rooms[x][y].status == "pit" :
                    textoutput_sensor_pitch("주위가 뜨겁습니다!") 



    # 플레이어 렌더링
    # screen.blit(player_img, (point(player.x, player.y)))
    screen.blit(magic_circle_img, (point(0, 0)))
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

    

    #게임오버 and 클리어
    if not rooms[player.x][player.y].status == "saferoom":
        #클리어
        if rooms[player.x][player.y].status == "gold":
            Mixer.playsound("assets\music\clear.mp3",0.1)
            screen.blit(clear_img, ((1300-920)/2 ,0))
            textoutput_sensor_gold("축하합니다! 성공입니다!")
            
            rooms[player.x][player.y].status == "saferoom"
            

        #게임오버
        else :
            player.x = 0
            player.y = 0
            player.arrows = 2
            Gameover_count += 1
            textoutput("당신은 죽었습니다.")
            textoutput(f"지금까지 죽은 횟수: {Gameover_count}")
            Mixer.playsound("assets\music\start.mp3",0.5)
            pos_X = 100
            pos_Y = 40
            frame = 0
            action = 7  
            MOVE_right = False
            MOVE_left = False
            MOVE_up = False
            MOVE_down = False
            MOVE = False
    
    #update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

    screen.blit(animation_list[action][frame], (pos_X, pos_Y))
    
    if click == True:
        mx, my = pygame.mouse.get_pos()
        screen.blit(cursor_img_on, (mx-20, my-20))
    
    if click == False:
        mx, my = pygame.mouse.get_pos()
        screen.blit(cursor_img_off, (mx-20, my-20))

    pygame.display.update()
   