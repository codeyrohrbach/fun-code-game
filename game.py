# Example file showing a basic pygame "game loop"
import pygame
from params import *
from background import make_background
from characters import *
from random import randint, choice
from text import *
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
for a in range(14):
    asteroid_group.add(Asteroid(choice([randint(-100,0),randint(WIDTH,WIDTH+100)]), choice([randint(-100,0),randint(HEIGHT,HEIGHT+100)])))

#player
player1 = Player(randint(0,WIDTH),randint(0,HEIGHT))

#enemies
easy_enemy = Enemy_Easy(randint(0,WIDTH), randint(0,HEIGHT))
medium_enemy = Enemy_Medium(randint(0,WIDTH), randint(0,HEIGHT))
hard_enemy = Enemy_Hard(randint(0,WIDTH), randint(0,HEIGHT))
##############
#init the joystick stuff
pygame.joystick.init()

text = Text()

while running:
    score = pygame.time.get_ticks()//100
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #controller
        if event.type == pygame.JOYDEVICEADDED:
            controller = pygame.joystick.Joystick(event.device_index)    
        #getting the value of how far the joystick is pushed up, down ,left, right
    left_right = controller.get_axis(0)
    up_down = -controller.get_axis(1) #negative so that moving joystick up is val of positive 1
    right_trigger = controller.get_axis(5)
    #updates, blitting
    asteroid_group.update()
    player1.update(left_right,up_down,right_trigger)
    text.update_score(score)
    screen.blit(background,(0,0))
    screen.blit(background,(1111,0))
    
    #drawing the groups and player
    text.draw(screen)
    asteroid_group.draw(screen)
    player1.draw(screen)

   
   
    #dont touch
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60
pygame.quit()