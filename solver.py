from maze import Maze
from linkedlist import Node
from graph import Graph, Edge
from threading import Thread
import time


class Solver:
    def __init__(self, maze: Maze, start: tuple, target: int):
        self.maze = maze
        self.start = start
        self.target = target

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

        last_element = None
        graphs = {}
        for i in range(0, self.maze.size[0]):
            for j in range(0, self.maze.size[1]):
                if self.maze.maze[i][j] == 1:
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
        self.maze.maze[last_element[0][0]][last_element[0][1]] = last_element[1]

        edges = {}
        # Find Edges
        for graph in graphs.keys():
            for move_direction in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if self.maze.size[0] > graphs[graph].y + move_direction[1] >= 0 and self.maze.size[1] > graphs[graph].x + move_direction[1] >= 0:
                    length = 0
                    while self.maze.maze[graphs[graph].y + move_direction[0]][graphs[graph].x + move_direction[1]] != 6:
                        length += 1
                    #ToDo: add Edges and add Edges to Graph





class WideSearchSolver(Solver):
    def wide_search(self):
        waypoints = [self.start]
        position = self.start
        start_node = Node(None, position)
        target = None
        nodes = {str(start_node): start_node}

        while self.maze.maze[position[0]][position[1]] != self.target and len(waypoints) != 0:
            position = waypoints[0]
            self.maze.steps_to_solve += 1
            if self.maze.maze[position[0]][position[1]] == self.target:
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

        while self.maze.maze[position[0]][position[1]] != self.target and len(waypoints) != 0:
            position = waypoints[0]
            self.maze.steps_to_solve += 1
            if self.maze.maze[position[0]][position[1]] == self.target:
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
        self.maze_to_graph()

    def run(self):
        running_thread = Thread(target=self.dijkstra)
        running_thread.start()
