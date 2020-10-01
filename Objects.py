

class Positon:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coordinates(self):
        return self.x, self.y


class Wall(Positon):
    def __init__(self, x, y):
        super().__init__(x, y)