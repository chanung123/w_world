import random
import PIL import Image

# 이미지 로드
image = Image.open("image.jpg")

# 이미지 표시
image.show()

class WumpusWorld:
    def __init__(self, size):
        self.size = size
        self.grid = [[Cell() for _ in range(size)] for _ in range(size)]
        self.player_position = (0, 0)
        self.generate_world()

    def generate_world(self):
        # Place the Wumpus
        wumpus_x = random.randint(0, self.size - 1)
        wumpus_y = random.randint(0, self.size - 1)
        self.grid[wumpus_x][wumpus_y].has_wumpus = True

        # Place the gold
        gold_x = random.randint(0, self.size - 1)
        gold_y = random.randint(0, self.size - 1)
        self.grid[gold_x][gold_y].has_gold = True

        # Place some pits
        num_pits = random.randint(1, self.size // 2)
        for _ in range(num_pits):
            pit_x = random.randint(0, self.size - 1)
            pit_y = random.randint(0, self.size - 1)
            self.grid[pit_x][pit_y].has_pit = True

    def move(self, direction):
        x, y = self.player_position

        if direction == 'up' and x > 0:
            x -= 1
        elif direction == 'down' and x < self.size - 1:
            x += 1
        elif direction == 'left' and y > 0:
            y -= 1
        elif direction == 'right' and y < self.size - 1:
            y += 1

        self.player_position = (x, y)
        self.check_cell()

    def check_cell(self):
        x, y = self.player_position
        cell = self.grid[x][y]

        if cell.has_wumpus:
            print("You got eaten by the Wumpus! Game over.")
        elif cell.has_pit:
            print("You fell into a pit! Game over.")
        elif cell.has_gold:
            print("Congratulations! You found the gold and won the game.")
        else:
            print("You are in an empty room.")

class Cell:
    def __init__(self):
        self.has_wumpus = False
        self.has_pit = False
        self.has_gold = False

# Creating and playing the game
size = 5
game = WumpusWorld(size)

while True:
    print("Enter your move (up, down, left, right):")
    move = input()
    game.move(move)