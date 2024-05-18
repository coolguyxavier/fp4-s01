# - FP4-S01 OOP Program - #
# - Xzavier Moosomin - #
# - 05/18/2024 - #

# - Imports - #
import pygame
import sys

# - Pygame Initialization - #
pygame.init()

# - Constants - #
width, height = 800, 600
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
paddle_width, paddle_height = 20, 100
ball_size = 20
paddle_speed = 7
ball_speed_x, ball_speed_y = 5, 5

# - Game Settings - #
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Ping Pong Game')

clock = pygame.time.Clock()

# - Scoring - #
score_font = pygame.font.Font(None, 74)
player1_score = 0
player2_score = 0

# - Classes - #
class Paddle:
    def __init__(self, x, y, color=white):
        self.rect = pygame.Rect(x, y, paddle_width, paddle_height)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= paddle_speed
        elif not up and self.rect.bottom < height:
            self.rect.y += paddle_speed

class Player1(Paddle):
    def __init__(self, x, y):
        super().__init__(x, y, green)

class Player2(Paddle):
    def __init__(self, x, y):
        super().__init__(x, y, blue)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ball_size, ball_size)
        self.speed_x = ball_speed_x
        self.speed_y = ball_speed_y

    def draw(self):
        pygame.draw.ellipse(screen, white, self.rect)  # creates ball

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.speed_y *= -1

        # if it collides with a paddle, it bounces
        if self.rect.colliderect(left_paddle.rect) or self.rect.colliderect(right_paddle.rect):
            self.speed_x *= -1

        # if it somehow goes off screen, it resets and updates score
        if self.rect.left <= 0:
            self.reset()
            return 'Player2'
        elif self.rect.right >= width:
            self.reset()
            return 'Player1'
        return None

    def reset(self):
        self.rect.center = (width // 2, height // 2)
        self.speed_x *= -1  # Change ball direction

# - Creates the Objects - #
left_paddle = Player1(30, height // 2 - paddle_height // 2)
right_paddle = Player2(width - 50, height // 2 - paddle_height // 2)
ball = Ball(width // 2, height // 2)

# - Main Code - #
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        left_paddle.move(up=True)
    if keys[pygame.K_s]:
        left_paddle.move(up=False)
    if keys[pygame.K_UP]:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN]:
        right_paddle.move(up=False)

    # Move ball and check for scoring
    scorer = ball.move()
    if scorer == 'Player1':
        player1_score += 1
    elif scorer == 'Player2':
        player2_score += 1

    # Draw everything
    screen.fill(black)
    left_paddle.draw()
    right_paddle.draw()
    ball.draw()

    # Display scores
    player1_text = score_font.render(str(player1_score), True, white)
    player2_text = score_font.render(str(player2_score), True, white)
    screen.blit(player1_text, (width // 4, 20))
    screen.blit(player2_text, (3 * width // 4, 20))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
