import pygame
import math
from constants import *


class Character():

    """A character class representing a character object."""

    def __init__(self, x, y, animation_list) -> None:
        self._rectangle = pygame.Rect(0, 0, 50, 50)
        self._rectangle.center = (x, y)
        self._animation_list = animation_list
        self._frame_index = 0
        self._action = 0    # 0 = idle, 1 = running
        self._update_time = pygame.time.get_ticks()
        self._image = animation_list[self._action][self._frame_index]
        self._flip = False

    def draw(self, surface):
        """Draw the rectangle onto the screen.

        Args:
            surface (object): the shape to be drawn on the screen
        """
        flipped_image = pygame.transform.flip(self._image, self._flip, False)
        surface.blit(flipped_image, self._rectangle)
        pygame.draw.rect(surface, RED, self._rectangle, 1)

    def move(self, dx, dy):
        """Moves the character by updating the character's coordinates.

        Args:
            dx (int): character's change in x position
            dy (int): character's change in y position
        """
        if dx < 0:
            self._flip = True
        if dx > 0:
            self._flip = False

        # Diagonal movement control
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        self._rectangle.x += dx
        self._rectangle.y += dy

    def update(self):
        """Updates character sprites to generate animation."""
        animation_cooldown = 35
        # Handle animation and update image
        self._image = self._animation_list[self._action][self._frame_index]
        # Check if enough time has passed since last update
        if (pygame.time.get_ticks() - self._update_time) > animation_cooldown:
            self._frame_index += 1
            self._update_time = pygame.time.get_ticks()
        # Check if animation has finished
        if self._frame_index >= len(self._animation_list[self._action]):
            self._frame_index = 0
