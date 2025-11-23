#imports
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

#set up the sprites
#asteroid group
asteroid_group = pygame.sprite.Group()
#randomise the position of the asteroid so it goes off the screen using a random choice of random range
for a in range(100):
    asteroid_group.add(Asteroid(reset_asteroid()[0],reset_asteroid()[1]))

#player, spawn in the middle
player1 = Player(randint(0,WIDTH), randint(0,HEIGHT),asteroid_group)
explosion = Explosion()
#enemies
easy_enemy = Enemy_Easy(randint(0,WIDTH), randint(0,HEIGHT), player1)
medium_enemy = Enemy_Medium(randint(0,WIDTH), randint(0,HEIGHT))
hard_enemy = Enemy_Hard(randint(0,WIDTH), randint(0,HEIGHT))

#init the joystick
pygame.joystick.init()

#set up different screens (text stuff)
title = Title()
gameover = GameOver()
controls = Controls()
circle = Button('Circle', 'start the game')
square = Button('Square', 'see the controls')
triangle = Button('Triangle','return to menu')
text = Text()

#time related variables
score = 0
time_since_shot = 0
explosion_time = 0
explosion_screentime = 1000
start_time = 0
previous_time_score = 0
time_score = 0
#starting state
state = 'level2'

#start game here
while running:
    #time stuff that changes
    runtime = pygame.time.get_ticks()
    laser_cooldown_time = 1000
    
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #controller setup
        if event.type == pygame.JOYDEVICEADDED:
            controller = pygame.joystick.Joystick(event.device_index)    
        #getting the value of how far the joystick is pushed up, down ,left, right
        try: #using try and excepts so the program works without a controller connected, you just can't move
            left_right = controller.get_axis(0)
            up_down = -controller.get_axis(1) #negative so that moving joystick up is val of positive 1
            right_trigger = controller.get_axis(5)
            controller_connected = True
        except: # if no controller is connected make sure the player doesn't move off the screen
            left_right = 0
            up_down = 0
            right_trigger = 0
    #if the game has started, this where things move
    if state == 'alive':
        previous_time_score = time_score
        time_score += (runtime - start_time)//250 - previous_time_score
        #updates, blitting
        asteroid_group.update()
        try: #all try and excepts are used in case no controller is connected
            player1.update(left_right,up_down,right_trigger)
        except: pass
        text.update_lives(player1.lives)
        screen.blit(background,(-10,0))
        
        #drawing the groups and player
        asteroid_group.draw(screen)
        text.draw(screen)
        #player shoot
        try:
            if controller.get_button(0) == 1:
               #player can only shoot if its been longer than cooldown time
                if runtime - time_since_shot >= laser_cooldown_time:
                    player1.shoot()
                    time_since_shot = runtime
        except: pass
        player1.draw(screen)
        #player hits the asteroid, explosion
        if player1.explode == 1:
            explosion.draw(background,player1.asteroid_collision[0].rect.left -25,player1.asteroid_collision[0].rect.top -25)
            explosion_time = runtime
            score+=1000
            try:
                controller.rumble(0.1,1,500)
            except: pass
        #laser hits the asteroid, explosion
        for l in player1.lasers:
            if l.explode == 1:
                explosion.draw(background,l.asteroid_collision[0].rect.left -25,l.asteroid_collision[0].rect.top -25)
                explosion_time = runtime
                #add 50 points
                score += 50
                try:
                    controller.rumble(0.5,0.5,150)
                except: pass
        #get rid of the explosions
        if runtime - explosion_time < 2000:
            if runtime - explosion_time > explosion_screentime:
                background = make_background()
        
        #optional, uncomment these to show the rects of all objects, also mask of asteroid
        '''#to see asteroid mask
        for a in asteroid_group:
            a.draw(screen)
      #''''''  
        #draw the rects
        for l in player1.lasers:
            pygame.draw.rect(screen,(255,255,255),l.rect,1)
        pygame.draw.rect(screen,(255,255,255),player1.rect,1)
        for a in asteroid_group:
            pygame.draw.rect(screen,(255,255,255),a.rect,1)
    '''
        #update the score in code and on screen
        score += time_score - previous_time_score
        text.update_score(score)
        #if player dies set the state to dead
        if player1.lives <= 0:
            state = 'dead'
        
        #level 2 code
        if score > 1000:
            state = 'level2'
            for a in asteroid_group:
                a.kill()
    
    #player dies, game over screen, allows to go to main menu by pressing triangle
    elif state == 'dead':
        gameover.draw(screen)
        try:
            if controller.get_button(3) ==1:
                state = 'menu'
        except: pass
    #controls screen, allows you to go to menu by pressing triangle, start game pressing circle
    elif state == 'controls':
        background = make_background()
        screen.blit(background,(-10,0))
        controls.draw(screen)
        circle.draw(screen,200)
        triangle.draw(screen,250)
        try:
            if controller.get_button(1) == 1:
                state = 'alive'
            elif controller.get_button(3) ==1:
                state = 'menu'
        except: pass
    #menu screen, start game with circle, controls screen with triangle
    elif state == 'menu':
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
                state = 'alive'
                start_time = runtime
            if controller.get_button(2) == 1:
                state = 'controls'
        except: pass
    #level 2
    elif state == 'level2':
        previous_time_score = time_score
        time_score += (runtime - start_time)//250 - previous_time_score
        #updates, blitting
        try: #all try and excepts are used in case no controller is connected
            player1.update(left_right,up_down,right_trigger)
        except: pass
        text.update_lives(player1.lives)
        screen.blit(background,(-10,0))
        
        #drawing the groups and player
        text.draw(screen)
        player1.draw(screen)
        #player shoot
        try:
            if controller.get_button(0) == 1:
               #player can only shoot if its been longer than cooldown time
                if runtime - time_since_shot >= laser_cooldown_time:
                    player1.shoot()
                    time_since_shot = runtime
        except: pass
        
        #update the score in code and on screen
        score += time_score - previous_time_score
        text.update_score(score)
        easy_enemy.update()
        easy_enemy.draw(screen)
        easy_enemy.shoot()
        
        if runtime - explosion_time < 2000:
            if runtime - explosion_time > explosion_screentime:
                background = make_background()
        
        #if player dies set the state to dead
        if player1.lives <= 0:
            state = 'dead'
    
    #dont touch
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60
pygame.quit()