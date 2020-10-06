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
        self.path = None

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
        name = str(akt_pos.x) + ':' + str(akt_pos.y)
        path = None
        self.posisions[name] = akt_pos
        self.way_to_target[name] = [akt_pos]
        while self.posisions.keys():
            self.maze.maze[akt_pos.y][akt_pos.x] = akt_pos
            neighbours = akt_pos.get_possible_switch(size=self.maze.size)
            neighbours = self.clean_neighbours(akt_pos, neighbours)
            if type(neighbours) == Target:
                self.path = self.way_to_target[name]
                break
            else:
                for neighbour in neighbours:
                    new_name = str(neighbour[0]) + ':' + str(neighbour[1])
                    self.posisions[new_name] = Visited(x=neighbour[0], y=neighbour[1])
                    self.way_to_target[new_name] = self.way_to_target[name].copy()
                    self.way_to_target[new_name].append(self.posisions[new_name])
                #del self.way_to_target[name]
                del self.posisions[list(self.posisions.keys())[0]]
                if not list(self.posisions.keys()):
                    break
                akt_pos = self.posisions[list(self.posisions.keys())[0]]
                name = str(akt_pos.x) + ':' + str(akt_pos.y)
                time.sleep(self.maze.delay)

    def clean_path(self):
        if self.path:
            start = True
            for object in self.path:
                if start:
                    self.maze.maze[object.y][object.x] = Start(x=object.x, y=object.y)
                    start = False
                else:
                    self.maze.maze[object.y][object.x] = Way(x=object.x, y=object.y)

    def run(self):
        self.widesearch()
        self.clean_path()
