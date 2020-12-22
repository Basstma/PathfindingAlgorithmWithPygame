import pygame as pg
import time

from Maze import *
from Bot import *
from depthsearch import *
from widesearch import *


class Visio:
    def __init__(self):
        self.maze = Maze(size=(50, 40))
        self.bot = None
        self.scale = 10

        self.window_size = (500, 500)
        self.navbar_size = (self.window_size[0], 100)
        self.maze_size = self.maze.size * 10

        self.running = True

        self.time_steps = [0.00001, 0.0001, 0.001, 0.01, 0.1, 0.5, 1]
        self.time_pos = 0

        self.colors = {"black": (0, 0, 0),
                       "white": (255, 255, 255),
                       "red": (255, 0, 0),
                       "green": (0, 255, 0),
                       "blue": (0, 0, 255),
                       "yellow": (255, 255, 0),
                       "pink": (255, 0, 255),
                       "turquoise": (0, 255, 255),
                       "grey_one": (50, 50, 50)}

        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(self.window_size)
        self.FPS = 60

    def build_naviagation(self):
        pass

    def draw_map(self):
        def draw_rectangle_maze(pos: list, color: str):
            pg.draw.rect(self.screen, self.colors[color],
                         (pos[0] * self.scale, (pos[1] * self.scale) + self.navbar_size[1], self.scale, self.scale))

        for i in range(0, self.maze.size[1]):
            for j in range(0, self.maze.size[0]):
                if type(self.maze.maze[i][j]) == Wall:
                    draw_rectangle_maze((j, i), "white")

                elif type(self.maze.maze[i][j]) == Target:
                    draw_rectangle_maze((j, i), "red")

                elif type(self.maze.maze[i][j]) == Visited:
                    draw_rectangle_maze((j, i), "grey_one")

                elif type(self.maze.maze[i][j]) == Way:
                    draw_rectangle_maze((j, i), "turquoise")

                elif type(self.maze.maze[i][j]) == Start:
                    draw_rectangle_maze((j, i), "green")

    def run(self):
        while self.running:
            self.screen.fill(self.colors["black"])
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        print("Build Maze")
                        self.maze.build()
                    if event.key == pg.K_d:
                        print("Depth search started")
                        d = DepthSearch(self.maze, (1, 0))
                        d.start()
                    if event.key == pg.K_w:
                        print("Wide search started")
                        w = WideSearch(self.maze, (1, 0))
                        w.start()
                    if event.key == pg.K_0:
                        print("Add Target at edge")
                        self.maze.add_target()
                    if event.key == pg.K_1:
                        print("Add Target random")
                        self.maze.add_target(kind="random")
                    if event.key == pg.K_2:
                        print("Add target in left_down_corner")
                        self.maze.add_target(kind="botton_right_coronor")
                    if event.key == pg.K_n:
                        print("Reseted Maze")
                        self.maze = Maze(size=(50, 50))
                    if event.key == pg.K_r:
                        print("Start removing every sign except Walls")
                        for i in range(len(self.maze.maze)):
                            for j in range(len(self.maze.maze[i])):
                                if type(self.maze.maze[i][j]) != Wall:
                                    self.maze.maze[i][j] = None
                    if event.key == pg.K_t:
                        self.time_pos += 1
                        if self.time_pos >= len(self.time_steps):
                            self.time_pos = 0
                        print("Delay auf:", self.time_steps[self.time_pos])
                        self.maze.delay = self.time_steps[self.time_pos]
                if event.type == pg.MOUSEBUTTONDOWN:
                    is_hold = True
                    while is_hold:
                        if event.button == 1:
                            x, y = self.get_position_in_maze(pg.mouse.get_pos())
                            if (x and y) or (x == 0 or y == 0):
                                self.maze.maze[y][x] = None
                        if event.button == 3:
                            x, y = self.get_position_in_maze(pg.mouse.get_pos())
                            print(x, y)
                            if (x and y) or (x == 0 or y == 0):
                                print(x)
                                self.maze.maze[y][x] = Wall(x=x, y=y)
                        for e in pg.event.get():
                            if e.type == pg.MOUSEBUTTONUP:
                                is_hold = False
                        self.draw_map()
                        pg.display.flip()
                """if event.type == pg.QUIT:
                    raise SystemExit"""
            self.draw_map()
            pg.display.flip()
            self.clock.tick(self.FPS)

    def get_position_in_maze(self, pos: list) -> list:
        pos = (pos[0], pos[1]-self.navbar_size[1])
        x = int((pos[0] - (pos[0] % self.scale)) / self.scale)
        y = int((pos[1] - (pos[1] % self.scale)) / self.scale)
        if x >= self.maze.size[0] or x < 0 or y >= self.maze.size[1] or y < 0:
            return None, None
        else:
            return x, y


if __name__ == '__main__':
    v = Visio()
    time.sleep(0.0001)
    v.run()