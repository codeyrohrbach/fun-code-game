import pygame
from params import *

#used for score and lives
class Text:
    def __init__(self):
        self.score_font = pygame.font.Font('assets/Xirod.otf', 30)
        self.score_surface = self.score_font.render('Score: 0',1,(255,0,0))
        self.lives_font = pygame.font.Font('assets/Xirod.otf', 30)
        self.lives_surface = self.lives_font.render('Lives: 3',1,(255,0,0))
    def draw(self, screen):
        screen.blit(self.score_surface, (20,20))
        screen.blit(self.lives_surface, (1075,20))
    def update_score(self, score):
        self.score_surface = self.score_font.render(f"Score: {score}",1,(255,0,0))
    def update_lives(self, lives):
        self.lives_surface = self.lives_font.render(f"Lives: {lives}",1,(255,0,0))

#used for the Title
class Title:
    def __init__(self):
        self.title_font = pygame.font.Font('assets/Xirod.otf',40)
        self.title_surface = self.title_font.render('Asteroid Avoidance / Gunship Attack',1,(255,0,0))
        self.rect = self.title_surface.get_rect()
        self.rect.center = (WIDTH//2,HEIGHT//2-50)
    def draw(self,screen):
        screen.blit(self.title_surface, self.rect)

#game over screen text
class GameOver:
    def __init__(self):
        self.font = pygame.font.Font('assets/Xirod.otf',60)
        self.surface = self.font.render('Game Over',1,(255,0,0))
        self.rect = self.surface.get_rect()
        self.rect.center = (WIDTH//2,HEIGHT//2)
        self.subfont = pygame.font.Font('assets/Xirod.otf',20)
        self.subsurface = self.subfont.render('Press triangle to return to Menu',1,(255,0,0))
        self.subrect = self.subsurface.get_rect()
        self.subrect.center = (WIDTH//2,HEIGHT//2+100)
    def draw(self,screen):
        screen.blit(self.surface, self.rect)
        screen.blit(self.subsurface, self.subrect)  

#controls screen text
class Controls:
    def __init__(self):
        self.font = pygame.font.Font('assets/Xirod.otf',60)
        self.surface = self.font.render('Controls',1,(255,0,0))
        self.rect = self.surface.get_rect()
        self.rect.center = (WIDTH//2,100)
        #change font for the controls section
        self.font = pygame.font.Font('assets/Xirod.otf',30)
        #joystick control text
        self.joystick_surface = self.font.render('Left Joystick: Movement',1,(255,0,0))
        self.joystick_rect = self.joystick_surface.get_rect()
        self.joystick_rect.center = (WIDTH//2,200)
        #trigger control text
        self.trigger_surface = self.font.render('Right Trigger (R2): Boost',1,(255,0,0))
        self.trigger_rect = self.trigger_surface.get_rect()
        self.trigger_rect.center = (WIDTH//2,300)
        #x button control text
        self.x_surface = self.font.render('X Button: Shoot',1,(255,0,0))
        self.x_rect = self.x_surface.get_rect()
        self.x_rect.center = (WIDTH//2,400)
    def draw(self,screen):
        screen.blit(self.surface, self.rect)
        screen.blit(self.joystick_surface, self.joystick_rect)
        screen.blit(self.trigger_surface, self.trigger_rect)
        screen.blit(self.x_surface, self.x_rect)

#for various button texts, used on menu, controls, and game over screen
class Button:
    #take the button and action it does as an input
    def __init__(self, button,action):
        self.font = pygame.font.Font('assets/Xirod.otf',20)
        self.surface = self.font.render(f'Press {button} to {action}',1,(255,0,0))
        self.rect = self.surface.get_rect()
        self.rect.center = (WIDTH//2,HEIGHT//2)
    def draw(self,screen,y,x=0):
        screen.blit(self.surface, (self.rect[0]+x, self.rect[1]+y))

#draw the wave number onto the screen
class Wave:
    def __init__(self):
        self.font = pygame.font.Font('assets/Xirod.otf',30)
    #takes the wave number as an input
    def draw(self,screen,wave_num):
        self.surface = self.font.render(f'Wave {wave_num}',1,(255,0,0))
        self.rect = self.surface.get_rect()
        self.rect.center = (WIDTH//2,60)
        screen.blit(self.surface, (self.rect[0], 25))