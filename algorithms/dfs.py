import pygame 
import sys
import time
from collections import deque
import tkinter as tk
from tkinter import messagebox

def dfs(win, grid50, start, end):
    stack = [start]
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # allows exit
                pygame.quit()
                sys.exit()

        current = stack.pop()
        current.visited = True
        if current == end:
            reconstruct_path(end, grid50, win)
            return True

        for neighbor in current.neighbors:
            if not neighbor.visited and not neighbor.wall:
                neighbor.previous = current
                stack.append(neighbor)
                neighbor.queued = True
                grid50.draw_grid(win)
                pygame.display.update()

        grid50.draw_grid(win)
        pygame.display.update()
    return False

def dfs_alt(win, grid50, start, end, stack = []): 
    start_time = time.time()
    print('start time:', start_time)
    stack.append(start)
    start.visited = True
    stats = {}
    stats['total visited'] = 1
    stats['max queue size'] = 1

    
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        for neighbor in stack[-1].neighbors:
            if neighbor == end:
                neighbor.previous = stack[-1]
                path_len = reconstruct_path(end, grid50, win)
                stats['path length'] = path_len
                stats['time'] = round(time.time() - start_time, 2)
                return stats
            
            if not neighbor.visited:
                neighbor.visited = True
                stats['total visited'] += 1
                neighbor.previous = stack[-1]
                stack.append(neighbor)
                stats['max queue size'] = max(stats['max queue size'], len(stack))
                neighbor.queued = True
                grid50.draw_grid(win)
                pygame.display.update()
                return dfs(win, grid50, neighbor, end, stack) 

            stack.pop()
            grid50.draw_grid(win)
            pygame.display.update()
    
    # return error message if no path found
    tk.Tk().wm_withdraw()
    messagebox.showerror('Error', 'No path found')
    return

def reconstruct_path(end, grid50, win):
    path_len = 0
    current = end
    while current.previous:
        current.path = True
        path_len += 1
        current = current.previous
        grid50.draw_grid(win)
        pygame.display.update()
    return path_len