import pygame
from random import randint, choice
from params import *

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x,y,size=1):
        pygame.sprite.Sprite.__init__(self)
        self.assets = [
            'assets/images/Meteors/meteorBrown_big1.png',
            'assets/images/Meteors/meteorBrown_big2.png',
            'assets/images/Meteors/meteorBrown_big3.png',
            'assets/images/Meteors/meteorBrown_big4.png'
        ]
        self.file_path = choice(self.assets)
        self.image = pygame.image.load(self.file_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.size = size
        self.rect.center = (x,y)
        self.vx = randint(-1000,1000)/1000
        self.vy = randint(-1000,1000)/1000
    def draw(self,screen):
        screen.blit(self.image, self.rect)
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x,self.y)



class Player:
    def __init__(self,x,y):
        self.file_path = 'assets/images/playerShip1_blue.png'
        self.image = pygame.image.load(self.file_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x,y)
    def draw(self,screen):
        screen.blit(self.image, self.rect)
    



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