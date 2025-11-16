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
for a in range(100):
    asteroid_group.add(Asteroid(reset_asteroid()[0],reset_asteroid()[1]))

#player
player1 = Player(WIDTH//2,HEIGHT//2,asteroid_group)
explosion = Explosion()
#enemies
easy_enemy = Enemy_Easy(randint(0,WIDTH), randint(0,HEIGHT))
medium_enemy = Enemy_Medium(randint(0,WIDTH), randint(0,HEIGHT))
hard_enemy = Enemy_Hard(randint(0,WIDTH), randint(0,HEIGHT))
##############
#init the joystick stuff
pygame.joystick.init()
title = Title()
gameover = GameOver()
controls = Controls()
circle = Button('Circle', 'start the game')
square = Button('Square', 'see the controls')
triangle = Button('Triangle','return to menu')
text = Text()
score = 0
time_since_shot = 0
explosion_time = 0
explosion_screentime = 1000
started = 0
while running:
    #time stuff
    runtime = pygame.time.get_ticks()
    laser_cooldown_time = 1000
    score = runtime//200
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #controller
        if event.type == pygame.JOYDEVICEADDED:
            controller = pygame.joystick.Joystick(event.device_index)    
        #getting the value of how far the joystick is pushed up, down ,left, right
        try:
            left_right = controller.get_axis(0)
            up_down = -controller.get_axis(1) #negative so that moving joystick up is val of positive 1
            right_trigger = controller.get_axis(5)
            controller_connected = True
        except:
            left_right = 0
            up_down = 0
            right_trigger = 0
    if started == 1:
        #updates, blitting
        asteroid_group.update()
        try:
            player1.update(left_right,up_down,right_trigger)
        except: pass
        text.update_score(score)
        text.update_lives(player1.lives)
        screen.blit(background,(-10,0))
        
        #drawing the groups and player
        asteroid_group.draw(screen)
        text.draw(screen)
        try:
            if controller.get_button(0) == 1:
                if runtime - time_since_shot >= laser_cooldown_time:
                    player1.shoot()
                    time_since_shot = runtime
        except: pass
        player1.draw(screen)
        if player1.explode == 1:
            explosion.draw(background,player1.asteroid_collision[0].rect.left -25,player1.asteroid_collision[0].rect.top -25)
            explosion_time = runtime
            try:
                controller.rumble(0.1,1,500)
            except: pass
        for l in player1.lasers:
            if l.explode == 1:
                explosion.draw(background,l.asteroid_collision[0].rect.left -25,l.asteroid_collision[0].rect.top -25)
                explosion_time = runtime
                try:
                    controller.rumble(0.5,0.5,150)
                except: pass
        #get rid of the explosions
        if runtime - explosion_time < 2000:
            if runtime - explosion_time > explosion_screentime:
                background = make_background()
        '''#to see asteroid mask
        for a in asteroid_group:
            a.draw(screen)'''
        '''
        #draw the rects
        for l in player1.lasers:
            pygame.draw.rect(screen,(255,255,255),l.rect,1)
        pygame.draw.rect(screen,(255,255,255),player1.rect,1)
        for a in asteroid_group:
            pygame.draw.rect(screen,(255,255,255),a.rect,1)
    '''
        #if player dies go to game over screen
        if player1.lives <= 0:
            started = 3
    #player dies, game over screen, allows to go to main menu by pressing triangle
    elif started == 3:
        gameover.draw(screen)
        try:
            if controller.get_button(3) ==1:
                started = 0
        except: pass
    #controls screen
    elif started == 4:
        background = make_background()
        screen.blit(background,(-10,0))
        controls.draw(screen)
        circle.draw(screen,200)
        triangle.draw(screen,250)
        try:
            if controller.get_button(1) == 1:
                started = 1
            elif controller.get_button(3) ==1:
                started = 0
        except: pass
    #game hasn't started / just reset
    else:
        background = make_background()
        screen.blit(background,(-10,0))
        title.draw(screen)
        circle.draw(screen,100)
        square.draw(screen,150)
        for a in asteroid_group:
            a.x = reset_asteroid()[0]
            a.y = reset_asteroid()[1]
        player1.lives = 3
        score = 0
        player1.x = WIDTH//2
        player1.y = HEIGHT//2
        try:
            if controller.get_button(1) == 1:
                started = 1
            if controller.get_button(2) == 1:
                started = 4
        except: pass
    #dont touch
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60
pygame.quit()