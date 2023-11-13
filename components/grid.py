class Grid:
    
    # TODO:

    ## Implement the class of the grid [DONE]
    ## You must be able to create a grid [DONE]
    ## You must be able to draw the grid [DONE]
    ## You must be able to reset the grid [DONE]
    ## You must be able to click on the nodes of the grid [DONE]
    ## You must also need to implement a method to update the neighbors of each node which 
    # builds on top of the previous [DONE]
    
    def __init__(self, rows):
        from components.spot import Spot
        self.grid = []
        for r in range(rows):
            arr = []
            for c in range(rows):
                arr.append(Spot(r, c))
            self.grid.append(arr)
    
    def reset(self):
        # resets everything except walls, start, and target 
        # useful for repeating visualizations
        for row in self.grid:
            for spot in row:
                spot.visited = False
                spot.path = False
                spot.queued = False
                spot.neighbors = []
                spot.previous = None
    
    def clear(self):
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
        for row in self.grid:
            for spot in row:
                if spot.start:
                    spot.draw_spot(window, (20, 235, 20)) # green
                elif spot.target:
                    spot.draw_spot(window, (235, 20, 20)) # red
                    # yellow 
                elif spot.path:
                    spot.draw_spot(window, (255, 0, 255)) # blue
                elif spot.wall:
                    spot.draw_spot(window, (0, 0, 0)) # black
                elif spot.queued:
                    spot.draw_spot(window, (200, 200, 20)) # light yellow
                elif spot.visited:
                    spot.draw_spot(window, (20, 120, 200)) # light blue
                else:
                    spot.draw_spot(window, (100, 100, 100)) #  grey
    
    def update_neighbors(self):
        for row in self.grid:
            for spot in row:
                spot.update_neighbors(self.grid)
    
    def num_wall(self):
        count = 0
        for row in self.grid:
            for spot in row:
                if spot.wall:
                    count += 1
        return count
    