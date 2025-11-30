#imports
import pygame
from random import randint, choice
from params import *
import math
from math import radians, cos, sin

#asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x,y,size=1):
        pygame.sprite.Sprite.__init__(self)
        self.assets = [
            'assets/images/Meteors/meteorBrown_big1.png',
            'assets/images/Meteors/meteorBrown_big2.png',
            'assets/images/Meteors/meteorBrown_big3.png',
            'assets/images/Meteors/meteorBrown_big4.png'
        ]
        #randomise what the asteroids look like
        self.file_path = choice(self.assets)
        #set up image and randomise the size of each asteroid
        self.image = pygame.image.load(self.file_path)
        self.image = pygame.transform.rotozoom(self.image,0,randint(40,100)/100)
        #get rect
        self.rect = self.image.get_rect()
        #coordinates
        self.x = x
        self.y = y
        self.size = size
        self.rect.center = (x,y)
        #randomise the speed of the asteroids
        self.vx = randint(-2000,2000)/750
        self.vy = randint(-2000,2000)/750

        #asteroid mask
        self.mask = pygame.mask.from_surface(self.image)
        #so i can see the mask
        self.mask_image = self.mask.to_surface()
    #putting the asteroids onto the screen
    def draw(self,screen):
        screen.blit(self.image, self.rect)
        #add the mask, uncomment line in game.py to see the mask
        screen.blit(self.mask_image,self.rect)
    #updating each asteroid
    def update(self):
        #move it the amount of vx and vy
        self.x += self.vx
        self.y += self.vy
        #recenter rect
        self.rect.center = (self.x,self.y)

        #if the asteroid moves off the screen, reset it to a random point off the screen
        if self.rect.left < -200 or self.rect.right > WIDTH+200 or self.rect.top < -200 or self.rect.bottom >HEIGHT+200:
            #randomise where it gets moved to
            self.x = reset_asteroid()[0]
            self.y = reset_asteroid()[1]
            #randomise the direction of asteroid (makes it seem like a new asteroid)
            self.vx = randint(-1000,1000)/750
            self.vy = randint(-1000,1000)/750
#function used to reset asteroid, randomises a spot off screen for it to spawn, returns (x,y)
def reset_asteroid():
    return (choice([randint(-100,0),randint(WIDTH,WIDTH+100)]), choice([randint(-100,0),randint(HEIGHT,HEIGHT+100)]))

def reset_game(asteroid_group, enemy_group,player1):
    for a in asteroid_group:
        a.kill()
    for a in range(100):
        asteroid_group.add(Asteroid(reset_asteroid()[0],reset_asteroid()[1]))
    for e in enemy_group:
        e.kill()
    for e in range (5):
        enemy_group.add(Enemy_Easy(reset_asteroid()[0],reset_asteroid()[1], player1, 'assets/images/Enemies/enemyBlack1.png'))
def enemy_waves(wave):
    if wave > 8:
        enemy_type = 'extreme'
        file = 'assets/images/Enemies/enemyBlack2.png'
        enemies = 8
    elif wave > 7:
        enemy_type = 'hard'
        file = 'assets/images/Enemies/enemyBlack4.png'
        enemies = 8
    elif wave > 5:
        enemy_type = 'hard'
        file = 'assets/images/Enemies/enemyBlack4.png'
        enemies = 7
    elif wave > 4:
        enemy_type = 'medium'
        file = 'assets/images/Enemies/enemyBlack5.png'
        enemies = 7
    elif wave > 2:
        enemy_type = 'medium'
        file = 'assets/images/Enemies/enemyBlack5.png'
        enemies = 6
    elif wave > 1:
        enemy_type = 'easy'
        file = 'assets/images/Enemies/enemyBlack1.png'
        enemies = 6
    else:    
        file = 'assets/images/Enemies/enemyBlack1.png'
        enemies = 5
        enemy_type = 'easy'
    return file, enemies, enemy_type

#player class
class Player:
    def __init__(self,x,y,asteroid_group):
        #init stuff
        self.file_path = 'assets/images/playerShip1_blue.png'
        self.og_image = pygame.image.load(self.file_path)
        self.rect = self.og_image.get_rect()
        self.boost_sound = pygame.mixer.Sound('assets/Audio/spaceEngineLow_000.ogg')
        self.boost_sound.set_volume(0.12)
        self.asteroid_group = asteroid_group
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.enemy_group = 0
        #change to change base lives
        self.lives = 3
        self.rect.center = (x,y)
        self.ogspeed = 5
        self.boost_speed = 7
        #laser code
        self.lasers = pygame.sprite.Group()
        
        #making a mask from the ship
        self.og_mask = pygame.mask.from_surface(self.og_image)
        #give the mask a surface so i can see the mask
        self.og_mask_image = self.og_mask.to_surface()
        
        #putting it on the screen
    def draw(self,screen):
        #rotates the ship, need a try and except in case a controller isn't connected, there wouldn't be a theta
        try:
            self.image = pygame.transform.rotozoom(self.og_image, math.degrees(self.theta)+90,0.6)
        except:
            self.image = self.og_image

        #update the rect and add player to the screen
        self.rect = self.image.get_rect(center=self.rect.center)
        screen.blit(self.image, self.rect)

        #rotates the mask with the ship
        try:
            self.mask_image = pygame.transform.rotozoom(self.og_mask_image, math.degrees(self.theta)+90,0.6)
        except:
            self.mask_image = self.og_mask_image
        
        #for testing, draws the mask, uncomment to see mask
        #screen.blit(self.mask_image,self.rect)
        
        #drawing the lasers
        for s in self.lasers:
            s.draw(screen)
    #code to get the direction of the player (gives theta used for player and laser stuff)
    def get_theta(self):
        # get our theta based on our vx and vy
        self.theta = math.atan2(self.vy,-self.vx)     
        
        #updating
    def update(self, left_right, up_down, right_trigger,screen=None):
        #variable explode to change if player hits asteroid
        self.explode = False
        self.hit = False
        self.speed = self.ogspeed
        #boost button, if right trigger pushed down then increase speed
        if right_trigger > 0.5:
            self.speed = self.boost_speed
            self.boost_sound.play(0,50)

        #takes the values of joysticks and sets vx and vy equal to it
        self.vx = left_right *self.speed
        self.get_theta()
        self.vy = -up_down *self.speed
        #moving the ship
        self.x += self.vx
        self.y += self.vy
        #update the rect
        self.rect.center = (self.x,self.y)

        #collision with asteroid
        #checking for rect collision
        if pygame.sprite.spritecollide(self,self.asteroid_group,0):
            #checking for mask collision
            self.asteroid_collision = pygame.sprite.spritecollide(self,self.asteroid_group,0,pygame.sprite.collide_mask)
            if self.asteroid_collision:
                #take a life away
                self.lives -=1
                #set explode = true so can check for it in game file
                self.explode = True
            # reset asteroid using the function I created earlier
                for f in self.asteroid_collision:
                    f.x = reset_asteroid()[0]
                    f.y = reset_asteroid()[1]
        #collision with enemy
        #checking for rect collision
        if pygame.sprite.spritecollide(self,self.enemy_group,0):
            #checking for mask collision
            self.enemy_collision = pygame.sprite.spritecollide(self,self.enemy_group,0,pygame.sprite.collide_mask)
            if self.enemy_collision:
                #take a life away
                self.lives -=1
                #set explode = true so can check for it in game file
                self.explode = True
            # kill enemy
                for e in self.enemy_collision:
                    e.kill()
        for e in self.enemy_group:
            #checking for rect collision
            if pygame.sprite.spritecollide(self,e.bad_lasers,0):
                #checking for mask collision
                self.enemy_laser_collision = pygame.sprite.spritecollide(self,e.bad_lasers,0,pygame.sprite.collide_mask)
                if self.enemy_laser_collision:
                    #take a life away
                    self.lives -=1
                    #set explode = true so can check for it in game file
                    self.hit = True
                # reset asteroid using the function I created earlier
                    for l in e.bad_lasers:
                        l.x = WIDTH +150


        #update the lasers
        self.lasers.update()
    #player shooting
    def shoot(self):
        #create a new laser at the players point with players theta, add it to spritegroup
        new_laser = Laser(self.rect.center,self.theta,self.asteroid_group,'assets/images/Lasers/laserBlue01.png')
        new_laser.enemy_group = self.enemy_group
        self.lasers.add(new_laser)

#laser code, sprite
class Laser(pygame.sprite.Sprite):
    def __init__(self,coordinates,theta,asteroid_group,fp):
        super().__init__()
        #init stuff
        self.file_path = fp
        #'assets/images/Lasers/laserBlue01.png'
        self.image = pygame.image.load(self.file_path)
        self.theta = theta
        self.speed = 20
        self.vx = -self.speed* cos(self.theta)
        self.vy = self.speed* sin(self.theta)
        self.rect = self.image.get_rect()
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.enemy_group = asteroid_group
        self.rect.center = (coordinates)
        #mask stuff
        self.og_mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.og_mask.to_surface()
        
        self.asteroid_group = asteroid_group
        self.explode = False
    #updating lasers
    def update(self):
        self.x += -self.speed* cos(self.theta)
        self.y += self.speed* sin(self.theta)
        #if the laser goes off the screen, kill it
        if self.x>WIDTH+100 or self.x<-100 or self.y>HEIGHT+100 or self.y<-100:
            self.kill()

        #checking if laser hits an asteroid
        if pygame.sprite.spritecollide(self,self.asteroid_group,0):
            #check if it hits using mask
            self.asteroid_collision = pygame.sprite.spritecollide(self,self.asteroid_group,0,pygame.sprite.collide_mask)
            if self.asteroid_collision:
                #so the game will draw explosion, same as with player's self.explode
                self.explode = True
                #move the laser off the screen, which kills it
                self.x = WIDTH +150
                #move the asteroid off the screen
                for f in self.asteroid_collision:
                        f.x = reset_asteroid()[0]
                        f.y = reset_asteroid()[1]
        
        #checking if laser hits enemy ship
        if pygame.sprite.spritecollide(self,self.enemy_group,0):
            #check if it hits using mask
            self.enemy_collision = pygame.sprite.spritecollide(self,self.enemy_group,0,pygame.sprite.collide_mask)
            if self.enemy_collision:
                #so the game will draw explosion, same as with player's self.explode
                self.explode = True
                #move the laser off the screen, which kills it
                self.x = WIDTH +150
                #move the asteroid off the screen
                for e in self.enemy_collision:
                        e.kill()

        #update lasers rect
        self.rect.center = (self.x,self.y)
    #drawing lasers
    def draw(self,screen):
        #rotate it based on players theta, then recenter rect, then add to screen
        self.new_image = pygame.transform.rotozoom(self.image,math.degrees(self.theta)+90,0.8)
        self.rect = self.new_image.get_rect(center=self.rect.center)
        screen.blit(self.new_image,self.rect)


        #mask stuff, uncomment two below to see laser mask
        #self.new_mask_image = pygame.transform.rotozoom(self.mask_image,math.degrees(self.theta)+90,0.8)
        #screen.blit(self.new_mask_image,self.rect)

#Explosion Code
class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.explosion_types = []
        self.assets = [
            'assets/PNG/Explosion/explosion00.png',
            'assets/PNG/Explosion/explosion01.png',
            'assets/PNG/Explosion/explosion02.png',
            'assets/PNG/Explosion/explosion03.png',
            'assets/PNG/Explosion/explosion04.png',
            'assets/PNG/Explosion/explosion05.png',
            'assets/PNG/Explosion/explosion06.png',
            'assets/PNG/Explosion/explosion07.png',
            'assets/PNG/Explosion/explosion08.png',
        ]
        for a in self.assets:
            self.file_path = choice(self.assets)
            self.image = pygame.image.load(self.file_path)
            #change size
            self.image = pygame.transform.rotozoom(self.image,0,0.2)
            self.explosion_types.append(self.image)
    #draw explosion
    def draw(self, screen, x,y):
        self.new_image = choice(self.explosion_types)
        screen.blit(self.new_image, (x,y))

class Enemy_Easy(pygame.sprite.Sprite):
    def __init__(self, x, y, player, filepath):
        super().__init__()
        self.file_path = filepath
        self.ogimage = pygame.image.load(self.file_path)
        self.ogimage = pygame.transform.rotozoom(self.ogimage, 0, 0.7)
        self.rect = self.ogimage.get_rect()
        self.x = x
        self.y = y
        self.speed = 2
        self.rect.center = (x,y)
        self.player = player
        self.bad_lasers = pygame.sprite.Group()
        self.time_since_tracked = 0
        self.tracking = 0
        self.time_since_shot = pygame.time.get_ticks()
        self.laser_cooldown_time = 1000
        self.trackingtime = 3000
        
        #making a mask from the ship
        self.og_mask = pygame.mask.from_surface(self.ogimage)
        #give the mask a surface so i can see the mask
        self.og_mask_image = self.og_mask.to_surface()

    def draw(self,screen):
        self.image = pygame.transform.rotozoom(self.ogimage, math.degrees(self.theta)-90, 0.75)
        self.rect = self.image.get_rect(center=self.rect.center)
        screen.blit(self.image, self.rect)
        for s in self.bad_lasers:
            s.file_path = 'assets/images/Lasers/laserRed01.png'
            s.draw(screen)
        
        #rotates the mask with the ship
        try:
            self.mask_image = pygame.transform.rotozoom(self.og_mask_image, math.degrees(self.theta)-90,0.75)
        except:
            self.mask_image = self.og_mask_image
        
        #for testing, draws the mask, uncomment to see mask
        #screen.blit(self.mask_image,self.rect)

    def get_theta(self):
        # calculate the theta in radians to the player
        delta_x = self.player.x - self.x
        delta_y = self.player.y - self.y
        # take atan2
        self.theta = math.atan2(delta_y, -delta_x)
    def shoot(self):
        #create a new laser at the players point with players theta, add it to spritegroup
        new_laser = Laser(self.rect.center,self.theta,self.player.asteroid_group,'assets/images/Lasers/laserRed01.png')
        new_laser.speed = 10
        self.bad_lasers.add(new_laser)
   
    def track(self):
        self.get_theta()
        self.vx = -(self.speed*cos(self.theta))
        self.vy = self.speed*sin(self.theta)
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x,self.y)
        self.bad_lasers.update()
    def go_straight(self):
        self.vx = -(self.speed*cos(self.theta))
        self.vy = self.speed*sin(self.theta)
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x,self.y)
        self.bad_lasers.update()





class Enemy_Medium:
    def __init__(self, x, y):
        self.file_path = 'assets/images/playerShip2_red.png'
        self.image = pygame.image.load(self.file_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x,y)
        self.speed = 2
    def draw(self,screen):
        screen.blit(self.image, self.rect)



class Enemy_Hard:
    def __init__(self, x, y):
        self.file_path = 'assets/images/playerShip1_red.png'
        self.image = pygame.image.load(self.file_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x,y)
        self.speed = 3
    def draw(self,screen):
        screen.blit(self.image, self.rect)

