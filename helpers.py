import pygame
from constants import *


def scale_image(image, scale):
    """Returns the scaled image of the specified image based on the 
    specified scale factor.

    Args:
        image (object): the image object needed to be scale
        scale (int/float): the scaling factor

    Returns:
        object: A scaled image object
    """
    width = image.get_width()
    height = image.get_height()
    return pygame.transform.scale(image, (width * scale, height * scale))


def draw_heart_info(player, screen, heart_full, heart_half, heart_empty):
    """Displays player heart information."""
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 50))
    pygame.draw.line(screen, WHITE, (0, 50), (SCREEN_WIDTH, 50))

    half_heart_drawn = False

    # draw lives
    for i in range(5):
        # if full health
        if player.get_health() >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        # if half health
        elif (player.get_health() % 20 > 0) and not half_heart_drawn:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))


def draw_text(text, font, text_color, x, y, screen):
    """Outputs text onto the screen."""
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


def draw_text_info(player, font, screen, level):
    """Displays text onto the screen."""
    draw_text("LEVEL: " + str(level), font,
              WHITE, SCREEN_WIDTH / 2, 15, screen)

    draw_text(f"X{player.get_score()}",
              font, WHITE, SCREEN_WIDTH - 100, 15, screen)


def reset_level(damage_text_group, magic_ball_group, item_group, boss_ball_group):
    damage_text_group.empty()
    magic_ball_group.empty()
    item_group.empty()
    boss_ball_group.empty()

    # create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data
