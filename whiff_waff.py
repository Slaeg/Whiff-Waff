# This bit makes the window appear in the top left corner.
# It needs to go before importing pgzrun or it won't work!
x = 10
y = 10
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'

import pgzrun
import random
import math

# Game constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 10
PADDLE_SPEED = 5
AI_PADDLE_SPEED = 3
BALL_SPEED_X = 4
BALL_SPEED_Y = 4
MAX_BOUNCE_ANGLE = 45  # Max bounce angle in degrees
WINNING_SCORE = 11
WINNING_MARGIN = 2

# Game states
INTRO_SCREEN = -1
TITLE_SCREEN = 0
GAME_PLAY = 1
GAME_OVER = 2
game_state = INTRO_SCREEN
single_player = False

# Load game objects
paddle1 = Actor('paddle', (30, HEIGHT // 2))
paddle2 = Actor('paddle', (WIDTH - 30, HEIGHT // 2))
ball = Actor('ball', (WIDTH // 2, HEIGHT // 2))

# Initial ball speed
ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

# Player scores
player1_score = 0
player2_score = 0

# AI delay and randomness
AI_REACTION_DELAY = 0.05
AI_RANDOMNESS = 20

# Music for the intro screen
music.play_once('intro_music')  # Ensure the music plays once

def draw():
    screen.clear()
    screen.blit('background', (0, 0))  # Draw the background
    if game_state == INTRO_SCREEN:
        draw_intro_screen()
    elif game_state == TITLE_SCREEN:
        draw_title_screen()
    elif game_state == GAME_PLAY:
        draw_game_play()
    elif game_state == GAME_OVER:
        draw_game_over()

def draw_intro_screen():
    screen.fill("black")  # Set the background to black
    screen.draw.text("Ping-pong was invented on the dining tables of England in the 19th century, and it was called Wiff-waff!", center=(WIDTH // 2, HEIGHT // 3), fontsize=30, color="white", width=WIDTH-40)
    screen.draw.text("And there, I think, you have the difference between us and the rest of the world.", center=(WIDTH // 2, HEIGHT // 3 + 40), fontsize=30, color="white", width=WIDTH-40)
    screen.draw.text("Other nations, the French, looked at a dining table and saw an opportunity to have dinner; we looked at it and saw an opportunity to play Whiff-waff.", center=(WIDTH // 2, HEIGHT // 3 + 80), fontsize=30, color="white", width=WIDTH-40)
    screen.draw.text("- Boris Johnson", center=(WIDTH // 2, HEIGHT // 3 + 120), fontsize=30, color="white", width=WIDTH-40)

def draw_title_screen():
    screen.draw.text("Whiff-Waff", center=(WIDTH // 2, HEIGHT // 3), fontsize=60, color="white")
    screen.draw.text("Press 1 for 1 Player", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")
    screen.draw.text("Press 2 for 2 Players", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=40, color="white")

def draw_game_play():
    paddle1.draw()
    paddle2.draw()
    ball.draw()
    screen.draw.text(str(player1_score), (WIDTH // 4, 20), fontsize=50)
    screen.draw.text(str(player2_score), (WIDTH * 3 // 4, 20), fontsize=50)

def draw_game_over():
    winner = "Player 1" if player1_score > player2_score else "Player 2"
    screen.draw.text(f"{winner} Wins!", center=(WIDTH // 2, HEIGHT // 3), fontsize=60, color="white")
    screen.draw.text("Press ENTER to Restart", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")

def update():
    if game_state == INTRO_SCREEN:
        update_intro_screen()
    elif game_state == TITLE_SCREEN:
        pass  # No update needed for the title screen
    elif game_state == GAME_PLAY:
        update_game_play()
    elif game_state == GAME_OVER:
        pass  # No update needed for the game over screen

def update_game_play():
    global player1_score, player2_score, game_state

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
        player2_score += 1
        sounds.wiffwaff.play()  # Play out-of-bounds sound
        if check_winner():
            game_state = GAME_OVER
        else:
            reset_ball(serving_player=1)
    if ball.right >= WIDTH:
        player1_score += 1
        sounds.wiffwaff.play()  # Play out-of-bounds sound
        if check_winner():
            game_state = GAME_OVER
        else:
            reset_ball(serving_player=2)

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

    # Convert the bounce angle to radians for calculation
    bounce_radians = math.radians(bounce_angle)
    speed = math.hypot(ball_speed[0], ball_speed[1])
    ball_speed[1] = speed * math.sin(bounce_radians)

    # Increase the ball speed
    ball_speed[0] *= 1.1
    ball_speed[1] *= 1.1

    # Ensure the ball doesn't clip through the paddle
    if ball_speed[0] > 0:
        ball.left = paddle.right
    else:
        ball.right = paddle.left
    
    # Play sound effect based on which paddle was hit
    if paddle == paddle1:
        sounds.waff.play()
    else:
        sounds.wiff.play()

def reset_ball(serving_player):
    global ball_speed
    if serving_player == 1:
        ball.x = paddle1.right + BALL_SIZE * 2  # Position near player 1's paddle, but not too close
        ball.y = paddle1.centery
        ball_speed[0] = BALL_SPEED_X
    else:
        ball.x = paddle2.left - BALL_SIZE * 2  # Position near player 2's paddle, but not too close
        ball.y = paddle2.centery
        ball_speed[0] = -BALL_SPEED_X
    ball_speed[1] = BALL_SPEED_Y * random.choice([-1, 1])  # Randomize vertical direction

def check_winner():
    if (player1_score >= WINNING_SCORE and player1_score - player2_score >= WINNING_MARGIN) or \
       (player2_score >= WINNING_SCORE and player2_score - player1_score >= WINNING_MARGIN):
        return True
    return False

def update_intro_screen():
    if not music.is_playing('intro_music'):
        global game_state
        game_state = TITLE_SCREEN
        music.set_volume(0.5)  # Set volume to 50%
        music.play('main_music')  # Start the main music and loop it


def on_key_down(key):
    global game_state, single_player
    if game_state == TITLE_SCREEN:
        if key == keys.K_1:
            single_player = True
            start_game()
        elif key == keys.K_2:
            single_player = False
            start_game()
    elif game_state == GAME_OVER:
        if key == keys.RETURN:
            game_state = TITLE_SCREEN

def start_game():
    global game_state, player1_score, player2_score
    game_state = GAME_PLAY
    player1_score = 0
    player2_score = 0
    reset_ball(serving_player=1)  # Player 1 serves first

pgzrun.go()
