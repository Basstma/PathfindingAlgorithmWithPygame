import numpy as np
from threading import Thread

from Maze import *
from Objects import *


class DepthSearch(Thread):
    def __init__(self, maze, start):
        super().__init__()
        self.maze = maze
        self.start_position = start
        self.path_to_target = {}

    def clean_neighbours(self, akt_pos, nbs):

        re = []
        for n in nbs:
            if not self.maze.maze[akt_pos.y + n[1]][akt_pos.x + n[0]]:
                re.append((akt_pos.x + n[0], akt_pos.y + n[1]))
            elif type(self.maze.maze[akt_pos.y + n[1]][akt_pos.x + n[0]]) == Target:
                return self.maze.maze[akt_pos.y + n[1]][akt_pos.x + n[0]]
        return re

    def depthsearch(self, start):
        akt_pos = Visited(x=start[0], y=start[1])
        self.path_to_target[str(akt_pos.x) + ':' + str(akt_pos.y)] = akt_pos
        self.maze.maze[akt_pos.y][akt_pos.x] = akt_pos
        neighbours = akt_pos.get_possible_switch(size=self.maze.size)
        neighbours = self.clean_neighbours(akt_pos, neighbours)
        if type(neighbours) == Target:
            return neighbours

        for neighbour in neighbours:
            time.sleep(self.maze.delay)
            res = self.depthsearch(start=neighbour)
            if res:
                return res
        del self.path_to_target[str(akt_pos.x) + ':' + str(akt_pos.y)]
        return None

    def clean_path(self):
        start = True
        for pos in self.path_to_target.keys():
            if start:
                self.maze.maze[self.path_to_target[pos].y][self.path_to_target[pos].x] = \
                    Start(x=[self.path_to_target[pos].x], y=[self.path_to_target[pos].y])
                start = False
            else:
                self.maze.maze[self.path_to_target[pos].y][self.path_to_target[pos].x] = \
                    Way(x=[self.path_to_target[pos].x], y=[self.path_to_target[pos].y])
    def run(self):
        self.depthsearch(self.start_position)
        self.clean_path()
