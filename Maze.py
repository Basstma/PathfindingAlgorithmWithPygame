import numpy as np
from threading import Thread

from Objects import *


class Maze:
    def __init__(self, size):
        self.size = size
        self.maze = [[None for i in range(self.size[0])] for j in range(self.size[1])]
        print('x:', len(self.maze[0]), 'y:', len(self.maze))

        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if i == 0 or i == self.size[1]-1:
                    self.maze[i][j] = Wall(x=j, y=i)
                if j == 0 or j == self.size[0]-1:
                    self.maze[i][j] = Wall(x=j, y=i)

        self.pos = {}

    def build(self):
        creation = Thread(target=self.create)
        creation.start()

    def create(self):
        np.random.seed(66)
        start_point = np.random.randint


if __name__ == '__main__':
    m = Maze(size=(10, 10))