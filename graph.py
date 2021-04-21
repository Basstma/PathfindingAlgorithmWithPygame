

class Graph:
    def __init__(self, position):
        self.x = position[1]
        self.y = position[0]
        self.edges = {}

    def add_edge(self, target_node, edge):
        self.edges[str(target_node)] = edge

    def get_edges_str(self):
        return ', '.join([str(self.edges[e]) + ', length: ' + str(self.edges[e].get_length()) for e in self.edges])

    def __str__(self):
        return str(self.y) + ":" + str(self.x)


class Edge:
    def __init__(self, node_one: Graph, node_two: Graph):
        self.node_one = node_one
        self.node_two = node_two
        self.length = None

    def set_length(self, length: float):
        self.length = length

    def get_length(self):
        return self.length

    def __str__(self):
        return str(self.node_one) + '-' + str(self.node_two)

    def get_way(self):
        """
        Generates all waypoints that are in the maze and are included in the edge
        :return: a list of (y, x) coordinates in maze
        """
        oy = self.node_one.y
        ox = self.node_one.x
        ty = self.node_two.y
        tx = self.node_two.x

        waypoints = []
        if oy == ty:
            if ox > tx:
                for i in range(tx+1, ox):
                    waypoints.append((oy, i))
            else:
                for i in range(ox+1, tx):
                    waypoints.append((oy, i))
        if ox == tx:
            if oy > ty:
                for i in range(ty+1, oy):
                    waypoints.append((i, ox))
            else:
                for i in range(oy+1, ty):
                    waypoints.append((i, ox))

        return waypoints