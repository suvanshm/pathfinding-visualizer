import heapq
import pygame
import sys

# TODO: Implement A* algorithm

## Hint: You must be able to reconstruct the path once the algorithm has finished
## Hint: You must be able to visualize the algorithm in action i.e call the methods to draw on the screen 
# to visualize the algorithm in action in the astar function

def h_manhattan(spot, target):
    return abs(spot.row - target.row) + abs(spot.col - target.col)

def h_eucledian(spot, target):
    return ((spot.row - target.row)**2 + (spot.col - target.col)**2)**0.5

def astar(win, grid50, start, end, heuristic):
    count = 0
    open_set = []
    g_score = {spot: float('inf') for row in grid50.grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid50.grid for spot in row}
    f_score[start] = heuristic(start, end) 

    heapq.heappush(open_set, (0, count, start))
    start.queued = True
    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # allows exit
                pygame.quit()
                sys.exit()

        current = heapq.heappop(open_set)[2]
        current.queued = False
        current.visited = True
        if current == end:
            reconstruct_path(end, grid50, win)
            return
        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                neighbor.previous = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                if not neighbor.queued:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    neighbor.queued = True
                    grid50.draw_grid(win)
                    pygame.display.update()
        pygame.display.update()

def reconstruct_path(end, grid50, win):
    current = end
    while current.previous:
        current.path = True
        grid50.draw_grid(win)
        pygame.display.update()
        current = current.previous
