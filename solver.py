from maze import Maze
from linkedlist import Node
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


class WideSearchSolver(Solver):
    def wide_search(self):
        waypoints = [self.start]
        position = self.start
        start_node = Node(None, position)
        target = None
        nodes = {str(start_node): start_node}

        while self.maze.maze[position[0]][position[1]] != self.target and len(waypoints) != 0:
            position = waypoints[0]
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