import pygame


def scale_image(image, scale):
    """Returns the scaled image of the specified image based on the 
    specified scale factor.

    Args:
        image (object): the image object needed to be scale
        scale (int/float): the scaling factor

    Returns:
        object: A scaled image object
    """
    width = image.get_width()
    height = image.get_height()
    return pygame.transform.scale(image, (width * scale, height * scale))
