from config import *
import pygame as pg
from maze import Maze


class Display:
    def __init__(self, maze: Maze, scale: int = 10):
        """
        Inint for Display class.
        :param maze: An maze from class maze
        :param scale: the size in pygame that should is used as size for one plotted rectangle
        """
        self.maze = maze

        self.scale = scale
        self.window_size = (self.maze.size[0] * scale, self.maze.size[1] * scale)

        self.running = True

        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(self.window_size)
        self.FPS = 60

    def run(self):
        """
        Function for running pygame window
        :return:
        """
        while self.running:
            pg.display.flip()
            self.display()
            self.clock.tick(self.FPS)

    def display(self):
        def draw_rectangle(pos: list, color: str):
            pg.draw.rect(self.screen, colors[color],
                         (pos[0] * self.scale, (pos[1] * self.scale), self.scale, self.scale))

        for i in range(0, self.maze.size[0]):
            for j in range(0, self.maze.size[1]):
                if self.maze.maze[i][j] == 0:
                    # Color for Borders
                    draw_rectangle((i, j), color="black")
                elif self.maze.maze[i][j] == 1:
                    # Color for waypoints
                    draw_rectangle((i, j), color="white")
                elif self.maze.maze[i][j] == 2:
                    # color for way
                    draw_rectangle((i, j), color="blue")
                elif self.maze.maze[i][j] == 3:
                    # color for start point
                    draw_rectangle((i, j), color="green")
                elif self.maze.maze[i][j] == 4:
                    # color for target point
                    draw_rectangle((i, j), color="red")
                elif self.maze.maze[i][j] == 5:
                    # color for way
                    draw_rectangle((i, j), color="blue_widesearch")
                elif self.maze.maze[i][j] == 6:
                    # color for nodes
                    draw_rectangle((i, j), color="grey_four")
                elif self.maze.maze[i][j] == 11:
                    # color for actual checking point in Graph generation
                    draw_rectangle((i, j), color="grey_three")
                elif self.maze.maze[i][j] == 12:
                    # color for actual checking point in Graph generation
                    draw_rectangle((i, j), color="grey_five")


if __name__ == '__main__':
    maze = Maze(size=(1000, 1000))
    d = Display(maze, scale=1)