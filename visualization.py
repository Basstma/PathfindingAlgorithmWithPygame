import pygame as pg
import time

from Maze import *


class Visio:
    def __init__(self):
        self.maze = Maze(size=(50, 50))
        self.scale = 10

        self.running = True

        self.colors = {"black": (0, 0, 0),
                       "white": (255, 255, 255),
                       "red": (255, 0, 0),
                       "green": (0, 255, 0),
                       "blue": (0, 0, 255),
                       "yellow": (255, 255, 0),
                       "pink": (255, 0, 255),
                       "turquoise": (0, 255, 255)}

        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.maze.size[0] * self.scale, self.maze.size[1] * self.scale))
        self.FPS = 60

    def draw_map(self):
        for i in range(0, self.maze.size[1]):
            for j in range(0, self.maze.size[0]):
                if type(self.maze.maze[i][j]) == Wall:
                    pg.draw.rect(self.screen, self.colors["white"],
                                 (j * self.scale, i * self.scale, self.scale, self.scale))

    def run(self):
        while self.running:
            self.screen.fill(self.colors["black"])
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        self.maze.build()
            self.draw_map()
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    v = Visio()
    time.sleep(0.5)
    v.run()