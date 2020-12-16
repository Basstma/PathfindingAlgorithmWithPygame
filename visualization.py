import pygame as pg
import time

from Maze import *
from Bot import *
from depthsearch import *
from widesearch import *


class Visio:
    def __init__(self):
        self.maze = Maze(size=(40, 40))
        self.bot = None
        self.scale = 10

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
                elif type(self.maze.maze[i][j]) == Start:
                    pg.draw.rect(self.screen, self.colors["green"],
                                 (j * self.scale, i * self.scale, self.scale, self.scale))

    def draw_bot(self):
        if self.bot:
            pg.draw.rect(self.screen, self.colors["yellow"],
                         (self.bot.position.y * self.scale, self.bot.position.x * self.scale, self.scale, self.scale))

    def run(self):
        while self.running:
            self.screen.fill(self.colors["black"])
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        print("Build Maze")
                        self.maze.build()
                    # if event.key == pg.K_w:
                    #     if self.bot:
                    #         print("Bot is searching!")
                    #         self.bot.find_target()
                    #     else:
                    #         print("Bot is builded")
                    #         self.bot = Bot(self.maze)
                    # if event.key == pg.K_q:
                    #     print("Bot deleted")
                    #     self.bot = None
                    if event.key == pg.K_d:
                        print("Depth search started")
                        d = DepthSearch(self.maze, (1, 0))
                        d.start()
                    if event.key == pg.K_f:
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