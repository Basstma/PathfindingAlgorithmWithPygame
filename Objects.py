

class Positon:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coordinates(self):
        return self.x, self.y

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

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

    def change(self, x_change, y_change):
        self.x += x_change
        self.y += y_change

    def get_possible_switch(self, size):
        switches = []

        if self.x + 1 < size[0]:
            switches.append((1, 0))
        if self.x - 1 >= 0:
            switches.append((-1, 0))
        if self.y + 1 < size[1]:
            switches.append((0, 1))
        if self.y - 1 >= 0:
            switches.append((0, -1))

        return switches


class Wall(Positon):
    def __init__(self, x, y):
        super().__init__(x, y)


class Target(Positon):
    def __init__(self, x, y):
        super().__init__(x, y)


class Visited(Positon):
    def __init__(self, x, y):
        super().__init__(x, y)


class Way(Positon):
    def __init__(self, x, y):
        super().__init__(x, y)

