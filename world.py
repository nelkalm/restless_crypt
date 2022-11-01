import enum

from constants import TILE_SIZE


class World():

    """A class to represent the World."""

    def __init__(self) -> None:
        self._map_tiles = []

    def process_data(self, data, tile_list):
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

                # add image data to main tiles list
                if tile >= 0:
                    self._map_tiles.append(tile_data)

    def draw(self, surface):
        """Draws the tile."""
        for tile in self._map_tiles:
            surface.blit(tile[0], tile[1])
