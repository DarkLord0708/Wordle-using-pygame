import pygame
import sys
import subprocess  # Import subprocess to execute other scripts

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WORDLE!")

# Define colors
bg_color = 0x121212
WHITE = (255, 255, 255)
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
# OUTLINE = 0x595959
OUTLINE = 0x191919
FILLED_OUTLINE = "#878a8c"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
HOVER_COLOR = (0, 200, 255)

# Font settings
font = pygame.font.SysFont("Arial", 60)
button_font = pygame.font.SysFont("Arial", 40)

# Button class
class Button:
    def __init__(self, text, x, y, width, height, color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = button_font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.centerx - text_surface.get_width() // 2, 
                                  self.rect.centery - text_surface.get_height() // 2))

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Create number buttons for state 2
numbers = [1,3,5,6,10]
buttons = []
button_width, button_height = 100, 60
start_y = HEIGHT // 3

for i, number in enumerate(numbers):
    x = WIDTH // 2 - button_width // 2
    y = start_y + i * (button_height + 10)
    button = Button(str(number), x, y, button_width, button_height, BLUE)
    buttons.append(button)

# State variable to track the current state
state = 1  # 1 = main menu, 2 = number selection
selected_number = None

# Main loop
running = True
fade_alpha = 0  # Alpha value for fade effect
fade_direction = 0  # 1 for fade-in, -1 for fade-out

while running:
    screen.fill(bg_color)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == 1:  # Main Menu state
                # If "Start Game" is clicked, transition to state 2
                start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)
                if start_button_rect.collidepoint(event.pos):
                    # Fade out effect
                    fade_direction = -1  # Start fading out
            elif state == 2:  # Number Selection state
                for button in buttons:
                    if button.is_hovered(event.pos):
                        selected_number = button.text
                        # print(f"Starting game with number {selected_number}")
                        running = False  # Exit the startup screen and start the game

    # Handle the fade effect
    if fade_direction == -1:  # Fade out
        fade_alpha += 5
        if fade_alpha >= 255:
            fade_alpha = 255
            state = 2  # Change state after fade out completes
            fade_direction = 1  # Start fade-in
    elif fade_direction == 1:  # Fade in
        fade_alpha -= 5
        if fade_alpha <= 0:
            fade_alpha = 0
            fade_direction = 0  # End fade-in

    # Draw the transition effect (a black surface with varying alpha)
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BLACK)
    fade_surface.set_alpha(fade_alpha)
    screen.blit(fade_surface, (0, 0))

    # State 1: Main Menu
    if state == 1:
        title_text = font.render("WELCOME TO WORDLE!", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # Start Game button
        start_button = Button("Start", WIDTH // 2 - 100, HEIGHT // 2, 200, 60, BLUE)
        if start_button.is_hovered(pygame.mouse.get_pos()):
            start_button.color = HOVER_COLOR
        else:
            start_button.color = BLUE
        start_button.draw(screen)

    # State 2: Number Selection
    elif state == 2:
        title_text = font.render("Choose the size of your word", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # Number buttons
        for button in buttons:
            if button.is_hovered(pygame.mouse.get_pos()):
                button.color = HOVER_COLOR
            else:
                button.color = BLUE
            button.draw(screen)

    # Update display
    pygame.display.update()

# Quit the startup window (close the Pygame window)
pygame.quit()

# Execute the game script based on selected number
if selected_number:
    subprocess.run(["python", "gametry3.py", selected_number])  # Run the game script

sys.exit()  # Exit the program
