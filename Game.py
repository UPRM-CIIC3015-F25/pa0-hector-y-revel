import anim_obj, pygame, sys, random, boss

def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Start the ball movement when the game begins
    # DONE Task 5 Create a Merge Conflict
    speed = 8
    if start:
        ball_speed_x = speed * random.choice((1, -1))  # Randomize initial horizontal direction
        ball_speed_y = speed * random.choice((1, -1))  # Randomize initial vertical direction
        start = False

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle
            # DONE Task 2: Fix score to increase by 1
            score += 1  # Increase player score
            ball_speed_y *= -1  # Reverse ball's vertical direction
            # DONE Task 6: Add sound effects HERE
            paddle_touch_sound = pygame.mixer.Sound(file="deltarune-explosion.wav")
            paddle_touch_sound.set_volume(0.3)
            paddle_touch_sound.play()
            # DONE BONUS: Add visual to correspond with paddle explosion sound
            paddle_explosion_vfx.start_animation()
            paddle_explosion_vfx.update_position((ball.x, ball.y - 50))


    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        global game_over
        game_over = True  # Display game over screen

# Two separate logics for two different jumpscares
def do_i_jumpscare():
    if random.randint(1, 1000) == 1:
        jumpscare_vfx.start_animation()
def maid():
    if random.randint(1, 1000) == 1:
        screen.blit(lebumbum, (0, 0))


def player_movement():
    """
    Handles the movement of the player paddle, keeping it within the screen boundaries.
    """
    player.x += player_speed  # Move the player paddle horizontally

    # Prevent the paddle from moving out of the screen boundaries
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def restart():
    """
    Resets the ball and player scores to the initial state.
    """
    global ball_speed_x, ball_speed_y, score
    ball.center = (screen_width / 2, screen_height / 2)  # Reset ball position to center
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement
    score = 0  # Reset player score

# Menu logic (this took so much trial and error, not even god can help me now... all the crashouts)
def menu():
    while True:
        screen.fill('black')
        start_text = basic_font.render(f'Press [SPACE] to start', False, light_grey)
        screen.blit(start_text, (screen_width / 2 - 200, screen_height / 2 - 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window setup
screen_width = 500  # Screen width (can be adjusted)
screen_height = 500  # Screen height (can be adjusted)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')  # Set window title

# Colors
bg_color = pygame.Color('grey12')

# Game Rectangles (ball and player paddle)
ball_start_pos_xy = int(screen_width / 2 - 15)
ball = pygame.Rect(ball_start_pos_xy, ball_start_pos_xy, 30, 30)  # Ball (centered)
# DONE Task 1 Make the paddle bigger
player_height = 15
player_width = 250
player_start_pos_x = int(screen_width/2 - 90)
player_start_pos_y = screen_height - 20
player = pygame.Rect(player_start_pos_x, player_start_pos_y, player_width, player_height)  # Player paddle

 # Additional visuals
paddle_explosion_vfx = anim_obj.AnimatedSprite(file_path="deltarune-realistic-explosion.png", rows=3, columns=6, position=(ball.x, ball.y))
jumpscare_vfx = anim_obj.AnimatedSprite(file_path="fnaf2-withered-foxy-jumpscare.png", rows=7, columns=2, position=(0,0))
lebumbum = pygame.image.load('lebumbum.png')
pygame.transform.scale(lebumbum, (screen_height, screen_width))

# Boss sprites and stuff

ENEMY_IMG = pygame.image.load("cacodemon.png").convert_alpha()
ENEMY_HIT_IMG = pygame.image.load("cacodemon2.png").convert_alpha()
ENEMY_IMG = pygame.transform.scale(ENEMY_IMG, (60, 60))
ENEMY_HIT_IMG = pygame.transform.scale(ENEMY_HIT_IMG, (60, 60))
boss = boss.Demon(screen_width // 2 - 30, 100, ENEMY_IMG, ENEMY_HIT_IMG, screen_width, screen_height)


# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0
# Music
pygame.mixer.set_num_channels(8)
channel_0 = pygame.mixer.Channel(0)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.load('theworld.mp3')
pygame.mixer.music.load('a_cruel_angels_thesis_8-bit_cover_neon_genesis_evangelion_op.wav')
pygame.mixer.fadeout(1000)
pygame.mixer.music.play(-1, 0.0)

# Visual declarations
light_grey = pygame.Color('grey83')
red = pygame.Color('red')
blue = pygame.Color('blue')

# Score Text setup
score = 0
game_over = False
basic_font = pygame.font.Font('freesansbold.ttf', 32)  # Font for displaying score

start = False # Indicates if the game has started
begin = False

pygame.mixer.unpause()
# Displays start menu
menu()

# Main game loop
while True:

    #
    # Event handling
    # DONE Task 4: Add your name
    name = "John Doe"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed -= 6  # Move paddle left
            if event.key == pygame.K_RIGHT:
                player_speed += 6  # Move paddle right
            # Restart game
            if event.key == pygame.K_SPACE:
                score = 0
                ball.x, ball.y = ball_start_pos_xy, ball_start_pos_xy
                player.x, player.y = player_start_pos_x, player_start_pos_y
                game_over = False
                start = True  # Start the ball movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 6  # Stop moving left
            if event.key == pygame.K_RIGHT:
                player_speed -= 6  # Stop moving right


    if not game_over:
        # Game Logic
        ball_movement()
        player_movement()
        do_i_jumpscare()
        maid()
        boss.update(ball, [ball_speed_x, ball_speed_y])

        # Visuals
        screen.fill(bg_color)  # Clear screen with background color
        pygame.draw.rect(screen, light_grey, player)  # Draw player paddle
        # DONE Task 3: Change the Ball Color
        pygame.draw.ellipse(screen, blue, ball)  # Draw ball
        player_text = basic_font.render(f'{score}', False, light_grey)  # Render player score
        screen.blit(player_text, (screen_width/2 - 15, 10))  # Display score on screen
        maid()
        boss.draw(screen)
        paddle_explosion_vfx.animate_next_frame(screen)
        jumpscare_vfx.animate_next_frame(screen)
        pygame.mixer.music.unpause()

    else:
        # Render Game Over text
        gameover_text = basic_font.render(f'Game Over! Final score: {score}', False, light_grey)
        restart_text = basic_font.render(f'Press [SPACE] to restart', False, light_grey)
        # Display Game Over on screen
        screen.blit(gameover_text, (screen_width/2 - 200, screen_height/2 - 50))
        screen.blit(restart_text, (screen_width/2 - 200, screen_height/2 - 20))
        pygame.mixer.music.pause()
        pygame.mixer.music.play()
        do_i_jumpscare()

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second