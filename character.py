import pygame
import math
from weapon import BossBall, Weapon
from constants import *


class Character():

    """A character class representing a character object."""

    def __init__(self, x, y, health, mob_animations, character_type, boss, size) -> None:
        self._rectangle = pygame.Rect(0, 0, TILE_SIZE * size, TILE_SIZE * size)
        self._rectangle.center = (x, y)
        self._character_type = character_type
        self._boss = boss
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
        self._hit = False
        self._last_hit = pygame.time.get_ticks()
        self._last_attack = pygame.time.get_ticks()
        self._stunned = False

    def get_score(self):
        """Returns player score."""
        return self._score

    def set_score(self, value):
        """Sets player score."""
        self._score = value

    def get_hit(self):
        """Returns player hit status."""
        return self._hit

    def set_hit(self, value):
        """Sets hit to a boolean value."""
        self._hit = value

    def set_last_hit(self, value):
        """Sets last hit to a value."""
        self._last_hit = value

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
            surface.blit(flipped_image, (self._rectangle.x - OFFSET * SCALE - 25,
                         self._rectangle.y - OFFSET * SCALE))
        elif self._character_type == 7:
            surface.blit(flipped_image, (self._rectangle.x - OFFSET * BOSS_SCALE + 50,
                         self._rectangle.y - OFFSET * BOSS_SCALE + 65))
        elif self._character_type == 3:
            surface.blit(flipped_image, (self._rectangle.x - OFFSET * ENEMY_SCALE + 165,
                         self._rectangle.y + OFFSET * ENEMY_SCALE - 300))
        elif self._character_type == 1:
            surface.blit(flipped_image, (self._rectangle.x - OFFSET * ENEMY_SCALE + 150,
                         self._rectangle.y + OFFSET * ENEMY_SCALE - 320))
        elif self._character_type == 0:
            surface.blit(flipped_image, (self._rectangle.x - OFFSET * ENEMY_SCALE + 175,
                         self._rectangle.y + OFFSET * ENEMY_SCALE - 300))
        else:
            surface.blit(flipped_image, (self._rectangle.x - OFFSET * ENEMY_SCALE + 200,
                         self._rectangle.y + OFFSET * ENEMY_SCALE - 250))

    def move(self, dx, dy, obstacle_tiles):
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

        # Check collision with map in x direction
        self._rectangle.x += dx
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self._rectangle):
                # check which side collision is from
                if dx > 0:
                    self._rectangle.right = obstacle[1].left
                if dx < 0:
                    self._rectangle.left = obstacle[1].right

        # Check collision with map in y direction
        self._rectangle.y += dy
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self._rectangle):
                # check which side collision is from
                if dy > 0:
                    self._rectangle.bottom = obstacle[1].top
                if dy < 0:
                    self._rectangle.top = obstacle[1].bottom

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

        # timer to reset player taking a hit
        hit_cooldown = 1000
        if self._character_type == 6:
            if self._hit == True and (pygame.time.get_ticks() - self._last_hit) > hit_cooldown:
                self._hit = False

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

    def ai(self, player, obstacle_tiles, screen_scroll, bossball_image):
        """Enables AI behaviors on enemies."""
        bossball = None

        clipped_line = ()

        stun_cooldown = 100

        ai_dx = 0
        ai_dy = 0

        # reposition enemies based on screen scroll
        self._rectangle.x += screen_scroll[0]
        self._rectangle.y += screen_scroll[1]

        # create line of sight from enemy to player
        line_of_sight = ((self._rectangle.centerx, self._rectangle.centery),
                         (player.get_rectangle().centerx, player.get_rectangle().centery))
        # pygame.draw.line(surface, RED, line_of_sight[0], line_of_sight[1])
        # check if line of sight passes through an obstacle tile
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)

        # check distance to player
        distance = math.sqrt(((self._rectangle.centerx - player.get_rectangle().centerx)
                              ** 2) + ((self._rectangle.centery - player.get_rectangle().centery)**2))
        if not clipped_line and distance > RANGE:
            # move enemies toward player
            if self._rectangle.centerx > player.get_rectangle().centerx:
                ai_dx = -ENEMY_SPEED
            if self._rectangle.centerx < player.get_rectangle().centerx:
                ai_dx = ENEMY_SPEED
            if self._rectangle.centery > player.get_rectangle().centery:
                ai_dy = -ENEMY_SPEED
            if self._rectangle.centery < player.get_rectangle().centery:
                ai_dy = ENEMY_SPEED

        if self._alive:
            if not self._stunned:
                # move towards player
                self.move(ai_dx, ai_dy, obstacle_tiles)
                # Attack player
                if distance < ATTACK_RANGE and player._hit == False:
                    player.change_health(-10)
                    player.set_hit(True)
                    player._last_hit = pygame.time.get_ticks()

                # boss enemy shoots bossball
                boss_ball_cooldown = 700
                if self._boss:
                    if distance < 500:
                        if pygame.time.get_ticks() - self._last_attack >= boss_ball_cooldown:
                            bossball = BossBall(
                                bossball_image, self._rectangle.centerx, self._rectangle.centery, player.get_rectangle().centerx, player.get_rectangle().centery)
                            self._last_attack = pygame.time.get_ticks()

            # check if hit
            if self._hit == True:
                self._hit = False
                self._last_hit = pygame.time.get_ticks()
                self._stunned = True
                self._running = False
                self.update_action(0)

            if (pygame.time.get_ticks() - self._last_hit > stun_cooldown):
                self._stunned = False

        return bossball
