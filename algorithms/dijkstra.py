from collections import deque
import pygame
import sys
import tkinter as tk
from tkinter import messagebox


#TODO: Implement the dijkstra algorithm

## Hint: You must be able to reconstruct the path once the algorithm has finished
## Hint: You must be able to visualize the algorithm in action i.e call the methods to draw on the 
# screen to visualize the algorithm in action in the dijkstra function

def dijkstra(win, grid50, start, end):
    queue = deque()
    queue.append(start)
    start.visited = True
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # allows exit
                pygame.quit()
                sys.exit()

        current = queue.popleft()
        current.queued = False
        if current == end:
            reconstruct_path(end, grid50, win)
            return
        for neighbor in current.neighbors:
            if not neighbor.visited:
                neighbor.visited = True
                neighbor.previous = current
                queue.append(neighbor)
                neighbor.queued = True
                grid50.draw_grid(win)
        pygame.display.update()
    # no path found, show error message box 
    tk.Tk().wm_withdraw()
    messagebox.showerror('Error', 'No path found')
    return


def reconstruct_path(end, grid50, win):
    current = end
    while current.previous:
        current.path = True
        grid50.draw_grid(win)
        pygame.display.update()
        current = current.previous