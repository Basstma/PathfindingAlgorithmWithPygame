import numpy as np
import time
from threading import Thread


class Maze:
    def __init__(self, size=(10, 10)):
        self.size = size
        self.maze = np.zeros(self.size)
        self.delay = 0
        self.active_prozess = False

    def set_delay(self, delay: int):
        self.delay = delay

    def clear(self):
        if not self.active_prozess:
            self.maze = self.maze = np.zeros(self.size)

    def build_maze(self, kind_of_algorithm: str, start_as_thread: bool=True):
        if not self.active_prozess:
            if kind_of_algorithm == "binary_tree":
                if start_as_thread:
                    binary_three_thrad = Thread(target=self.binary_tree)
                    binary_three_thrad.start()
                else:
                    self.binary_tree()
                self.active_prozess = True

            if kind_of_algorithm == "prims":
                if start_as_thread:
                    prims_thread =Thread(target=self.prims)
                    prims_thread.start()
                else:
                    self.prims()
                self.active_prozess = True

    def binary_tree(self):
        for i in range(0, self.size[0], 2):
            for j in range(0, self.size[1], 2):
                options_to_go = []
                self.maze[i][j] = 1.
                if self.maze[i][j-2] == 1.:
                    options_to_go.append([i, j-1])
                if self.maze[i-2][j] == 1:
                    options_to_go.append([i-1, j])

                if len(options_to_go) == 2:
                    to_wall = options_to_go[np.random.randint(0, 2)]
                    self.maze[to_wall[0]][to_wall[1]] = 1.
                elif options_to_go:
                    to_wall = options_to_go[0]
                    self.maze[to_wall[0]][to_wall[1]] = 1.
                if self.delay:
                    time.sleep(self.delay)
        self.active_prozess = False

    def prims(self):
        points = [(0, 0)]
        while len(points) > 0:
            index = np.random.randint(0, len(points))
            starting_point = points[index]
            # Get Next Points
            if self.maze[starting_point[0]][starting_point[1] - 2] == 0 and starting_point[1] - 2 >= 0:
                self.maze[starting_point[0]][starting_point[1] - 2] = 2
                points.append((starting_point[0], starting_point[1] - 2))
            if starting_point[1] + 2 < self.size[1]:
                if self.maze[starting_point[0]][starting_point[1] + 2] == 0:
                    self.maze[starting_point[0]][starting_point[1] + 2] = 2
                    points.append((starting_point[0], starting_point[1] + 2))
            if self.maze[starting_point[0] - 2][starting_point[1]] == 0 and starting_point[0] - 2 >= 0:
                self.maze[starting_point[0] - 2][starting_point[1]] = 2
                points.append((starting_point[0] - 2, starting_point[1]))
            if starting_point[0] + 2 < self.size[0]:
                if self.maze[starting_point[0] + 2][starting_point[1]] == 0:
                    self.maze[starting_point[0] + 2][starting_point[1]] = 2
                    points.append((starting_point[0] + 2, starting_point[1]))


            # Build Ways
            self.maze[starting_point[0]][starting_point[1]] = 1

            options_to_go = []

            if self.maze[starting_point[0]][starting_point[1] - 2] == 1:
                options_to_go.append((0, -1))
            if starting_point[1] + 2 < self.size[1]:
                if self.maze[starting_point[0]][starting_point[1] + 2] == 1:
                    options_to_go.append((0, 1))
            if self.maze[starting_point[0] - 2][starting_point[1]] == 1:
                options_to_go.append((-1, 0))
            if starting_point[0] + 2 < self.size[0]:
                if self.maze[starting_point[0] + 2][starting_point[1]] == 1:
                    options_to_go.append((1, 0))

            if options_to_go:
                to_way = options_to_go[np.random.randint(0, len(options_to_go))]
                self.maze[starting_point[0] + to_way[0]][starting_point[1] + to_way[1]] = 1
            time.sleep(self.delay)

            points.pop(index)

        self.active_prozess = False


if __name__ == '__main__':
    maze = Maze()
    maze.build_maze("binary_tree")