import pygame
import csv
from constants import *
from helpers import *
from character import Character
from weapon import Weapon
from items import Item
from world import World

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Restless Crypt")

font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

# Create frame rate clock
clock = pygame.time.Clock()

# Define game variables
level = 1
screen_scroll = [0, 0]


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

# Load weapon image
weapon_image = scale_image(pygame.image.load(
    "assets/sprites/Weapons/Empty.png").convert_alpha(), WEAPON_SCALE)

magic_ball_image = scale_image(pygame.image.load(
    "assets/sprites/Weapons/magic_ball.png").convert_alpha(), MAGIC_SCALE)

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
            image = scale_image(image, SCALE)
            temp_list.append(image)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

# Create player
player = Character(400, 300, 100, mob_animations, 6)

# Create weapon
weapon = Weapon(weapon_image, magic_ball_image)

# Create sprite groups
damage_text_group = pygame.sprite.Group()
magic_ball_group = pygame.sprite.Group()

# Create item group
item_group = pygame.sprite.Group()
potion = Item(200, 200, 1, [red_potion])
item_group.add(potion)
coin = Item(400, 400, 0, coin_images)
item_group.add(coin)

score_coin = Item(SCREEN_WIDTH - 115, 23, 0, coin_images, True)
item_group.add(score_coin)

# Create enemy
enemy = Character(300, 300, 100, mob_animations, 0)

# Create empty enemy list
enemy_list = []
enemy_list.append(enemy)

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

world = World()
world.process_data(world_data, tile_list)


# def draw_grid():
#     for x in range(30):
#         pygame.draw.line(screen, WHITE, (x * TILE_SIZE, 0),
#                          (x * TILE_SIZE, SCREEN_HEIGHT))
#         pygame.draw.line(screen, WHITE, (0, x * TILE_SIZE),
#                          (SCREEN_WIDTH, x * TILE_SIZE))


# Create the game loop
run = True
while run:
    # control frame rate
    clock.tick(FPS)

    screen.fill(BG)

    # draw_grid()

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
    screen_scroll = player.move(dx, dy)

    # Update all objects
    world.update(screen_scroll)

    player.update()
    magic_ball = weapon.update(player)
    if magic_ball:
        magic_ball_group.add(magic_ball)
    for magic_ball in magic_ball_group:
        damage, damage_position = magic_ball.update(screen_scroll, enemy_list)
        if damage:
            damage_text = DamageText(
                damage_position.centerx, damage_position.y, str(damage), RED)
            damage_text_group.add(damage_text)

    # Update damage text
    damage_text_group.update()

    # Update item
    item_group.update(screen_scroll, player)

    # Draw the world
    world.draw(screen)

    # Draw player on screen
    player.draw(screen)
    weapon.draw(screen)
    for magic_ball in magic_ball_group:
        magic_ball.draw(screen)

    # Update enemies
    for enemy in enemy_list:
        enemy.ai(screen_scroll)
        enemy.update()

    # Draw enemies on screeen
    for enemy in enemy_list:
        enemy.draw(screen)

    # Draw damage text
    damage_text_group.draw(screen)

    # print(enemy.get_health())

    # Draw item group
    item_group.draw(screen)

    # Draw info
    draw_heart_info(player, screen, heart_full, heart_half, heart_empty)
    draw_text_info(player, font, screen)
    score_coin.draw(screen)

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
