from asyncio import constants
import pygame
from constants import *
from helpers import *
from character import Character

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Restless Crypt")

# Create frame rate clock
clock = pygame.time.Clock()

# Define player movement
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# Load character images
mob_animations = []

# indices: demon: 0, dragon: 1, jinn: 2, lizard: 3, medusa: 4, small_dragon: 5
# Heroes: 6, boss_wraith: 7
mob_types = ['demon', 'dragon', 'jinn', 'lizard', 'medusa', 'small_dragon']
main_types = ['Heroes', 'boss_wraith']

# Load animation
animation_types = ["Idle", "Walk"]

for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        # Reset temp list of images
        temp_list = []
        for i in range(1, 4):
            image = pygame.image.load(
                f"assets/sprites/Characters/{mob}/{animation}/{animation}{i}.png").convert_alpha()
            image = scale_image(image, SCALE)
            temp_list.append(image)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

for mob in main_types:
    animation_list = []
    for animation in animation_types:
        # Reset temp list of images
        temp_list = []
        for i in range(1, 11):
            image = pygame.image.load(
                f"assets/sprites/Characters/{mob}/{animation}/{animation}{i}.png").convert_alpha()
            image = scale_image(image, SCALE)
            temp_list.append(image)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

# Create player
player = Character(100, 100, mob_animations, 6)

# Create the game loop
run = True
while run:
    # control frame rate
    clock.tick(FPS)

    screen.fill(BG)

    # Positional update (x, y)
    dx = 0
    dy = 0
    if moving_right == True:
        dx = SPEED
    if moving_left == True:
        dx = -SPEED
    if moving_up == True:
        dy = -SPEED
    if moving_down == True:
        dy = SPEED

    # Move player
    player.move(dx, dy)

    # Update player
    player.update()

    # Draw player on screen
    player.draw(screen)

    # Event handling for clicking
    for event in pygame.event.get():
        # Quitting
        if event.type == pygame.QUIT:
            run = False

        # Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                moving_up = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                moving_down = True

        # Keyboard releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                moving_up = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                moving_down = False

    # Update the display from draw methods
    pygame.display.update()

pygame.quit()
