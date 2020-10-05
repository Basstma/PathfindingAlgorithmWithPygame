import numpy as np
from threading import Thread

from Maze import *
from Objects import *


class WideSearch(Thread):
    def __init__(self, maze, start):
        super().__init__()
        self.maze = maze
        self.start_position = start
        self.posisions = {}
        self.way_to_target = {}

    def clean_neighbours(self, akt_pos, nbs):

        re = []
        for n in nbs:
            if not self.maze.maze[akt_pos.y + n[1]][akt_pos.x + n[0]]:
                re.append((akt_pos.x + n[0], akt_pos.y + n[1]))
            elif type(self.maze.maze[akt_pos.y + n[1]][akt_pos.x + n[0]]) == Target:
                return self.maze.maze[akt_pos.y + n[1]][akt_pos.x + n[0]]
        return re

    def widesearch(self):
        akt_pos = Visited(x=self.start_position[0], y=self.start_position[1])
        self.posisions[str(akt_pos.x) + ':' + str(akt_pos.y)] = akt_pos
        while self.posisions.keys():
            self.maze.maze[akt_pos.y][akt_pos.x] = akt_pos
            neighbours = akt_pos.get_possible_switch(size=self.maze.size)
            neighbours = self.clean_neighbours(akt_pos, neighbours)
            for neighbour in neighbours:
                self.posisions[str(neighbour[0]) + ':' + str(neighbour[1])] = Visited(x=neighbour[0], y=neighbour[1])
            del self.posisions[list(self.posisions.keys())[0]]
            if not list(self.posisions.keys()):
                break
            akt_pos = self.posisions[list(self.posisions.keys())[0]]
            if type(akt_pos) == Target:
                break
            time.sleep(0.01)

    def run(self):
        self.widesearch()
        #self.clean_path()
