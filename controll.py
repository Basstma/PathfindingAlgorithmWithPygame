import tkinter as tk
from show import Display
from solver import *


class Controll:
    def __init__(self):
        self.display = None
        self.maze = None

        self.root = tk.Tk()

        self.size_label = tk.Label(text="Size of Maze (y, x):")
        self.size_x_entry = tk.Entry()
        self.size_y_entry = tk.Entry()

        self.delay_label = tk.Label(text="Delay(in s):")
        self.delay_entry = tk.Entry()
        self.delay_change = tk.Button(text="Change", command=self.change_delay)

        self.scale_label = tk.Label(text="Scale:")
        self.scale_entry = tk.Entry()

        self.run_button = tk.Button(self.root, text="Starte Pygame Oberfläche", command=self.start_display)
        self.algorithms_lable = tk.Label(self.root, text="Possible generation Algorithm:")
        self.binary_tree_button = tk.Button(self.root, text="Erstelle BinaryTree", command=self.start_binary_tree_build)
        self.prims_button = tk.Button(self.root, text="Erstelle Prims", command=self.start_prims_build)

        self.wide_search_button = tk.Button(self.root, text="WideSearch", command=self.start_wide_search)
        self.depth_search_button = tk.Button(self.root, text="DepthSearch", command=self.start_depth_search)
        self.dijkstra_search_button = tk.Button(self.root, text="DijkstraSearch", command=self.start_dijkstra_search)

        self.clear_button = None
        self.clear_except_walls_button = None
        self.stop_button = tk.Button(self.root, text="Quit", command=self.stop)

        self.size_label.grid(row=0, column=0)
        self.size_x_entry.grid(row=0, column=1)
        self.size_y_entry.grid(row=0, column=2)

        self.delay_label.grid(row=1, column=0)
        self.delay_entry.grid(row=1, column=1)
        self.scale_label.grid(row=1, column=2)
        self.scale_entry.grid(row=1, column=3)

        self.run_button.grid(row=2, column=0)
        self.stop_button.grid(row=3, column=0)

        self.root.mainloop()

    def start_display(self):
        x = int(self.size_x_entry.get() if self.size_x_entry.get() else 0)
        y = int(self.size_y_entry.get() if self.size_y_entry.get() else 0)

        delay = float(self.delay_entry.get() if self.delay_entry.get() else 0)

        scale = int(self.scale_entry.get() if self.scale_entry.get() else 40)

        if x and y:
            pass
        else:
            x, y = 11, 11

        self.maze = Maze(size=(y, x))
        if delay:
            self.maze.set_delay(delay)
        self.maze.start = (0, 0)

        self.clear_button = tk.Button(self.root, text="Clear", command=self.maze.clear)
        self.clear_except_walls_button = tk.Button(self.root, text="ClearExceptWalls", command=self.maze.clear_except_walls)

        self.display = Display(maze=self.maze, scale=scale)
        self.navigation()
        run_display = Thread(target=self.display.run)
        run_display.start()

    def navigation(self):
        self.run_button.grid_remove()

        self.size_label.grid_remove()
        self.size_x_entry.grid_remove()
        self.size_y_entry.grid_remove()

        self.delay_label.grid_remove()
        self.delay_entry.grid_remove()
        self.scale_label.grid_remove()
        self.scale_entry.grid_remove()
        self.stop_button.grid_remove()

        self.delay_label["text"] = "Delay to:"
        self.delay_label.grid(row=0, column=0)
        self.delay_entry.grid(row=0, column=1)
        self.delay_change.grid(row=0, column=2)

        self.algorithms_lable.grid(row=1, column=0)
        self.binary_tree_button.grid(row=1, column=1)
        self.prims_button.grid(row=1, column=2)

        self.wide_search_button.grid(row=2, column=0)
        self.depth_search_button.grid(row=2, column=1)
        self.dijkstra_search_button.grid(row=2, column=2)

        self.clear_button.grid(row=9, column=0)
        self.clear_except_walls_button.grid(row=9, column=1)
        self.stop_button.grid(row=10, column=2)

    def start_binary_tree_build(self):
        self.display.maze.build_maze(kind_of_algorithm="binary_tree")

    def start_prims_build(self):
        self.display.maze.build_maze(kind_of_algorithm="prims")

    def start_wide_search(self):
        solver = WideSearchSolver(self.maze, 4)
        solver.run()

    def start_depth_search(self):
        solver = DepthSearchSolver(self.maze, 4)
        solver.run()

    def start_dijkstra_search(self):
        solver = DijkstraSolver(self.maze, 4)
        solver.run()

    def change_delay(self):
        delay = float(self.delay_entry.get() if self.delay_entry.get() else 0)
        self.maze.set_delay(delay)

    def stop(self):
        if self.display:
            self.display.running = False
        self.root.quit()


if __name__ == "__main__":
    c = Controll()