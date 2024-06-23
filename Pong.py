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

# Load game objects
paddle1 = Actor('paddle', (30, HEIGHT // 2))
paddle2 = Actor('paddle', (WIDTH - 30, HEIGHT // 2))
ball = Actor('ball', (WIDTH // 2, HEIGHT // 2))



# Initial ball speed
ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

# AI delay and randomness
AI_REACTION_DELAY = 0.05
AI_RANDOMNESS = 20

def draw():
    screen.clear()
    screen.blit('background', (0, 0))  # Draw the background
    if game_state == TITLE_SCREEN:
        draw_title_screen()
    elif game_state == GAME_PLAY:
        draw_game_play()

def draw_title_screen():
    screen.draw.text("Pong Game", center=(WIDTH // 2, HEIGHT // 3), fontsize=60, color="white")
    screen.draw.text("Press 1 for 1 Player", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")
    screen.draw.text("Press 2 for 2 Players", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=40, color="white")

def draw_game_play():
    paddle1.draw()
    paddle2.draw()
    ball.draw()
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
        reset_ball(serving_player=2)
    if ball.right >= WIDTH:
        PLAYER1_SCORE += 1
        reset_ball(serving_player=1)

def ai_move():
    # Predict where the ball will be when it reaches the AI paddle's x position
    if ball_speed[0] > 0:  # Ball is moving towards the AI paddle
        # Time until the ball reaches the AI paddle
        time_to_reach_paddle = (paddle2.left - ball.right) / ball_speed[0]
        # Predicted ball position on the y-axis
        predicted_y = ball.y + ball_speed[1] * time_to_reach_paddle

        # Add randomness to the prediction to simulate human-like inaccuracy
        predicted_y += random.randint(-AI_RANDOMNESS, AI_RANDOMNESS)

        # Ensure the AI paddle does not move out of bounds
        target_y = max(min(predicted_y - PADDLE_HEIGHT // 2, HEIGHT - PADDLE_HEIGHT), 0)

        # Move the paddle towards the target position
        if paddle2.centery < target_y:
            paddle2.y += AI_PADDLE_SPEED
        elif paddle2.centery > target_y:
            paddle2.y -= AI_PADDLE_SPEED
    else:
        # If the ball is moving away, keep the paddle centered
        if paddle2.centery < HEIGHT // 2:
            paddle2.y += AI_PADDLE_SPEED
        elif paddle2.centery > HEIGHT // 2:
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

def reset_ball(serving_player):
    global ball_speed
    if serving_player == 1:
        ball.x = paddle2.x - BALL_SIZE - 1  # Position near player 2's paddle
        ball.y = paddle2.centery - BALL_SIZE // 2
        ball_speed[0] = -BALL_SPEED_X  # Ball moves towards player 1
    else:
        ball.x = paddle1.x + PADDLE_WIDTH + 1  # Position near player 1's paddle
        ball.y = paddle1.centery - BALL_SIZE // 2
        ball_speed[0] = BALL_SPEED_X  # Ball moves towards player 2
    ball_speed[1] = BALL_SPEED_Y * random.choice([-1, 1])  # Randomize vertical direction

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
    reset_ball(serving_player=1)  # Player 1 serves first

pgzrun.go()
