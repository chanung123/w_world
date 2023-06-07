class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.arrows = 2

    def die(self):
        """사망"""
        print("죽었다!")
        # 웜푸스를 만났을떄
        # pit에 빠졌을떄
