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
        self.rectangle = self._image.get_rect()
        self._magic_ball_image = magic_ball_image
        self._fired = False
        self._last_shot = pygame.time.get_ticks()

    def update(self, player):
        """Position the weapon at the center of the player.
        Returns an instance of the 'Arrow' every time the mouse is clicked."""
        magic_ball = None
        shot_cooldown = 400

        self.rectangle.center = player.get_rectangle_center()

        pos = pygame.mouse.get_pos()
        x_distance = pos[0] - self.rectangle.centerx
        y_distance = -(pos[1] - self.rectangle.centery)
        self._angle = math.degrees(math.atan2(y_distance, x_distance))

        # get mouse click (left click is 0, right click is 1)
        if pygame.mouse.get_pressed()[0] and self._fired == False and (pygame.time.get_ticks() - self._last_shot) >= shot_cooldown:
            magic_ball = MagicBall(self._magic_ball_image, self.rectangle.centerx,
                                   self.rectangle.centery, self._angle)
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
        surface.blit(self._image, ((self.rectangle.centerx - int(self._image.get_width()/2)),
                     self.rectangle.centery - int(self._image.get_height()/2)))


class MagicBall(pygame.sprite.Sprite):

    """An MagicBall class inherited from the Pygame Sprite module."""

    def __init__(self, image, x, y, angle) -> None:
        pygame.sprite.Sprite.__init__(self)
        self._original_image = image
        self._angle = angle
        self._image = pygame.transform.rotate(
            self._original_image, self._angle)
        self.rectangle = self._image.get_rect()
        self.rectangle.center = (x, y)

        # Calculate horizontal and vertical speed based on the angle
        self._dx = math.cos(math.radians(self._angle)) * MAGIC_SPEED
        self._dy = -math.sin(math.radians(self._angle)) * MAGIC_SPEED

    def draw(self, surface):
        """Draw the MagicBall."""
        surface.blit(self._image, ((self.rectangle.centerx - int(self._image.get_width()/2)),
                     self.rectangle.centery - int(self._image.get_height()/2)))

    def update(self, screen_scroll, obstacle_tiles, enemy_list):
        """Updates magic ball animation."""
        # reset variables
        damage = 0
        damage_position = None

        # Repositioning based on speed
        self.rectangle.x += self._dx + screen_scroll[0]
        self.rectangle.y += self._dy + screen_scroll[1]

        # check for collision between arrow and tile walls:
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rectangle):
                self.kill()

        # Check if magic ball goes off screen
        if self.rectangle.right < 0 or self.rectangle.left > SCREEN_WIDTH or self.rectangle.bottom < 0 or self.rectangle.top > SCREEN_HEIGHT:
            self.kill()

        # Check collision between magicball and enemies
        for enemy in enemy_list:
            if enemy.get_rectangle().colliderect(self.rectangle) and enemy.get_alive():
                damage = 10 + random.randint(-5, 5)
                damage_position = enemy.get_rectangle()
                enemy.change_health(-damage)
                enemy.set_hit(True)
                self.kill()
                break

        return damage, damage_position


class BossBall(pygame.sprite.Sprite):

    """An BossBall class inherited from the Pygame Sprite module."""

    def __init__(self, image, x, y, target_x, target_y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self._original_image = image
        x_distance = target_x - x
        y_distance = -(target_y - y)
        self._angle = math.degrees(math.atan2(y_distance, x_distance))
        self._image = pygame.transform.rotate(
            self._original_image, self._angle)
        self.rectangle = self._image.get_rect()
        self.rectangle.center = (x, y)

        # Calculate horizontal and vertical speed based on the angle
        self._dx = math.cos(math.radians(self._angle)) * BOSS_BALL_SPEED
        self._dy = -math.sin(math.radians(self._angle)) * BOSS_BALL_SPEED

    def draw(self, surface):
        """Draw the MagicBall."""
        surface.blit(self._image, ((self.rectangle.centerx - int(self._image.get_width()/2)),
                     self.rectangle.centery - int(self._image.get_height()/2)))

    def update(self, screen_scroll, player):
        """Updates magic ball animation."""
        # Repositioning boss ball based on speed
        self.rectangle.x += self._dx + screen_scroll[0]
        self.rectangle.y += self._dy + screen_scroll[1]

        # Check if boss ball goes off screen
        if self.rectangle.right < 0 or self.rectangle.left > SCREEN_WIDTH or self.rectangle.bottom < 0 or self.rectangle.top > SCREEN_HEIGHT:
            self.kill()

        # Check collision between boss ball and player
        if player.get_rectangle().colliderect(self.rectangle) and player.get_hit() == False:
            player.set_hit(True)
            player.set_last_hit(pygame.time.get_ticks())
            player.change_health(-10)
            self.kill()
