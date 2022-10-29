import pygame
import math
import random
from constants import *


class Weapon():

    """A class representing a weapon."""

    def __init__(self, image, magic_ball_image) -> None:
        self._original_image = image
        self._angle = 0
        self._image = pygame.transform.rotate(
            self._original_image, self._angle)
        self._rectangle = self._image.get_rect()
        self._magic_ball_image = magic_ball_image
        self._fired = False
        self._last_shot = pygame.time.get_ticks()

    def update(self, player):
        """Position the weapon at the center of the player.
        Returns an instance of the 'Arrow' every time the mouse is clicked."""
        magic_ball = None
        shot_cooldown = 400

        self._rectangle.center = player.get_rectangle_center()

        pos = pygame.mouse.get_pos()
        x_distance = pos[0] - self._rectangle.centerx
        y_distance = -(pos[1] - self._rectangle.centery)
        self._angle = math.degrees(math.atan2(y_distance, x_distance))

        # get mouse click (left click is 0, right click is 1)
        if pygame.mouse.get_pressed()[0] and self._fired == False and (pygame.time.get_ticks() - self._last_shot) >= shot_cooldown:
            magic_ball = MagicBall(self._magic_ball_image, self._rectangle.centerx,
                                   self._rectangle.centery, self._angle)
            self._fired = True
            self._last_shot = pygame.time.get_ticks()

        # Reset mouse click
        if pygame.mouse.get_pressed()[0] == False:
            self._fired = False

        return magic_ball

    def draw(self, surface):
        """Draw the weapon."""
        self._image = pygame.transform.rotate(
            self._original_image, self._angle)
        surface.blit(self._image, ((self._rectangle.centerx - int(self._image.get_width()/2)),
                     self._rectangle.centery - int(self._image.get_height()/2)))


class MagicBall(pygame.sprite.Sprite):

    """An MagicBall class inherited from the Pygame Sprite module."""

    def __init__(self, image, x, y, angle) -> None:
        pygame.sprite.Sprite.__init__(self)
        self._original_image = image
        self._angle = angle
        self._image = pygame.transform.rotate(
            self._original_image, self._angle)
        self._rectangle = self._image.get_rect()
        self._rectangle.center = (x, y)

        # Calculate horizontal and vertical speed based on the angle
        self._dx = math.cos(math.radians(self._angle)) * MAGIC_SPEED
        self._dy = -math.sin(math.radians(self._angle)) * MAGIC_SPEED

    def draw(self, surface):
        """Draw the MagicBall."""
        surface.blit(self._image, ((self._rectangle.centerx - int(self._image.get_width()/2)),
                     self._rectangle.centery - int(self._image.get_height()/2)))

    def update(self, enemy_list):
        """Updates magic ball animation."""

        # Repositioning based on speed
        self._rectangle.x += self._dx
        self._rectangle.y += self._dy

        # Check if magic ball goes off screen
        if self._rectangle.right < 0 or self._rectangle.left > SCREEN_WIDTH or self._rectangle.bottom < 0 or self._rectangle.top > SCREEN_HEIGHT:
            self.kill()

        # Check collision between magicball and enemies
        for enemy in enemy_list:
            if enemy.get_rectangle().colliderect(self._rectangle) and enemy.get_alive():
                damage = 10 + random.randint(-5, 5)
                enemy.set_health(-damage)
                self.kill()
                break
