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
    # Test 1: (1s are walls, 0s are free spaces)
    '''
    0 0 0 0 0
    0 0 1 0 0 
    0 0 1 0 0
    0 0 1 0 0
    0 0 1 0 0
    '''
    #building the graph with our implementation
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
    stats = dijkstra_test(grid,start,end)
    len = stats['path length']
    graph = Graph()
    walls = [(1,2),(2,2), (3,2), (4,2)]
    
    #build the same graph in python's native implementation
    for row in range(5):
        for column in range(5):
            current = (row,column)
            if current not in walls:
                neighbour_list = [(row,column + 1),(row + 1,column),(row -1, column),(row, column -1)]
                for neighbour in neighbour_list:
                    if (neighbour not in walls and neighbour >= (0,0)):
                        graph.add_edge(current, neighbour,1)
    #once the graph is built, we test whether the shortest path length found by Python's Dijkstra and our implementation is the same.
    stats_python_implementation = find_path(graph,(1,1), (4,4))
    len_python = stats_python_implementation[3]
    assert len == len_python


    #Test when no path is available:
    '''
    0 0 1 0 0
    0 0 1 0 0 
    0 0 1 0 0
    0 0 1 0 0
    0 0 1 0 0
    '''
    grid[0][2].wall = True
    for row in range(5):
        for col in range(5):
            grid[row][col].update_neighbors(grid)
    assert dijkstra_test(grid, start,end) == None

    #No walls, large test (100 x 100 grid)
    # build the graph in our implementation
    grid100 = [[Spot(row, col) for col in range(100)] for row in range(100)] 
    for row in range(100):
        for col in range(100):
            grid100[row][col].update_neighbors(grid100)
    # build the graph in python's native implementation
    graph100 = Graph()
    for row in range(100):
        for column in range(100):
            current = (row,column)
            neighbour_list = [(row,column + 1),(row + 1,column),(row -1, column),(row, column -1)]
            for neighbour in neighbour_list:
                if (neighbour >= (0,0)):
                    graph100.add_edge(current, neighbour,1)
    #test if both implementations give the same length 
    assert dijkstra_test(grid100, grid100[1][1],grid100[85][99])['path length'] == find_path(graph100,(1,1),(85,99))[3]

def dijkstra_test(grid, start, end):
    """
    Finds the shortest path between a start and end node on a grid using Dijkstra's algorithm.

    Args:
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
    path_len = 0
    stats['path length'] = float('infinity')
    while queue:
        current = queue.popleft()
        current.queued = False # color of spot is linked to different attributes so changing them automatically generates the animation
        if current == end: # found target
            path_len = reconstruct_path(end, grid)
            stats['path length'] = path_len
            stats['time'] = round(time.time() - start_time, 2) 
            return stats

        for neighbor in current.neighbors:
            if not neighbor.visited:
                neighbor.visited = True
                path_len += 1
                stats['total visited'] += 1
                neighbor.previous = current
                queue.append(neighbor)
                stats['max queue size'] = max(stats['max queue size'], len(queue))
                neighbor.queued = True

def reconstruct_path(end, grid):
    path_len = 0
    current = end 
    while current.previous:
        current.path = True 
        path_len += 1
        current = current.previous
    return path_len