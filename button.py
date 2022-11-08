import pygame


class Button():

    """A class representing a Button."""

    def __init__(self, x, y, image) -> None:
        self._image = image
        self.rectangle = self._image.get_rect()
        self.rectangle.topleft = (x, y)

    def draw(self, surface):
        """Draw the button and returns the boolean result of user.
        initiated action.

        Args:
            surface (object): The surface object to draw on.

        Returns:
            bool: True if the action is initiated. False otherwise.
        """
        action = False

        # Get mouse position
        position = pygame.mouse.get_pos()

        # Check mouseover and clicked condition
        if self.rectangle.collidepoint(position):
            if pygame.mouse.get_pressed()[0]:
                action = True

        surface.blit(self._image, self.rectangle)

        return action
