from graph import *

class Node:
    def __init__(self, privious, position: tuple):
        self.y = position[0]
        self.x = position[1]
        self.privious = privious

    def __str__(self):
        return str(self.y) + ':' + str(self.x)


class NodeGraph:
    def __init__(self, itself: Graph, privious: Graph, edge: Edge):
        self.itself = itself
        self.privious = privious
        self.edge = edge
        self.length = 0

    def add_length(self, length):
        self.length += length

    def get_length(self):
        return self.length
