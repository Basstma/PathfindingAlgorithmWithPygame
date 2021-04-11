from config import *
from threading import Thread
import pygame as pg
from maze import Maze
import time


class Display:
    def __init__(self, maze: Maze, scale:int=10):
        self.maze = maze

        self.scale = scale
        self.window_size = (self.maze.size[0] * scale, self.maze.size[1] * scale)

        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(self.window_size)
        self.FPS = 60

        self.run()

    def run(self):
        i = 0
        while True:
            pg.display.flip()
            self.display()
            self.clock.tick(self.FPS)
            if i == 5:
                #print("Build Maze")
                self.maze.build_maze("binary_tree")
                #print("Maze is build")
            i += 1

    def display(self):

        def draw_rectangle(pos: list, color: str):
            pg.draw.rect(self.screen, colors[color],
                         (pos[0] * self.scale, (pos[1] * self.scale), self.scale, self.scale))

        for i in range(0, self.maze.size[0]):
            for j in range(0, self.maze.size[1]):
                if self.maze.maze[j][i] == 1:
                    draw_rectangle((i, j), color="white")



if __name__ == '__main__':
    maze = Maze(size=(20, 20))
    d = Display(maze, scale=10)