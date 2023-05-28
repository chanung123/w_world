class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.arrows = 2

    def shoot_arrow(self, direction, currentroom):
        """히히 화살발사"""
        if self.arrows > 0:
            self.arrows -= 1
            if direction == "w":
                currentroom.status = "wumpus"
                print("나이샷! 웜푸스가 뒤졌습니다!")
            else:
                print("어따쏘는거죠? 웜푸스를 놓쳤습니다.")

    def die(self):
        """사망"""
        print("죽었다!")
        # 웜푸스를 만났을떄
        # pit에 빠졌을떄
