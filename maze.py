import numpy as np
import time


class Maze:
    def __init__(self, size=(10, 10)):
        self.size = size
        self.maze = np.zeros(self.size)

    def build_maze(self, kind_of_algorithm: str):
        if kind_of_algorithm == "binary_tree":
            self.binary_tree()

    def binary_tree(self):
        for i in range(0, self.size[0], 1):
            for j in range(0, self.size[1], 1):
                options_to_go = []
                if j-1 >= 0:
                    options_to_go.append([i, j-1])
                if i-1 >= 0:
                    options_to_go.append([i-1, j])
                    if len(options_to_go) == 2:
                        wall = options_to_go[np.random.randint(0, 2)]
                        self.maze[wall[0], wall[1]] = 1
                    elif options_to_go:
                        wall = options_to_go[0]
                        self.maze[wall[0], wall[1]] = 1


if __name__ == '__main__':
    maze = Maze()
    maze.build_maze("binary_tree")