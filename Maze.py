import numpy as np
from threading import Thread
import time

from Objects import *


class Maze:
    def __init__(self, size):
        self.size = size
        self.maze = [[None for i in range(self.size[0])] for j in range(self.size[1])]
        self.delay = 0

        self.pos = {}

    def build(self):
        creation = Thread(target=self.create)
        creation.start()

    def create(self):
        #np.random.seed(69)
        actual_point = (0, 1)
        already_visited = []
        points = {
            str(actual_point[0]) + ':' + str(actual_point[1]): self.maze[actual_point[1]][actual_point[0]]
        }

        actual_name = str(actual_point[0]) + ':' + str(actual_point[1])
        actual = points[actual_name]

        while points.keys():
            """
            Takes all neighbor in points.
            Only not if they already in points. Than look if this point is a Wall if yes: 
                If more than one wall returned than self cant be an new wall
            """
            nbs = []
            if not actual:
                actual = Positon(actual_point[0], actual_point[1])
            neighbor = actual.get_neighbor(self.size)
            wall_count = 0
            for p in neighbor:
                p_name = str(p[0]) + ':' + str(p[1])
                if p_name not in points.keys() and p_name not in already_visited:
                    points[p_name] = self.maze[p[1]][p[0]]
                    nbs.append(p)
                if type(self.maze[p[1]][p[0]]) == Wall:
                    wall_count += 1

            if wall_count <= 1 and np.random.randint(0, 10) != 1:
                self.maze[actual_point[1]][actual_point[0]] = Wall(actual_point[0], actual_point[1])
                points[str(actual_point[0]) + ':' + str(actual_point[1])] = self.maze[actual_point[1]][actual_point[0]]

            already_visited.append(actual_name)
            del points[actual_name]

            if nbs:
                actual_point = nbs[np.random.randint(0, len(nbs))]
                actual = points[str(actual_point[0]) + ':' + str(actual_point[1])]
            else:
                if list(points.keys()):
                    point = np.random.choice(list(points.keys()))
                    actual_point = [int(number) for number in point.split(':')]
                    actual = points[point]

            actual_name = str(actual_point[0]) + ':' + str(actual_point[1])
            time.sleep(self.delay)
        print("Maze is builded")

    def add_target(self, kind='standard'):
        if kind == 'standard':
            x = np.random.randint(0, self.size[0])
            y = np.random.randint(0, self.size[1])

            if np.random.randint(0, 2) == 1:
                x = np.random.choice([0, self.size[0] - 1])
            else:
                y = np.random.choice([0, self.size[1] - 1])
        elif kind == 'random':
            x = np.random.randint(0, self.size[0])
            y = np.random.randint(0, self.size[1])
        else:
            x = self.size[0] - 1
            y = self.size[1] - 1

        self.maze[y][x] = Target(x=x, y=y)
        print("Target added", x, y)


if __name__ == '__main__':
    m = Maze(size=(10, 10))