# Example file showing a basic pygame "game loop"
import pygame
from params import *
from background import make_background
from characters import *
from random import randint, choice
# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
background = make_background()

######moving pieces
asteroid1 = Asteroid(randint(0,WIDTH), randint(0,HEIGHT))
player1 = Player(randint(0,WIDTH),randint(0,HEIGHT))
easy_enemy = Enemy_Easy(randint(0,WIDTH), randint(0,HEIGHT))
medium_enemy = Enemy_Medium(randint(0,WIDTH), randint(0,HEIGHT))
hard_enemy = Enemy_Hard(randint(0,WIDTH), randint(0,HEIGHT))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background,(0,0))
    ######### RENDER YOUR GAME HERE ########################
    asteroid1.draw(screen)
    player1.draw(screen)
    easy_enemy.draw(screen)
    medium_enemy.draw(screen)
    hard_enemy.draw(screen)
   
   
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()