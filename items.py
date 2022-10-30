import pygame


class Item(pygame.sprite.Sprite):

    """A class representing an Item."""

    def __init__(self, x, y, item_type, animation_list) -> None:
        pygame.sprite.Sprite.__init__(self)
        self._item_type = item_type     # 0: coin, 1: health potion
        self._animation_list = animation_list
        self._frame_index = 0
        self._update_time = pygame.time.get_ticks()
        self.image = self._animation_list[self._frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, player) -> None:
        """Updates item sprites to generate animation and handle collision.

        Args:
            player (object): the Player object
        """
        animation_cooldown = 150
        self.image = self._animation_list[self._frame_index]
        # Check if enough time has passed since last update
        if (pygame.time.get_ticks() - self._update_time) > animation_cooldown:
            self._frame_index += 1
            self._update_time = pygame.time.get_ticks()
        # Check if animation has finished
        if self._frame_index >= len(self._animation_list):
            self._frame_index = 0

        # Check if item has been collected
        if self.rect.colliderect(player.get_rectangle()):
            # coin collected
            if self._item_type == 0:
                player.increase_score(1)
            # potion collected
            elif self._item_type == 1:
                player.change_health(10)
                if player.get_health() > 100:
                    player.change_health(0)
            self.kill()

    def draw(self, surface):
        """Draws item."""
        surface.blit(self.image, self.rect)
