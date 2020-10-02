

class Positon:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coordinates(self):
        return self.x, self.y

    def get_neighbor(self, size):
        neighbor = []

        pos_x = (-1, 0, 1)
        pos_y = (-1, 0, 1)
        for y in pos_y:
            for x in pos_x:
                if x == 0 and y == 0:
                    continue
                elif self.x + x < 0 or self.x + x >= size[0] or self.y + y < 0 or self.y + y >= size[1]:
                    continue
                else:
                    neighbor.append((self.x + x, self.y + y))
        return neighbor


class Wall(Positon):
    def __init__(self, x, y):
        super().__init__(x, y)