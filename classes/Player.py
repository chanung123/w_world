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