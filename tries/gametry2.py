import pygame
from sys import exit

pygame.init()
WIDTH, HEIGHT = 800, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WORDLE!")
clock = pygame.time.Clock()

icon = pygame.image.load("assets/letter-w.png")
pygame.display.set_icon(icon)

# making the grid
GRID_SIZE = (5,6)
CELL_SIZE = 60
MARGIN = 10
bg_color = 0x121212
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = 0x595959
FILLED_OUTLINE = "#878a8c"
FONT = pygame.font.Font("assets/FreeSansBold.otf", 33)


# Calculate grid dimensions
grid_width = GRID_SIZE[0] * (CELL_SIZE + MARGIN) - MARGIN
grid_height = GRID_SIZE[1] * (CELL_SIZE + MARGIN) - MARGIN

# Center the grid
start_x = (WIDTH - grid_width) // 2
start_y = 100

grid = [["" for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
current_row = 0
current_col = 0

def draw_grid():
    screen.fill(bg_color)
    for row in range(GRID_SIZE[1]):
        for col in range(GRID_SIZE[0]):
            x = start_x + col * (CELL_SIZE + MARGIN)
            y = start_y + row * (CELL_SIZE + MARGIN)
            rect_color = OUTLINE if grid[row][col] == "" else FILLED_OUTLINE # Default color
            pygame.draw.rect(screen, rect_color, (x, y, CELL_SIZE, CELL_SIZE), 2)
            if grid[row][col]:
                text = FONT.render(grid[row][col], True, WHITE)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                # screen.blit(text, (x + CELL_SIZE // 3, y + CELL_SIZE // 4))
                screen.blit(text,text_rect)
    pygame.display.flip()



running = True
while running:
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            pygame.quit()
            exit()

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



    # draw all elements and update everything
    pygame.display.update()
    clock.tick(60)
