import pgzrun
import random


# Game constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 10
PADDLE_SPEED = 5
AI_PADDLE_SPEED = 3
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
PLAYER1_SCORE = 0
PLAYER2_SCORE = 0
MAX_BOUNCE_ANGLE = 45  # Max bounce angle in degrees

# Game states
TITLE_SCREEN = 0
GAME_PLAY = 1
game_state = TITLE_SCREEN
single_player = False

# Game objects
paddle1 = Rect((30, HEIGHT // 2 - PADDLE_HEIGHT // 2), (PADDLE_WIDTH, PADDLE_HEIGHT))  # type: ignore
paddle2 = Rect((WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2), (PADDLE_WIDTH, PADDLE_HEIGHT))  # type: ignore
ball = Rect((WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2), (BALL_SIZE, BALL_SIZE))  # type: ignore
ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

# AI delay and randomness
AI_REACTION_DELAY = 0.05
AI_RANDOMNESS = 20

def draw():
    screen.clear()  # type: ignore
    if game_state == TITLE_SCREEN:
        draw_title_screen()
    elif game_state == GAME_PLAY:
        draw_game_play()

def draw_title_screen():
    screen.draw.text("Pong Game", center=(WIDTH // 2, HEIGHT // 3), fontsize=60, color="white")  # type: ignore
    screen.draw.text("Press 1 for 1 Player", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")  # type: ignore
    screen.draw.text("Press 2 for 2 Players", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=40, color="white")  # type: ignore

def draw_game_play():
    screen.draw.rect(paddle1, 'white')  # type: ignore
    screen.draw.rect(paddle2, 'white')  # type: ignore
    screen.draw.filled_rect(ball, 'white')  # type: ignore
    screen.draw.text(str(PLAYER1_SCORE), (WIDTH // 4, 20), fontsize=50)  # type: ignore
    screen.draw.text(str(PLAYER2_SCORE), (WIDTH * 3 // 4, 20), fontsize=50)  # type: ignore

def update():
    if game_state == GAME_PLAY:
        update_game_play()

def update_game_play():
    global PLAYER1_SCORE, PLAYER2_SCORE

    # Player 1 movement
    if keyboard.w and paddle1.top > 0:  # type: ignore
        paddle1.y -= PADDLE_SPEED
    if keyboard.s and paddle1.bottom < HEIGHT:  # type: ignore
        paddle1.y += PADDLE_SPEED

    # Player 2 movement
    if not single_player:
        if keyboard.up and paddle2.top > 0:  # type: ignore
            paddle2.y -= PADDLE_SPEED
        if keyboard.down and paddle2.bottom < HEIGHT:  # type: ignore
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
    if ball.colliderect(paddle1):  # type: ignore
        bounce_ball(paddle1)
    if ball.colliderect(paddle2):  # type: ignore
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
        # If the ball is closer, move towards the ball with added randomness
        target_y = ball.centery - PADDLE_HEIGHT // 2 + random.randint(-AI_RANDOMNESS, AI_RANDOMNESS)

    # Move the paddle towards the target position with a delay
    if paddle2.centery < target_y:
        paddle2.y += AI_PADDLE_SPEED
    elif paddle2.centery > target_y:
        paddle2.y -= AI_PADDLE_SPEED

    # Prevent the AI paddle from going out of bounds
    if paddle2.top < 0:
        paddle2.top = 0
    if paddle2.bottom > HEIGHT:
        paddle2.bottom = HEIGHT

def bounce_ball(paddle):
    global ball_speed
    offset = (ball.centery - paddle.centery) / (PADDLE_HEIGHT / 2)
    bounce_angle = offset * MAX_BOUNCE_ANGLE
    ball_speed[0] = -ball_speed[0]  # Reverse horizontal direction
    ball_speed[1] = BALL_SPEED_X * offset  # Adjust vertical direction

    # Increase the ball speed
    ball_speed[0] *= 1.1
    ball_speed[1] *= 1.1

def reset_ball():
    global ball_speed
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    ball_speed[0] = BALL_SPEED_X if ball_speed[0] < 0 else -BALL_SPEED_X
    ball_speed[1] = BALL_SPEED_Y

def on_key_down(key):
    global game_state, single_player
    if game_state == TITLE_SCREEN:
        if key == keys.K_1:  # type: ignore
            single_player = True
            start_game()
        elif key == keys.K_2:  # type: ignore
            single_player = False
            start_game()

def start_game():
    global game_state, PLAYER1_SCORE, PLAYER2_SCORE
    game_state = GAME_PLAY
    PLAYER1_SCORE = 0
    PLAYER2_SCORE = 0
    reset_ball()

pgzrun.go()
