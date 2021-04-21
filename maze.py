import numpy as np
import time
from threading import Thread


class Maze:
    def __init__(self, size=(101, 101)):

        self.size = size
        self.maze = np.zeros(self.size)
        self.delay = 0
        self.active_prozess = False

        self.steps_to_solve = 0

        self.target = None
        self.start = None

    def set_delay(self, delay: float):
        self.delay = delay

    def clear(self):
        """
        Removes every created structure and reset complete maze to 0 so it's like a new start
        :return:
        """
        if not self.active_prozess:
            self.maze = np.zeros(self.size)

    def clear_except_walls(self):
        """
        Clears everything, except walls. This mean it brings the maze in the status after an maze is generated
        :return:
        """
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                if self.maze[i][j] != 0:
                    self.maze[i][j] = 1
        self.add_target()

    def build_maze(self, kind_of_algorithm: str, start_as_thread: bool = True):
        """
        This function is for starting the build algorithms.
        :param kind_of_algorithm: The algorithm, that should be used to build the maze that should be used to build
        :param start_as_thread: This makes it possible to start the bulding algoritmhs as an Thread
        :return:
        """
        if not self.active_prozess:
            if kind_of_algorithm == "binary_tree":
                if start_as_thread:
                    binary_three_thrad = Thread(target=self.binary_tree)
                    binary_three_thrad.start()
                else:
                    self.binary_tree()
                self.active_prozess = True

            elif kind_of_algorithm == "prims":
                if start_as_thread:
                    prims_thread = Thread(target=self.prims)
                    prims_thread.start()
                else:
                    self.prims()
                self.active_prozess = True

            """
            elif kind_of_algorithm == "depth_search":
                if start_as_thread:
                    depth_search_thread = Thread(target=self.depth_search_builder)
                    depth_search_thread.start()
                else:
                    self.depth_search_builder()
                self.active_prozess = True
            """

    def binary_tree(self):
        """
        Algorithm for build the maze with binary tree algorithm
        :return:
        """

        # Visit every second y and x coordinate in the maze
        for i in range(0, self.size[0], 2):
            for j in range(0, self.size[1], 2):
                options_to_go = []

                # sets the actual point to an wall
                self.maze[i][j] = 1.

                # looks to west and north if there is an wall. If it is the point between the two walls (actual point,
                # and look for) is nothing, it could be an wall and can be added to options_to_go
                if self.maze[i][j-2] == 1.:
                    options_to_go.append([i, j-1])
                if self.maze[i-2][j] == 1:
                    options_to_go.append([i-1, j])

                # If there are two possible connections it randomly select one of them and make this to wall
                # else the only possibility gets an wall
                if len(options_to_go) == 2:
                    to_wall = options_to_go[np.random.randint(0, 2)]
                    self.maze[to_wall[0]][to_wall[1]] = 1.
                elif options_to_go:
                    to_wall = options_to_go[0]
                    self.maze[to_wall[0]][to_wall[1]] = 1.
                if self.delay:
                    time.sleep(self.delay)

        self.fix_outer_row()
        self.add_target()
        self.active_prozess = False

    def prims(self):
        points = [(0, 0)]
        while len(points) > 0:
            index = np.random.randint(0, len(points))
            starting_point = points[index]

            # Looks for possible next points in maze, that can be visited.
            # First each if check if the next point is in the maze.
            # In if it marks the point as an next to visit point 2 and add it to the next points to visit
            if self.maze[starting_point[0]][starting_point[1] - 2] == 0 and starting_point[1] - 2 >= 0:
                self.maze[starting_point[0]][starting_point[1] - 2] = 2
                points.append((starting_point[0], starting_point[1] - 2))

            if starting_point[1] + 2 < self.size[1]:
                if self.maze[starting_point[0]][starting_point[1] + 2] == 0:
                    self.maze[starting_point[0]][starting_point[1] + 2] = 2
                    points.append((starting_point[0], starting_point[1] + 2))

            if self.maze[starting_point[0] - 2][starting_point[1]] == 0 and starting_point[0] - 2 >= 0:
                self.maze[starting_point[0] - 2][starting_point[1]] = 2
                points.append((starting_point[0] - 2, starting_point[1]))

            if starting_point[0] + 2 < self.size[0]:
                if self.maze[starting_point[0] + 2][starting_point[1]] == 0:
                    self.maze[starting_point[0] + 2][starting_point[1]] = 2
                    points.append((starting_point[0] + 2, starting_point[1]))

            # sets the point as an Wall
            self.maze[starting_point[0]][starting_point[1]] = 1

            # Looks for the possible points, that can be possible be walls
            # It looks if in each direction if actual position + 2 is in maze and if it is a wall.
            # If its an valid waypoint it the point between the two walls is appended to options_to_go
            options_to_go = []

            if self.maze[starting_point[0]][starting_point[1] - 2] == 1:
                options_to_go.append((0, -1))
            if starting_point[1] + 2 < self.size[1]:
                if self.maze[starting_point[0]][starting_point[1] + 2] == 1:
                    options_to_go.append((0, 1))
            if self.maze[starting_point[0] - 2][starting_point[1]] == 1:
                options_to_go.append((-1, 0))
            if starting_point[0] + 2 < self.size[0]:
                if self.maze[starting_point[0] + 2][starting_point[1]] == 1:
                    options_to_go.append((1, 0))

            # If there are possible points for waypoint, it's random select an point from options_to_go and set it
            # in maze to 1.
            if options_to_go:
                to_way = options_to_go[np.random.randint(0, len(options_to_go))]
                self.maze[starting_point[0] + to_way[0]][starting_point[1] + to_way[1]] = 1
            time.sleep(self.delay)

            # Removes the actual used point from possible next points that ought to get checked
            points.pop(index)
        self.fix_outer_row()
        self.add_target()
        self.active_prozess = False

    def fix_outer_row(self):
        """
        If the size of the maze in a direction is an even number, the algorithms doesn't reach the last line.
        This line gets an complete line filled with way
        :return:
        """
        if self.size[0] % 2 == 0:
            self.maze[-1:] = 1
        if self.size[1] % 2 == 0:
            self.maze[:, -1:] = 1

    def add_target(self, coordinates: tuple = (100, 100)):
        """
        Adds an Target to the maze. Actual it always set the right outer cornor to maze
        :param coordinates: coordinates of the target
        :return:
        """
        self.maze[self.size[0] - 1][self.size[1] - 1] = 4
        self.target = (self.size[0] - 1, self.size[1] - 1)

    def add_start(self, coordinates: tuple = (100, 100)):
        """
        Sets an start in the maze. Actual (0, 0) is always the start
        :param coordinates: coordinates of the start
        :return:
        """
        self.start = (0, 0)


if __name__ == '__main__':
    maze = Maze()
    maze.build_maze("binary_tree")