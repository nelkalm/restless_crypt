import pygame
import math
from constants import *


class Character():

    """A character class representing a character object."""

    def __init__(self, x, y) -> None:
        self.rectangle = pygame.Rect(0, 0, 50, 50)
        self.rectangle.center = (x, y)

    def draw(self, surface):
        """Draw the rectangle onto the screen.

        Args:
            surface (object): the shape to be drawn on the screen
        """
        pygame.draw.rect(surface, RED, self.rectangle)

    def move(self, dx, dy):
        """Moves the character by updating the character's coordinates

        Args:
            dx (int): character's change in x position
            dy (int): character's change in y position
        """
        # Diagonal movement control
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)
        self.rectangle.x += dx
        self.rectangle.y += dy
