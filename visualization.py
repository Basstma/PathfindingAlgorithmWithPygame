import pygame as pg
import time

from Maze import *
from Bot import *
from depthsearch import *
from widesearch import *


class Visio:
    def __init__(self):
        self.maze = Maze(size=(50, 50))
        self.bot = None
        self.scale = 10

        self.running = True

        self.colors = {"black": (0, 0, 0),
                       "white": (255, 255, 255),
                       "red": (255, 0, 0),
                       "green": (0, 255, 0),
                       "blue": (0, 0, 255),
                       "yellow": (255, 255, 0),
                       "pink": (255, 0, 255),
                       "turquoise": (0, 255, 255),
                       "grey_one": (102, 102, 102)}

        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.maze.size[0] * self.scale, self.maze.size[1] * self.scale))
        self.FPS = 60

    def draw_map(self):
        for i in range(0, self.maze.size[1]):
            for j in range(0, self.maze.size[0]):
                if type(self.maze.maze[i][j]) == Wall:
                    pg.draw.rect(self.screen, self.colors["white"],
                                 (j * self.scale, i * self.scale, self.scale, self.scale))
                elif type(self.maze.maze[i][j]) == Target:
                    pg.draw.rect(self.screen, self.colors["red"],
                                 (j * self.scale, i * self.scale, self.scale, self.scale))
                elif type(self.maze.maze[i][j]) == Visited:
                    pg.draw.rect(self.screen, self.colors["grey_one"],
                                 (j * self.scale, i * self.scale, self.scale, self.scale))
                elif type(self.maze.maze[i][j]) == Way:
                    pg.draw.rect(self.screen, self.colors["turquoise"],
                                 (j * self.scale, i * self.scale, self.scale, self.scale))

    def draw_bot(self):
        if self.bot:
            pg.draw.rect(self.screen, self.colors["green"],
                         (self.bot.position.y * self.scale, self.bot.position.x * self.scale, self.scale, self.scale))

    def run(self):
        while self.running:
            self.screen.fill(self.colors["black"])
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        self.maze.build()
                    if event.key == pg.K_w:
                        if self.bot:
                            self.bot.find_target()
                        else:
                            self.bot = Bot(self.maze)
                    if event.key == pg.K_q:
                        self.bot = None
                    if event.key == pg.K_d:
                        d = DepthSearch(self.maze, (1, 0))
                        d.start()
                    if event.key == pg.K_f:
                        w = WideSearch(self.maze, (1, 0))
                        w.start()
                    if event.key == pg.K_0:
                        self.maze.add_target()
                    if event.key == pg.K_1:
                        self.maze.add_target(kind="random")
                    if event.key == pg.K_2:
                        self.maze.add_target(kind="botton_right_coronor")
                    if event.key == pg.K_n:
                        self.maze = Maze(size=(50, 50))
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pg.mouse.get_pos()
                        x = int((pos[0] - (pos[0] % self.scale)) / self.scale)
                        y = int((pos[1] - (pos[1] % self.scale)) / self.scale)
                        self.maze.maze[y][x] = None
                    if event.button == 3:
                        pos = pg.mouse.get_pos()
                        x = int((pos[0] - (pos[0] % self.scale)) / self.scale)
                        y = int((pos[1] - (pos[1] % self.scale)) / self.scale)
                        self.maze.maze[y][x] = Wall(x=x, y=y)
                """if event.type == pg.QUIT:
                    raise SystemExit"""
            self.draw_map()
            self.draw_bot()
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    v = Visio()
    time.sleep(0.0001)
    v.run()