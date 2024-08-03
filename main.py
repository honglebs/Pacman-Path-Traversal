import pygame
import heapq
import sys
from collections import deque

# Constants 
MAZE_WIDTH = 20
MAZE_HEIGHT = 22
CELL_SIZE = 30  # Adjusted to fit the maze in the window
WIDTH = MAZE_WIDTH * CELL_SIZE
HEIGHT = MAZE_HEIGHT * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Game components
EMPTY = 0 
WALL = 1
FOOD = 2

# Define the maze layout
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
PACMAN_START = (1, 1)
GHOST_STARTS = [(10, 9), (10, 10), (9, 9), (9, 10)]

# directions
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class PacmanGame:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man A* Pathfinding")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.pacman = PACMAN_START
        self.ghosts = GHOST_STARTS.copy()
        self.score = 0
        self.maze = [row[:] for row in MAZE]
        self.algorithm = 'a_star'

    def draw_grid(self):
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if cell == WALL:
                    pygame.draw.rect(self.window, BLUE, rect)
                elif cell == FOOD:
                    pygame.draw.rect(self.window, BLACK, rect)
                    pygame.draw.circle(self.window, WHITE, rect.center, CELL_SIZE // 10)
                else:
                    pygame.draw.rect(self.window, BLACK, rect)

    def draw_entities(self):
        self.draw_circle(self.pacman, YELLOW)
        for ghost in self.ghosts:
            self.draw_circle(ghost, RED)

    def draw_circle(self, position, color):
        center = ((position[1] + 0.5) * CELL_SIZE, (position[0] + 0.5) * CELL_SIZE)
        pygame.draw.circle(self.window, color, center, CELL_SIZE // 2)

    def draw_text(self, text, position):
        text_surface = self.font.render(text, True, WHITE)
        self.window.blit(text_surface, position)

    def move_pacman(self, direction):
        new_pos = (self.pacman[0] + direction[0], self.pacman[1] + direction[1])
        if self.is_valid_move(new_pos):
            if self.maze[new_pos[0]][new_pos[1]] == FOOD:
                self.score += 10
                self.maze[new_pos[0]][new_pos[1]] = EMPTY
            self.pacman = new_pos

    def is_valid_move(self, position):
        return (0 <= position[0] < len(self.maze) and
                0 <= position[1] < len(self.maze[0]) and
                self.maze[position[0]][position[1]] != WALL)

    def move_ghosts(self):
        for i, ghost in enumerate(self.ghosts):
            path = self.find_path(ghost, self.pacman)
            if path and len(path) > 1:
                self.ghosts[i] = path[1]

    def find_path(self, start, goal):
        if self.algorithm == 'a_star':
            return self.a_star(start, goal)
        elif self.algorithm == 'dijkstra':
            return self.dijkstra(start, goal)

    def a_star(self, start, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == goal:
                return self.reconstruct_path(came_from, current)

            for direction in DIRECTIONS:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if self.is_valid_move(neighbor):
                    tentative_g_score = g_score[current] + 1
                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def dijkstra(self, start, goal):
        queue = deque([(0, start)])
        came_from = {}
        cost_so_far = {start: 0}

        while queue:
            current_cost, current = queue.popleft()
            if current == goal:
                return self.reconstruct_path(came_from, current)

            for direction in DIRECTIONS:
                next_node = (current[0] + direction[0], current[1] + direction[1])
                if self.is_valid_move(next_node):
                    new_cost = current_cost + 1
                    if new_cost < cost_so_far.get(next_node, float('inf')):
                        cost_so_far[next_node] = new_cost
                        queue.append((new_cost, next_node))
                        came_from[next_node] = current

        return None

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

    def game_over_screen(self):
        self.window.fill(BLACK)
        game_over_text = self.font.render('Game Over', True, RED)
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        restart_text = self.font.render('Press R to Restart or Q to Quit', True, WHITE)

        self.window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
        self.window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        self.window.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 3 * HEIGHT // 4))

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "restart"
                    if event.key == pygame.K_q:
                        return "quit"
                    
    def win_screen(self):
        self.window.fill(BLACK)
        win_text = self.font.render('You Win!', True, GREEN)
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        restart_text = self.font.render('Press R to Restart or Q to Quit', True, WHITE)

        self.window.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 4))
        self.window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        self.window.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 3 * HEIGHT // 4))

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "restart"
                    if event.key == pygame.K_q:
                        return "quit"

    def check_win_condition(self):
        for row in self.maze:
            if FOOD in row:
                return False
        return True

    def run(self):
        running = True
        while running:
            self.clock.tick(5)  # Adjust game speed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_pacman((-1, 0))
                    elif event.key == pygame.K_DOWN:
                        self.move_pacman((1, 0))
                    elif event.key == pygame.K_LEFT:
                        self.move_pacman((0, -1))
                    elif event.key == pygame.K_RIGHT:
                        self.move_pacman((0, 1))
                    elif event.key == pygame.K_a:
                        self.algorithm = 'a_star'
                    elif event.key == pygame.K_d:
                        self.algorithm = 'dijkstra'

            self.move_ghosts()

            if self.pacman in self.ghosts:
                result = self.game_over_screen()
                if result == "restart":
                    self.reset_game()
                else:
                    running = False
                continue

            if self.check_win_condition():
                result = self.win_screen()
                if result == "restart":
                    self.reset_game()
                else:
                    running = False
                continue

            self.window.fill(BLACK)
            self.draw_grid()
            self.draw_entities()
            self.draw_text(f'Score: {self.score}', (10, 10))
            self.draw_text(f'Algorithm: {self.algorithm.capitalize()}', (10, 50))

            pygame.display.update()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PacmanGame()
    game.run()
