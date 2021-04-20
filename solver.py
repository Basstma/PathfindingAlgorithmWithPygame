from maze import Maze
from linkedlist import Node, NodeGraph
from graph import Graph, Edge
from threading import Thread
import time


class Solver:
    def __init__(self, maze: Maze, target: int):
        self.maze = maze
        self.start = self.maze.start
        self.target = self.maze.target

    def run(self):
        pass

    def draw_way(self, nodes: dict, end_node: Node):
        self.maze.maze[end_node.y][end_node.x] = 4
        self.maze.maze[self.start[0]][self.start[1]] = 3
        node = end_node.privious
        while node.privious:
            self.maze.maze[node.y][node.x] = 5
            node = nodes[str(node.privious)]
            time.sleep(self.maze.delay)

    def find_possible_next_steps(self, actual_possition: tuple):
        next_steps = []
        if actual_possition[1] + 1 < self.maze.size[1]:
            if self.maze.maze[actual_possition[0]][actual_possition[1] + 1] == 1:
                next_steps.append((actual_possition[0], actual_possition[1] + 1))
                self.maze.maze[actual_possition[0]][actual_possition[1] + 1] = 11
            elif self.maze.maze[actual_possition[0]][actual_possition[1] + 1] == 4:
                next_steps.append((actual_possition[0], actual_possition[1] + 1))

        if actual_possition[1] - 1 >= 0:
            if self.maze.maze[actual_possition[0]][actual_possition[1] - 1] == 1:
                next_steps.append((actual_possition[0], actual_possition[1] - 1))
                self.maze.maze[actual_possition[0]][actual_possition[1] - 1] = 11
            elif self.maze.maze[actual_possition[0]][actual_possition[1] - 1] == 1:
                next_steps.append((actual_possition[0], actual_possition[1] - 1))

        if actual_possition[0] + 1 < self.maze.size[0]:
            if self.maze.maze[actual_possition[0] + 1][actual_possition[1]] == 1:
                next_steps.append((actual_possition[0] + 1, actual_possition[1]))
                self.maze.maze[actual_possition[0] + 1][actual_possition[1]] = 11
            elif self.maze.maze[actual_possition[0] + 1][actual_possition[1]] == 1:
                next_steps.append((actual_possition[0] + 1, actual_possition[1]))

        if actual_possition[0] - 1 >= 0:
            if self.maze.maze[actual_possition[0] - 1][actual_possition[1]] == 1:
                next_steps.append((actual_possition[0] - 1, actual_possition[1]))
                self.maze.maze[actual_possition[0] - 1][actual_possition[1]] = 11
            elif self.maze.maze[actual_possition[0] - 1][actual_possition[1]] == 1:
                next_steps.append((actual_possition[0] - 1, actual_possition[1]))

        return next_steps

    def maze_to_graph(self):
        def is_edge(y, x):
            w1, w2, w3, w4 = False, False, False, False
            if y > 0:
                if self.maze.maze[y - 1][x] == 1 or self.maze.maze[y - 1][x] == 6:
                    w1 = True
            if self.maze.size[0] > y + 1:
                if self.maze.maze[y + 1][x] == 1 or self.maze.maze[y + 1][x] == 6:
                    w2 = True
            if x > 0:
                if self.maze.maze[y][x - 1] == 1 or self.maze.maze[y][x - 1] == 6:
                    w3 = True
            if self.maze.size[1] > x + 1:
                if self.maze.maze[y][x + 1] == 1 or self.maze.maze[y][x + 1] == 6:
                    w4 = True
            return ((w1 and w2) and not (w3 or w4)) or ((w3 and w4) and not (w1 or w2))

        self.maze.maze[self.maze.target[0]][self.maze.target[1]] = 1
        last_element = None
        graphs = {}
        for i in range(0, self.maze.size[0]):
            for j in range(0, self.maze.size[1]):
                if self.maze.maze[i][j] == 1:# or self.maze.maze[i][j] == 4:
                    # Visualisation
                    if last_element:
                        if self.maze.maze[last_element[0][0]][last_element[0][1]] != 6:
                            self.maze.maze[last_element[0][0]][last_element[0][1]] = last_element[1]
                    last_element = ((i, j), self.maze.maze[i][j])
                    self.maze.maze[i][j] = 11
                    if not is_edge(i, j):
                        g = Graph((i, j))
                        graphs[str(g)] = g
                        self.maze.maze[i][j] = 6
                    time.sleep(self.maze.delay)
        if last_element:
            if self.maze.maze[last_element[0][0]][last_element[0][1]] != 6:
                self.maze.maze[last_element[0][0]][last_element[0][1]] = last_element[1]

        edges = {}
        # Find Edges

        for graph in graphs.keys():
            for move_direction in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if (self.maze.size[0] > graphs[graph].y + move_direction[0] >= 0) and \
                        (self.maze.size[1] > graphs[graph].x + move_direction[1] >= 0) and \
                        (self.maze.maze[graphs[graph].y + move_direction[0]][graphs[graph].x + move_direction[1]] in (1., 4., 6.)):
                    length = 1
                    x = graphs[graph].x + move_direction[1]
                    y = graphs[graph].y + move_direction[0]
                    last_element = ((y, x), self.maze.maze[y][x])
                    while not (self.maze.maze[y][x] == 6 or self.maze.maze[y][x] == 4):
                        x += move_direction[1]
                        y += move_direction[0]
                        length += 1
                    self.maze.maze[last_element[0][0]][last_element[0][1]] = last_element[1]
                    new_edge = Edge(graphs[graph], graphs[str(y) + ':' + str(x)])
                    new_edge.set_length(length)
                    graphs[graph].add_edge(graphs[str(y) + ':' + str(x)], new_edge)
                    edges[str(new_edge)] = new_edge
                    time.sleep(self.maze.delay)
        return graphs, edges


class WideSearchSolver(Solver):
    def wide_search(self):
        waypoints = [self.start]
        position = self.start
        start_node = Node(None, position)
        target = None
        nodes = {str(start_node): start_node}

        while self.maze.maze[position[0]][position[1]] != 4 and len(waypoints) != 0:
            position = waypoints[0]
            self.maze.steps_to_solve += 1
            if self.maze.maze[position[0]][position[1]] == 4:
                target = Node(nodes[str(position[0]) + ':' + str(position[1])], position)
            for point in self.find_possible_next_steps(position):
                if point not in waypoints:
                    waypoints.append(point)
                    new_node = Node(nodes[str(position[0]) + ':' + str(position[1])], point)
                    nodes[str(new_node)] = new_node
            time.sleep(self.maze.delay)
            waypoints.pop(0)

        if target:
            self.draw_way(nodes, end_node=nodes[str(target)])

    def run(self):
        running_thread = Thread(target=self.wide_search)
        running_thread.start()


class DepthSearchSolver(Solver):
    def depth_search(self):
        waypoints = [self.start]
        position = self.start
        start_node = Node(None, position)
        target = None
        nodes = {str(start_node): start_node}

        while self.maze.maze[position[0]][position[1]] != 4 and len(waypoints) != 0:
            position = waypoints[0]
            self.maze.steps_to_solve += 1
            if self.maze.maze[position[0]][position[1]] == 4:
                target = Node(nodes[str(position[0]) + ':' + str(position[1])], position)
            for point in self.find_possible_next_steps(position):
                if point not in waypoints:
                    waypoints.insert(1, point)
                    new_node = Node(nodes[str(position[0]) + ':' + str(position[1])], point)
                    nodes[str(new_node)] = new_node
            time.sleep(self.maze.delay)
            waypoints.pop(0)
        if target:
            self.draw_way(nodes, end_node=nodes[str(target)])

    def run(self):
        running_thread = Thread(target=self.depth_search)
        running_thread.start()


class DijkstraSolver(Solver):
    def dijkstra(self):
        graphs, edges = self.maze_to_graph()
        start = graphs[str(self.maze.start[0]) + ":" + str(self.maze.start[1])]
        target = graphs[str(self.maze.target[0]) + ":" + str(self.maze.target[1])]

        actual_way = {
            str(start): NodeGraph(start, None, None)
        }
        node_way = {}
        while str(target) not in actual_way.keys():
            neares_node = actual_way[min(actual_way, key=lambda k: actual_way[k].get_length())]
            for edge in neares_node.itself.edges:
                node_to_add = neares_node.itself.edges[edge].node_two
                new_node = NodeGraph(node_to_add, neares_node, neares_node.itself.edges[edge])

                # Add only if not in nodes to visit and not in visited nodes
                if str(new_node.itself) not in list(actual_way.keys()) and \
                        str(new_node.itself) not in list(node_way.keys()):
                    new_node.add_length(neares_node.itself.edges[edge].get_length())
                    actual_way[str(new_node.itself)] = new_node

            node_way[str(neares_node.itself)] = neares_node
            actual_way.pop(str(neares_node.itself))

        way = []
        point = actual_way[str(target)]
        time.sleep(5)
        while str(point.itself) != str(start):
            way.append(point)
            point = point.privious
        way.append(node_way[str(start)])
        self.maze.maze[self.maze.target[0]][self.maze.target[1]] = 4
        for node in way[::-1]:
            if node.itself and node.privious:
                edge_way = node.edge.get_way()
                for wp in edge_way:
                    self.maze.maze[wp[0]][wp[1]] = 5
                time.sleep(self.maze.delay)


    def run(self):
        running_thread = Thread(target=self.dijkstra)
        running_thread.start()
