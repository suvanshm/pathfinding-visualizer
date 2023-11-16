import pygame


class Spot:
    """
    A class representing a spot on the grid.

    Attributes:
        row (int): The row number of the spot.
        col (int): The column number of the spot.
        start (bool): A boolean indicating whether the spot is the starting point.
        target (bool): A boolean indicating whether the spot is the target point.
        wall (bool): A boolean indicating whether the spot is a wall.
        visited (bool): A boolean indicating whether the spot has been visited.
        queued (bool): A boolean indicating whether the spot has been queued.
        path (bool): A boolean indicating whether the spot is part of the path.
        neighbors (list): A list of neighboring spots.
        previous (Spot): The previous spot in the path.
    """

    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.start = False
        self.target = False
        self.wall = False
        self.visited = False
        self.queued = False
        self.path = False
        self.neighbors = []
        self.previous = None

    def __repr__(self) -> str:
        return f'({self.row}, {self.col})'

    def draw_spot(self, window, color):
        """
        Draws a spot on the given window with the given color at the position specified by the row and column of the spot.

        Args:
            window (pygame.Surface): The window on which the spot is to be drawn.
            color (tuple): The RGB color tuple for the spot.

        Returns:
            None
        """
        # we get length of one side of the spot
        from main import SPOT_SIZE

        # we leave a 2 pixel gap between each spot to make it easier to see the grid
        pygame.draw.rect(window, color, (self.row * SPOT_SIZE,
                         self.col * SPOT_SIZE, SPOT_SIZE-2, SPOT_SIZE-2))

    def update_neighbors(self, grid):
        """
        Updates the list of neighbors for the current spot based on the given grid.
        A neighbor is considered valid if it is not a wall and is within the bounds of the grid.

        Args:
            grid (list of list of Spot): The grid of spots representing the current maze.

        Returns:
            None
        """
        self.neighbors = []
        # check if spot is in a valid position, and check if neighbor is wall
        # DOWN
        if self.row < len(grid) - 1 and not grid[self.row + 1][self.col].wall:
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].wall:  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < len(grid[0]) - 1 and not grid[self.row][self.col + 1].wall:  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].wall:  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
