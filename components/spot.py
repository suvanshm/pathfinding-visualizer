import pygame 

class Spot:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.start = False
        self.target = False
        self.wall = False
        self.visited = False
        self.path = False
        self.neighbors = []
        self.previous = None

    def __repr__(self) -> str:
        return f'Spot({self.row}, {self.col})'
    
    def draw_spot(self, window, color):
        from main import SPOT_SIZE
        pygame.draw.rect(window, color, (self.row * SPOT_SIZE, self.col * SPOT_SIZE, SPOT_SIZE-2, SPOT_SIZE-2))
    
    def update_neighbors(self, grid):
            self.neighbors = []
            # check if spot is in a valid position, and check if neighbor is wall
            if self.row < len(grid) - 1 and not grid[self.row + 1][self.col].wall: # DOWN
                self.neighbors.append(grid[self.row + 1][self.col])
            if self.row > 0 and not grid[self.row - 1][self.col].wall: # UP
                self.neighbors.append(grid[self.row - 1][self.col])
            if self.col < len(grid[0]) - 1 and not grid[self.row][self.col + 1].wall: # RIGHT
                self.neighbors.append(grid[self.row][self.col + 1])
            if self.col > 0 and not grid[self.row][self.col - 1].wall: # LEFT
                self.neighbors.append(grid[self.row][self.col - 1])
        
        
