from collections import deque
import time

from components.spot import Spot
import sys
import tkinter as tk
from tkinter import messagebox

def reconstruct_path(start_previous, end_previous, intersect_node):
    len_path = 0
    current = intersect_node

    # add nodes from intersection node to start node
    while current is not None:
        len_path += 1
        current.path = True
        current = start_previous.get(current)
 
    current = end_previous.get(intersect_node)

    # add nodes from intersection node to end node
    while current is not None:
        len_path += 1
        current.path = True
        current = end_previous.get(current) # moving backwards from intersection node to end node

    return len_path

def bidirectional_BFS(grid50, start, end):

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

                    # if neighbor is visited by both BFS searches, we have found the intersection node
                    if neighbor in start_visited and neighbor in end_visited:
                        intersect_node = neighbor
                        break

            if intersect_node:
                break

            stats['total visited'] += 1
            
        if intersect_node:
            break
    if intersect_node is not None:
        stats['path length'] = reconstruct_path(start_previous, end_previous, intersect_node)
        stats['time'] = round(time.time() - start_time, 2)
    return stats

def test_bidirectional_bfs():
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
    stats =  bidirectional_BFS(grid,grid[2][3],grid[3][1])
    assert stats['path length'] == 8 #checking if the path length is correct

    #Test 2: No path
    '''
    1 1 1 1 1
    1 0 1 0 1
    1 0 1 0 0
    1 0 1  0
    0 0 0 1 0 
    '''
    grid[4][3].wall == True
    for row in range(5):
        for column in range(5):
            grid[row][column].update_neighbors(grid)
    
    stats2 =  bidirectional_BFS(grid,grid[1][1],grid[1][3])
    assert stats2 == None

