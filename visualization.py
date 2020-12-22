import pygame as pg
import time

from Maze import *
from Bot import *
from depthsearch import *
from widesearch import *
from Forms import *


class Visio:
    def __init__(self):
        self.scale = 10

        self.window_size = (500, 500)

        self.navbar_size = (self.window_size[0], 100)
        print(int(self.window_size[0]/self.scale), int((self.window_size[1]-self.navbar_size[1])/self.scale))
        self.maze = Maze(
            size=(int(self.window_size[0]/self.scale), int((self.window_size[1]-self.navbar_size[1])/self.scale))
        )

        self.maze_size = self.maze.size * self.scale

        self.running = True

        self.time_steps = [0.00001, 0.0001, 0.001, 0.01, 0.1, 0.5, 1]
        self.time_pos = 0

        self.colors = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "pink": (255, 0, 255),
            "turquoise": (0, 255, 255),
            "grey_one": (50, 50, 50)}

        self.active_drawing = {
            "mannual": False,
            "target": False,
            "start": False,
        }

        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(self.window_size)
        self.FPS = 60

        self.buttons = [
            Button((5, 5), (40, 20), self.colors["white"], function=self.activate_manual_drawing),  # Button Manual draw
            Button((50, 5), (40, 20), self.colors["red"], function=self.activate_target_drawing),  # Button for Target draw
            Button((95, 5), (40, 20), self.colors["green"], function=self.activate_start_drawing),  # Button for Start draw
        ]

    def build_naviagation(self):
        for button in self.buttons:
            button.draw(self.screen)

        # pg.draw.line(self.screen,
        #              color=self.colors["white"],
        #              start_pos=(0, self.navbar_size[1]),
        #              end_pos=(self.window_size[0], self.navbar_size[1]))

    def check_button_is_clicked(self,click_pos):
        for button in self.buttons:
            if button.is_clicked(click_pos):
                button.action()

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

                else:
                    draw_rectangle_maze((j,i), "black")

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
                        d = DepthSearch(self.maze)
                        d.start()
                    if event.key == pg.K_w:
                        print("Wide search started")
                        w = WideSearch(self.maze)
                        w.start()
                    if event.key == pg.K_n:
                        print("Reseted Maze")
                        self.maze = Maze(size=self.maze.size)
                        self.maze.start = None
                    if event.key == pg.K_r:
                        print("Start removing every sign except Walls")
                        for i in range(len(self.maze.maze)):
                            for j in range(len(self.maze.maze[i])):
                                if type(self.maze.maze[i][j]) != Wall:
                                    self.maze.maze[i][j] = None
                        self.maze.start = None
                    if event.key == pg.K_t:
                        self.change_timedelay()
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if pos[1] < self.navbar_size[1]:
                        self.check_button_is_clicked(pos)
                    else:
                        if self.active_drawing["mannual"]:
                            self.draw_manualy_maze(event, pos)
                        elif self.active_drawing["start"]:
                            self.handl_start(event, pos)
                        elif self.active_drawing["target"]:
                            self.handl_target(event, pos)
            self.display()
            pg.display.flip()
            self.clock.tick(self.FPS)

    def display(self):
        self.build_naviagation()
        self.draw_map()

    def change_timedelay(self):
        self.time_pos += 1
        if self.time_pos >= len(self.time_steps):
            self.time_pos = 0
        print("Delay auf:", self.time_steps[self.time_pos])
        self.maze.delay = self.time_steps[self.time_pos]

    def handl_start(self, event, pos):
        if self.maze.start:
            is_hold = True
            while is_hold:
                if event.button == 1:
                    x, y = self.get_position_in_maze(pos)
                    self.maze.move_start(x, y)
                for e in pg.event.get():
                    if e.type == pg.MOUSEBUTTONUP:
                        is_hold = False
                    else:
                        pos = pg.mouse.get_pos()
                # Draw window
                self.display()
                pg.display.flip()
        else:
            x, y = self.get_position_in_maze(pos)
            self.maze.add_start(x, y)

    def handl_target(self, event, pos):
        if self.maze.target:
            is_hold = True
            while is_hold:
                if event.button == 1:
                    x, y = self.get_position_in_maze(pos)
                    self.maze.move_target(x, y)
                for e in pg.event.get():
                    if e.type == pg.MOUSEBUTTONUP:
                        is_hold = False
                    else:
                        pos = pg.mouse.get_pos()
                # Draw window
                self.display()
                pg.display.flip()
        else:
            x, y = self.get_position_in_maze(pos)
            self.maze.add_target(x, y)

    def draw_manualy_maze(self, event, pos):
        is_hold = True
        while is_hold:
            if event.button == 1:
                x, y = self.get_position_in_maze(pos)
                if (x and y) or (x == 0 or y == 0):
                    self.maze.maze[y][x] = None
            if event.button == 3:
                x, y = self.get_position_in_maze(pos)
                if (x and y) or (x == 0 or y == 0):
                    self.maze.maze[y][x] = Wall(x=x, y=y)
            for e in pg.event.get():
                if e.type == pg.MOUSEBUTTONUP:
                    is_hold = False
                else:
                    pos = pg.mouse.get_pos()
            # Draw window
            self.display()
            pg.display.flip()

    def get_position_in_maze(self, pos: list) -> list:
        pos = (pos[0], pos[1]-self.navbar_size[1])
        x = int((pos[0] - (pos[0] % self.scale)) / self.scale)
        y = int((pos[1] - (pos[1] % self.scale)) / self.scale)
        if x >= self.maze.size[0] or x < 0 or y >= self.maze.size[1] or y < 0:
            return None, None
        else:
            return x, y

    def activate_draw(self, kind: str):
        for k in self.active_drawing.keys():
            self.active_drawing[k] = False
        self.active_drawing[kind] = True
        print(self.active_drawing)

    def activate_manual_drawing(self):
        self.activate_draw("mannual")

    def activate_target_drawing(self):
        self.activate_draw("target")

    def activate_start_drawing(self):
        self.activate_draw("start")


if __name__ == '__main__':
    v = Visio()
    time.sleep(0.0001)
    v.run()