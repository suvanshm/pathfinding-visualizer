from collections import deque
import pygame
import time
import sys
import tkinter as tk
from tkinter import messagebox

def reconstruct_path(start_previous, end_previous, intersect_node, win, grid50):
    len_path = 0
    current = intersect_node

    # add nodes from intersection node to start node
    while current is not None:
        len_path += 1
        current.path = True
        grid50.draw_grid(win)
        pygame.display.update()
        current = start_previous.get(current)
 
    current = end_previous.get(intersect_node)

    # add nodes from intersection node to end node
    while current is not None:
        len_path += 1
        current.path = True
        grid50.draw_grid(win)
        pygame.display.update()
        current = end_previous.get(current) # moving backwards from intersection node to end node

    return len_path

def bidirectional_BFS(win, grid50, start, end):

    """
    Performs a bidirectional BFS search on a grid to find the shortest path between two nodes.

    Args:
    - win: the Pygame window object
    - grid50: the Grid object representing the grid
    - start: the starting Spot object
    - end: the ending Spot object

    Returns:
    - A dictionary containing statistics about the search, including:
        - 'total visited': the total number of nodes visited during the search
        - 'max queue size': the maximum size of the search queue during the search
        - 'path length': the length of the shortest path found (if a path was found)
        - 'time': the time taken to perform the search
    """

    start_time = time.time()

    stats = {} # dictionary to store stats 
    stats['total visited'] = 1
    stats['max queue size'] = 1

    # created two queues, one for each BFS search, two sets of visited nodes from each side, 
    # and two dicts of previous nodes from each side
    start_deque = deque([start])
    start_visited = {start}
    start_previous = {}

    end_deque = deque([end])
    end_visited = {end}
    end_previous = {}

    intersect_node = None

    while start_deque and end_deque:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # allows exit
                pygame.quit()
                sys.exit()
        
        # alternating between BFS searches from start and end nodes
        for que, visited, previous in [(start_deque, start_visited, start_previous), (end_deque, end_visited, end_previous)]:
            # regular BFS search within this loop
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

                    # if neighbor is visited by both BFS searches, we have found the intersection node
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