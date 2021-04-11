import numpy as np
import time
from threading import Thread


class Maze:
    def __init__(self, size=(10, 10)):
        self.size = size
        self.maze = np.zeros(self.size)

    def build_maze(self, kind_of_algorithm: str):
        if kind_of_algorithm == "binary_tree":
            binary_three_thrad = Thread(target=self.binary_tree)
            binary_three_thrad.start()
            #self.binary_tree()

    def binary_tree(self):
        for i in range(0, self.size[0], 2):
            for j in range(0, self.size[1], 2):
                options_to_go = []
                self.maze[i][j] = 1
                if self.maze[j-2][i] == 1:
                    options_to_go.append([i, j-1])
                if self.maze[j][i-2] == 1:
                    options_to_go.append([i-1, j])

                if len(options_to_go) == 2:
                    to_wall = options_to_go[np.random.randint(0, 2)]
                    self.maze[to_wall[0]][to_wall[1]] = 1
                elif options_to_go:
                    to_wall = options_to_go[0]
                    self.maze[to_wall[0]][to_wall[1]] = 1
                time.sleep(1)


if __name__ == '__main__':
    maze = Maze()
    maze.build_maze("binary_tree")