import heapq
import pygame
import sys
import tkinter as tk
from tkinter import messagebox
import time

# TODO: Implement A* algorithm

## Hint: You must be able to reconstruct the path once the algorithm has finished
## Hint: You must be able to visualize the algorithm in action i.e call the methods to draw on the screen 
# to visualize the algorithm in action in the astar function

def h_manhattan(spot, target):
    # manhattan distance is the sum of the absolute values of the differences in the x and y coordinates
    # good for when you can only move in 4 directions (as in our case)
    return abs(spot.row - target.row) + abs(spot.col - target.col)

def h_eucledian(spot, target):
    # eucledian distance is the square root of the sum of the squares of the differences in the x and y coordinates
    # good for when you can move in any direction
    return ((spot.row - target.row)**2 + (spot.col - target.col)**2)**0.5

def astar(win, grid50, start, end, heuristic):
    """
    A* algorithm implementation to find the shortest path between start and end nodes in a grid.

    Parameters:
    win (pygame.Surface): The pygame window surface.
    grid50 (Grid): The grid object representing the game board.
    start (Spot): The starting node.
    end (Spot): The ending node.
    heuristic (function): The heuristic function to use for estimating the distance between nodes.

    Returns:
    stats: A dictionary containing statistics about the search, including the total number of nodes visited, 
    the length of the path found, the time taken to find the path, and the maximum size of the queue during the search.
    """
def astar(win, grid50, start, end, heuristic):
    start_time = time.time()
    stats = {}
    stats['total visited'] = 0
    stats['heuristic'] = heuristic.__name__[2:] # heuristic.__name__ is 'h_manhattan' or 'h_eucledian', so we get the part after the underscore
    count = 0 # used to break ties in the priority queue
    open_set = [] # priority queue

    # initialize g and f scores to infinity
    g_score = {spot: float('inf') for row in grid50.grid for spot in row}
    f_score = {spot: float('inf') for row in grid50.grid for spot in row}

    g_score[start] = 0 # g score of start is 0
    f_score[start] = heuristic(start, end) # f score of start is the heuristic value of start

    heapq.heappush(open_set, (0, count, start))
    start.queued = True
    stats['max queue size'] = 1

    while open_set: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # allows exit
                pygame.quit()
                sys.exit()

        current = heapq.heappop(open_set)[2] # get the spot object from the tuple
        stats['total visited'] += 1
        current.queued = False # color of spot is linked to different attributes so changing them automatically generates the animation
        current.visited = True

        if current == end: # found target
            path_len = reconstruct_path(end, grid50, win)
            stats['path length'] = path_len
            stats['time'] = round(time.time() - start_time, 2)
            return stats
        
        for neighbor in current.neighbors: 
            temp_g = g_score[current] + 1 # since all weights are 1
            if temp_g < g_score[neighbor]: # found a better path
                neighbor.previous = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end) # f score = g + h scores
                if not neighbor.queued:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    stats['max queue size'] = max(stats['max queue size'], len(open_set))
                    neighbor.queued = True
                    grid50.draw_grid(win)
                    pygame.display.update() # important to update display after every change to grid
        
        # set up text surface
        instructionsfont = pygame.font.SysFont('courier', 16)
        text = f'searching using A*({heuristic.__name__[2:]})'
        text_surface = instructionsfont.render(text, True, (255, 255, 255)) # white
        # draw rectangle to cover up previous text 
        pygame.draw.rect(win, (0, 0, 0), (600, 100, 300, 30))
        win.blit(text_surface, (605, 105)) # display text "searching using A*(heuristic)"
        pygame.display.update()

    # no path found, show error message box
    tk.Tk().wm_withdraw()
    messagebox.showerror('Error', 'No path found')
    return stats

def reconstruct_path(end, grid50, win):
    """
    Reconstructs the path from the end node to the start node.

    Args:
    - end: The end node of the path.
    - grid50: The grid object representing the game board.
    - win: The Pygame window object.

    Returns:
    - path_len: The length of the path from the end node to the start node.
    """
    path_len = 0
    current = end
    while current.previous:
        current.path = True # changes color of spot, see grid.py
        path_len += 1
        grid50.draw_grid(win)
        pygame.display.update() 
        current = current.previous
    return path_len
