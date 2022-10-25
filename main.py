from asyncio import constants
import pygame
from constants import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Restless Crypt")

# Create the game loop
run = True
while run:

    # Event handling for clicking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
