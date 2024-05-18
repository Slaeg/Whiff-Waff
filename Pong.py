import pgzrun

# Game constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 10
PADDLE_SPEED = 5
BALL_SPEED_X = 4
BALL_SPEED_Y = 4
PLAYER1_SCORE = 0
PLAYER2_SCORE = 0

# Game objects
paddle1 = Rect((30, HEIGHT // 2 - PADDLE_HEIGHT // 2), (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle2 = Rect((WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2), (PADDLE_WIDTH, PADDLE_HEIGHT))
ball = Rect((WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2), (BALL_SIZE, BALL_SIZE))
ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

def draw():
    screen.clear()
    screen.draw.rect(paddle1, 'white')
    screen.draw.rect(paddle2, 'white')
    screen.draw.filled_rect(ball, 'white')
    screen.draw.text(str(PLAYER1_SCORE), (WIDTH // 4, 20), fontsize=50)
    screen.draw.text(str(PLAYER2_SCORE), (WIDTH * 3 // 4, 20), fontsize=50)

def update():
    global PLAYER1_SCORE, PLAYER2_SCORE

    # Player 1 movement
    if keyboard.w and paddle1.top > 0:
        paddle1.y -= PADDLE_SPEED
    if keyboard.s and paddle1.bottom < HEIGHT:
        paddle1.y += PADDLE_SPEED

    # Player 2 movement
    if keyboard.up and paddle2.top > 0:
        paddle2.y -= PADDLE_SPEED
    if keyboard.down and paddle2.bottom < HEIGHT:
        paddle2.y += PADDLE_SPEED

    # Ball movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with paddles
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed[0] = -ball_speed[0]

    # Ball goes out of bounds
    if ball.left <= 0:
        PLAYER2_SCORE += 1
        reset_ball()
    if ball.right >= WIDTH:
        PLAYER1_SCORE += 1
        reset_ball()

def reset_ball():
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    ball_speed[0] *= -1

pgzrun.go()
