from Objects import *

import numpy as np
import time
from threading import Thread


class Bot:
    def __init__(self, maze):
        self.position = Positon(1, 1)
        self.maze = maze

    def find_target(self):
        find = Thread(target=self.random_search())
        find.start()

    def random_search(self):
        neighbours = self.position.get_possible_switch(self.maze.size)

        n = neighbours[np.random.randint(0, len(neighbours))]
        next_position = self.maze.maze[n[1]][n[0]]

        while next_position != type(Target):
            self.position.change(x_change=n[0], y_change=n[1])
            neighbours = self.position.get_possible_switch(self.maze.size)
            n = neighbours[np.random.randint(0, len(neighbours))]
            next_position = self.maze.maze[n[1]][n[0]]
            time.sleep(1)

