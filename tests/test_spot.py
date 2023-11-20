import pytest
import pygame
from components.spot import Spot
import pygame
from unittest.mock import Mock

def test_update_neighbors():
    # create a 3x3 grid with no walls
    grid = [[Spot(row, col) for col in range(3)] for row in range(3)]
    spot = grid[1][1]  # middle spot
    spot.update_neighbors(grid)
    assert len(spot.neighbors) == 4  # should have 4 neighbors
    assert grid[0][1] in spot.neighbors  # top neighbor
    assert grid[2][1] in spot.neighbors  # bottom neighbor
    assert grid[1][0] in spot.neighbors  # left neighbor
    assert grid[1][2] in spot.neighbors  # right neighbor

    # create a 3x3 grid with walls on the top and bottom rows
    grid = [[Spot(row, col) for col in range(3)] for row in range(3)]
    grid[0][0].wall = True
    grid[0][1].wall = True
    grid[0][2].wall = True
    grid[2][0].wall = True
    grid[2][1].wall = True
    grid[2][2].wall = True
    spot = grid[1][1]  # middle spot
    spot.update_neighbors(grid)
    assert len(spot.neighbors) == 2  # should have 2 neighbors
    assert grid[1][0] in spot.neighbors  # left neighbor
    assert grid[1][2] in spot.neighbors  # right neighbor

    # create a 3x3 grid with walls on the left and right columns
    grid = [[Spot(row, col) for col in range(3)] for row in range(3)]
    grid[0][0].wall = True
    grid[1][0].wall = True
    grid[2][0].wall = True
    grid[0][2].wall = True
    grid[1][2].wall = True
    grid[2][2].wall = True
    spot = grid[1][1]  # middle spot
    spot.update_neighbors(grid)
    assert len(spot.neighbors) == 2  # should have 2 neighbors
    assert grid[0][1] in spot.neighbors  # top neighbor
    assert grid[2][1] in spot.neighbors  # bottom neighbor

    # create a 1x1 grid with no walls
    grid = [[Spot(0, 0)]]
    spot = grid[0][0]
    spot.update_neighbors(grid)
    assert len(spot.neighbors) == 0  # should have no neighborsdef test_draw_spot():
    

    