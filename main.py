import pygame
import heapq
import sys
from collections import deque

#initializing pygame
pygame.init()

# Constants 
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man A* Pathfinding")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# defining the restart and quit buttons
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20
BUTTON_Y = HEIGHT - BUTTON_HEIGHT - BUTTON_MARGIN


# Define grid
# 0 represents the empty spaces
# 1 represents the walls 
# 2 represents the dots / pacman food

# MAZE = [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
#     [1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
#     [1, 2, 1, 0, 1, 2, 1, 0, 0, 0, 0, 0, 1, 2, 1, 0, 1, 0, 2, 1],
#     [1, 2, 1, 0, 1, 2, 1, 0, 1, 1, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1],
#     [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
#     [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
#     [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
#     [1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
#     [1, 2, 1, 0, 1, 2, 1, 0, 0, 0, 0, 0, 1, 2, 1, 0, 1, 0, 2, 1],
#     [1, 2, 1, 0, 1, 2, 1, 0, 1, 1, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1],
#     [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]

# # Define Pac-Man and Ghosts positions
# PACMAN = (1, 1)
# GHOSTS = [(10, 18), (10, 1), (1, 18)]

MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2, 1, 1, 1, 1],
    [0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1],
    [1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1],
    [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# New starting positions for Pac-Man and Ghosts
PACMAN = (1, 1)
GHOSTS = [(10, 9), (10, 10), (9, 9), (9, 10)]

# directions
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


#implementing A* algo
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, current)

        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] != 1:
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

#using dijkstra's algothrim to compare
def dijkstra(grid, start, goal):
    queue = deque([(0, start)])
    came_from = {}
    cost_so_far = {start: 0}

    while queue:
        current_cost, current = queue.popleft()

        if current == goal:
            return reconstruct_path(came_from, current)

        for dx, dy in DIRECTIONS:
            next_node = (current[0] + dx, current[1] + dy)
            if 0 <= next_node[0] < len(grid) and 0 <= next_node[1] < len(grid[0]) and grid[next_node[0]][next_node[1]] != 1:
                new_cost = current_cost + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost
                    queue.append((priority, next_node))
                    came_from[next_node] = current

    return None

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

# visualizing the game and drawing out the entities
def draw_grid(win, grid):
    cell_width = WIDTH // len(grid[0])
    cell_height = HEIGHT // len(grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                pygame.draw.rect(win, BLUE, (j * cell_width, i * cell_height, cell_width, cell_height))
            elif grid[i][j] == 2:
                pygame.draw.rect(win, BLACK, (j * cell_width, i * cell_height, cell_width, cell_height))
                pygame.draw.circle(win, WHITE, (j * cell_width + cell_width // 2, i * cell_height + cell_height // 2), 
                                   min(cell_width, cell_height) // 10)
            else:
                pygame.draw.rect(win, BLACK, (j * cell_width, i * cell_height, cell_width, cell_height))

def draw_entities(win, pacman, ghosts):
    cell_width = WIDTH // len(MAZE[0])
    cell_height = HEIGHT // len(MAZE)
    pygame.draw.circle(win, YELLOW, (pacman[1] * cell_width + cell_width // 2, pacman[0] * cell_height + cell_height // 2), min(cell_width, cell_height) // 2)
    for ghost in ghosts:
        pygame.draw.circle(win, RED, (ghost[1] * cell_width + cell_width // 2, ghost[0] * cell_height + cell_height // 2), min(cell_width, cell_height) // 2)

def move_ghosts(grid, ghosts, pacman, algorithm='a_star'):
    new_ghosts = []
    for ghost in ghosts:
        if algorithm == 'a_star':
            path = a_star(grid, ghost, pacman)
        elif algorithm == 'dijkstra':
            path = dijkstra(grid, ghost, pacman)
        if path and len(path) > 1:
            new_ghosts.append(path[1])  # Move ghost to the next step in the path
        else:
            new_ghosts.append(ghost)  # Stay in place if no path found
    return new_ghosts

def draw_button(win, text, x, y, width, height, color, text_color):
    pygame.draw.rect(win, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
    win.blit(text_surface, text_rect)

def check_button_click(mouse_pos, x, y, width, height):
    return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height


def game_over_screen(win, score):
    win.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render('Game Over', True, RED)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/4))
    win.blit(text, text_rect)

    score_font = pygame.font.Font(None, 48)
    score_text = score_font.render(f'Score: {score}', True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH/2, HEIGHT/2))
    win.blit(score_text, score_rect)

    # Draw restart button
    restart_button_x = WIDTH / 4 - 75
    restart_button_y = HEIGHT / 2 + 50
    draw_button(win, "Restart", restart_button_x, restart_button_y, 150, 50, GREEN, WHITE)

    # Draw quit button
    quit_button_x = 3 * WIDTH / 4 - 75
    quit_button_y = HEIGHT / 2 + 50
    draw_button(win, "Quit", quit_button_x, quit_button_y, 150, 50, RED, WHITE)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if check_button_click(mouse_pos, restart_button_x, restart_button_y, 150, 50):
                    return "restart"
                if check_button_click(mouse_pos, quit_button_x, quit_button_y, 150, 50):
                    return "quit"


def game_loop():
    clock = pygame.time.Clock()
    pacman = PACMAN
    ghosts = GHOSTS.copy()
    score = 0
    maze_copy = [row[:] for row in MAZE]
    algorithm = 'a_star'  # Default algorithm
    
    while True:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", score
            if event.type == pygame.KEYDOWN:
                new_pos = pacman
                if event.key == pygame.K_UP and pacman[0] > 0 and maze_copy[pacman[0] - 1][pacman[1]] != 1:
                    new_pos = (pacman[0] - 1, pacman[1])
                if event.key == pygame.K_DOWN and pacman[0] < len(maze_copy) - 1 and maze_copy[pacman[0] + 1][pacman[1]] != 1:
                    new_pos = (pacman[0] + 1, pacman[1])
                if event.key == pygame.K_LEFT and pacman[1] > 0 and maze_copy[pacman[0]][pacman[1] - 1] != 1:
                    new_pos = (pacman[0], pacman[1] - 1)
                if event.key == pygame.K_RIGHT and pacman[1] < len(maze_copy[0]) - 1 and maze_copy[pacman[0]][pacman[1] + 1] != 1:
                    new_pos = (pacman[0], pacman[1] + 1)
                
                if maze_copy[new_pos[0]][new_pos[1]] == 2:
                    score += 10
                    maze_copy[new_pos[0]][new_pos[1]] = 0
                pacman = new_pos
            
                if event.key == pygame.K_a:
                    algorithm = 'a_star'
                elif event.key == pygame.K_d:
                    algorithm = 'dijkstra'


        ghosts = move_ghosts(maze_copy, ghosts, pacman, algorithm)

        if pacman in ghosts:
            return game_over_screen(WIN, score), score

        WIN.fill(BLACK)
        draw_grid(WIN, maze_copy)
        draw_entities(WIN, pacman, ghosts)
        
        # Draw score 
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        WIN.blit(score_text, (10, 10))
        
        #and current algorithm
        algo_text = font.render(f'Algorithm: {algorithm.capitalize()}', True, WHITE)
        WIN.blit(algo_text, (10, 50))
        
        pygame.display.update()

def main():
    high_score = 0
    while True:
        result, score = game_loop()
        high_score = max(high_score, score)
        if result == "quit":
            break
        # if result is "restart", the loop will continue and start a new game

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
