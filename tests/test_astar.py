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
import heapq
def h_manhattan(spot, target):
    # manhattan distance is the sum of the absolute values of the differences in the x and y coordinates
    # good for when you can only move in 4 directions (as in our case)
    return abs(spot.row - target.row) + abs(spot.col - target.col)

def h_eucledian(spot, target):
    # eucledian distance is the square root of the sum of the squares of the differences in the x and y coordinates
    # good for when you can move in any direction
    return ((spot.row - target.row)**2 + (spot.col - target.col)**2)**0.5

def manhattan(u,v,e,prev_e):
    start_row, start_col = u
    end_row, end_col = v
    return (abs(start_row - end_row) + abs(start_col - end_col))
def euclidean(u,v,e,prev_e):
    start_row, start_col = u
    end_row, end_col = v
    return ((start_row - end_row)**2 + (start_col - end_col)**2)**0.5

def astar(grid5, start, end, heuristic):
    start_time = time.time()
    stats = {}
    stats['total visited'] = 0
    stats['heuristic'] = heuristic.__name__[2:] # heuristic.__name__ is 'h_manhattan' or 'h_eucledian', so we get the part after the underscore
    count = 0 # used to break ties in the priority queue
    open_set = [] # priority queue

    # initialize g and f scores to infinity
    g_score = {spot: float('inf') for row in grid5 for spot in row}
    f_score = {spot: float('inf') for row in grid5 for spot in row}

    g_score[start] = 0 # g score of start is 0
    f_score[start] = heuristic(start, end) # f score of start is the heuristic value of start

    heapq.heappush(open_set, (0, count, start))
    start.queued = True
    stats['max queue size'] = 1

    while open_set: 
        current = heapq.heappop(open_set)[2] # get the spot object from the tuple
        stats['total visited'] += 1
        current.queued = False # color of spot is linked to different attributes so changing them automatically generates the animation
        current.visited = True

        if current == end: # found target
            path_len = reconstruct_path(end, grid5)
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

def reconstruct_path(end, grid):
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
        current = current.previous
    return path_len



def test_astar():
    grid = [[Spot(row, col) for col in range(5)] for row in range(5)]
    grid[1][2].wall = True
    grid[2][2].wall = True
    grid[3][2].wall = True
    grid[4][2].wall = True
    for row in range(5):
        for column in range(5):
            grid[row][column].update_neighbors(grid)
    start = grid[1][1]
    end = grid[4][4]
    #Test A star with Manhattan Metric
    stats = astar(grid,start,end,h_manhattan)
    len_manhattan = stats['path length'] 
    assert len_manhattan == 8
    #Test A star with Euclidean Metric
    stats = astar(grid,start,end,h_eucledian)
    len_euclidean = stats['path length'] 
    assert len_euclidean == 8
    #test A star against built in python method (Dijkstar with each heuristic)
    #build the graph:
    graph = Graph()
    walls = [(1,2),(2,2), (3,2), (4,2)]
    for row in range(5):
        for column in range(5):
            current = (row,column)
            if current not in walls:
                neighbour_list = [(row,column + 1),(row + 1,column),(row -1, column),(row, column -1)]
                for neighbour in neighbour_list:
                    if (neighbour not in walls and neighbour >= (0,0)):
                        graph.add_edge(current, neighbour,1)
    stats_python = find_path(graph,(1,1),(4,4),None,None,manhattan)
    assert stats_python[3] == len_manhattan
    stats_python = find_path(graph,(1,1),(4,4),None,None,euclidean)
    assert stats_python[3] == len_euclidean
