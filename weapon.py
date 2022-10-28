import pygame


class Weapon():

    """A class representing a weapon."""

    def __init__(self, image) -> None:
        self._original_image = image
        self._angle = 0
        self._image = pygame.transform.rotate(
            self._original_image, self._angle)
        self._rectangle = self._image.get_rect()

    def update(self, player):
        """Position the weapon at the center of the player."""
        self._rectangle.center = player.get_rectangle_center()

    def draw(self, surface):
        """Draw the weapon."""
        surface.blit(self._image, self._rectangle)


class
