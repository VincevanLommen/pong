import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.font.init()  # Initialize the font module

font = pygame.font.Font(None, 36)


# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Difficulty Selection")

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
button_width = 200
button_height = 50
spacing = 20
start_y = WINDOW_HEIGHT // 2 - (3 * button_height + 2 * spacing) // 2

easy_button = Button(WINDOW_WIDTH//2 - button_width//2, start_y, 
                    button_width, button_height, "Easy", GREEN)
medium_button = Button(WINDOW_WIDTH//2 - button_width//2, start_y + button_height + spacing,
                      button_width, button_height, "Medium", ORANGE)
hard_button = Button(WINDOW_WIDTH//2 - button_width//2, start_y + 2 * (button_height + spacing),
                    button_width, button_height, "Hard", RED)

running = True
level = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if easy_button.is_clicked(event.pos):
                level = "easy"
                running = False
            elif medium_button.is_clicked(event.pos):
                level = "medium"
                running = False
            elif hard_button.is_clicked(event.pos):
                level = "hard"
                running = False

    # Draw everything
    screen.fill(WHITE)
    
    # Draw title
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Select Difficulty", True, BLACK)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4))
    screen.blit(title_text, title_rect)
    
    # Draw buttons
    easy_button.draw(screen)
    medium_button.draw(screen)
    hard_button.draw(screen)
    
    pygame.display.flip()

pygame.quit()

# Ask for the username
input_active = True
user_name = ""
input_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, start_y + 3 * (button_height + spacing), 200, 50)
font = pygame.font.Font(None, 36)

while input_active:
    screen.fill(WHITE)
    
    # Draw input box
    pygame.draw.rect(screen, ORANGE, input_rect, 2)
    input_surface = font.render(user_name, True, BLACK)
    screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            input_active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                input_active = False  # Confirm input
                print(f"Hello {user_name}, you selected {level} difficulty!")
            elif event.key == pygame.K_BACKSPACE:
                user_name = user_name[:-1]  # Remove last character
            else:
                user_name += event.unicode  # Add typed character

    pygame.display.flip()