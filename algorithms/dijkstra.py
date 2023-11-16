from collections import deque
import pygame
import sys
import tkinter as tk
from tkinter import messagebox
import time


#TODO: Implement the dijkstra algorithm [DONE]
## Hint: You must be able to reconstruct the path once the algorithm has finished [DONE]
## Hint: You must be able to visualize the algorithm in action i.e call the methods to draw on the screen to visualize the algorithm in action in the dijkstra function [DONE]

def dijkstra(win, grid50, start, end):
    """
    Finds the shortest path between a start and end node on a grid using Dijkstra's algorithm.

    Args:
        win (pygame.Surface): The Pygame window surface to draw the grid on.
        grid50 (Grid): The grid object representing the grid.
        start (Spot): The starting node.
        end (Spot): The ending node.

    Returns:
        stats: A dictionary containing statistics about the search, including the total number of nodes visited,
        the maximum size of the queue during the search, the length of the shortest path found, and the time taken to
        complete the search.
    """

    start_time = time.time()
    # since all weights are 1, dijkstra's is the same as bfs, so we can just use a queue instead of a priority queue
    queue = deque() 
    queue.append(start)
    start.visited = True
    stats = {} # dictionary to store stats 
    stats['total visited'] = 1
    stats['max queue size'] = 1
    
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # allows exit
                pygame.quit()
                sys.exit()

        current = queue.popleft()
        current.queued = False
        if current == end:
            path_len = reconstruct_path(end, grid50, win)
            stats['path length'] = path_len
            stats['time'] = round(time.time() - start_time, 2)
            return stats

        for neighbor in current.neighbors:
            if not neighbor.visited:
                neighbor.visited = True
                stats['total visited'] += 1
                neighbor.previous = current
                queue.append(neighbor)
                stats['max queue size'] = max(stats['max queue size'], len(queue))
                neighbor.queued = True
                grid50.draw_grid(win)
        
        instructionsfont = pygame.font.SysFont('courier', 16)
        text = 'searching using dijkstra\'s'
        text_surface = instructionsfont.render(text, True, (255, 255, 255)) # white
        # draw rectangle to cover up previous text 
        pygame.draw.rect(win, (0, 0, 0), (600, 100, 300, 30))
        win.blit(text_surface, (605, 105))

        # draw rectangle to cover up previous stats
        pygame.draw.rect(win, (0, 0, 0), (600, 190, 300, 100))
        # draw stats 
        titlefont = pygame.font.SysFont('courier', 22)
        seperator = titlefont.render('----------------------', True, (255, 255, 255))
        win.blit(seperator, (605, 190))
        statsfont = pygame.font.SysFont('courier', 16)
        text = 'stats/info:' 
        text_surface = statsfont.render(text, True, (255, 255, 255)) 
        win.blit(text_surface, (605, 210))
        text = f'start:{start}, end:{end}'
        text_surface = statsfont.render(text, True, (255, 255, 255))
        win.blit(text_surface, (605, 230))
        text = f'walls:{grid50.num_wall()}'
        text_surface = statsfont.render(text, True, (255, 255, 255))
        win.blit(text_surface, (605, 250))

        pygame.display.update()
    
    # no path found, show error message box 
    tk.Tk().wm_withdraw()
    messagebox.showerror('Error', 'No path found')
    return stats


def reconstruct_path(end, grid50, win):
    """
    Reconstructs the shortest path from the start node to the end node as an animation. Also provides the length of the path.

    Args:
        end(Spot): The end node of the path.
        grid50 (Grid): The grid object representing the game board.
        win (pygame.Surface): The window surface to draw the grid on.

    Returns:
        int: The length of the reconstructed path.
    """
    path_len = 0
    current = end 
    while current.previous:
        current.path = True
        # after changing state of current, redraw grid and update display, this is what makes the animation work
        grid50.draw_grid(win) 
        pygame.display.update()
        path_len += 1
        current = current.previous
    return path_len