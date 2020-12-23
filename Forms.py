import pygame as pg


class Rectangle:
    def __init__(self, pos: list, size: list, color: list):
        self.pos = pos
        self.size = size
        self.color = color

    def draw(self, screen):
        (self.pos[0], self.pos[1], self.size[0], self.size[1])
        pg.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))

    # def draw_text(self, text):
    #     middl = (self.size[0]/2),
    #     for e in text.upper():


class Button(Rectangle):
    def __init__(self, pos: list, size: list, color: list, function):
        Rectangle.__init__(self, pos, size, color)
        self.function = function

    def is_clicked(self, click_pos):
        in_x = self.pos[0] <= click_pos[0] <= self.pos[0] + self.size[0]
        in_y = self.pos[1] <= click_pos[1] <= self.pos[1] + self.size[1]
        if in_x and in_y:
            return True
        else:
            return False

    def action(self):
        self.function()
