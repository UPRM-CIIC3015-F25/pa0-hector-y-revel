import anim_obj, pygame, spritesheet, sys, random

def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Start the ball movement when the game begins
    # TODO Task 5 Create a Merge Conflict
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
            # TODO BONUS: Add visual to correspond with paddle explosion sound
            paddle_explosion_vfx.start_animation()


    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        restart()  # Reset the game

def do_i_jumpscare():
    if random.randint(1, 1000) == 1:
        jumpscare_vfx.start_animation()
def maid():
    if random.randint(1, 1000) == 1:
        lebumbum.start_animation()

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

# TODO BONUS: make a start screen for the game

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

# Additional sprite sheets and vfx
paddle_explosion_vfx = anim_obj.AnimatedSprite(file_path="deltarune-realistic-explosion.png", rows=3, columns=6, position=(0,0))
jumpscare_vfx = anim_obj.AnimatedSprite(file_path="fnaf2-withered-foxy-jumpscare.png", rows=7, columns=2, position=(0,0))
lebumbum = anim_obj.AnimatedSprite(file_path="lebumbum.png", rows=7, columns=2, position=(0,0))

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)  # Ball (centered)
# TODO Task 1 Make the paddle bigger
player_height = 15
player_width = 200
player = pygame.Rect(screen_width/2 - 45, screen_height - 20, player_width, player_height)  # Player paddle

# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0

# Score Text setup
score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)  # Font for displaying score

start = False  # Indicates if the game has started

# Main game loop
while True:
    # Event handling
    # TODO Task 4: Add your name
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
            if event.key == pygame.K_SPACE:
                start = True  # Start the ball movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 6  # Stop moving left
            if event.key == pygame.K_RIGHT:
                player_speed -= 6  # Stop moving right

    # Game Logic
    ball_movement()
    player_movement()
    do_i_jumpscare()
    maid()

    # Visuals
    light_grey = pygame.Color('grey83')
    red = pygame.Color('red')
    blue = pygame.Color('blue')
    screen.fill(bg_color)  # Clear screen with background color
    pygame.draw.rect(screen, light_grey, player)  # Draw player paddle
    # TODO Task 3: Change the Ball Color
    pygame.draw.ellipse(screen, blue, ball)  # Draw ball
    player_text = basic_font.render(f'{score}', False, light_grey)  # Render player score
    screen.blit(player_text, (screen_width/2 - 15, 10))  # Display score on screen
    paddle_explosion_vfx.animate_next_frame(screen)
    jumpscare_vfx.animate_next_frame(screen)
    lebumbum.animate_next_frame(screen)

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second