import pygame
pygame.init()
pygame.font.init()

import sys
import components.grid as grid
import algorithms.dijkstra as dijkstra
import algorithms.a_star as a_star

# TODO: This is the server
# 1. Add a button to select the algorithm [DONE]
# 2. You must be able to select the start and end nodes [DONE]
# 3. You must be able to add barriers [DONE]
# 4. You must be able to reset the grid [DONE]
# 5. You must be able to run the visualizer again after it has finished [DONE]
# 6. The visualizer must stop once the start and end nodes find each other. [DONE]
# 7. A path must be drawn from the start node to the end node once the visualizer has finished. [DONE]

# DIMENSIONS
MENU_OFFSET = 300  # side menu for buttons and stats
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


# Creating buttons 
def button_fn(screen, msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            pygame.time.delay(300)
            return action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.SysFont('courier', 12)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)

def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0)) 
    return textSurface, textSurface.get_rect()



# button action functions 
def dijkstra_action(win, grid50, start, end, clicked=False):
    if clicked:
        if start and end:
            grid50.reset()
            grid50.update_neighbors()
            stats = dijkstra.dijkstra(win, grid50, start, end) 
            #print(stats)
            return stats

def astar_manhattan_action(win, grid50, start, end, clicked=False):
    if clicked and start and end:
        grid50.reset()
        grid50.update_neighbors()
        stats = a_star.astar(win, grid50, start, end, a_star.h_manhattan)
        return stats

def astar_euclidean_action(win, grid50, start, end, clicked=False):
    if clicked and start and end:
        grid50.reset()
        grid50.update_neighbors()
        stats = a_star.astar(win, grid50, start, end, a_star.h_eucledian)
        return stats

def reset_buttons(win):
    # Reset all buttons to their original color
    button_fn(win, "Dijkstra", 610, 125, 70, 25, colors['LIGHT_GREY'], colors['RED'])
    button_fn(win, "A*(Manhattan)", 690, 125, 95, 25, colors['LIGHT_GREY'], colors['RED'])
    button_fn(win, "A*(Euclidean)", 795, 125, 95, 25, colors['LIGHT_GREY'], colors['RED'])


def main(win):
    # create grid object, named grid50 to distinguish from grid.py
    grid50 = grid.Grid(N_SPOTS)
    start = None
    end = None
    stats_surface = pygame.Surface((200, 600))  # surface for stats
    prev_stats = None

    buttons = [
        {"label": "Dijkstra", "x": 610, "y": 125, "width": 70, "height": 25, 
         "idle_color": colors['LIGHT_GREY'], "active_color": colors['RED'], 
         "action": lambda: (reset_buttons(win), dijkstra_action(win, grid50, start, end, clicked = True))},
        {"label": "A*(Manhattan)", "x": 690, "y": 125, "width": 95, "height": 25, 
         "idle_color": colors['LIGHT_GREY'], "active_color": colors['RED'], 
         "action": lambda: (reset_buttons(win), astar_manhattan_action(win, grid50, start, end, clicked = True))},
        {"label": "A*(Euclidean)", "x": 795, "y": 125, "width": 95, "height": 25, 
         "idle_color": colors['LIGHT_GREY'], "active_color": colors['RED'], 
         "action": lambda: (reset_buttons(win), astar_euclidean_action(win, grid50, start, end, clicked = True))}
    ]

    while True:
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
                    start = None
                    end = None
                    # reset stats
                    stats_surface.fill((0, 0, 0))
                    prev_stats = None
                # press 'd' to run dijkstra's algorithm
                if event.key == pygame.K_d:
                    if start and end:
                        grid50.reset()
                        grid50.update_neighbors()
                        dijkstra.dijkstra(win, grid50, start, end)
                # press 'a' to run a* algorithm (manhattan distance)
                if event.key == pygame.K_a:
                    if start and end:
                        grid50.reset()
                        grid50.update_neighbors()
                        a_star.astar(win, grid50, start,
                                     end, a_star.h_manhattan)
                # press 'e' to run a* algorithm (euclidean distance)
                if event.key == pygame.K_e:
                    if start and end:
                        grid50.reset()
                        grid50.update_neighbors()
                        a_star.astar(win, grid50, start,
                                     end, a_star.h_eucledian)

            if pygame.mouse.get_pressed()[0]:  # left click
                pos = pygame.mouse.get_pos()
                # check if click in grid
                if 0 <= pos[0] < WIN_HEIGHT and 0 <= pos[1] < WIN_HEIGHT:
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
                if 0 <= pos[0] < WIN_HEIGHT and 0 <= pos[1] < WIN_HEIGHT:
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
                    if 0 <= pos[0] < WIN_HEIGHT and 0 <= pos[1] < WIN_HEIGHT:
                        row = pos[0] // SPOT_SIZE
                        col = pos[1] // SPOT_SIZE
                        spot = grid50.grid[row][col]
                        # if spot.wall: # reset functionality removed
                        # spot.wall = False
                        if not spot.start and not spot.target:
                            spot.wall = True  # left click and motion sets wall

        win.fill(colors['BLACK'])  # background fill

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

        for button in buttons:
            stats = button_fn(win, button["label"], button["x"], button["y"], button["width"], button["height"], button["idle_color"], button["active_color"], button["action"])
            if stats:
                break
        
        # draw buttons
        #stats = button(win, "Dijkstra", 610, 125, 70, 25, colors['LIGHT_GREY'], colors['RED'], lambda: (reset_buttons(win), dijkstra_action(win, grid50, start, end, clicked = True)))
        #if stats: print(stats[1])
        #stats2 = button(win, "A*(Manhattan)", 690, 125, 95, 25, colors['LIGHT_GREY'], colors['RED'], lambda: (reset_buttons(win), astar_manhattan_action(win, grid50, start, end, clicked = True)))
        #button(win, "A*(Euclidean)", 795, 125, 95, 25, colors['LIGHT_GREY'], colors['RED'], lambda: (reset_buttons(win), astar_euclidean_action(win, grid50, start, end, clicked = True)))

        # draw stats 
        win.blit(seperator, (605, 190))
        statsfont = pygame.font.SysFont('courier', 16)
        text = 'stats/info:' 
        text_surface = statsfont.render(text, True, (255, 255, 255)) 
        win.blit(text_surface, (605, 210))
        text = f'start:{start}, end:{end}'
        text_surface = statsfont.render(text, True, (255, 255, 255))
        win.blit(text_surface, (605, 230))
        text = f'walls:{grid50.num_wall()}'
        text_surface = statsfont.render(text, True, (255, 255, 255))
        win.blit(text_surface, (605, 250))

        if stats != prev_stats and stats:
            stats_surface.fill((0, 0, 0))  # clear the stats surface
            y_offset = 0  # start at the top of the surface
            for stat, value in stats[1].items():
                stat_text = statsfont.render(f'{stat}: {value}', True, (255, 255, 255))
                stats_surface.blit(stat_text, (0, y_offset))
                y_offset += 20
            prev_stats = stats  # update the previous stats

        win.blit(stats_surface, (605, 270))
        grid50.draw_grid(win)
        pygame.display.update()

main(window)
