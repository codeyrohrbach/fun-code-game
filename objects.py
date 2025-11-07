import pygame
from random import randint, choice
from params import *
import math


class Explosion:
    def __init__(self):
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

