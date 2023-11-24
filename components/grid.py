class Grid:
    """
    A class representing a grid of spots.

    Attributes:
        grid : list
            A 2D list of Spot objects representing the grid.
    """

    def __init__(self, rows):
        """
        Initializes a grid object with a 2D list of Spot objects.

        Args:
        - rows (int): The number of rows and columns in the grid.

        Returns:
        - None
        """
        from components.spot import Spot
        self.grid = []
        for r in range(rows):
            arr = []
            for c in range(rows):
                arr.append(Spot(r, c))
            self.grid.append(arr)

    def reset(self):
        """
        Resets all the attributes of each spot in the grid except walls, start, and target.
        This method is useful for repeating visualizations with the same grid pattern.
        """
        for row in self.grid:
            for spot in row:
                spot.visited = False
                spot.path = False
                spot.queued = False
                spot.neighbors = []
                spot.previous = None

    def clear(self):
        """
        Clears the grid by resetting all spot attributes to their default values.
        """
        for row in self.grid:
            for spot in row:
                spot.start = False
                spot.target = False
                spot.wall = False
                spot.visited = False
                spot.path = False
                spot.queued = False
                spot.neighbors = []
                spot.previous = None

    def draw_grid(self, window):
        """
        Draws the grid on the given window, with each spot colored according to its state.

        Parameters:
        window (pygame.display): The window on which to draw the grid.

        Returns:
        None
        """
        for row in self.grid:
            for spot in row:
                if spot.start:
                    spot.draw_spot(window, (20, 235, 20))  # green
                elif spot.target:
                    spot.draw_spot(window, (235, 20, 20))  # red
                elif spot.path:
                    spot.draw_spot(window, (255, 0, 255))  # blue
                elif spot.wall:
                    spot.draw_spot(window, (0, 0, 0))  # black
                elif spot.queued:
                    spot.draw_spot(window, (200, 200, 20))  # light yellow
                elif spot.visited:
                    spot.draw_spot(window, (20, 120, 200))  # light blue
                else:
                    spot.draw_spot(window, (100, 100, 100))  # grey (default)

    def update_neighbors(self):
        """
        Updates the neighbors of each spot in the grid based on the current state of the grid.
        """
        for row in self.grid:
            for spot in row:
                spot.update_neighbors(self.grid)

    def num_wall(self):
        """
        Returns the number of wall spots in the grid.
        """
        count = 0
        for row in self.grid:
            for spot in row:
                if spot.wall:
                    count += 1
        return count
