import anim_obj, pygame, sys, random, boss

# Solved a scary merge conflict

# Music state tracking
boss_music_playing = False
main_music_playing = False
game_over_music_playing = False
win_screen_music_playing = False

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
            paddle_explosion_vfx.animate_next_frame(screen)
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
        on_game_over() # Do game over logic

# Two separate logics for two different jumpscares
def do_i_jumpscare():
    global juampscare
    if (random.randint(1, 1000) == 1) and (juampscare == False):
        jumpscare_sfx = pygame.mixer.Sound(file="fnaf2-jumpscare-sound.wav")
        jumpscare_sfx.play()
        jumpscare_vfx.start_animation(hang_over=50)
        juampscare = True

def maid():
    if random.randint(1, 10000) == 1:
        screen.blit(lebumbum, (0, 0))

def get_big_bossed():
    global funny_boss, delay
    if funny_boss == False:
        # Display Big Boss for a frame
        screen.blit(big_boss, (0, 0))
        bigboss_sfx = pygame.mixer.Sound(big_boss_mus)
        kept = pygame.mixer.Sound(kept_u_waiting)
        bigboss_sfx.play()
        kept.play()
        for i in range(1, 10):
            if delay == 0:
                kept.play()
        funny_boss = True

# Things to do once the boss is dead
def on_boss_death():
    global main_music_playing

    # Reset music to normal
    pygame.mixer.music.stop()
    pygame.mixer.music.load(win_screen_mus)
    pygame.mixer.music.play(-1)
    main_music_playing = True

# Things to do once in a game over
def on_game_over():
    global boss_music_playing
    pygame.mixer.music.stop()


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

# Restart
def restart():
    """
    Resets the ball and player scores to the initial state, unpauses music
    """
    global ball_speed_x, ball_speed_y, score, game_over, juampscare, start, main_music_playing, boss_music_playing

    # Reset positions
    ball.center = (ball_start_pos_xy, ball_start_pos_xy)  # Reset ball position to center
    player.center = (player_start_pos_x, player_start_pos_y) # Reset player position to start
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement

    # Reset globals
    game_over = False
    juampscare = False
    start = True  # Start the ball movement
    score = 0  # Reset player score

    # Reset music for new game
    pygame.mixer.music.stop()
    pygame.mixer.music.load(game_mus)
    pygame.mixer.music.play(-1)
    main_music_playing = True
    boss_music_playing = False

    boss.reset() # Reset boss so he isn't weaker or dead on reset

    pygame.mixer.unpause()  # Play music

# Menu logic (this took so much trial and error, not even god can help me now... all the crashouts)
def menu():
    global boss_music_playing, main_music_playing, win_screen_music_playing

    # Reset music states when returning to menu
    boss_music_playing = False
    main_music_playing = False
    win_screen_music_playing = False

    while True:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(main_theme)
            pygame.mixer.music.play(-1, 0.0)
            main_music_playing = True

        screen.fill('black')
        welcome_text = big_font.render(f'PONG', False, light_grey)
        start_text = basic_font.render(f'Press [SPACE] to start', False, light_grey)
        screen.blit(start_text, (screen_width / 2 - 200, screen_height / 2 + 20))
        screen.blit(welcome_text, (screen_width / 2 - 200, screen_height / 2 - 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart()
                    return


def win_screen():
    global boss_music_playing, main_music_playing, win_screen_music_playing, juampscare

    # Reset music states when returning to menu
    boss_music_playing = False
    main_music_playing = False
    win_screen_music_playing = False

    # Start animations
    tenna_gif_vfx.start_animation()
    screen.fill('black') # Feel free to put this back in the display loop, i was just trying to see if Foxy stuck but nah

    while True:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(win_screen_mus)
            pygame.mixer.music.play(-1, 0.0)
            win_screen_music_playing = True


        congrats = basic_font.render(f'YOU BEAT THE BOSS!!!', False, light_grey)
        final_score = basic_font.render(f'Your final score is {score}', False, light_grey)
        message = basic_font.render(f'Now give us our award...', False, light_grey)
        leave = basic_font.render(f'press space', False, light_grey)
        screen.blit(leave, (screen_width / 2 - 200, screen_height / 2 + 20))
        screen.blit(message, (screen_width / 2 - 200, screen_height / 2 - 100))
        screen.blit(final_score, (screen_width / 2 - 200, screen_height / 2 - 150))
        screen.blit(congrats, (screen_width / 2 - 200, screen_height / 2 - 200))
        tenna_gif_vfx.animate_next_frame(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart()
                    return

# Determine whether boss should drop
def boss_drop():
    global boss_music_playing

    if score >= 15 and not boss_music_playing:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(boss_theme)
        pygame.mixer.music.play(-1)
        boss_music_playing = True
    elif score < 15 and boss_music_playing:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(game_mus)
        pygame.mixer.music.play(-1)
        boss_music_playing = False

    if score >= 15:
        boss.draw(screen)

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
player_width = 200
player_start_pos_x = int(screen_width/2 + 90)
player_start_pos_y = screen_height - 20
player = pygame.Rect(player_start_pos_x, player_start_pos_y, player_width, player_height)  # Player paddle

 # Additional visuals
paddle_explosion_vfx = anim_obj.AnimatedSprite(file_path="deltarune-realistic-explosion.png", rows=3, columns=6,
                                               position=(0, 0))
jumpscare_vfx = anim_obj.AnimatedSprite(file_path="fnaf2-withered-foxy-jumpscare.png", rows=2, columns=7,
                                        position=(0,0))
tenna_gif_vfx = anim_obj.AnimatedSprite(file_path="tenna-dancing-gif.png", rows=8, columns=13,
                                        position=(screen_width - 100, screen_height - 200), looping=True)
lebumbum = pygame.image.load('lebumbum.png')
big_boss = pygame.image.load('big_boss.png')
pygame.transform.scale(lebumbum, (screen_height, screen_width))
pygame.transform.scale(big_boss, (screen_width, screen_width))

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
music_playing = False
pygame.mixer.set_num_channels(8)
channel_0 = pygame.mixer.Channel(0)
pygame.mixer.music.set_volume(0.6)
main_theme = 'a_cruel_angels_thesis_8-bit_cover_neon_genesis_evangelion_op.wav'
boss_theme = "standing_here.wav"
big_boss_mus = "invisible-duran.mp3"
win_screen_mus = "theworld.mp3"
kept_u_waiting = 'kept.mp3'
game_mus = 'devil_may_cry_5_devil_trigger_nes_8-bit_remix.wav'


# Visual declarations
light_grey = pygame.Color('grey83')
red = pygame.Color('red')
blue = pygame.Color('blue')

# Score Text setup
score = 0
game_over = False
basic_font = pygame.font.Font('freesansbold.ttf', 32)  # Font for displaying score
big_font = pygame.font.Font('freesansbold.ttf', 128)

# important variables
start = False
begin = False
juampscare = False
funny_boss = False
delay = 10

pygame.mixer.unpause()

# Displays start menu
menu()

# The funny timer
TIMER_RESET = 500
timer = TIMER_RESET

# Main game loop
while True:
    # He boss
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
                timer = TIMER_RESET
                restart()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 6  # Stop moving left
            if event.key == pygame.K_RIGHT:
                player_speed -= 6  # Stop moving right


    if not game_over:

        # Game Logic
        ball_movement()
        player_movement()
        boss.update(ball, [ball_speed_x, ball_speed_y])

        # Visuals
        screen.fill(bg_color)  # Clear screen with background color
        pygame.draw.rect(screen, light_grey, player)  # Draw player paddle
        # DONE Task 3: Change the Ball Color
        pygame.draw.ellipse(screen, blue, ball)  # Draw ball
        player_text = basic_font.render(f'{score}', False, light_grey)  # Render player score
        screen.blit(player_text, (screen_width/2 - 15, 10))  # Display score on screen
        maid() # maid

        # Boss draw come back
        boss_drop()
        paddle_explosion_vfx.animate_next_frame(screen)
        jumpscare_vfx.animate_next_frame(screen)

        # Check if boss is dead to execute boss death protocol
        if boss_music_playing and boss.is_dead():
            on_boss_death()
            win_screen()

    else:
        # Game over... logic?
        do_i_jumpscare()

        # Render Game Over text
        gameover_text = basic_font.render(f'Game Over! Final score: {score}', False, light_grey)
        restart_text = basic_font.render(f'Press [SPACE] to restart', False, light_grey)
        # Display Game Over on screen
        screen.blit(gameover_text, (screen_width/2 - 200, screen_height/2 - 50))
        screen.blit(restart_text, (screen_width/2 - 200, screen_height/2 - 20))

        if timer <= 0:
            timer = TIMER_RESET
            get_big_bossed()

        if delay == 0:
            delay = 10

        timer -= 1
        delay -= 1
        print(timer)

        # Other visuals
        if juampscare:
            jumpscare_vfx.animate_next_frame(screen)

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second