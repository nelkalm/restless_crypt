import pygame
from constants import *


class ScreenFade():

    """A class for handling screen fade."""

    def __init__(self, fade_type, color, speed) -> None:
        self._fade_type = fade_type
        self._color = color
        self._speed = speed
        self._fade_counter = 0

    def set_fade_counter(self, value):
        """Sets the fade counter to specified value."""
        self._fade_counter = value

    def fade(self, screen):
        """Creates a screen fade effect.

        Args:
            screen (object): the screen game drawn.

        Returns:
            bool: True if the screen fade is completed. False otherwise.
        """
        fade_complete = False

        self._fade_counter += self._speed
        if self._fade_type == 1:
            pygame.draw.rect(screen, self._color,
                             (0 - self._fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self._color,
                             (SCREEN_WIDTH // 2 + self._fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self._color,
                             (0, 0 - self._fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self._color,
                             (0, SCREEN_HEIGHT // 2 + self._fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        elif self._fade_type == 2:  # vertical screen fade down
            pygame.draw.rect(screen, self._color,
                             (0, 0, SCREEN_WIDTH, 0 + self._fade_counter))

        if self._fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete
