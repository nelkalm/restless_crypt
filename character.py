import pygame
import math
from constants import *


class Character():

    """A character class representing a character object."""

    def __init__(self, x, y, health, mob_animations, character_type) -> None:
        self._rectangle = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self._rectangle.center = (x, y)
        self._character_type = character_type
        self._score = 0
        self._animation_list = mob_animations[character_type]
        self._frame_index = 0
        self._action = 0    # 0 = idle, 1 = running
        self._update_time = pygame.time.get_ticks()
        self._running = False
        self._health = health
        self._alive = True
        self._image = self._animation_list[self._action][self._frame_index]
        self._flip = False

    def get_score(self):
        """Returns player score."""
        return self._score

    def set_score(self, value):
        """Sets player score."""
        self._score = value

    def get_rectangle_center(self):
        """Returns the center of the rectangle."""
        return self._rectangle.center

    def get_rectangle(self):
        """Returns the rectangle of the Character."""
        return self._rectangle

    def get_alive(self):
        """Returns the alive status of the Character."""
        return self._alive

    def get_health(self):
        """Returns health of the Character."""
        return self._health

    def set_health(self, value):
        """Sets the health of the Character."""
        self._health = value

    def change_health(self, value):
        """Changes the health of the Character.

        Args:
            value (int): value to increase
        """
        self._health += value

    def increase_score(self, value):
        """Increases the score of the Character.

        Args:
            value (int): value to increase
        """
        self._score += value

    def draw(self, surface):
        """Draw the rectangle onto the screen.

        Args:
            surface (object): the shape to be drawn on the screen
        """
        flipped_image = pygame.transform.flip(self._image, self._flip, False)
        if self._character_type == 6:
            surface.blit(flipped_image, (self._rectangle.x - OFFSET * SCALE - 50,
                         self._rectangle.y - OFFSET * SCALE))
        else:
            surface.blit(flipped_image, (self._rectangle.x - OFFSET * ENEMY_SCALE + 125,
                         self._rectangle.y + OFFSET * SCALE - 90))
        pygame.draw.rect(surface, RED, self._rectangle, 1)

    def move(self, dx, dy):
        """Moves the character by updating the character's coordinates.

        Args:
            dx (int): character's change in x position
            dy (int): character's change in y position
        """
        screen_scroll = [0, 0]

        self._running = False

        if dx != 0 or dy != 0:
            self._running = True

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

        # logic only applicable to player
        if self._character_type == 6:
            # update scroll based on player position
            # move camera left and right
            if self._rectangle.right > (SCREEN_WIDTH - SCROLL_THRES):
                screen_scroll[0] = (
                    SCREEN_WIDTH - SCROLL_THRES) - self._rectangle.right
                self._rectangle.right = SCREEN_WIDTH - SCROLL_THRES
            if self._rectangle.left < SCROLL_THRES:
                screen_scroll[0] = SCROLL_THRES - self._rectangle.left
                self._rectangle.left = SCROLL_THRES

            # move camera up and down
            if self._rectangle.bottom > (SCREEN_HEIGHT - SCROLL_THRES):
                screen_scroll[1] = (
                    SCREEN_HEIGHT - SCROLL_THRES) - self._rectangle.bottom
                self._rectangle.bottom = SCREEN_HEIGHT - SCROLL_THRES
            if self._rectangle.top < SCROLL_THRES:
                screen_scroll[1] = SCROLL_THRES - self._rectangle.top
                self._rectangle.top = SCROLL_THRES

            return screen_scroll

    def update(self):
        """Updates character sprites to generate animation."""
        # Check if character has died
        if self._health <= 0:
            self._health = 0
            self._alive = False

        # Check what action player is performing
        # 1: running, 0: idle
        if self._running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 35
        if self._character_type != 6:
            animation_cooldown = 150
        # Handle animation and update image
        self._image = self._animation_list[self._action][self._frame_index]
        # Check if enough time has passed since last update
        if (pygame.time.get_ticks() - self._update_time) > animation_cooldown:
            self._frame_index += 1
            self._update_time = pygame.time.get_ticks()
        # Check if animation has finished
        if self._frame_index >= len(self._animation_list[self._action]):
            self._frame_index = 0

    def update_action(self, new_action):
        """Updates character action for animation."""
        # Check if the new action is different to the previous one
        if new_action != self._action:
            self._action = new_action

            # update animation settings
            self._frame_index = 0
            self._update_time = pygame.time.get_ticks()

    def ai(self, screen_scroll):

        # reposition enemies based on screen scroll
        self._rectangle.x += screen_scroll[0]
        self._rectangle.y += screen_scroll[1]
