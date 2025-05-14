import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 36)

WINDOW_SIZE = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BORDER_THICKNESS = 10


ball_radius = 10
ball_speed = 1
ball_dx = ball_speed
ball_dy = ball_speed

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
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

# Ask for difficulty level
button_width = 200
button_height = 50
spacing = 20
start_y = WINDOW_SIZE // 2 - (3 * button_height + 2 * spacing) // 2

easy_button = Button(WINDOW_SIZE//2 - button_width//2, start_y, button_width, button_height, "Easy", GREEN)
medium_button = Button(WINDOW_SIZE//2 - button_width//2, start_y + button_height + spacing, button_width, button_height, "Medium", ORANGE)
hard_button = Button(WINDOW_SIZE//2 - button_width//2, start_y + 2 * (button_height + spacing), button_width, button_height, "Hard", RED)

running = True
level = None
theme_color = WHITE 

#ASK LEVEL
while running:
    screen.fill(WHITE)
    
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Select Difficulty", True, BLACK)
    title_rect = title_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//5))
    screen.blit(title_text, title_rect)
    
    # Draw buttons
    easy_button.draw(screen)
    medium_button.draw(screen)
    hard_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if easy_button.is_clicked(event.pos):
                level = "Easy"
                theme_color = GREEN
                running = False
            elif medium_button.is_clicked(event.pos):
                level = "Medium"
                theme_color = ORANGE
                running = False
            elif hard_button.is_clicked(event.pos):
                level = "Hard"
                theme_color = RED
                running = False

    pygame.display.flip()

# ASK USERNAME
if level:
    input_active = True
    user_name = ""
    input_rect = pygame.Rect(WINDOW_SIZE//2 - 100, start_y + 3 * (button_height + spacing), 200, 50)

    while input_active:
        screen.fill(WHITE) 

        pygame.draw.rect(screen, theme_color, input_rect, 2)
        input_surface = font.render(user_name, True, BLACK)
        screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 10))

        prompt_surface = font.render("Enter your name and press ENTER:", True, BLACK)
        prompt_rect = prompt_surface.get_rect(center=(WINDOW_SIZE//2, start_y - 50))
        screen.blit(prompt_surface, prompt_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input_active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False  # Stop asking for input
                elif event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]  # Remove last character
                else:
                    user_name += event.unicode  # Add typed character

        pygame.display.flip()


field_x = 0
field_y = 0

x_min = BORDER_THICKNESS + ball_radius
x_max = WINDOW_SIZE - ball_radius
y_min = BORDER_THICKNESS + ball_radius
y_max = WINDOW_SIZE - BORDER_THICKNESS - ball_radius

ball_x = random.randint(x_min, x_max)
ball_y = random.randint(y_min, y_max)

#CREATE FIELD
running = True
while running:
    screen.fill(WHITE)

    pygame.draw.rect(screen, theme_color, (field_x, field_y, WINDOW_SIZE, BORDER_THICKNESS))  # Top
    pygame.draw.rect(screen, theme_color, (field_x, field_y + WINDOW_SIZE - BORDER_THICKNESS, WINDOW_SIZE, BORDER_THICKNESS))  # Bottom
    pygame.draw.rect(screen, theme_color, (field_x, field_y, BORDER_THICKNESS, WINDOW_SIZE))  # Left

    pygame.draw.rect(screen, BLACK, (field_x + BORDER_THICKNESS, field_y + BORDER_THICKNESS, 
                                     WINDOW_SIZE - BORDER_THICKNESS, WINDOW_SIZE - 2 * BORDER_THICKNESS), 2)


    ball_x += ball_dx
    ball_y += ball_dy

    if ball_x - ball_radius <= BORDER_THICKNESS:
        ball_dx = abs(ball_dx)
    if ball_x + ball_radius >= WINDOW_SIZE:
        ball_dx = -abs(ball_dx)
    if ball_y - ball_radius <= BORDER_THICKNESS:
        ball_dy = abs(ball_dy)
    if ball_y + ball_radius >= WINDOW_SIZE - BORDER_THICKNESS:
        ball_dy = -abs(ball_dy)

    pygame.draw.circle(screen, theme_color, (ball_x, ball_y), ball_radius)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()