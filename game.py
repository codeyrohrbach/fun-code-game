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
#asteroid group
asteroid_group = pygame.sprite.Group()
#randomise the position of the asteroid so it goes off the screen using a random choice of random range
for a in range(8):
    asteroid_group.add(Asteroid(choice([randint(-100,0),randint(WIDTH,WIDTH+100)]), choice([randint(-100,0),randint(HEIGHT,HEIGHT+100)])))

#player
player1 = Player(randint(0,WIDTH),randint(0,HEIGHT))

#enemies
easy_enemy = Enemy_Easy(randint(0,WIDTH), randint(0,HEIGHT))
medium_enemy = Enemy_Medium(randint(0,WIDTH), randint(0,HEIGHT))
hard_enemy = Enemy_Hard(randint(0,WIDTH), randint(0,HEIGHT))


##############

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    asteroid_group.update()
    #ERROR: the background doesn't fill the screen so when
    #you update the asteroids the old one doesnt get covered up by the background
    screen.blit(background,(0,0))
    screen.blit(background,(1111,0))
    ######### RENDER YOUR GAME HERE ########################
    
    asteroid_group.draw(screen)
    player1.draw(screen)

   
   

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()