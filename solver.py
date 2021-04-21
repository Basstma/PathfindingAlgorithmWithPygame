from maze import Maze
from linkedlist import Node, NodeGraph
from graph import Graph, Edge
from threading import Thread
import time


class Solver:
    def __init__(self, maze: Maze, target):
        """
        Basic Class for an Solver, that soves the maze
        :param maze:
        :param target:
        """
        self.maze = maze
        #self.start = self.maze.start
        self.target = self.maze.target

    def run(self):
        """
        Function have to get overwrite in each Child class. This function have to start the Thread for the solver
        algorithm
        :return:
        """
        pass

    def draw_way(self, nodes: dict, end_node: Node):
        """
        draws the way from linked List with maze coordinates
        :param nodes: All Nodes that are existing
        :param end_node: last node
        :return:
        """
        self.maze.maze[end_node.y][end_node.x] = 4
        self.maze.maze[self.start[0]][self.start[1]] = 3
        node = end_node.privious
        # From last node to node that was privous for the actual node
        while node.privious:
            self.maze.maze[node.y][node.x] = 5
            node = nodes[str(node.privious)]
            time.sleep(self.maze.delay)

    def find_possible_next_steps(self, actual_possition: tuple) -> list:
        """
        Conrtorls in maze in which direction its possible to go.
        That means that there is no wall and the point isn't visited.
        1|1|0       Part of Maze: X is actuall position.
        1|X|0       The function looks from x in North, East, West and South direction and check if this filed is in
        1|0|0       maze and if it is an Waypoint
        The funktion possible ways to 11 for visualisation and so it dosn't get detected in this function.
        If the Waypoint is 4 it's the target and it shouldn't get another color but should be an waypoint
        :param actual_possition: touple with actual x and y coordiantes
        :return: list with posible coordinates to go.
        """
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
        """
        Build an Graph from the actual maze.
        :return: Return two dictionarys one contains all Nodes, its called graphs
                    The other one contains all edges
        """
        def is_edge(y, x):
            """
            Function that controlls if an point is an Node or an Edge.
            :param y: y Value of the actual point in Maze
            :param x: x value of the actual point in Maze
            :return: True if it is an edge False if it is an Node
            """

            #Declare Variables
            w1, w2, w3, w4 = False, False, False, False
            # Each if check if an point have an neighbor in Nort, East, West and South
            # In inner if it controls if the neightboor is an Waypoint or an Node.
            # If it is its an valid point in Maze(Node or Waypoint) than set the bool for this waypoint to True
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

            # Returns True if the Point is no end, crossing or curve
            # That means the Points are in an horizontal or vertical Line and nothing else
            return ((w1 and w2) and not (w3 or w4)) or ((w3 and w4) and not (w1 or w2))

        self.maze.maze[self.maze.target[0]][self.maze.target[1]] = 1
        last_element = None
        graphs = {}
        for i in range(0, self.maze.size[0]):
            for j in range(0, self.maze.size[1]):
                if self.maze.maze[i][j] == 1:
                    # The following if is only for visualisation. It set the last visited element to the value
                    # it was before, so its possible to undo the last change, if it was an edge that gets controlled
                    if last_element:
                        if self.maze.maze[last_element[0][0]][last_element[0][1]] != 6:
                            self.maze.maze[last_element[0][0]][last_element[0][1]] = last_element[1]
                    last_element = ((i, j), self.maze.maze[i][j])
                    time.sleep(self.maze.delay)
                    # Sets the actual visited point to 11 so its possible to see where the algorithm is actual checking
                    # for nodes
                    self.maze.maze[i][j] = 11

                    # If the actual Point is an Node an new Graph Element is created and added to the dictionary
                    # Set the corresponding point to 6 so it can be visualised as an Node in Maze
                    if not is_edge(i, j):
                        g = Graph((i, j))
                        graphs[str(g)] = g
                        self.maze.maze[i][j] = 6

        # Undo the value change for last controlled point if its no Node
        if last_element:
            if self.maze.maze[last_element[0][0]][last_element[0][1]] != 6:
                self.maze.maze[last_element[0][0]][last_element[0][1]] = last_element[1]

        edges = {}

        for graph in graphs.keys():
            # move_direction is each direction an neighbor waypoint can be (West, East, South, North)
            for move_direction in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                # Controls if the way is an valid point to go.
                # 1. If it is in Maze y-size range
                # 2. If it is in Maze x-size range
                # 3. If the maze[y][x] is an valid point, where the way can go
                if (self.maze.size[0] > graphs[graph].y + move_direction[0] >= 0) and \
                        (self.maze.size[1] > graphs[graph].x + move_direction[1] >= 0) and \
                        (self.maze.maze[graphs[graph].y + move_direction[0]][graphs[graph].x + move_direction[1]] in (1., 4., 6.)):
                    # initialise the variables for the next step
                    length = 1
                    x = graphs[graph].x + move_direction[1]
                    y = graphs[graph].y + move_direction[0]

                    # last element is for storing the information for the actual point
                    last_element = ((y, x), self.maze.maze[y][x])

                    # Controls how long the edge is. That means it goes in the direction until there is an Waypoint or
                    # the target and add 1 to length for each step.
                    while not (self.maze.maze[y][x] == 6 or self.maze.maze[y][x] == 4):
                        x += move_direction[1]
                        y += move_direction[0]
                        length += 1

                    self.maze.maze[last_element[0][0]][last_element[0][1]] = last_element[1]

                    # Creates an new ege for with the values from the upper while function and added it to the
                    # edges-dictionary
                    new_edge = Edge(graphs[graph], graphs[str(y) + ':' + str(x)])
                    new_edge.set_length(length)
                    graphs[graph].add_edge(graphs[str(y) + ':' + str(x)], new_edge)
                    edges[str(new_edge)] = new_edge
                    time.sleep(self.maze.delay)
        return graphs, edges


class WideSearchSolver(Solver):
    def wide_search(self):
        """
        Algorithm for WideSearch
        :return:
        """

        # Initialise all needed variables
        waypoints = [self.start]
        position = self.start
        start_node = Node(None, position)
        target = None

        # nodes dict is only for visualisation
        nodes = {str(start_node): start_node}

        # Search while the actual position isn't target and there are possibles waypoints left
        while self.maze.maze[position[0]][position[1]] != 4 and len(waypoints) != 0:

            # Takes the first waypoint, this mean the "nearest"
            position = waypoints[0]
            self.maze.steps_to_solve += 1

            # If it is target, the Node have to get generated
            if self.maze.maze[position[0]][position[1]] == 4:
                target = Node(nodes[str(position[0]) + ':' + str(position[1])], position)

            # Adds all possible next waypoints from actual waypoint
            for point in self.find_possible_next_steps(position):
                # Add only to next waypoints if it isn't already in there.
                if point not in waypoints:
                    # Added at end so the points that are added earlier are got visited earlier
                    waypoints.append(point)
                    new_node = Node(nodes[str(position[0]) + ':' + str(position[1])], point)
                    nodes[str(new_node)] = new_node
            time.sleep(self.maze.delay)
            # Remove the actual visited waypoint, so it can't be visited twice
            waypoints.pop(0)

        if target:
            self.draw_way(nodes, end_node=nodes[str(target)])

    def run(self):
        running_thread = Thread(target=self.wide_search)
        running_thread.start()


class DepthSearchSolver(Solver):
    def depth_search(self):
        """
        Algorithm for depth search
        Could also be build recursive, but python has an limitation in max recursion depth and in bigger mazes this
        can cause errors
        :return:
        """

        # Initialise all needed variables
        waypoints = [self.start]
        position = self.start
        start_node = Node(None, position)
        target = None

        # nodes dict is only for visualisation
        nodes = {str(start_node): start_node}

        # Search while the actual position isn't target and there are possibles waypoints left
        while self.maze.maze[position[0]][position[1]] != 4 and len(waypoints) != 0:
            position = waypoints[0]
            self.maze.steps_to_solve += 1

            # If it is target, the Node have to get generated
            if self.maze.maze[position[0]][position[1]] == 4:
                target = Node(nodes[str(position[0]) + ':' + str(position[1])], position)

            for point in self.find_possible_next_steps(position):
                # Adds all possible next waypoints from actual waypoint
                if point not in waypoints:
                    # Inserts the waypoint at index 1 in waypoints, that make it possible to finish an path until it
                    # hasn't possible next waypoints or it is an target.
                    # This is the alternative for recursion.
                    waypoints.insert(1, point)
                    new_node = Node(nodes[str(position[0]) + ':' + str(position[1])], point)
                    nodes[str(new_node)] = new_node
            time.sleep(self.maze.delay)
            # removes the actual used waypoint, so it doesn't get visited twice
            waypoints.pop(0)

        # If target is found it visualise the way to target
        if target:
            self.draw_way(nodes, end_node=nodes[str(target)])

    def run(self):
        running_thread = Thread(target=self.depth_search)
        running_thread.start()


class DijkstraSolver(Solver):
    def dijkstra(self):
        """
        Start to search for Target with dijkstra algorithm
        :return:
        """

        # Initialise the needed variables
        graphs, edges = self.maze_to_graph()
        start = graphs[str(self.maze.start[0]) + ":" + str(self.maze.start[1])]
        target = graphs[str(self.maze.target[0]) + ":" + str(self.maze.target[1])]

        # In actual_ay all possible next nodes are stored
        actual_way = {
            str(start): NodeGraph(start, None, None)
        }
        # node_way contains all already visited nodes
        node_way = {}

        while str(target) not in actual_way.keys():
            # Takes the node with smallest length, that isn't visited
            neares_node = actual_way[min(actual_way, key=lambda k: actual_way[k].get_length())]

            # Create all next possible Nodes, from the actual Node, with the edges that can be go from the actual node
            for edge in neares_node.itself.edges:
                node_to_add = neares_node.itself.edges[edge].node_two
                new_node = NodeGraph(node_to_add, neares_node, neares_node.itself.edges[edge])

                # Add only if not in nodes to visit and not in visited nodes so no node get's visited two times.
                # If it is already visited there is an shorter way to reach this Node and cause the algorithm looks for
                # the shortest way its not in need to visit this node again
                if str(new_node.itself) not in list(actual_way.keys()) and \
                        str(new_node.itself) not in list(node_way.keys()):
                    new_node.add_length(neares_node.itself.edges[edge].get_length())
                    actual_way[str(new_node.itself)] = new_node

            # Add the actual node to node_way and remove it from possible next waypoints
            node_way[str(neares_node.itself)] = neares_node
            actual_way.pop(str(neares_node.itself))

        # For visualisation makes. Start by target, because the linked List works with previous Nodes
        way = []
        point = actual_way[str(target)]
        time.sleep(5)

        # Starts to search for start of maze
        while str(point.itself) != str(start):
            way.append(point)
            point = point.privious

        # Add the start to way
        way.append(node_way[str(start)])

        # Change value of target, only for visualisation
        self.maze.maze[self.maze.target[0]][self.maze.target[1]] = 4

        # Reverse the list of waypoints and go through it, that means start at start and at end
        for node in way[::-1]:
            if node.itself and node.privious:
                # Visualise each edge with time delay.
                edge_way = node.edge.get_way()
                for wp in edge_way:
                    self.maze.maze[wp[0]][wp[1]] = 5
                time.sleep(self.maze.delay)

    def run(self):
        # Function for start dijkstra search algorithm
        running_thread = Thread(target=self.dijkstra)
        running_thread.start()
