# import the modules required

import pygame  # the primary module used for making this game
import sys  # for exiting the game using sys.exit
import random  # for generating random pipes possitions and height

# Defining The functions required


def draw_floor():
    screen.blit(floor, (floor_x_possition, 450))
    screen.blit(floor, (floor_x_possition + 288, 450))


def create_pipe():
    random_pipe_possition = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(450, random_pipe_possition))
    top_pipe = pipe_surface.get_rect(
        midbottom=(450, random_pipe_possition - 150))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False

    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        death_sound.play()
        can_score = True
        return False
    return True


def rotate_bird(bird_):
    new_bird = pygame.transform.rotozoom(bird_, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(
            str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(
            f'Score {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f'High Score {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 400))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def pipe_score_check():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 48 < pipe.centerx < 52 and can_score:
                score += 1
                score_update_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


                # Creating a game screen/window, initializing pygame and making clock variable for FPS
WIDTH = 288
HEIGHT = 512
pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_font = pygame.font.Font('04B_19.ttf', 20)

clock = pygame.time.Clock()


# game variables

gravity = 0.125
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True


# Background image import

bg_surface = pygame.image.load('assets/background-day.png').convert()

# Floor image Import

floor = pygame.image.load('assets/base.png').convert()
floor_x_possition = 0

# Bird image Imports and making a rect around it

bird_downflap = pygame.image.load(
    'assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_upflap, bird_midflap, bird_upflap]
bird_index = 0
bird = bird_frames[bird_index]
bird_rect = bird.get_rect(center=(110, 288))

BirdFlap = pygame.USEREVENT + 1
pygame.time.set_timer(BirdFlap, 200)


# Pipe image Import and making it spawn automatically

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_list = []
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)
pipe_height = [200, 300, 400]

# Gameover Image

gameover_surface = pygame.image.load('assets/message.png').convert_alpha()
gameover_rect = gameover_surface.get_rect(center=(144, 256))

# Game sounds (Flapping,Collisions,Points)

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_update_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 125

# Game loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 4.5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (110, 288)
                bird_movement = 0
                score = 0

        if event.type == SPAWN_PIPE:
            pipe_list.extend(create_pipe())

        if event.type == BirdFlap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active == True:

        # Bird Movements

        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes

        pipe_list == move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score

        pipe_score_check()
        score_display('main_game')

    else:
        screen.blit(gameover_surface, gameover_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor movements

    floor_x_possition -= 1
    draw_floor()
    if floor_x_possition <= -288:

        floor_x_possition = 0
    pygame.display.update()
    clock.tick(120)
