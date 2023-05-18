import random


class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = "saferoom"


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.arrows = 2

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def shoot_arrow(self, direction, currentroom):
        if self.arrows > 0:
            self.arrows -= 1
            if direction == "w":
                print("나이샷! 웜푸스가 뒤졌습니다!")
            else:
                print("어따쏘는거죠? 웜푸스를 놓쳤습니다.")

    def sense_wumpus(currentroom):
        # TODO: 4가지 방향에 웜푸스가 있을경우 snetch
        if currentroom.status == "wumpus":
            print("You smell a Wumpus!")
        else:
            print("You don't smell a Wumpus.")

    def sense_pit(self):
        # TODO: 4가지 방향에 웅덩이가 있을경우 breeze
        if self.pit and self.x == self.pit.x and self.y == self.pit.y:
            print("You feel a breeze!")
        else:
            print("You don't feel a breeze.")


def main():
    # Create the rooms
    rooms = [[], [], [], []]
    for i in range(4):
        for j in range(4):
            rooms[i].append(Room(i, j))

    # 어디위치에 있는지 설정하기.
    rooms[2][2].status = "wumpus"
    rooms[2][3].status = "pit"
    rooms[3][3].status = "gold"

    # Create the player
    player = Player(0, 0)

    print(rooms)

    # Start the game
    while True:
        # Print the player's location
        currentRoom = rooms[player.x][player.y]
        # TODO: Gameover
        if currentRoom.status == "wumpus":
            print("으악! 웜푸스한테 잡아먹혔습니다. YOU DIE")
        elif currentRoom.status == "pit":
            print("읍...웅덩이에 빠져죽었습니다. YOU DIE")
        # Check if the player has won or lost
        elif currentRoom.status == "gold":
            print("이겼다!")
            break

        print("현재위치 {}.".format((player.x, player.y)))

        # Let the player sense the Wumpus and the pit
        snetch = player.sense_wumpus(currentRoom, rooms)
        breeze = player.sense_pit(currentRoom)
        if snetch:
            print("웜푸스 냄새가 납니다.")
        if breeze:
            print("바람소리가 들립니다.")

        # 화살쏘기
        if player.arrows > 0:
            shoot = input("화살쏠거? (y/n): ")
            if shoot == "y":
                # TODO: 화살을 어디로 쏠거냐???
                direction = int(input("어디로 쏠래? (w,a,s,d)"))
                player.shoot_arrow(direction, snetch)

        # 방옮기기
        move = input("Enter a move (w, a, s, d): ")
        if move == "w":
            player.move(-1, 0)
        elif move == "a":
            player.move(0, -1)
        elif move == "s":
            player.move(1, 0)
        elif move == "d":
            player.move(0, 1)


if __name__ == "__main__":
    main()
