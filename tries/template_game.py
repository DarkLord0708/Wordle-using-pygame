import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 600
GRID_SIZE = (5, 6)  # 5 letters, 6 attempts
CELL_SIZE = 80
MARGIN = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
FONT = pygame.font.Font(None, 50)
bg_color = 0x121212

# Calculate grid dimensions
grid_width = GRID_SIZE[0] * (CELL_SIZE + MARGIN) - MARGIN
grid_height = GRID_SIZE[1] * (CELL_SIZE + MARGIN) - MARGIN

# Center the grid
start_x = (WIDTH - grid_width) // 2
start_y = (HEIGHT - grid_height) // 2

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle Clone")

# Game variables
grid = [["" for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
current_row = 0
current_col = 0

def draw_grid():
    screen.fill(bg_color)
    for row in range(GRID_SIZE[1]):
        for col in range(GRID_SIZE[0]):
            x = start_x + col * (CELL_SIZE + MARGIN)
            y = start_y + row * (CELL_SIZE + MARGIN)
            rect_color = BLACK if grid[row][col] == "" else GRAY  # Default color
            pygame.draw.rect(screen, rect_color, (x, y, CELL_SIZE, CELL_SIZE), 2)
            if grid[row][col]:
                text = FONT.render(grid[row][col], True, WHITE)
                screen.blit(text, (x + CELL_SIZE // 3, y + CELL_SIZE // 4))
    pygame.display.flip()

running = True
while running:
    draw_grid()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Submit word
                if current_col == 5:  # Full word entered
                    current_row += 1
                    current_col = 0
            elif event.key == pygame.K_BACKSPACE:  # Delete letter
                if current_col > 0:
                    current_col -= 1
                    grid[current_row][current_col] = ""
            elif pygame.K_a <= event.key <= pygame.K_z:  # Add letter
                if current_col < 5:
                    grid[current_row][current_col] = chr(event.key).upper()
                    current_col += 1

pygame.quit()
