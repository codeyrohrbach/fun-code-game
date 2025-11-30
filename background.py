import pygame
#making the background using drawn image, returns the pygame image
def make_background():
    background_loc = 'assets/bg2.png'
    background = pygame.image.load(background_loc)
    return background