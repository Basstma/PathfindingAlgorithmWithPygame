

class Graph:
    def __init__(self, position):
        self.x = position[1]
        self.y = position[0]

        self.edges = {}

    def add_edge(self, target_node, edge):
        self.edges[str(target_node)] = edge

    def __str__(self):
        return str(self.y) + ":" + str(self.x)


class Edge:
    def __init__(self, node_one: Graph, node_two: Graph):
        self.node_one = node_one
        self.node_two = node_two
