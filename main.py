import random
import math
import pygame
import asyncio
import os

# Game constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 10
PADDLE_SPEED = 7
AI_PADDLE_SPEED = 5
BALL_SPEED_X = 6
BALL_SPEED_Y = 6
MAX_BOUNCE_ANGLE = 60  # Max bounce angle in degrees
WINNING_SCORE = 11
WINNING_MARGIN = 2

# Game states
INTRO_SCREEN = -1
TITLE_SCREEN = 0
GAME_PLAY = 1
GAME_OVER = 2

class WhiffWaff:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # RESIZABLE for web
        pygame.display.set_caption("Whiff Waff")
        self.intro_screen_start_time = pygame.time.get_ticks()
        
        # Modify asset loading for web compatibility
        def load_image(filename):
            try:
                # Try loading from assets directory
                return pygame.image.load(os.path.join('assets', filename))
            except:
                # Fallback to direct filename (for pygbag)
                return pygame.image.load(filename)
        
        def load_sound(filename):
            try:
                # Try loading from assets directory
                return pygame.mixer.Sound(os.path.join('assets', filename))
            except:
                # Fallback to direct filename (for pygbag)
                return pygame.mixer.Sound(filename)
        
        # Load images
        self.intro_screen_background_initial = load_image('intro_screen_background_initial.png')
        self.background = load_image('background.png')
        self.intro_screen_background = load_image('intro_screen_background.png')
        self.title_screen_background = load_image('title_screen_background.png')
        self.paddle1_img = load_image('paddle.png')
        self.paddle2_img = load_image('paddle2.png')
        self.ball_img = load_image('ball.png')
        
        # Load sounds
        pygame.mixer.init()
        self.intro_music = load_sound('intro_music.ogg')
        self.main_music = load_sound('main_music.ogg')
        self.wiff_sound = load_sound('wiff.wav')
        self.waff_sound = load_sound('waff.wav')
        self.wiffwaff_sound = load_sound('wiffwaff.wav')
        self.victory_sound = load_sound('victory.wav')
        
        # Font
        self.font = pygame.font.Font(None, 50)

        # Game state variables
        self.game_state = INTRO_SCREEN
        self.single_player = False

        # Paddles and ball setup
        self.paddle1 = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.paddle2 = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

        # Ball speed
        self.ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

        # Scores
        self.player1_score = 0
        self.player2_score = 0

        # Victory flag
        self.victory_sound_played = False

        # AI parameters
        self.AI_REACTION_DELAY = 0.05
        self.AI_RANDOMNESS = 10

        # Start intro music
        self.intro_music.play()

    def draw(self):
        # Clear screen and draw background
        self.screen.blit(self.background, (0, 0))
        
        if self.game_state == INTRO_SCREEN:
            self.draw_intro_screen()
        elif self.game_state == TITLE_SCREEN:
            self.draw_title_screen()
        elif self.game_state == GAME_PLAY:
            self.draw_game_play()
        elif self.game_state == GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()

    def draw_intro_screen(self):
        current_time = pygame.time.get_ticks()
    
        # Check if less than 8 seconds have passed
        if current_time - self.intro_screen_start_time < 8000:
            self.screen.blit(self.intro_screen_background_initial, (0, 0))
        else:
            self.screen.blit(self.intro_screen_background, (0, 0))

    def draw_title_screen(self):
        self.screen.blit(self.title_screen_background, (0, 0))
        
        # Render title
        title_text = self.font.render("Whiff-Waff", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.screen.blit(title_text, title_rect)
        
        # Render menu options
        single_player_text = self.font.render("Press 1 for 1 Player", True, (255, 255, 255))
        single_player_rect = single_player_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(single_player_text, single_player_rect)
        
        two_player_text = self.font.render("Press 2 for 2 Players", True, (255, 255, 255))
        two_player_rect = two_player_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        self.screen.blit(two_player_text, two_player_rect)

        # Create a smaller font for controls
        controls_font = pygame.font.Font(None, 36)
        
        # Render controls information
        controls_title = controls_font.render("Controls:", True, (255, 255, 255))
        controls_title_rect = controls_title.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        self.screen.blit(controls_title, controls_title_rect)
        
        p1_controls = controls_font.render("Player 1: W/S to move up/down", True, (255, 255, 255))
        p1_rect = p1_controls.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        self.screen.blit(p1_controls, p1_rect)
        
        p2_controls = controls_font.render("Player 2: ↑/↓ to move up/down", True, (255, 255, 255))
        p2_rect = p2_controls.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 180))
        self.screen.blit(p2_controls, p2_rect)

    def draw_game_play(self):
        # Draw paddles
        self.screen.blit(self.paddle1_img, self.paddle1)
        self.screen.blit(self.paddle2_img, self.paddle2)
        
        # Draw ball
        self.screen.blit(self.ball_img, self.ball)
        
        # Draw scores
        score1_text = self.font.render(str(self.player1_score), True, (255, 255, 255))
        score2_text = self.font.render(str(self.player2_score), True, (255, 255, 255))
        
        self.screen.blit(score1_text, (WIDTH // 4, 20))
        self.screen.blit(score2_text, (WIDTH * 3 // 4, 20))

    def draw_game_over(self):
        self.screen.blit(self.title_screen_background, (0, 0))
        winner = "Player 1" if self.player1_score > self.player2_score else "Player 2"
        
        if not self.victory_sound_played:
            self.victory_sound.play()
            self.victory_sound_played = True
        
        # Render winner text
        winner_text = self.font.render(f"{winner} Wins!", True, (255, 255, 255))
        winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.screen.blit(winner_text, winner_rect)
        
        # Render restart instructions
        restart_text = self.font.render("Press ENTER to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(restart_text, restart_rect)

    def update(self):
        if self.game_state == INTRO_SCREEN:
            self.update_intro_screen()
        elif self.game_state == GAME_PLAY:
            self.update_game_play()

    def update_intro_screen(self):
        current_time = pygame.time.get_ticks()
    
        # Check if intro music has finished
        if current_time - self.intro_screen_start_time > 10000 and not pygame.mixer.get_busy():
            self.game_state = TITLE_SCREEN
            pygame.mixer.music.set_volume(0.4)
            self.main_music.play(-1)  # Loop main music

    def update_game_play(self):
        # Player 1 movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.paddle1.top > 0:
            self.paddle1.y -= PADDLE_SPEED
        if keys[pygame.K_s] and self.paddle1.bottom < HEIGHT:
            self.paddle1.y += PADDLE_SPEED

        # Player 2 movement
        if not self.single_player:
            if keys[pygame.K_UP] and self.paddle2.top > 0:
                self.paddle2.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and self.paddle2.bottom < HEIGHT:
                self.paddle2.y += PADDLE_SPEED
        else:
            self.ai_move()

        # Ball movement
        self.ball.x += self.ball_speed[0]
        self.ball.y += self.ball_speed[1]

        # Ball collision with top/bottom
        if self.ball.top <= 0 or self.ball.bottom >= HEIGHT:
            self.ball_speed[1] = -self.ball_speed[1]

        # Ball collision with paddles
        if self.ball.colliderect(self.paddle1):
            self.bounce_ball(self.paddle1)
        if self.ball.colliderect(self.paddle2):
            self.bounce_ball(self.paddle2)

        # Ball goes out of bounds
        if self.ball.left <= 0:
            self.player2_score += 1
            self.wiffwaff_sound.play()
            if self.check_winner():
                self.game_state = GAME_OVER
            else:
                self.reset_ball(serving_player=1)
        if self.ball.right >= WIDTH:
            self.player1_score += 1
            self.wiffwaff_sound.play()
            if self.check_winner():
                self.game_state = GAME_OVER
            else:
                self.reset_ball(serving_player=2)

    def ai_move(self):
        if self.ball_speed[0] > 0:
            time_to_reach = (self.paddle2.left - self.ball.right) / self.ball_speed[0]
            predicted_y = self.ball.y + self.ball_speed[1] * time_to_reach
            predicted_y += random.randint(-self.AI_RANDOMNESS, self.AI_RANDOMNESS)
            target_y = max(min(predicted_y - PADDLE_HEIGHT // 2, HEIGHT - PADDLE_HEIGHT), 0)
            if self.paddle2.centery < target_y:
                self.paddle2.y += AI_PADDLE_SPEED
            elif self.paddle2.centery > target_y:
                self.paddle2.y -= AI_PADDLE_SPEED
        else:
            if self.paddle2.centery < HEIGHT // 2:
                self.paddle2.y += AI_PADDLE_SPEED
            elif self.paddle2.centery > HEIGHT // 2:
                self.paddle2.y -= AI_PADDLE_SPEED

        # Prevent AI paddle from going out of bounds
        self.paddle2.top = max(0, self.paddle2.top)
        self.paddle2.bottom = min(HEIGHT, self.paddle2.bottom)

    def bounce_ball(self, paddle):
        # Calculate paddle hit location more precisely
        relative_intersect_y = (paddle.centery - self.ball.centery) / (PADDLE_HEIGHT / 2)
        
        # Reduce max angle to create more horizontal bounces
        max_angle = math.radians(45)  # Reduced from 75 to 45 degrees
        bounce_angle = relative_intersect_y * max_angle

        # Calculate new ball speed with more controlled variation
        current_speed = math.hypot(self.ball_speed[0], self.ball_speed[1])
        speed_increase_factor = random.uniform(1.02, 1.08)  # Reduced speed boost

        # Preserve direction while adjusting trajectory
        direction_x = 1 if self.ball_speed[0] < 0 else -1
    
        # Calculate new velocities
        new_speed_x = abs(current_speed * math.cos(bounce_angle)) * direction_x * speed_increase_factor
        new_speed_y = current_speed * math.sin(bounce_angle) * speed_increase_factor
    
        # Ensure horizontal speed is always significant
        MIN_HORIZONTAL_RATIO = 0.7  # At least 70% of speed should be horizontal
        total_speed = math.hypot(new_speed_x, new_speed_y)
        if abs(new_speed_x) < total_speed * MIN_HORIZONTAL_RATIO:
            # Adjust speeds to maintain minimum horizontal ratio while preserving total speed
            new_speed_x = (total_speed * MIN_HORIZONTAL_RATIO) * (1 if new_speed_x > 0 else -1)
            new_speed_y = math.copysign(math.sqrt(total_speed**2 - new_speed_x**2), new_speed_y)

        # Update ball speeds
        self.ball_speed[0] = new_speed_x
        self.ball_speed[1] = new_speed_y

        # Prevent excessive speed
        MAX_BALL_SPEED = 12  # Slightly reduced max speed
        self.ball_speed[0] = max(min(self.ball_speed[0], MAX_BALL_SPEED), -MAX_BALL_SPEED)
        self.ball_speed[1] = max(min(self.ball_speed[1], MAX_BALL_SPEED), -MAX_BALL_SPEED)

        # Reposition ball to prevent sticking
        if self.ball_speed[0] > 0:
            self.ball.left = paddle.right
        else:
            self.ball.right = paddle.left

        # Play sounds with slight pitch variation
        sound = self.waff_sound if paddle == self.paddle1 else self.wiff_sound
        sound.set_volume(random.uniform(0.7, 1.0))
        sound.play()

    def reset_ball(self, serving_player):
        if serving_player == 1:
            self.ball.x = self.paddle1.right + BALL_SIZE * 2
            self.ball.y = self.paddle1.centery
            self.ball_speed[0] = BALL_SPEED_X
        else:
            self.ball.x = self.paddle2.left - BALL_SIZE * 2
            self.ball.y = self.paddle2.centery
            self.ball_speed[0] = -BALL_SPEED_X
        self.ball_speed[1] = BALL_SPEED_Y * random.choice([-1, 1])

    def check_winner(self):
        if (self.player1_score >= WINNING_SCORE and self.player1_score - self.player2_score >= WINNING_MARGIN) or \
           (self.player2_score >= WINNING_SCORE and self.player2_score - self.player1_score >= WINNING_MARGIN):
            self.victory_sound_played = False
            return True
        return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_state == TITLE_SCREEN:
                    if event.key == pygame.K_1:
                        self.single_player = True
                        self.start_game()
                    elif event.key == pygame.K_2:
                        self.single_player = False
                        self.start_game()
                
                if self.game_state == GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        self.game_state = TITLE_SCREEN
        
        return True

    def start_game(self):
        self.game_state = GAME_PLAY
        self.player1_score = 0
        self.player2_score = 0
        self.victory_sound_played = False
        self.reset_ball(serving_player=1)

async def main():
    game = WhiffWaff()
    
    while True:
        if not game.handle_events():
            break
        
        game.update()
        game.draw()
        
        pygame.display.flip()  # Ensure screen updates
        await asyncio.sleep(0)

asyncio.run(main())
