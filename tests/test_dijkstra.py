import pytest
import pygame
from components.spot import Spot
import pygame
from unittest.mock import Mock
import dijkstar
from collections import deque
import tkinter as tk
from tkinter import messagebox
from dijkstar import Graph, find_path
import time


def test_dijkstra():
     # create a 5x5 grid with walls in the third column from the 2nd to 5th row (divider)
    grid = [[Spot(row, col) for col in range(5)] for row in range(5)]
    grid[1][2].wall = True
    grid[2][2].wall = True
    grid[3][2].wall = True
    grid[4][2].wall = True
    grid[5][2].wall = True
    for row in range(5):
        for column in range(5):
            grid[row][column].update_neighbors(grid)
    stats = dijkstra_test(grid,[1,1],grid[4,4])
    len = stats['path length']
    graph = Graph()
    walls = [(1,2),(2,2), (3,2), (4,2), (5,2)]
    for row in range(5):
        for column in range(5):
            current = (row,column)
            if current not in walls:
                neighbour_list = [(0,1),(1,0),(-1,0),(0,-1)]
                for neighbour_difference in neighbour_list:
                    if (current + neighbour_difference) not in walls:
                        graph.add_edge(current, current +neighbour_difference, 1) # adds adjacent neighbours
    #once the graph is built, we test whether the shortest path length found by Python's Dijkstra and our implementation is the same.
    stats_python_implementation = find_path(graph,(1,1), (4,4))
    len_python = stats_python_implementation[total_cost]
    assert len == len_python
    
    #build the same graph in python's native implementation
    

def dijkstra_test(grid, start, end):
    """
    Finds the shortest path between a start and end node on a grid using Dijkstra's algorithm.

    Args:
        win (pygame.Surface): The Pygame window surface to draw the grid on.
        grid (Grid): The grid object representing the grid.
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
        current = queue.popleft()
        current.queued = False # color of spot is linked to different attributes so changing them automatically generates the animation
        if current == end: # found target
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
    