import pygame
import sys
import random
import math

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

ball_radius = 4        # Diameter is 8
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


restart = True
while restart:

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
                restart = False
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
    
    if not restart:
        break

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
                    restart = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False  # Stop asking for input
                    elif event.key == pygame.K_BACKSPACE:
                        user_name = user_name[:-1]  # Remove last character
                    else:
                        user_name += event.unicode  # Add typed character

            pygame.display.flip()
        
        if not restart:
            break

    field_x = 0
    field_y = 0

    x_min = BORDER_THICKNESS + ball_radius
    x_max = WINDOW_SIZE - ball_radius
    y_min = BORDER_THICKNESS + ball_radius
    y_max = WINDOW_SIZE - BORDER_THICKNESS - ball_radius

    ball_x = random.randint(x_min, x_max)
    ball_y = random.randint(y_min, y_max)
    
    #ball speed
    if level == "Easy":
        ball_speed = 1
    elif level == "Medium":
        ball_speed = 1.5
    elif level == "Hard":
        ball_speed = 2

 # bal plaatsen
    ball_x = BORDER_THICKNESS + ball_radius
    ball_y = random.randint(y_min, y_max)
    random_angle_deg = random.uniform(-45, 45)
    random_angle_rad = math.radians(random_angle_deg)
    ball_dx = ball_speed * math.cos(random_angle_rad)
    ball_dy = ball_speed * math.sin(random_angle_rad)

    if ball_dx < 0:
        ball_dx = -ball_dx

    #GROOTTE PADDLE
    if level == "Easy":
        paddle_height = 70
    elif level == "Medium":
        paddle_height = 50
    elif level == "Hard":
        paddle_height = 40
    paddle_width = 10
    paddle_x = WINDOW_SIZE - paddle_width
    paddle_y = (WINDOW_SIZE - paddle_height) // 2


    #create lives
    lives = 3
    start_time = pygame.time.get_ticks()

    #CREATE FIELD
    running = True
    while running:
        screen.fill(WHITE)

        pygame.draw.rect(screen, theme_color, (field_x, field_y, WINDOW_SIZE, BORDER_THICKNESS))  # Top
        pygame.draw.rect(screen, theme_color, (field_x, field_y + WINDOW_SIZE - BORDER_THICKNESS, WINDOW_SIZE, BORDER_THICKNESS))  # Bottom
        pygame.draw.rect(screen, theme_color, (field_x, field_y, BORDER_THICKNESS, WINDOW_SIZE))  # Left

        pygame.draw.rect(screen, BLACK, (field_x + BORDER_THICKNESS, field_y + BORDER_THICKNESS, 
                                         WINDOW_SIZE - BORDER_THICKNESS, WINDOW_SIZE - 2 * BORDER_THICKNESS), 2)
    
        lives_text = font.render("Lives: " + str(lives), True, BLACK)
        screen.blit(lives_text, (WINDOW_SIZE - 100, 10))
    
        #Timer
        current_time = (pygame.time.get_ticks() - start_time) / 1000.0
        timer_text = font.render(f"Time: {current_time:.2f} sec", True, BLACK)
        screen.blit(timer_text, (10, 10))

        # Peddel controll
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                restart = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    paddle_y -= 35
                    if paddle_y < 0:
                        paddle_y = 0
                elif event.key == pygame.K_s:
                    paddle_y += 35
                    if paddle_y > WINDOW_SIZE - paddle_height:
                        paddle_y = WINDOW_SIZE - paddle_height

        ball_x += ball_dx
        ball_y += ball_dy

        if ball_x - ball_radius <= BORDER_THICKNESS:
            ball_dx = abs(ball_dx)
        if ball_y - ball_radius <= BORDER_THICKNESS:
            ball_dy = abs(ball_dy)
        if ball_y + ball_radius >= WINDOW_SIZE - BORDER_THICKNESS:
            ball_dy = -abs(ball_dy)
#wiskunde
        if ball_x + ball_radius >= WINDOW_SIZE:
            if ball_y >= paddle_y and ball_y <= paddle_y + paddle_height:
    
                paddle_center = paddle_y + paddle_height / 2.0
                offset = ball_y - paddle_center
                segment = (paddle_height / 2.0) / 5.0
                if abs(offset) < 0.0001:
                    bounce_angle_deg = 0
                elif abs(offset) <= 1 * segment:
                    bounce_angle_deg = 15
                elif abs(offset) <= 2 * segment:
                    bounce_angle_deg = 30
                elif abs(offset) <= 3 * segment:
                    bounce_angle_deg = 45
                elif abs(offset) <= 4 * segment:
                    bounce_angle_deg = 60
                else:
                    bounce_angle_deg = 75
                if offset < 0:
                    bounce_angle_deg = -bounce_angle_deg
                bounce_angle_rad = math.radians(bounce_angle_deg)
                ball_dx = -ball_speed * math.cos(bounce_angle_rad)
                ball_dy = ball_speed * math.sin(bounce_angle_rad)
            else:
                lives -= 1
                if lives <= 0:
                    running = False
                else:
                    ball_x = random.randint(x_min, x_max)
                    ball_y = random.randint(y_min, y_max)
                    random_angle_deg = random.uniform(-75, 75)
                    random_angle_rad = math.radians(random_angle_deg)
                    ball_dx = ball_speed * math.cos(random_angle_rad)
                    ball_dy = ball_speed * math.sin(random_angle_rad)
                    if ball_dx <= 0:
                        ball_dx = abs(ball_dx)

        pygame.draw.circle(screen, theme_color, (int(ball_x), int(ball_y)), ball_radius)
        pygame.draw.rect(screen, theme_color, (paddle_x, int(paddle_y), paddle_width, paddle_height))

        pygame.display.flip()
    
    if not restart:
        break

    #Stop timer
    end_time = pygame.time.get_ticks()
    elapsed_time = (end_time - start_time) / 1000.0

    #File save
    with open("scores.txt", "a") as f:
        f.write(f"{user_name};{level};{elapsed_time}\n")

    scores = []
    try:
        with open("scores.txt", "r") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) == 3:
                    name, lvl, tijd = parts
                    try:
                        tijd = float(tijd)
                        scores.append((name, lvl, tijd))
                    except:
                        pass
    except:
        pass

    scores.sort(key=lambda x: x[2], reverse=True)
    top_scores = scores[:3]

    #AFTER GAME
    game_over = True
    retry_button = Button(WINDOW_SIZE//2 - 60, 300, 120, 50, "Replay", theme_color)
    
    while game_over:
        screen.fill(WHITE)
        game_over_text = font.render("Game Over", True, BLACK)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_SIZE//2, 30))
        screen.blit(game_over_text, game_over_rect)
        
        table_x = 20
        table_y = 60
        table_width = WINDOW_SIZE - 40
        row_height = 30
        table_height = row_height * 4
        
        pygame.draw.rect(screen, BLACK, (table_x, table_y, table_width, table_height), 2)
        for i in range(1, 5):
            pygame.draw.line(screen, BLACK, (table_x, table_y + i * row_height), (table_x + table_width, table_y + i * row_height), 2)
        col_width = table_width // 3
        pygame.draw.line(screen, BLACK, (table_x + col_width, table_y), (table_x + col_width, table_y + table_height), 2)
        pygame.draw.line(screen, BLACK, (table_x + 2 * col_width, table_y), (table_x + 2 * col_width, table_y + table_height), 2)
        
        header_name = font.render("Naam", True, BLACK)
        header_time = font.render("Tijd", True, BLACK)
        header_level = font.render("Level", True, BLACK)
        screen.blit(header_name, (table_x + 10, table_y + 5))
        screen.blit(header_time, (table_x + col_width + 10, table_y + 5))
        screen.blit(header_level, (table_x + 2 * col_width + 10, table_y + 5))
        
        for idx, score in enumerate(top_scores):
            name, lvl, tijd = score
            score_name = font.render(name, True, BLACK)
            score_time = font.render(str(tijd), True, BLACK)
            score_level = font.render(lvl, True, BLACK)
            screen.blit(score_name, (table_x + 10, table_y + (idx+1)*row_height + 5))
            screen.blit(score_time, (table_x + col_width + 10, table_y + (idx+1)*row_height + 5))
            screen.blit(score_level, (table_x + 2 * col_width + 10, table_y + (idx+1)*row_height + 5))
        
        #END INFO
        player_info = font.render(f"Score: {user_name}  {elapsed_time:.2f} sec in {level}", True, BLACK)
        player_info_rect = player_info.get_rect(center=(WINDOW_SIZE//2, table_y + table_height + 20))
        screen.blit(player_info, player_info_rect)
        
        retry_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                restart = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.is_clicked(event.pos):
                    game_over = False
                    
        pygame.display.flip()
        
#stop
pygame.quit()