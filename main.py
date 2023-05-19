import sys
import pygame
from pygame.locals import *
<<<<<<<<< Temporary merge branch 1
=========
import random
import time

# ------------------------------------


# class Room:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.status = "saferoom"


# class Player:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.arrows = 2

#     def move(self, dx, dy):
#         self.x += dx
#         self.y += dy

#     def shoot_arrow(self, direction, currentroom):
#         if self.arrows > 0:
#             self.arrows -= 1
#             if direction == "w":
#                 print("나이샷! 웜푸스가 뒤졌습니다!")
#             else:
#                 print("어따쏘는거죠? 웜푸스를 놓쳤습니다.")

#     def sense_wumpus(currentroom):
#         # TODO: 4가지 방향에 웜푸스가 있을경우 snetch
#         if currentroom.status == "wumpus":
#             print("You smell a Wumpus!")
#         else:
#             print("You don't smell a Wumpus.")

#     def sense_pit(self):
#         # TODO: 4가지 방향에 웅덩이가 있을경우 breeze
#         if self.pit and self.x == self.pit.x and self.y == self.pit.y:
#             print("You feel a breeze!")
#         else:
#             print("You don't feel a breeze.")


# def main():
#     # Create the rooms
#     rooms = [[], [], [], []]
#     for i in range(4):
#         for j in range(4):
#             rooms[i].append(Room(i, j))

#     # 어디위치에 있는지 설정하기.
#     rooms[2][2].status = "wumpus"
#     rooms[2][3].status = "pit"
#     rooms[3][3].status = "gold"

#     # Create the player
#     player = Player(0, 0)

#     print(rooms)


# if __name__ == "__main__":
#     main()


# ------------------------------------

>>>>>>>>> Temporary merge branch 2

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

# 격자만들기(가로)
x = 0  # (0,0)
y = 130
z = 100
r = 35


## 게임 창 설정 ##
screen = pygame.display.set_mode((1300, 720))
screen.fill(WHITE)  # 하얀색으로 배경 채우기
pygame.display.set_caption("움푸스 월드")  # 창 이름 설정

# 에셋 불러오기
map_img = pygame.image.load("assets/map.png")
map_img = pygame.transform.scale(map_img, (670, 700))

fire_img = pygame.image.load("assets/fire.png")
fire_img = pygame.transform.scale(fire_img, (y, y))
fire_img_u = pygame.transform.rotate(fire_img, 0)
fire_img_d = pygame.transform.rotate(fire_img, 180)
fire_img_l = pygame.transform.rotate(fire_img, 90)
fire_img_r = pygame.transform.rotate(fire_img, -90)


gold_img = pygame.image.load("assets/gold in box.png")
gold_img = pygame.transform.scale(gold_img, (y, y))

wumpus_img = pygame.image.load("assets/wumpus.png")
wumpus_img = pygame.transform.scale(wumpus_img, (y, y))

pitch_img = pygame.image.load("assets/pitch.png")
pitch_img = pygame.transform.scale(pitch_img, (y, y))

pitch_img2 = pygame.image.load("assets/pitch_rava.png")
pitch_img2 = pygame.transform.scale(pitch_img2, (y, y))

player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (y, y))

dark_img = pygame.image.load("assets/dark.png")
dark_img = pygame.transform.scale(dark_img, (y, y))

player_posX = 0
player_posY = 0

# def rand_point(x , y):


def point(postionX, postionY):
    if postionX >= 0 and postionX <= 3:
        if postionY >= 0 and postionY <= 3:
            return ((postionX * y) + z, ((postionY) * y) + z)

    if postionX > 3 or postionY > 3:
        return (((postionX) * y) + z, ((postionY - 1) * y) + z)


# def light():


def dark():
    for i in range(4):
        for j in range(4):
            if i != player_posX or j != player_posY:
                screen.blit(dark_img, (point(i, j)))


text_color = WHITE  # Black
font = pygame.font.Font(None, 36)
>>>>>>>>> Temporary merge branch 2

# text_surface = font.render("asdasdasdasd", True, text_color)
textArr = []


def textOutput(text):
    text_surface = font.render(text, True, text_color)
    textArr.append(text_surface)
    if len(textArr) > 10:
        del textArr[0]


while True:
    Clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
<<<<<<<<< Temporary merge branch 1
            textOutput("멍충한 놈~")
=========
            textOutput("hahahahaha")
>>>>>>>>> Temporary merge branch 2
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

    screen.fill(BLACK)

    screen.blit(map_img, (24, 10))

    screen.blit(fire_img, (y + r, 0))
    screen.blit(fire_img, ((3 * y) + r, 0))

    screen.blit(fire_img_d, (y + r, y * 4 + r * 2))
    screen.blit(fire_img_d, ((3 * y) + 35, y * 4 + r * 2))

    screen.blit(fire_img_l, (0, y + r))
    screen.blit(fire_img_l, (0, (3 * y) + r))

    screen.blit(fire_img_r, ((4 * y) + r * 2, y + r))
    screen.blit(fire_img_r, ((4 * y) + r * 2, (3 * y) + r))

    screen.blit(wumpus_img, (point(2, 2)))

    screen.blit(wumpus_img, (point(0, 2)))

    screen.blit(pitch_img, (point(2, 3)))

    screen.blit(pitch_img2, (point(1, 0)))

    screen.blit(gold_img, (point(3, 3)))
    # 격자만들기(가로)
    x = 0  # (0,0)
    y = 130
    z = 100

    for i in range(5):
        pygame.draw.line(screen, BLACK, (x + z, 0 + z), (x + z, (y * 4) + z), width=3)
        pygame.draw.line(screen, BLACK, (0 + z, x + z), ((y * 4) + z, x + z), width=3)
        x += y

    screen.blit(player_img, (point(player_posX, player_posY)))

    dark()

    screen.blit(
        font.render(str(player_posX) + "," + str(player_posY), True, text_color),
        (800, 100),
    )
    for text in textArr:
<<<<<<<<< Temporary merge branch 1
        x = 40 * (textArr.index(text) + 1)
=========
        x = 20 * (textArr.index(text) + 1)
>>>>>>>>> Temporary merge branch 2
        screen.blit(text, (800, x + 100))

    # # 게임을 종료시키는 함수
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
