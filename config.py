import numpy as np


# Sets random seed for numpy
#np.random.seed(seed=1)

# Defines possible colors for maze, in RGB
colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "blue_depthsearch": (66, 135, 245),
    "blue_widesearch": (47, 115, 224),
    "yellow": (255, 255, 0),
    "pink": (255, 0, 255),
    "turquoise": (0, 255, 255),
    "grey_one": (50, 50, 50),
    "grey_two": (100, 100, 100),
    "grey_three": (150, 150, 150),
    "grey_four": (220, 220, 220),
    "grey_five": (230, 230, 0),
}


# The points that aren't walls
colors_no_barrier = (1, 3, 4, 6)