import numpy as np
from threading import Thread
import time

from Objects import *


class Maze:
    def __init__(self, size):
        self.size = size
        self.maze = [[None for i in range(self.size[0])] for j in range(self.size[1])]

        #for i in range(self.size[1]):
        #    for j in range(self.size[0]):
        #        if i == 0 or i == self.size[1]-1:
        #            self.maze[i][j] = Wall(x=j, y=i)
        #        if j == 0 or j == self.size[0]-1:
        #            self.maze[i][j] = Wall(x=j, y=i)

        self.pos = {}

    def build(self):
        creation = Thread(target=self.create)
        creation.start()

    def create(self):
        np.random.seed(66)
        actual_point = (0, 2)
        points = {
            str(actual_point[0]) + ':' + str(actual_point[1]): self.maze[actual_point[1]][actual_point[0]]
        }

        actual = points[str(actual_point[0]) + ':' + str(actual_point[1])]

        while points.keys():
            """
            Takes all neighbor in points.
            Only not if they already in points. Than look if this point is a Wall if yes: 
                If more than one wall returned than self cant be an new wall
            """
            if not actual:
                actual = Positon(actual_point[0], actual_point[1])
            neighbor = actual.get_neighbor(self.size)
            wall_count = 0
            for p in neighbor:
                p_name = str(p[0]) + ':' + str(p[1])
                if p_name not in points.keys():
                    points[p_name] = self.maze[p[1]][p[0]]
                if type(points[p_name]) == Wall:
                    wall_count += 1

            if wall_count <= 1: #np.random.randint(1, 3):
                self.maze[actual_point[1]][actual_point[0]] = Wall(actual_point[0], actual_point[1])
                points[str(actual_point[0]) + ':' + str(actual_point[1])] = self.maze[actual_point[1]][actual_point[0]]

            del points[str(actual_point[0]) + ':' + str(actual_point[1])]

            actual_point = neighbor[np.random.randint(0, len(neighbor))]
            actual = points[str(actual_point[0]) + ':' + str(actual_point[1])]

            #time.sleep(0.001)




if __name__ == '__main__':
    m = Maze(size=(10, 10))