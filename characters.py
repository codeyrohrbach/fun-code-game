import pygame
from random import randint, choice
from params import *
import math

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
        self.vx = randint(-1000,1000)/750
        self.vy = randint(-1000,1000)/750
    def draw(self,screen):
        screen.blit(self.image, self.rect)
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x,self.y)

        #if the asteroid moves off the screen 
        if self.rect.left < -200 or self.rect.right > WIDTH+200 or self.rect.top < -200 or self.rect.bottom >HEIGHT+200:
            #randomise where it gets moved to
            self.x = choice([randint(-100,0),randint(WIDTH,WIDTH+100)])
            self.y = choice([randint(-100,0),randint(HEIGHT,HEIGHT+100)])
            #randomise the direction of asteroid (makes it seem like a new asteroid)
            self.vx = randint(-1000,1000)/750
            self.vy = randint(-1000,1000)/750



class Player:
    def __init__(self,x,y):
        self.file_path = 'assets/images/playerShip1_blue.png'
        self.og_image = pygame.image.load(self.file_path)
        self.rect = self.og_image.get_rect()
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.rect.center = (x,y)
        #putting it on the screen
    def draw(self,screen):
        #screen.blit(self.image, self.rect.center)

        self.image = pygame.transform.rotozoom(self.og_image, math.degrees(self.theta)+90,0.6)
        self.rect = self.image.get_rect(center=self.rect.center)
        screen.blit(self.image, self.rect)
        
    def get_theta(self):
        # get our theta based on our vx and vy
        self.theta = math.atan2(self.vy,-self.vx)     
        
        #updating
    def update(self, left_right, up_down, right_trigger):
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