import pygame
from sys import exit
from random import choice
from words import game_words
import sys

# # Get the selected number passed from the startup screen
# selected_number = sys.argv[1]  # This will get the number selected in the startup screen

# if(selected_number==1):
#     pass
# elif(selected_number==3):
#     pass
# elif(selected_number==5):
#     pass
# elif(selected_number==6):
#     pass
# elif(selected_number==10):
#     pass




pygame.init()
ATTEMPTS = 6
game_active = True
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WORDLE!")
clock = pygame.time.Clock()

icon = pygame.image.load("assets/letter-w.png")
pygame.display.set_icon(icon)

# making the grid
GRID_SIZE = (5, 6)  # 5 letters, 6 attempts
CELL_SIZE = 60
MARGIN = 10
bg_color = 0x121212
WHITE = (255, 255, 255)
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
# OUTLINE = 0x595959
OUTLINE = 0x191919
FILLED_OUTLINE = "#878a8c"
FONT = pygame.font.Font("assets/FreeSansBold.otf", 33)

# Calculate grid dimensions
grid_width = GRID_SIZE[0] * (CELL_SIZE + MARGIN) - MARGIN
grid_height = GRID_SIZE[1] * (CELL_SIZE + MARGIN) - MARGIN

# Center the grid
start_x = (WIDTH - grid_width) // 2
start_y = 130

# Select a random word from the list
l = game_words
curr_word = choice(l).upper()  # Convert to uppercase as input will be in uppercase
print(curr_word)

grid = [["" for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
current_row = 0
current_col = 0

# Function to evaluate guess and provide feedback
def evaluate_guess(guess):
    word_dict = {letter: curr_word.count(letter) for letter in set(curr_word)}
    reply = [0] * 5  # 0 = gray, 1 = yellow, 2 = green
    
    # First pass: Check for green (correct letter, correct position)
    for i in range(len(guess)):
        if guess[i] == curr_word[i] and word_dict[guess[i]] > 0:
            reply[i] = 2  # Green
            # LETTER_STATE[guess[i]] = "green"
            word_dict[guess[i]] -= 1

    # Second pass: Check for yellow (correct letter, wrong position)
    for i in range(len(guess)):
        if guess[i] != curr_word[i] and guess[i] in curr_word and word_dict[guess[i]] > 0:
            if reply[i] == 0:  # Only color it yellow if it hasn't been colored green already
                reply[i] = 1  # Yellow
                # LETTER_STATE[guess[i]] = "yellow"
                word_dict[guess[i]] -= 1

    return reply

def draw_play_again_button():
    # Define button properties
    button_width = 200
    button_height = 50
    button_x = (WIDTH - button_width) // 2
    button_y = HEIGHT - 75
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    button_color = 0x758BFD
    # button_color = 0xBEB2C8
    button_text = FONT.render("Play Again", True, WHITE,None)
    button_text_rect = button_text.get_rect(center=button_rect.center)

    # Draw the button
    pygame.draw.rect(screen, button_color, button_rect,border_radius=15)
    screen.blit(button_text, button_text_rect)
    
    return button_rect

def display_result(message, word):
    result_font = pygame.font.Font("assets/Slabo27px-Regular.ttf", 50)  # Larger font for emphasis
    word_font = pygame.font.Font("assets/Slabo27px-Regular.ttf", 30)  # Smaller font for the correct word
    
    # Render "You Win!" or "You Lose!"
    result_text = result_font.render(message, True, WHITE,None)
    result_text_rect = result_text.get_rect(center=(WIDTH // 2, 50))  # Positioned at the top
    
    # Render the correct word
    word_text = word_font.render(f"The word was: {word}", True, WHITE,None)
    word_text_rect = word_text.get_rect(center=(WIDTH // 2, 100))  # Below the result text
    
    # Blit (draw) the text onto the screen
    screen.blit(result_text, result_text_rect)
    screen.blit(word_text, word_text_rect)


def reset_game():
    global grid, current_row, current_col, feedback, ATTEMPTS, curr_word
    grid = [["" for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
    feedback = [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
    current_row = 0
    current_col = 0
    ATTEMPTS = 6
    curr_word = choice(game_words).upper()  # Get a new word
    LETTER_STATE = {chr(i).upper(): "default" for i in range(pygame.K_a, pygame.K_z + 1)}
    print(curr_word)

# Function to draw grid and display feedback
def draw_grid():
    screen.fill(bg_color)
    for row in range(GRID_SIZE[1]):
        for col in range(GRID_SIZE[0]):
            x = start_x + col * (CELL_SIZE + MARGIN)
            y = start_y + row * (CELL_SIZE + MARGIN)
            
            # Determine the color based on feedback
            if grid[row][col] == "":
                rect_color = OUTLINE  # Default border color
            else:
                if feedback[row][col] == 2:  # Green
                    rect_color = GREEN
                elif feedback[row][col] == 1:  # Yellow
                    rect_color = YELLOW
                else:  # Gray
                    rect_color = GREY
            
            pygame.draw.rect(screen, rect_color, (x, y, CELL_SIZE, CELL_SIZE))
            if grid[row][col]:
                text = FONT.render(grid[row][col], True, WHITE,None)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)

    pygame.display.flip()

def is_valid_word(word):
    # You can replace 'game_words' with the actual list of valid words you have
    return word.lower() in game_words


# # drawing keyboard
# # Puts the indicator and its text on the screen at the desired position.
# # Alphabet
# ALPHABET = [
#     "QWERTYUIOP",   # Row 1
#     "ASDFGHJKL",    # Row 2
#     "ZXCVBNM"       # Row 3
# ]

# # Keyboard layout
# class Indicator:
#     def __init__(self, x, y, letter):
#         self.x = x
#         self.y = y
#         self.letter = letter
#         self.bg_color = OUTLINE  # Default background color
#         self.text = letter
#         self.rect = pygame.Rect(self.x, self.y, 50, 50)  # Size of the key

#     def update_state(self, state):
#         if state == "gray":
#             self.bg_color = GREY
#         elif state == "yellow":
#             self.bg_color = YELLOW
#         elif state == "green":
#             self.bg_color = GREEN

#     def draw(self):
#         pygame.draw.rect(screen, self.bg_color, self.rect)
#         self.text_surface = FONT.render(self.text, True, "white")
#         self.text_rect = self.text_surface.get_rect(center=(self.x+25, self.y+25))
#         screen.blit(self.text_surface, self.text_rect)

# # Create the list of indicators (keys)
# indicators = []
# indicator_x, indicator_y = 20, 600

# # Populate the indicator list with the keyboard layout
# for i in range(3):
#     for letter in ALPHABET[i]:
#         new_indicator = Indicator(indicator_x, indicator_y, letter)
#         indicators.append(new_indicator)
#         indicator_x += 60
#     indicator_y += 100
#     if i == 0:
#         indicator_x = 50
#     elif i == 1:
#         indicator_x = 105

# KEYBOARD_LAYOUT = [
#     "QWERTYUIOP",
#     "ASDFGHJKL",
#     "ZXCVBNM"
# ]

# # LETTER_STATE = {chr(i): "default" for i in range(pygame.K_a, pygame.K_z + 1)}
# LETTER_STATE = {chr(i).upper(): "default" for i in range(pygame.K_a, pygame.K_z + 1)}


# KEY_SIZE = 50
# KEY_MARGIN = 5
# KEYBOARD_START_Y = HEIGHT - 300  # Position of the keyboard

# def draw_keyboard():
#     keyboard_x = (WIDTH - (10 * (KEY_SIZE + KEY_MARGIN))) // 2  # Centering keyboard

#     for row_idx, row in enumerate(KEYBOARD_LAYOUT):
#         row_y = KEYBOARD_START_Y + row_idx * (KEY_SIZE + KEY_MARGIN)
#         row_x = keyboard_x + (KEY_SIZE // 2 if row_idx == 2 else 0)  # Shift last row

#         for letter in row:
#             letter_color = OUTLINE  # Default color
#             if LETTER_STATE[letter] == "gray":
#                 letter_color = GREY
#             elif LETTER_STATE[letter] == "yellow":
#                 letter_color = YELLOW
#             elif LETTER_STATE[letter] == "green":
#                 letter_color = GREEN

#             key_rect = pygame.Rect(row_x, row_y, KEY_SIZE, KEY_SIZE)
#             pygame.draw.rect(screen, letter_color, key_rect, border_radius=8)

#             text = FONT.render(letter, True, WHITE)
#             text_rect = text.get_rect(center=key_rect.center)
#             screen.blit(text, text_rect)

#             row_x += KEY_SIZE + KEY_MARGIN  # Move to next key





# Initialize feedback list (to store feedback for each guess)
feedback = [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]

# Main game loop
running = True
while running:
    if(game_active):
        draw_grid()
        # draw_keyboard()
    else:
        display_result("You Lose!" if ATTEMPTS == 0 else "You Win!", curr_word)
        button_rect = draw_play_again_button()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Submit word
                if current_col == 5:  # Full word entered
                    # if() //verify word in the wordlist here
                    guess = "".join(grid[current_row])  # Convert list to string
                    if not is_valid_word(guess):
                        # Display a message indicating the word is not in the word list
                        invalid_word_font = pygame.font.Font("assets/Slabo27px-Regular.ttf", 30)
                        invalid_word_text = invalid_word_font.render("Word not in word list!", True, WHITE)
                        invalid_word_text_rect = invalid_word_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        screen.blit(invalid_word_text, invalid_word_text_rect)
                        pygame.display.update()
                        pygame.time.wait(1000)  # Wait for a second before clearing the message
                        continue  # Skip the rest of the logic for this guess

                    ATTEMPTS-=1
                    if(ATTEMPTS==0):
                        game_active=False
                    
                    feedback[current_row] = evaluate_guess(guess)  # Get feedback
                    current_row += 1
                    current_col = 0
                    if feedback[current_row - 1] == [2] * 5:  # All green means win
                        print("You Win!")
                        draw_grid()
                        # draw_keyboard()
                        game_active = False
                        # running = False
            elif event.key == pygame.K_BACKSPACE:  # Delete letter
                if current_col > 0:
                    current_col -= 1
                    grid[current_row][current_col] = ""
                    # draw_grid()
                    # draw_keyboard()
            elif pygame.K_a <= event.key <= pygame.K_z:  # Add letter
                if current_col < 5:
                    grid[current_row][current_col] = chr(event.key).upper()
                    current_col += 1
                    # draw_grid()
                    # draw_keyboard()
            
        if event.type == pygame.MOUSEBUTTONDOWN and not game_active:
            if button_rect.collidepoint(event.pos):
                reset_game()
                game_active = True
                # draw_grid()
                # draw_keyboard()
            
        # pygame.quit()
        # exit()
    pygame.display.update()
    clock.tick(60)

# pygame.quit()
