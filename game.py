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
easy_enemy = Enemy_Easy(randint(0,WIDTH), randint(0,HEIGHT), player1, 'assets/images/Enemies/enemyBlack1.png')

#enemy group
enemy_group = pygame.sprite.Group()
for e in range (3):
    enemy_group.add(Enemy_Easy(reset_asteroid()[0],reset_asteroid()[1], player1, 'assets/images/Enemies/enemyBlack1.png'))

player1.enemy_group = enemy_group
#init the joystick
pygame.joystick.init()

#set up different screens (text stuff)
title = Title()
gameover = GameOver()
controls = Controls()
circle = Button('Circle', 'Play Asteroid Avoidance')
square = Button('Square', 'see the controls')
triangle = Button('Triangle','return to menu')
cross = Button('X','Play Gunship Attack')
text = Text()
wavetxt = Wave()
#sound stuff
good_laser_sound = pygame.mixer.Sound('assets/Audio/laserSmall_002.ogg')
bad_laser_sound = pygame.mixer.Sound('assets/Audio/laserSmall_001.ogg')
explosion_sound1 = pygame.mixer.Sound('assets/Audio/explosionCrunch_001.ogg')
explosion_sound2 = pygame.mixer.Sound('assets/Audio/explosionCrunch_003.ogg')
explosion_sound1.set_volume(0.15)
explosion_sound2.set_volume(0.15)
#time related variables
score = 0
time_since_shot = 0
enemy_time_since_shot = 0
explosion_time = 0
explosion_screentime = 750
start_time = 0
previous_time_score = 0
time_score = 0
time_since_tracked = 0
laser_cooldown_time = 650
tracking = 0
wave = 0
enemies = 0
enemy_type = 'easy'
#starting state
state = 'menu'
#start game here
while running:
    #time stuff that changes
    runtime = pygame.time.get_ticks()
    
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
            print('exception in game')
    #if the game has started, this where things move
    if state == 'level1':
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
                    good_laser_sound.play()
        except: pass
        player1.draw(screen)
        #player hits the asteroid, explosion
        if player1.explode == 1:
            explosion.draw(background,player1.asteroid_collision[0].rect.left -25,player1.asteroid_collision[0].rect.top -25)
            explosion_time = runtime
            explosion_sound1.play()
            try:
                controller.rumble(0.1,1,500)
            except: pass
        #laser hits the asteroid, explosion
        for l in player1.lasers:
            if l.explode == 1:
                explosion.draw(background,l.asteroid_collision[0].rect.left -25,l.asteroid_collision[0].rect.top -25)
                explosion_time = runtime
                explosion_sound2.play()
                #add 50 points
                score += 50
                try:
                    controller.rumble(0.5,0.5,150)
                except: pass
        #get rid of the explosions
        if runtime - explosion_time < 2000:
            if runtime - explosion_time > explosion_screentime:
                background = make_background()
        

        #update the score in code and on screen
        score += time_score - previous_time_score
        text.update_score(score)
        
        for a in asteroid_group:
            if a.vx > 0:
                a.vx += time_score/45000
            elif a.vx < 0:
                a.vx -= time_score/45000
            if a.vy > 0:
                a.vy += time_score/45000
            elif a.vy < 0:
                a.vy -= time_score/45000
            
        
        #if player dies set the state to dead
        if player1.lives <= 0:
            state = 'dead'
            
    
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
        cross.draw(screen,250)
        triangle.draw(screen,300)
        try:
            if controller.get_button(1) == 1:
                state = 'level1'
                start_time = runtime
                reset_game(asteroid_group,enemy_group,player1)
                time_score = 0
            if controller.get_button(3) ==1:
                state = 'menu'
            if controller.get_button(0) == 1:
                state = 'level2'
                reset_game(asteroid_group,enemy_group,player1)
                enemies = 0 
                wave = 0
                enemy_type = 'easy'
        except: pass
    #menu screen, start game with circle, controls screen with triangle
    elif state == 'menu':
        background = make_background()
        screen.blit(background,(-10,0))
        title.draw(screen)
        circle.draw(screen,100)
        square.draw(screen,300)
        cross.draw(screen,150)
        for a in asteroid_group:
            a.x = reset_asteroid()[0]
            a.y = reset_asteroid()[1]
        player1.lives = 3
        score = 0
        player1.x = WIDTH//2
        player1.y = HEIGHT//2
        try:
            if controller.get_button(1) == 1:
                state = 'level1'
                time_score = 0
                start_time = runtime
                reset_game(asteroid_group,enemy_group,player1)
            if controller.get_button(2) == 1:
                state = 'controls'
            if controller.get_button(0) == 1:
                state = 'level2'
                reset_game(asteroid_group,enemy_group,player1)
                enemies = 0 
                wave = 0
                enemy_type = 'easy'
        except: pass
    #level 2
    elif state == 'level2':
        try:
            for a in asteroid_group:
                a.kill()
        except: pass
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
                    good_laser_sound.play()
                    time_since_shot = runtime
        except: pass
        
        #update the score in code and on screen
        score += time_score - previous_time_score
        text.update_score(score)
        #enemy movement code
        for e in enemy_group:
            e.update()
            e.draw(screen)
        
        #explosion code
        if player1.explode == 1:
            explosion.draw(background,player1.enemy_collision[0].rect.left -25,player1.enemy_collision[0].rect.top -25)
            explosion_time = runtime
            explosion_sound1.play()
            try:
                controller.rumble(0.1,1,500)
            except: pass
        if player1.hit == 1:
            try:
                explosion.draw(background,player1.enemy_laser_collision[0].rect.left -25,player1.enemy_laser_collision[0].rect.top -25)
                explosion_time = runtime
                explosion_sound1.play()
                controller.rumble(0.1,1,500)
            except: pass
        if runtime - explosion_time < 2000:
            if runtime - explosion_time > explosion_screentime:
                background = make_background()
        #players laser hits the enemy, explosion
        for l in player1.lasers:
            if l.explode == 1:
                explosion_sound2.play()
                try:
                    explosion.draw(background,l.enemy_collision[0].rect.left -25,l.enemy_collision[0].rect.top -25)
                except:
                    pass
                explosion_time = runtime
                #add points
                if enemy_type == 'easy':
                    score += 100
                if enemy_type == 'medium':
                    score += 200
                if enemy_type == 'hard':
                    score += 300
                try:
                    controller.rumble(0.5,0.5,150)
                except: pass
        #waves code
        if len(enemy_group) == 0:
            wave += 1
            player1.lives +=1
            file = enemy_waves(wave)[0]
            enemies = enemy_waves(wave)[1]
            enemy_type = enemy_waves(wave)[2]
            for e in range (enemies):
                enemy_group.add(Enemy_Easy(reset_asteroid()[0],reset_asteroid()[1], player1, file))
            for e in enemy_group:
                if enemy_type == 'easy':
                    e.speed = 3
                if enemy_type == 'medium':
                    e.speed = 4
                if enemy_type == 'hard':
                    e.speed = 5
                if enemy_type == 'extreme':
                    e.speed = 6
        
        wavetxt.draw(screen, wave)
        
        #if player dies set the state to dead
        if player1.lives <= 0:
            state = 'dead'
    
    
    #dont touch
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60
pygame.quit()