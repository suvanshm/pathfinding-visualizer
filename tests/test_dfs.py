import pygame 
import sys
from components.spot import Spot
import time
import tkinter as tk
from tkinter import messagebox

def dfs(grid, start, end):
    """
    Depth-first search algorithm to find a path from start to end node in a grid.

    Args:
    - grid: Grid object representing the grid
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
        current = stack.pop()
        print(current)
        current.queued = False # changes color of spot
        current.visited = True 
        stats['total visited'] += 1

        if current == end: # found target
            path_trav = reconstruct_path(end)
            stats['path'] = path_trav
            stats['time'] = round(time.time() - start_time, 2)
            return stats

        for neighbor in current.neighbors:
            if not neighbor.visited and not neighbor.wall:
                neighbor.previous = current
                stack.append(neighbor) # add neighbor to stack
                stats['max queue size'] = max(stats['max queue size'], len(stack))
                neighbor.queued = True # changes color of spot

def reconstruct_path(end):
    """
    Reconstructs the path from the start node to the end node with an animation. Returns the length of the path also.

    Args:
    - end: The end node of the path.
    Returns:
    - The DFS path to reach the end node
    """
    path_len = 0
    current = end
    path = [str(current)]
    while current.previous:
        path.append(str(current.previous))
        current.path = True
        path_len += 1
        current = current.previous
    return path

def test_dfs():
    grid = [[Spot(row, col) for col in range(5)] for row in range(5)]
    #Test 1: Simple Path (1 is a wall, 0 is a free space) 
    '''
    1 1 1 1 1
    1 0 1 0 1
    1 0 1 0 0
    1 0 1 1 0
    0 0 0 0 0 
    '''
    #Constructing the Graph
    walls = [(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,2),(1,4),(2,0),(2,2),(3,0), (3,2),(3,3)]
    for wall in walls:
        u,v = wall
        grid[u][v].wall = True
    for row in range(5):
        for column in range(5):
            grid[row][column].update_neighbors(grid)
    stats = dfs(grid, grid[2][3],grid[3][1])
    assert stats['path'] == ['(3, 1)', '(4, 1)', '(4, 2)', '(4, 3)', '(4, 4)', '(3, 4)', '(2, 4)', '(2, 3)']
    #more complicated example, multiple paths, grid looks like
    '''
    1 1 0 0 1
    0 0 1 0 0 
    0 0 1 1 0
    0 0 0 1 0 
    0 0 0 0 0
    '''
    grid = [[Spot(row, col) for col in range(5)] for row in range(5)]
    walls = [(0,0),(0,1),(0,4),(1,2),(2,2),(2,3),(3,3)]
    for wall in walls:
        u,v = wall
        grid[u][v].wall = True
    for row in range(5):
        for column in range(5):
            grid[row][column].update_neighbors(grid)
    stats = dfs(grid, grid[1][0],grid[1][3])
    assert stats['path'] == ['(1, 3)', '(1, 4)', '(2, 4)', '(3, 4)', '(4, 4)', '(4, 3)', '(4, 2)', '(3, 2)', '(3, 1)', '(3, 0)', '(2, 0)', '(2, 1)', '(1, 1)', '(1, 0)']  
    # No path available (we block off the previous path)
    '''
    1 1 0 0 1
    0 0 1 0 0 
    0 0 1 1 0
    0 0 0 1 0 
    0 0 0 1 0
    '''
    grid[4][3].wall = True
    for row in range(5):
        for column in range(5):
            grid[row][column].update_neighbors(grid)
    stats = dfs(grid, grid[1][0],grid[1][3])
    assert stats == None