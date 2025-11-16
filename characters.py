import pygame
from random import randint, choice
from params import *
import math
from math import radians, cos, sin

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
        self.image = pygame.image.load(self.file_path)
        self.image = pygame.transform.rotozoom(self.image,0,randint(40,100)/100)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.size = size
        self.rect.center = (x,y)
        self.vx = randint(-2000,2000)/750
        self.vy = randint(-2000,2000)/750

        #asteroid mask
        self.mask = pygame.mask.from_surface(self.image)
        #so i can see the mask
        self.mask_image = self.mask.to_surface()
    def draw(self,screen):
        screen.blit(self.image, self.rect)
        #mask
        screen.blit(self.mask_image,self.rect)
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x,self.y)

        #if the asteroid moves off the screen 
        if self.rect.left < -200 or self.rect.right > WIDTH+200 or self.rect.top < -200 or self.rect.bottom >HEIGHT+200:
            #randomise where it gets moved to
            self.x = reset_asteroid()[0]
            self.y = reset_asteroid()[1]
            #randomise the direction of asteroid (makes it seem like a new asteroid)
            self.vx = randint(-1000,1000)/750
            self.vy = randint(-1000,1000)/750

def reset_asteroid():
    return (choice([randint(-100,0),randint(WIDTH,WIDTH+100)]), choice([randint(-100,0),randint(HEIGHT,HEIGHT+100)]))

class Player:
    def __init__(self,x,y,asteroid_group):
        self.file_path = 'assets/images/playerShip1_blue.png'
        self.og_image = pygame.image.load(self.file_path)
        self.rect = self.og_image.get_rect()
        self.asteroid_group = asteroid_group
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.lives = 3
        self.rect.center = (x,y)
        #laser code
        self.lasers = pygame.sprite.Group()
        
        #making a mask from the ship
        self.og_mask = pygame.mask.from_surface(self.og_image)
        #so i can see the mask
        self.og_mask_image = self.og_mask.to_surface()
        
        #putting it on the screen
    def draw(self,screen):
        try:
            self.image = pygame.transform.rotozoom(self.og_image, math.degrees(self.theta)+90,0.6)
        except:
            self.image = self.og_image
        self.rect = self.image.get_rect(center=self.rect.center)
        screen.blit(self.image, self.rect)

        #rotates the mask with the ship
        try:
            self.mask_image = pygame.transform.rotozoom(self.og_mask_image, math.degrees(self.theta)+90,0.6)
        except:
            self.mas_image = self.og_mask_image
        #for testing, draws the mask
        #screen.blit(self.mask_image,self.rect)
        
        for s in self.lasers:
            s.draw(screen)
    def get_theta(self):
        # get our theta based on our vx and vy
        self.theta = math.atan2(self.vy,-self.vx)     
        
        #updating
    def update(self, left_right, up_down, right_trigger,screen=None):
        self.explode = False
        speed = 3
        #boost button, if right trigger pushed down then increase speed
        if right_trigger > 0.5:
            speed = 5
        #takes the values of joysticks and sets vx and vy equal to it
        self.vx = left_right *speed
        self.get_theta()
        self.vy = -up_down *speed
        #moving the ship
        self.x += self.vx
        self.y += self.vy
        #update the rect
        self.rect.center = (self.x,self.y)


        #collision with asteroid
        if pygame.sprite.spritecollide(self,self.asteroid_group,0):
            self.asteroid_collision = pygame.sprite.spritecollide(self,self.asteroid_group,0,pygame.sprite.collide_mask)
            if self.asteroid_collision:
                self.lives -=1
                self.explode = True
            # reset asteroid
                for f in self.asteroid_collision:
                    f.x = reset_asteroid()[0]
                    f.y = reset_asteroid()[1]
        self.lasers.update()
    
    def shoot(self):
        new_laser = Laser(self.rect.center,self.theta,self.asteroid_group)
        self.lasers.add(new_laser)
                
class Laser(pygame.sprite.Sprite):
    def __init__(self,coordinates,theta,asteroid_group):
        super().__init__()
        self.file_path = 'assets/images/Lasers/laserBlue01.png'
        self.image = pygame.image.load(self.file_path)
        self.theta = theta
        self.speed = 20
        self.vx = -self.speed* cos(self.theta)
        self.vy = self.speed* sin(self.theta)
        self.rect = self.image.get_rect()
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.rect.center = (coordinates)
        self.og_mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.og_mask.to_surface()
        self.asteroid_group = asteroid_group
        self.explode = False
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x>WIDTH+100 or self.x<-100 or self.y>HEIGHT+100 or self.y<-100:
            self.kill()

        if pygame.sprite.spritecollide(self,self.asteroid_group,0):
            self.asteroid_collision = pygame.sprite.spritecollide(self,self.asteroid_group,0,pygame.sprite.collide_mask)
            if self.asteroid_collision:
                self.explode = True
                self.x = WIDTH +150
                for f in self.asteroid_collision:
                        f.x = reset_asteroid()[0]
                        f.y = reset_asteroid()[1]
        self.rect.center = (self.x,self.y)
    def draw(self,screen):
        self.new_image = pygame.transform.rotozoom(self.image,math.degrees(self.theta)+90,0.8)
        self.rect = self.new_image.get_rect(center=self.rect.center)
        screen.blit(self.new_image,self.rect)


        #mask stuff
        #self.new_mask_image = pygame.transform.rotozoom(self.mask_image,math.degrees(self.theta)+90,0.8)
        #screen.blit(self.new_mask_image,self.rect)


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
            self.image = pygame.transform.rotozoom(self.image,0,0.2)
            self.explosion_types.append(self.image)
    def draw(self, screen, x,y):
        self.new_image = choice(self.explosion_types)
        screen.blit(self.new_image, (x,y))

class Enemy_Easy:
    def __init__(self, x, y):
        self.file_path = 'assets/images/playerShip3_red.png'
        self.image = pygame.image.load(self.file_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x,y)
        self.speed = 1
    def draw(self,screen):
        screen.blit(self.image, self.rect)



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

