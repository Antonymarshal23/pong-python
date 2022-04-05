import pygame
import os

# initiation the pygame
pygame.init()

pygame.mixer.init()
# for window
WIDTH, HEIGHT = 700, 500
# create a window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pong")
SURFACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'yellow.jpg')), (WIDTH, HEIGHT))

PADDLE_SOUND = pygame.mixer.Sound('Assets/ball.wav')
LOSING_SOUND = pygame.mixer.Sound('Assets/losing_sound.wav')
WINNER_SOUND = pygame.mixer.Sound('Assets/winning_sound.wav')


FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# create paddle height and width
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

# radius for ball
BALL_RADIUS = 7

# for score font
SCORE_FONT = pygame.font.SysFont("comics", 50)

# for winner
WINNING_SCORE = 10


class Paddle:
    COLOR = BLACK
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 6
    COLOR = BLACK

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        # start opponent side if you get lose
        self.x_vel *= -1
        LOSING_SOUND.play()


def draw(win, paddles, ball, left_score, right_score):
    # for surface color
    WIN.blit(SURFACE, (0, 0))
    # for score text
    left_score_text = SCORE_FONT.render(f"{left_score}", True, BLACK)
    right_score_text = SCORE_FONT.render(f"{right_score}", True, BLACK)
    # draw
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3 / 4) -
                                right_score_text.get_width() // 2, 20))

    # for paddle creation
    for paddle in paddles:
        paddle.draw(win)

    # for line in the middle
    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        # pygame.draw.rect(surface, color, (put it on center = WIDTH // 2 - 5
        # , make a gap for middle line = i, width = 10, height = HEIGHT // 20))
        pygame.draw.rect(win, BLACK, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))
    ball.draw(win)

    # update the display
    pygame.display.update()


# for ball handle_collision
def handle_collision(ball, left_paddle, right_paddle):
    # for ceiling of a screen
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # for left paddle
    # if the x vel is negative it  will move left
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y:
            if ball.y <= left_paddle.y + left_paddle.height:
                if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                    ball.x_vel *= -1
                    # for y direction
                    middle_y = left_paddle.y + left_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                    # find the mv of y
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    PADDLE_SOUND.play()

    else:
        # # change y direction for left_paddle
        if ball.y >= right_paddle.y:
            if ball.y <= right_paddle.y + right_paddle.height:
                if ball.x + ball.radius >= right_paddle.x:
                    ball.x_vel *= -1

                    # change y direction for right_paddle
                    middle_y = right_paddle.y + right_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    PADDLE_SOUND.play()


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def main():
    run = True
    clock = pygame.time.Clock()
    # left_paddle = Paddle(x, y, WIDTH, HEIGHT)
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT //
                         2, PADDLE_WIDTH, PADDLE_HEIGHT)
    # right_paddle = Paddle(x, y, WIDTH, HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                          2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    paddles = [left_paddle, right_paddle]
    # ball = Ball(x, y, radius)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, paddles, ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        # for score
        if ball.x < 0:
            right_score += 1
            LOSING_SOUND.play()
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            LOSING_SOUND.play()
            ball.reset()
        # for winner_score
        win_text = ""
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "left player won"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "right player won"

        if won:
            text = SCORE_FONT.render(win_text, True, BLACK)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            WINNER_SOUND.play()
            pygame.display.update()
            pygame.time.delay(9800)
            ball.reset()
            WINNER_SOUND.stop()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


# call the main function
if __name__ == '__main__':
    main()
