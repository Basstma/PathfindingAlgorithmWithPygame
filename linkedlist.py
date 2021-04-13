class Node:
    def __init__(self, privious, position: tuple):
        self.y = position[0]
        self.x = position[1]
        self.privious = privious

    def __str__(self):
        return str(self.y) + ':' + str(self.x)