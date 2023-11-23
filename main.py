import pygame
pygame.init()
pygame.font.init()

import sys
import components.grid as grid
import algorithms.dijkstra as dijkstra
import algorithms.a_star as a_star
import algorithms.dfs as dfs
import algorithms.bidirectional_bfs as bidirectional_bfs

# DIMENSIONS
MENU_OFFSET = 300  # width of side menu for buttons and stats
WIN_HEIGHT = 600  # size of one side of the square grid
WIN_WIDTH = WIN_HEIGHT + MENU_OFFSET # width of window = grid size + menu size
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

# creating window
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Pathfinding Visualizer') # title of window


def button_fn(screen, msg, x, y, w, h, ic, ac, action=None):
    """
    Draws a button on the screen with the given parameters and returns the stats from the action function if the button is clicked.

    Args:
    screen: pygame.display object representing the game window
    msg: string representing the text to be displayed on the button
    x: integer representing the x-coordinate of the top-left corner of the button
    y: integer representing the y-coordinate of the top-left corner of the button
    w: integer representing the width of the button
    h: integer representing the height of the button
    ic: tuple representing the RGB color code of the button in inactive state
    ac: tuple representing the RGB color code of the button in active state
    action: function to be executed when the button is clicked (default is None)

    Returns:
    The stats returned by the action function if the button is clicked, otherwise None.
    """
    mouse = pygame.mouse.get_pos() # get mouse position
    click = pygame.mouse.get_pressed() # get info on if mouse is clicked

    if x + w > mouse[0] > x and y + h > mouse[1] > y: # if mouse is hovering over button
        pygame.draw.rect(screen, ac, (x, y, w, h)) # draw button in active color
        if click[0] == 1 and action != None: # if button is clicked and has an action function assigned
            pygame.time.delay(300) # delay to prevent multiple clicks
            return action() # return the stats from the action function
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h)) # draw button in inactive color

    smallText = pygame.font.SysFont('courier', 12) # font for button text
    text_surface = smallText.render(msg, True, (0, 0, 0)) 
    text_rect = text_surface.get_rect(center=((x + (w / 2)), (y + (h / 2)))) # center text in button
    screen.blit(text_surface, text_rect) # display text in button



# button action functions 

def dijkstra_action(win, grid50, start, end, clicked=False):
    """
    Runs Dijkstra's algorithm on the given grid. This is an action function to be fed into the button_fn function.

    Args:
        win (pygame.display): The Pygame window surface.
        grid50 (Grid): The grid object representing the game board.
        start (Spot): The starting node for Dijkstra's algorithm.
        end (Spot): The ending node for Dijkstra's algorithm.
        clicked (bool, optional): Whether or not the mouse was clicked. Defaults to False.
    
    Returns:
        stats: A dictionary containing statistics about the Dijkstra's algorithm run.
    """
    if clicked and start and end:
        grid50.reset() # reset grid
        grid50.update_neighbors() # update neighbors for each spot
        stats = dijkstra.dijkstra(win, grid50, start, end) 
        return stats  # return stats from dijkstra's algorithm

def astar_manhattan_action(win, grid50, start, end, clicked=False):
    """
    Runs the A* algorithm with the Manhattan distance heuristic on the given grid. This is an action function to be fed into the button_fn function.

    Args:
        win (pygame.display): The Pygame window surface.
        grid50 (Grid): The grid object representing the game board.
        start (Spot): The starting node for the A* algorithm.
        end (Spot): The ending node for the A* algorithm.
        clicked (bool, optional): Whether or not the mouse was clicked. Defaults to False.

    Returns:
        stats: A dictionary containing statistics about the A* algorithm run.
    """
    if clicked and start and end:
        grid50.reset()
        grid50.update_neighbors()
        stats = a_star.astar(win, grid50, start, end, a_star.h_manhattan)
        return stats

def astar_euclidean_action(win, grid50, start, end, clicked=False):
    """
    Runs the A* algorithm with the euclidean distance heuristic on the given grid. This is an action function to be fed into the button_fn function.

    Args:
        win (pygame.display): The Pygame window surface.
        grid50 (Grid): The grid object representing the game board.
        start (Spot): The starting node for the A* algorithm.
        end (Spot): The ending node for the A* algorithm.
        clicked (bool, optional): Whether or not the mouse was clicked. Defaults to False.

    Returns:
        stats: A dictionary containing statistics about the A* algorithm run.
    """
    if clicked and start and end:
        grid50.reset()
        grid50.update_neighbors()
        stats = a_star.astar(win, grid50, start, end, a_star.h_eucledian)
        return stats

def dfs_action(win, grid50, start, end, clicked=False):
    """
    Runs the depth-first search algorithm on the given grid. This is an action function to be fed into the button_fn function.

    Args:
        win (pygame.display): The Pygame window surface.
        grid50 (Grid): The grid object representing the game board.
        start (Spot): The starting node for the DFS algorithm.
        end (Spot): The ending node for the DFS algorithm.
        clicked (bool, optional): Whether or not the mouse was clicked. Defaults to False.
    
    Returns:
        stats: A dictionary containing statistics about the DFS algorithm run.
    """
    if clicked and start and end:
        grid50.reset()
        grid50.update_neighbors()
        stats = dfs.dfs(win, grid50, start, end)
        return stats

def bidirectional_BFS_action(win, grid50, start, end, clicked=False):
    """
    Runs the bidirectional BFS algorithm on the given grid and returns statistics about the search. This is an action function to be fed into the button_fn function.

    Args:
        win (pygame.display): The Pygame window surface to draw the grid on.
        grid50 (Grid): The grid object to run the search on.
        start (Spot): The starting node for the search.
        end (Spot): The ending node for the search.
        clicked (bool, optional): Whether the function was called due to a mouse click. Defaults to False.

    Returns:
        stats: A dictionary containing statistics about the search, including the number of nodes visited and the path found.
    """
    if clicked and start and end:
        grid50.reset()
        grid50.update_neighbors()
        stats = bidirectional_bfs.bidirectional_BFS(win, grid50, start, end)
        return stats

def reset_buttons(win):
    """
    Redraws all buttons. This is called alongside the action buttons whenever a button is clicked. Firstly, it locks the buttons 
    so that the user cannot click another button while an algorithm is running, we do this by calling button_fn for each button again 
    but without passing in an action function.
    This is also needed to fix a graphics glitch. Without this, if an algorithm button is clicked, it hides all the other buttons,
    and makes the menu display look odd.

    Parameters:
    win (Pygame.display): The Pygame display object representing the window.

    Returns:
    None
    """
    # calls button_fn for each button again 
    # we do not need to pass in any action because we do not want these buttons to do anything when clicked 
    # we just want them to be displayed while an algo runs
    # this means the user can't click another button while an algo is running 
    button_fn(win, "Dijkstra", 610, 125, 70, 25, colors['LIGHT_GREY'], colors['RED'])
    button_fn(win, "A*(Manhattan)", 690, 125, 95, 25, colors['LIGHT_GREY'], colors['RED'])
    button_fn(win, "A*(Euclidean)", 795, 125, 95, 25, colors['LIGHT_GREY'], colors['RED'])
    button_fn(win, "DFS", 610, 155, 50, 25, colors['LIGHT_GREY'], colors['RED'])
    button_fn(win, "2-side BFS", 665, 155, 75, 25, colors['LIGHT_GREY'], colors['RED'])


def main(win): 
    """
    Runs the main loop of the pathfinding visualizer program. 
    Allows the user to interact with the grid, set start and end points, set walls, and run various pathfinding algorithms. 
    Displays statistics and information about the current state of the grid and the pathfinding algorithm being run.

    Args:
    win (pygame.Display): The display object representing the window on which the program is displayed.

    Returns:
    None
    """

    # create grid object, named grid50 to distinguish from grid.py module and Grid class
    grid50 = grid.Grid(N_SPOTS) 

    # initialize start and end to None
    start = None
    end = None

    # initialize stats surface, which will display stats about the current state of the grid and the pathfinding algorithm being run
    stats_surface = pygame.Surface((200, 600)) 
    prev_stats = None # used to keep track of the previous stats so that we can clear the stats surface when the stats change

    # initialize buttons list, each element in list is a dictionary representing a button, the keys are the parameters for the button_fn function, 
    # and the values are the  corresponding values for those parameters
    # in the main loop, we iterate through this list and call button_fn for each button
    # the action key is a lambda function that calls the corresponding action function for the button and also redraws all the buttons
    # having one list here outside the main loop allows us to easily add more buttons in the future 
    buttons = [
        {"label": "Dijkstra", "x": 610, "y": 125, "width": 70, "height": 25, 
         "idle_color": colors['LIGHT_GREY'], "active_color": colors['RED'], 
         "action": lambda: (reset_buttons(win), dijkstra_action(win, grid50, start, end, clicked = True))},
        {"label": "A*(Manhattan)", "x": 690, "y": 125, "width": 95, "height": 25, 
         "idle_color": colors['LIGHT_GREY'], "active_color": colors['RED'], 
         "action": lambda: (reset_buttons(win), astar_manhattan_action(win, grid50, start, end, clicked = True))},
        {"label": "A*(Euclidean)", "x": 795, "y": 125, "width": 95, "height": 25, 
         "idle_color": colors['LIGHT_GREY'], "active_color": colors['RED'], 
         "action": lambda: (reset_buttons(win), astar_euclidean_action(win, grid50, start, end, clicked = True))},
        {"label": "DFS", "x": 610, "y": 155, "width": 50, "height": 25,
        "idle_color": colors['LIGHT_GREY'], "active_color": colors['RED'], 
        "action": lambda: (reset_buttons(win), dfs_action(win, grid50, start, end, clicked = True))}, 
        {"label": "2-side BFS", "x": 665, "y": 155, "width": 75, "height": 25,
        "idle_color": colors['LIGHT_GREY'], "active_color": colors['RED'],
        "action": lambda: (reset_buttons(win), bidirectional_BFS_action(win, grid50, start, end, clicked = True))}
    ]

    # this is the main loop of the program, it runs until the user exits the program
    while True:

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # allows exit
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # reset grid with key 'R', keeps walls,target,start
                if event.key == pygame.K_r:
                    grid50.reset()
                    # reset stats
                    stats_surface.fill((0, 0, 0))
                    prev_stats = None
                # clear grid with key 'C', resets everything
                if event.key == pygame.K_c:
                    grid50.clear()
                    # reset start and end
                    start = None
                    end = None
                    # reset stats
                    stats_surface.fill((0, 0, 0))
                    prev_stats = None

            # left click and motion toggles a spot to be a wall/reset a wall
            if pygame.mouse.get_pressed()[0]:  # left click
                pos = pygame.mouse.get_pos()
                # check if click in grid 
                if 0 <= pos[0] < WIN_HEIGHT and 0 <= pos[1] < WIN_HEIGHT:
                    row = pos[0] // SPOT_SIZE # get row and col of spot clicked
                    col = pos[1] // SPOT_SIZE
                    spot = grid50.grid[row][col] # get spot object
                    if spot.wall:
                        spot.wall = False # if spot is wall, reset it
                    elif not spot.start and not spot.target:
                        spot.wall = True  # if spot is not start or target, set it to be a wall

            # right click toggles setting and resetting both start and end nodes
            if pygame.mouse.get_pressed()[2]:  # right click
                pos = pygame.mouse.get_pos()
                # check if click in grid
                if 0 <= pos[0] < WIN_HEIGHT and 0 <= pos[1] < WIN_HEIGHT:
                    row = pos[0] // SPOT_SIZE
                    col = pos[1] // SPOT_SIZE
                    spot = grid50.grid[row][col]
                    # if spot is start or target, reset it
                    if spot.start:
                        spot.start = False
                        start = None
                    elif spot.target:
                        spot.target = False
                        end = None
                    # if we don't already have a start node, and spot is not wall or target, set it to be start
                    elif not start and not spot.target and not spot.wall:
                        spot.start = True
                        start = spot
                    # if we don't already have an end node, and spot is not wall or start, set it to be end
                    elif not end and not spot.start and not spot.wall:
                        spot.target = True
                        end = spot

            # this allows you to drag mouse to make walls
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # left click and motion
                    pos = pygame.mouse.get_pos()
                    # check if click in grid
                    if 0 <= pos[0] < WIN_HEIGHT and 0 <= pos[1] < WIN_HEIGHT:
                        row = pos[0] // SPOT_SIZE
                        col = pos[1] // SPOT_SIZE
                        spot = grid50.grid[row][col]
                        # if spot is not start or target, set it to be a wall
                        if not spot.start and not spot.target:
                            spot.wall = True  

        
        # -------------- GUI ---------------- 

        # fill background with black
        win.fill(colors['BLACK']) 

        # draw title
        titlefont = pygame.font.SysFont('courier', 22)
        text_surface = titlefont.render('pathfinding visualizer', True, (255, 255, 255))
        win.blit(text_surface, (605, 10))
        seperator = titlefont.render('----------------------', True, (255, 255, 255))
        win.blit(seperator, (605, 30))

        # draw instructions
        instructionsfont = pygame.font.SysFont('courier', 16)
        instructions = 'left-click: toggle wall' 
        instr2 = 'right-click: toggle start/end'
        instr3 = 'r: reset algo, c: clear grid'
        instr4 = 'click algo button to start:'
        text_surface = instructionsfont.render(instructions, True, (255, 255, 255))
        text_surface2 = instructionsfont.render(instr2, True, (255, 255, 255))
        text_surface3 = instructionsfont.render(instr3, True, (255, 255, 255))
        text_surface4 = instructionsfont.render(instr4, True, (255, 255, 255))
        win.blit(text_surface, (605, 45))
        win.blit(text_surface2, (605, 60))
        win.blit(text_surface3, (605, 75))
        win.blit(seperator, (605, 85))
        win.blit(text_surface4, (605, 105))

        # loop calls button_fn for each button in buttons list
        # if a button is clicked, the stats from the action function are returned
        # if stats are returned, we break out of the loop and display the stats
        for button in buttons:
            stats = button_fn(win, button["label"], button["x"], button["y"], button["width"], button["height"], button["idle_color"], button["active_color"], button["action"])
            if stats:
                break
        

        # draw stats 

        win.blit(seperator, (605, 190))
        statsfont = pygame.font.SysFont('courier', 16)
        text = 'stats/info:' 
        text_surface = statsfont.render(text, True, (255, 255, 255)) 
        win.blit(text_surface, (605, 210))

        # display start and end coordinates if they exist (1-indexed)
        # top left corner is (1, 1), bottom right corner is (n_spots, n_spots)
        if start and end:
            text = f'start:({start.col+1}, {start.row+1}), end:({end.col+1}, {end.row+1})'
        # if either start or end is None, display the coordinates of the one that is not None
        elif start:
            text = f'start:({start.col+1}, {start.row+1}), end:({end})'
        elif end: 
            text = f'start:({start}), end:({end.col+1}, {end.row+1})'
        # both are None
        else:
            text = f'start:({start}), end:({end})' 
        
        # display number of walls 
        text_surface = statsfont.render(text, True, (255, 255, 255))
        win.blit(text_surface, (605, 230))
        text = f'walls:{grid50.num_wall()}'
        text_surface = statsfont.render(text, True, (255, 255, 255))
        win.blit(text_surface, (605, 250))

        # display stats from algorithm if they exist and have changed
        if stats != prev_stats and stats:
            stats_surface.fill((0, 0, 0))  # clear the stats surface
            y_offset = 0  # start at the top of the surface

            # weird bug where stats gets returned as tuple: (None, {dictionary we need}), so we just get the dictionary from stats[1]
            # display the stats in the stats surface by iterating through the dictionary
            # we use y_offset to keep track of the y-coordinate of the text we are displaying
            for stat, value in stats[1].items(): 
                stat_text = statsfont.render(f'{stat}: {value}', True, (255, 255, 255))
                stats_surface.blit(stat_text, (0, y_offset))
                y_offset += 20
            prev_stats = stats  # update the previous stats to check future changes

        # display the stats surface
        win.blit(stats_surface, (605, 270))
        # draw grid and update display
        grid50.draw_grid(win)
        pygame.display.update()


main(window) # run main function
