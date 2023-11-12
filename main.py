import pygame
import sys
import components.grid as grid
import algorithms.dijkstra as dijkstra
import algorithms.a_star as a_star

# TODO: This is the server
# 1. Add a button to select the algorithm [can toggle from keyboard, yet to add buttons in UI]
# 2. You must be able to select the start and end nodes [DONE]
# 3. You must be able to add barriers [DONE]
# 4. You must be able to reset the grid [DONE]
# 5. You must be able to run the visualizer again after it has finished [DONE]
# 6. The visualizer must stop once the start and end nodes find each other. [DONE]
# 7. A path must be drawn from the start node to the end node once the visualizer has finished. [DONE]

# DIMENSIONS
MENU_OFFSET = 200  # side menu for buttons and stats
WIN_HEIGHT = 600  # square grid size in px
WIN_WIDTH = WIN_HEIGHT + MENU_OFFSET
N_SPOTS = 50  # no. of spots in each row and col
SPOT_SIZE = WIN_HEIGHT // N_SPOTS  # size of each spot in px

# COLORS
colors = {
    'WHITE': (255, 255, 255),
    'RED': (255, 0, 0),
    'BLACK': (0, 0, 0),
    'GREY': (30, 30, 30),
    'LIGHT_GREY': (120, 120, 120)
}

# Creating Window
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Pathfinding Visualizer')


def main(win):
    # create grid object, named grid50 to distinguish from grid.py
    grid50 = grid.Grid(N_SPOTS)
    start = None
    end = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # allows exit
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # reset grid with key 'R', keeps walls,target,start
                if event.key == pygame.K_r:
                    grid50.reset()
                # clear grid with key 'C', resets everything
                if event.key == pygame.K_c:
                    grid50.clear()
                    start = None
                    end = None
                # press 'd' to run dijkstra's algorithm
                if event.key == pygame.K_d:
                    if start and end:
                        grid50.update_neighbors()
                        dijkstra.dijkstra(win, grid50, start, end)
                # press 'a' to run a* algorithm (manhattan distance)
                if event.key == pygame.K_a:
                    if start and end:
                        grid50.update_neighbors()
                        a_star.astar(win, grid50, start, end, a_star.h_manhattan)
                # press 'e' to run a* algorithm (euclidean distance)
                if event.key == pygame.K_e:
                    if start and end:
                        grid50.update_neighbors()
                        a_star.astar(win, grid50, start, end, a_star.h_eucledian)

            if pygame.mouse.get_pressed()[0]:  # left click
                pos = pygame.mouse.get_pos()
                # check if click in grid
                if pos[0] < WIN_HEIGHT and pos[1] < WIN_HEIGHT:
                    row = pos[0] // SPOT_SIZE
                    col = pos[1] // SPOT_SIZE
                    spot = grid50.grid[row][col]
                    if spot.wall:
                        spot.wall = False
                    elif not spot.start and not spot.target:
                        spot.wall = True  # left click resets and sets wall

            if pygame.mouse.get_pressed()[2]:  # right click
                pos = pygame.mouse.get_pos()
                # check if click in grid
                if pos[0] < WIN_HEIGHT and pos[1] < WIN_HEIGHT:
                    row = pos[0] // SPOT_SIZE
                    col = pos[1] // SPOT_SIZE
                    spot = grid50.grid[row][col]
                    # right click resets and sets start and target, in that order
                    if spot.start:
                        spot.start = False
                        start = None
                    elif spot.target:
                        spot.target = False
                        end = None
                    elif not start and not spot.target and not spot.wall:
                        spot.start = True
                        start = spot
                    elif not end and not spot.start and not spot.wall:
                        spot.target = True
                        end = spot
            
            if event.type == pygame.MOUSEMOTION: 
                if event.buttons[0]:  # left click and motion
                    pos = pygame.mouse.get_pos()
                    # check if click in grid
                    if pos[0] < WIN_HEIGHT and pos[1] < WIN_HEIGHT:
                        row = pos[0] // SPOT_SIZE
                        col = pos[1] // SPOT_SIZE
                        spot = grid50.grid[row][col]
                        #if spot.wall: # reset functionality removed
                            #spot.wall = False
                        if not spot.start and not spot.target:
                            spot.wall = True  # left click and motion sets wall

        win.fill(colors['BLACK'])  # background fill
        grid50.draw_grid(win)
        pygame.display.update()


main(window)
