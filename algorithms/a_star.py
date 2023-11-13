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
    return abs(spot.row - target.row) + abs(spot.col - target.col)

def h_eucledian(spot, target):
    return ((spot.row - target.row)**2 + (spot.col - target.col)**2)**0.5

def astar(win, grid50, start, end, heuristic):
    start_time = time.time()
    stats = {}
    stats['total visited'] = 0
    stats['heuristic'] = heuristic.__name__[2:]
    count = 0
    open_set = []
    g_score = {spot: float('inf') for row in grid50.grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid50.grid for spot in row}
    f_score[start] = heuristic(start, end) 

    heapq.heappush(open_set, (0, count, start))
    start.queued = True
    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # allows exit
                pygame.quit()
                sys.exit()

        current = heapq.heappop(open_set)[2]
        stats['total visited'] += 1
        current.queued = False
        current.visited = True
        if current == end:
            path_len = reconstruct_path(end, grid50, win)
            stats['path length'] = path_len
            stats['time'] = round(time.time() - start_time, 2)
            return stats
        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                neighbor.previous = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                if not neighbor.queued:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    neighbor.queued = True
                    grid50.draw_grid(win)
                    pygame.display.update()
        
        instructionsfont = pygame.font.SysFont('courier', 16)
        text = f'searching using A*({heuristic.__name__[2:]})'
        text_surface = instructionsfont.render(text, True, (255, 255, 255)) # white
        # draw rectangle to cover up previous text 
        pygame.draw.rect(win, (0, 0, 0), (600, 100, 300, 30))
        win.blit(text_surface, (605, 105))
        pygame.display.update()
    # no path found, show error message box
    tk.Tk().wm_withdraw()
    messagebox.showerror('Error', 'No path found')
    return

def reconstruct_path(end, grid50, win):
    path_len = 0
    current = end
    while current.previous:
        current.path = True
        path_len += 1
        grid50.draw_grid(win)
        pygame.display.update()
        current = current.previous
    return path_len
