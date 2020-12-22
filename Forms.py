import pygame as pg

class Button:
    def __init__(self, pos: list, size: list, color: list, function):
        self.pos = pos
        self.size = size
        self.color = color
        self.function = function

    def draw(self, screen):
        (self.pos[0], self.pos[1], self.size[0], self.size[1])
        pg.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))

    def is_clicked(self, click_pos):
        in_x = self.pos[0] <= click_pos[0] <= self.pos[0] + self.size[0]
        in_y = self.pos[1] <= click_pos[1] <= self.pos[1] + self.size[1]
        if in_x and in_y:
            return True
        else:
            return False

    def action(self):
        self.function()