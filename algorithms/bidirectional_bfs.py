from collections import deque
import pygame
import time
import sys
import tkinter as tk
from tkinter import messagebox

def reconstruct_path(start_previous, end_previous, intersect_node, win, grid50):
    path = []
    current = intersect_node

    # add nodes from start node to intersection node
    while current is not None:
        path.append(current)
        current.path = True
        grid50.draw_grid(win)
        pygame.display.update()
        current = start_previous.get(current)

    path = path[::-1]  # reverse so that it's from start to intersection

    current = end_previous.get(intersect_node)

    # add nodes from intersection node to end node
    while current is not None:
        path.append(current)
        current.path = True
        grid50.draw_grid(win)
        pygame.display.update()
        current = end_previous.get(current)

    return len(path)

def bidirectional_BFS(win, grid50, start, end):
    start_time = time.time()

    stats = {} # dictionary to store stats 
    stats['total visited'] = 1
    stats['max queue size'] = 1

    start_deque = deque([start])
    start_visited = {start}
    start_previous = {}

    end_deque = deque([end])
    end_visited = {end}
    end_previous = {}

    intersect_node = None


    while start_deque and end_deque:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for que, visited, previous in [(start_deque, start_visited, start_previous), (end_deque, end_visited, end_previous)]:
            current_node = que.popleft()
            current_node.visited = True
            current_node.queued = False

            for neighbor in current_node.neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    previous[neighbor] = current_node
                    que.append(neighbor)
                    stats['max queue size'] = max(stats['max queue size'], len(que))
                    neighbor.queued = True
                    grid50.draw_grid(win)
                    pygame.display.update()

                    if neighbor in start_visited and neighbor in end_visited:
                        intersect_node = neighbor
                        break

            if intersect_node:
                break

            stats['total visited'] += 1
            

        if intersect_node:
            break
        
        grid50.draw_grid(win)
        pygame.display.update()

    if intersect_node is not None:
        stats['path length'] = reconstruct_path(start_previous, end_previous, intersect_node, win, grid50)
        stats['time'] = round(time.time() - start_time, 2)
    else:
        # no path found, give error message
        tk.Tk().wm_withdraw()
        messagebox.showerror('Error', 'No path found')
    return stats