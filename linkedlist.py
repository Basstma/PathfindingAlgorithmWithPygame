from graph import *


class Node:
    def __init__(self, privious, position: tuple):
        """
        Init for class Node, for linked List
        :param privious: Element in List that is one position in front of the actual item
        :param position: The x and y coardinates in the maze
        """
        self.y = position[0]
        self.x = position[1]
        self.privious = privious

    def __str__(self):
        """
        Function that returns an string that is used for indexing the Node in dict
        :return:
        """
        return str(self.y) + ':' + str(self.x)


class NodeGraph:
    def __init__(self, itself: Graph, privious: Graph, edge: Edge):
        """
        Init for Node in linked List
        Its used for Nodes after converting the maze in an Graph
        :param itself: The node that is the actual point in the Graph
        :param privious: The element of the privious Node
        :param edge:
        """
        self.itself = itself
        self.privious = privious
        self.edge = edge
        self.length = 0

    def add_length(self, length):
        """
        Length to this waypoint from start
        :param length: the length to add
        :return:
        """
        self.length += length

    def get_length(self):

        return self.length
