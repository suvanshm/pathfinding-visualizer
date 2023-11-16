import pygame 
import sys
import time
import tkinter as tk
from tkinter import messagebox

def dfs(win, grid50, start, end):
    """
    Depth-first search algorithm to find a path from start to end node in a grid.

    Args:
    - win: pygame window object
    - grid50: Grid object representing the grid
    - start: Spot object representing the starting node
    - end: Spot object representing the ending node

    Returns:
    - stats: dictionary containing statistics of the search, including:
        - 'total visited': total number of nodes visited during the search
        - 'max queue size': maximum size of the stack during the search
        - 'path length': length of the path found (if a path is found)
        - 'time': time taken to complete the search
    """
    start_time = time.time()
    stats = {} 
    stats['total visited'] = 0
    stack = [start] 
    stats['max queue size'] = 1
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # allows exit
                pygame.quit()
                sys.exit()

        current = stack.pop()
        current.queued = False # changes color of spot
        current.visited = True 
        stats['total visited'] += 1

        if current == end: # found target
            len_path = reconstruct_path(end, grid50, win)
            stats['path length'] = len_path
            stats['time'] = round(time.time() - start_time, 2)
            return stats

        for neighbor in current.neighbors:
            if not neighbor.visited and not neighbor.wall:
                neighbor.previous = current
                stack.append(neighbor) # add neighbor to stack
                stats['max queue size'] = max(stats['max queue size'], len(stack))
                neighbor.queued = True # changes color of spot
                grid50.draw_grid(win)
                pygame.display.update()

        grid50.draw_grid(win)
        pygame.display.update()

        # set up text surface
        instructionsfont = pygame.font.SysFont('courier', 16)
        text = f'searching using dfs'
        text_surface = instructionsfont.render(text, True, (255, 255, 255)) # white
        # draw rectangle to cover up previous text 
        pygame.draw.rect(win, (0, 0, 0), (600, 100, 300, 30))
        win.blit(text_surface, (605, 105)) # display text "searching using A*(heuristic)"
        pygame.display.update()

    # return error message if no path found
    tk.Tk().wm_withdraw()
    messagebox.showerror('Error', 'No path found')
    return stats

def reconstruct_path(end, grid50, win):
    """
    Reconstructs the path from the start node to the end node with an animation. Returns the length of the path also.

    Args:
    - end: The end node of the path.
    - grid50: The grid object representing the game board.
    - win: The window object representing the game window.

    Returns:
    - The length of the path.
    """
    path_len = 0
    current = end
    while current.previous:
        current.path = True
        path_len += 1
        current = current.previous
        grid50.draw_grid(win)
        pygame.display.update()
    return path_len