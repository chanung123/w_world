class Room:
    """방"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = "saferoom"
        self.canmove = False
        self.view = False