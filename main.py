import pygame
import csv
from constants import *
from helpers import *
from weapon import Weapon
from items import Item
from world import World
from screen_fade import ScreenFade
from button import Button
from pygame import mixer

mixer.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Restless Crypt")

font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

# Create frame rate clock
clock = pygame.time.Clock()

# Define game variables
level = 1
start_intro = False
screen_scroll = [0, 0]
start_game = False
pause_game = False


class DamageText(pygame.sprite.Sprite):
    """A class to represent damage text."""

    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self) -> None:
        """Move damage text up."""

        # Reposition based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()


# Define player movement
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# Load music and sound
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)

# Load in sound effects
shot_fx = pygame.mixer.Sound("assets/audio/magic_shot.mp3")
shot_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound("assets/audio/magic_hit.wav")
hit_fx.set_volume(0.5)
coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
coin_fx.set_volume(0.5)
heal_fx = pygame.mixer.Sound("assets/audio/heal.wav")
heal_fx.set_volume(0.5)

# Load weapon image
weapon_image = scale_image(pygame.image.load(
    "assets/sprites/Weapons/Empty.png").convert_alpha(), WEAPON_SCALE)

magic_ball_image = scale_image(pygame.image.load(
    "assets/sprites/Weapons/magic_ball.png").convert_alpha(), MAGIC_SCALE)

boss_magic_ball_image = scale_image(pygame.image.load(
    "assets/sprites/Weapons/fireball.png").convert_alpha(), BOSS_BALL_SCALE)

# Load buttom images
restart_image = scale_image(pygame.image.load(
    "assets/sprites/Buttons/button_restart.png").convert_alpha(), BUTTON_SCALE)
start_image = scale_image(pygame.image.load(
    "assets/sprites/Buttons/button_start.png").convert_alpha(), BUTTON_SCALE)
resume_image = scale_image(pygame.image.load(
    "assets/sprites/Buttons/button_resume.png").convert_alpha(), BUTTON_SCALE)
exit_image = scale_image(pygame.image.load(
    "assets/sprites/Buttons/button_exit.png").convert_alpha(), BUTTON_SCALE)

# Load heart images
heart_empty = scale_image(pygame.image.load(
    "assets/sprites/Items/heart_empty.png").convert_alpha(), ITEM_SCALE)
heart_half = scale_image(pygame.image.load(
    "assets/sprites/Items/heart_half.png").convert_alpha(), ITEM_SCALE)
heart_full = scale_image(pygame.image.load(
    "assets/sprites/Items/heart_full.png").convert_alpha(), ITEM_SCALE)

# Load in item images
coin_images = []
for i in range(4):
    img = scale_image(pygame.image.load(
        f"assets/sprites/Items/coin_f{i}.png").convert_alpha(), ITEM_SCALE)
    coin_images.append(img)

red_potion = scale_image(pygame.image.load(
    "assets/sprites/Items/potion_red.png").convert_alpha(), POTION_SCALE)

item_images = []
item_images.append(coin_images)
item_images.append(red_potion)

# Load tilemap images
tile_list = []
for n in range(TILE_TYPES):
    tile_image = pygame.image.load(
        f'assets/sprites/tiles/{n}.png').convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
    tile_list.append(tile_image)

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
            image = scale_image(image, ENEMY_SCALE)
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
            if mob == 'Heroes':
                image = scale_image(image, SCALE)
            elif mob == "boss_wraith":
                image = scale_image(image, BOSS_SCALE)
            temp_list.append(image)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

# Create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

# Load in level data and create world
with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

# Create World
world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)

# Create player
# player = Character(400, 300, 100, mob_animations, 6)
player = world.get_player()

# Create weapon
weapon = Weapon(weapon_image, magic_ball_image)

# Create sprite groups
damage_text_group = pygame.sprite.Group()
magic_ball_group = pygame.sprite.Group()

# Create item group
item_group = pygame.sprite.Group()
# potion = Item(200, 200, 1, [red_potion])
# item_group.add(potion)
# coin = Item(400, 400, 0, coin_images)
# item_group.add(coin)

# Add items from level data
for item in world.get_item_list():
    item_group.add(item)


score_coin = Item(SCREEN_WIDTH - 115, 23, 0, coin_images, True)
item_group.add(score_coin)

# Create boss magic ball
bossball_group = pygame.sprite.Group()

# Create enemy
# enemy = Character(300, 300, 100, mob_animations, 0)

# Extract enemies from world data
enemy_list = world.get_enemy_list()
# enemy_list.append(enemy)


# def draw_grid():
#     for x in range(30):
#         pygame.draw.line(screen, WHITE, (x * TILE_SIZE, 0),
#                          (x * TILE_SIZE, SCREEN_HEIGHT))
#         pygame.draw.line(screen, WHITE, (0, x * TILE_SIZE),
#                          (SCREEN_WIDTH, x * TILE_SIZE))

# Create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)

# Create buttons
restart_button = Button(SCREEN_WIDTH // 2 - 175,
                        SCREEN_HEIGHT // 2 - 50, restart_image)
start_button = Button(SCREEN_WIDTH // 2 - 145,
                      SCREEN_HEIGHT // 2 - 150, start_image)
resume_button = Button(SCREEN_WIDTH // 2 - 175,
                       SCREEN_HEIGHT // 2 - 150, resume_image)
exit_button = Button(SCREEN_WIDTH // 2 - 110,
                     SCREEN_HEIGHT // 2 + 50, exit_image)

# Create the game loop
run = True
while run:
    # control frame rate
    clock.tick(FPS)

    if start_game == False:
        screen.fill(MENU_BG)
        start_button.draw(screen)
        exit_button.draw(screen)
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:

        # Check for game pausing
        if pause_game is True:
            screen.fill(MENU_BG)
            if resume_button.draw(screen):
                pause_game = False
            if exit_button.draw(screen):
                run = False
        else:
            screen.fill(BG)

            # draw_grid()

            if player.get_alive():
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
                screen_scroll, level_complete = player.move(
                    dx, dy, world.get_obstacle_tiles(), world.get_exit_tile())

                # Update all objects
                world.update(screen_scroll)

                player.update()
                magic_ball = weapon.update(player)
                if magic_ball:
                    magic_ball_group.add(magic_ball)
                    shot_fx.play()
                for magic_ball in magic_ball_group:
                    damage, damage_position = magic_ball.update(
                        screen_scroll, world.get_obstacle_tiles(), enemy_list)
                    if damage:
                        damage_text = DamageText(
                            damage_position.centerx, damage_position.y, str(damage), RED)
                        damage_text_group.add(damage_text)
                        hit_fx.play()

                # Update damage text
                damage_text_group.update()

                # Update item
                item_group.update(screen_scroll, player, coin_fx, heal_fx)

            # Draw the world
            world.draw(screen)

            # Draw player on screen
            player.draw(screen)
            weapon.draw(screen)
            for magic_ball in magic_ball_group:
                magic_ball.draw(screen)

            # Update enemies
            for enemy in enemy_list:
                boss_ball = enemy.ai(player, world.get_obstacle_tiles(),
                                     screen_scroll, boss_magic_ball_image)
                if boss_ball:
                    bossball_group.add(boss_ball)

                if enemy.get_alive():
                    enemy.update()

            # Draw enemies on screeen
            for enemy in enemy_list:
                enemy.draw(screen)

            # Draw damage text
            damage_text_group.draw(screen)

            bossball_group.update(screen_scroll, player)
            for bossball in bossball_group:
                bossball.draw(screen)

            # print(enemy.get_health())

            # Draw item group
            item_group.draw(screen)

            # Draw info
            draw_heart_info(player, screen, heart_full,
                            heart_half, heart_empty)
            draw_text_info(player, font, screen, level)
            score_coin.draw(screen)

            # Check level complete
            if level_complete is True:
                start_intro = True
                level += 1
                world_data = reset_level(
                    damage_text_group, magic_ball_group, item_group, bossball_group)
                with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter=",")
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                world.process_data(world_data, tile_list,
                                   item_images, mob_animations)
                temp_health = player.get_health()
                temp_score = player.get_score()
                player = world.get_player()
                player.set_health(temp_health)
                player.set_score(temp_score)
                enemy_list = world.get_enemy_list()
                score_coin = Item(SCREEN_WIDTH - 115, 23, 0, coin_images, True)
                item_group.add(score_coin)
                for item in world.get_item_list():
                    item_group.add(item)

            # Show intro
            if start_intro == True:
                if intro_fade.fade(screen):
                    start_intro = False
                    intro_fade.set_fade_counter(0)

            # Show death screen
            if player.get_alive() is False:
                if death_fade.fade(screen):
                    if restart_button.draw(screen):

                        death_fade.set_fade_counter(0)
                        start_intro = True
                        world_data = reset_level(
                            damage_text_group, magic_ball_group, item_group, bossball_group)
                        with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                            reader = csv.reader(csvfile, delimiter=",")
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        world.process_data(world_data, tile_list,
                                           item_images, mob_animations)
                        temp_score = player.get_score()
                        player = world.get_player()
                        player.set_score(temp_score)
                        enemy_list = world.get_enemy_list()
                        score_coin = Item(SCREEN_WIDTH - 115, 23,
                                          0, coin_images, True)
                        item_group.add(score_coin)
                        for item in world.get_item_list():
                            item_group.add(item)

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
            if event.key == pygame.K_ESCAPE:
                pause_game = True

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
