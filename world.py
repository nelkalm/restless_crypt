from character import Character
from items import Item
from constants import TILE_SIZE


class World():

    """A class to represent the World."""

    def __init__(self) -> None:
        self._map_tiles = []
        self._obstacle_tiles = []
        self._exit_tile = None
        self._item_list = []
        self._player = None
        self._enemy_list = []

    def get_item_list(self):
        """Returns the item list."""
        return self._item_list

    def get_player(self):
        """Returns the player."""
        return self._player

    def get_enemy_list(self):
        """Returns the enemy list."""
        return self._enemy_list

    def process_data(self, data, tile_list, item_images, mob_animations):
        """Processes tile data.

        Args:
            data (list): a matrix representation of tile images
            tile_list (list): a list of tile images
        """
        self.level_length = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rectangle = image.get_rect()
                image_x = x * TILE_SIZE
                image_y = y * TILE_SIZE
                image_rectangle.center = (image_x, image_y)
                tile_data = [image, image_rectangle, image_x, image_y]

                # check for obstacle collision
                if tile == 7:
                    self._obstacle_tiles.append(tile_data)
                elif tile == 8:     # check for exit data
                    self._exit_tile = tile_data
                elif tile == 9:
                    coin = Item(image_x, image_y, 0, item_images[0])
                    self._item_list.append(coin)
                    tile_data[0] = tile_list[0]
                elif tile == 10:
                    potion = Item(image_x, image_y, 1, [item_images[1]])
                    self._item_list.append(potion)
                    tile_data[0] = tile_list[0]
                elif tile == 11:
                    player = Character(
                        image_x, image_y, 100, mob_animations, 6, False, 1)
                    self._player = player
                    tile_data[0] = tile_list[0]
                elif tile == 17:
                    enemy = Character(
                        image_x, image_y, 100, mob_animations, 7, True, 1)
                    self._enemy_list.append(enemy)
                    tile_data[0] = tile_list[0]
                # elif tile >= 12 and tile < 17:
                #     enemy = Character(
                #         image_x, image_y, 100, mob_animations, tile - 13, False)
                #     self._enemy_list.append(enemy)
                #     tile_data[0] = tile_list[0]
                elif tile == 13:
                    enemy = Character(
                        image_x, image_y, 100, mob_animations, 0, False, 1)
                    self._enemy_list.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 14:
                    enemy = Character(
                        image_x, image_y, 100, mob_animations, 1, False, 1)
                    self._enemy_list.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 15:
                    enemy = Character(
                        image_x, image_y, 100, mob_animations, 2, False, 1)
                    self._enemy_list.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 16:
                    enemy = Character(
                        image_x, image_y, 100, mob_animations, 3, False, 1)
                    self._enemy_list.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 12:
                    enemy = Character(
                        image_x, image_y, 100, mob_animations, 4, False, 1)
                    self._enemy_list.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 18:
                    enemy = Character(
                        image_x, image_y, 100, mob_animations, 5, False, 1)
                    self._enemy_list.append(enemy)
                    tile_data[0] = tile_list[0]

                # add image data to main tiles list
                if tile >= 0:
                    self._map_tiles.append(tile_data)

    def draw(self, surface):
        """Draws the tile."""
        for tile in self._map_tiles:
            surface.blit(tile[0], tile[1])

    def update(self, screen_scroll):
        """Updates the map in the screen scroll."""
        for tile in self._map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])
