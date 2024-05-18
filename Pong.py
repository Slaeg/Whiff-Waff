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
MAX_BOUNCE_ANGLE = 45  # Max bounce angle in degrees

# Game states
TITLE_SCREEN = 0
GAME_PLAY = 1
game_state = TITLE_SCREEN
single_player = False

# Game objects
paddle1 = Rect((30, HEIGHT // 2 - PADDLE_HEIGHT // 2), (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle2 = Rect((WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2), (PADDLE_WIDTH, PADDLE_HEIGHT))
ball = Rect((WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2), (BALL_SIZE, BALL_SIZE))
ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

def draw():
    screen.clear()
    if game_state == TITLE_SCREEN:
        draw_title_screen()
    elif game_state == GAME_PLAY:
        draw_game_play()

def draw_title_screen():
    screen.draw.text("Pong Game", center=(WIDTH // 2, HEIGHT // 3), fontsize=60, color="white")
    screen.draw.text("Press 1 for 1 Player", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")
    screen.draw.text("Press 2 for 2 Players", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=40, color="white")

def draw_game_play():
    screen.draw.rect(paddle1, 'white')
    screen.draw.rect(paddle2, 'white')
    screen.draw.filled_rect(ball, 'white')
    screen.draw.text(str(PLAYER1_SCORE), (WIDTH // 4, 20), fontsize=50)
    screen.draw.text(str(PLAYER2_SCORE), (WIDTH * 3 // 4, 20), fontsize=50)

def update():
    if game_state == GAME_PLAY:
        update_game_play()

def update_game_play():
    global PLAYER1_SCORE, PLAYER2_SCORE

    # Player 1 movement
    if keyboard.w and paddle1.top > 0:
        paddle1.y -= PADDLE_SPEED
    if keyboard.s and paddle1.bottom < HEIGHT:
        paddle1.y += PADDLE_SPEED

    # Player 2 movement
    if not single_player:
        if keyboard.up and paddle2.top > 0:
            paddle2.y -= PADDLE_SPEED
        if keyboard.down and paddle2.bottom < HEIGHT:
            paddle2.y += PADDLE_SPEED
    else:
        # AI opponent movement
        ai_move()

    # Ball movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with paddles
    if ball.colliderect(paddle1):
        bounce_ball(paddle1)
    if ball.colliderect(paddle2):
        bounce_ball(paddle2)

    # Ball goes out of bounds
    if ball.left <= 0:
        PLAYER2_SCORE += 1
        reset_ball()
    if ball.right >= WIDTH:
        PLAYER1_SCORE += 1
        reset_ball()

def ai_move():
    # Calculate the distance from the ball to the AI paddle
    distance = ball.x - paddle2.x

    # If the ball is far, keep the paddle in the center
    if distance > WIDTH // 2:
        target_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    else:
        # If the ball is closer, move towards the ball
        target_y = ball.centery - PADDLE_HEIGHT // 2

    # Move the paddle towards the target position
    if paddle2.centery < target_y:
        paddle2.y += PADDLE_SPEED
    elif paddle2.centery > target_y:
        paddle2.y -= PADDLE_SPEED

    # Prevent the AI paddle from going out of bounds
    if paddle2.top < 0:
        paddle2.top = 0
    if paddle2.bottom > HEIGHT:
        paddle2.bottom = HEIGHT

def bounce_ball(paddle):
    offset = (ball.centery - paddle.centery) / (PADDLE_HEIGHT / 2)
    bounce_angle = offset * MAX_BOUNCE_ANGLE
    ball_speed[0] = -ball_speed[0]  # Reverse horizontal direction
    ball_speed[1] = BALL_SPEED_X * offset  # Adjust vertical direction

def reset_ball():
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    ball_speed[0] = BALL_SPEED_X if ball_speed[0] < 0 else -BALL_SPEED_X
    ball_speed[1] = BALL_SPEED_Y

def on_key_down(key):
    global game_state, single_player
    if game_state == TITLE_SCREEN:
        if key == keys.K_1:
            single_player = True
            start_game()
        elif key == keys.K_2:
            single_player = False
            start_game()

def start_game():
    global game_state, PLAYER1_SCORE, PLAYER2_SCORE
    game_state = GAME_PLAY
    PLAYER1_SCORE = 0
    PLAYER2_SCORE = 0
    reset_ball()

pgzrun.go()
