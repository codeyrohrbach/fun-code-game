import pygame
from params import *
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
        #make it only render the score every 10 points (every point was distracting)
        if score %10 == 0:
            self.score_surface = self.score_font.render(f"Score: {score}",1,(255,0,0))
    def update_lives(self, lives):
        self.lives_surface = self.lives_font.render(f"Lives: {lives}",1,(255,0,0))
class Title:
    def __init__(self):
        self.title_font = pygame.font.Font('assets/Xirod.otf',60)
        self.subtitle_font = pygame.font.Font('assets/Xirod.otf',20)
        self.title_surface = self.title_font.render('Asteroid Avoidance',1,(255,0,0))
        self.subtitle_surface = self.subtitle_font.render('Press Circle (O) to start',1,(255,0,0))
        self.rect = self.title_surface.get_rect()
        self.subrect = self.subtitle_surface.get_rect()
        self.rect.center = (WIDTH//2,HEIGHT//2)
        self.subrect.center = (WIDTH//2,HEIGHT//2+100)
    def draw(self,screen):
        screen.blit(self.title_surface, self.rect)
        #screen.blit(self.subtitle_surface, self.subrect)

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
class Controls:
    def __init__(self):
        self.font = pygame.font.Font('assets/Xirod.otf',60)
        self.surface = self.font.render('Controls',1,(255,0,0))
        self.rect = self.surface.get_rect()
        self.rect.center = (WIDTH//2,100)
        
        self.font = pygame.font.Font('assets/Xirod.otf',30)

        self.joystick_surface = self.font.render('Left Joystick: Movement',1,(255,0,0))
        self.joystick_rect = self.joystick_surface.get_rect()
        self.joystick_rect.center = (WIDTH//2,200)

        self.trigger_surface = self.font.render('Right Trigger (R2): Boost',1,(255,0,0))
        self.trigger_rect = self.trigger_surface.get_rect()
        self.trigger_rect.center = (WIDTH//2,300)

        self.x_surface = self.font.render('X Button: Shoot',1,(255,0,0))
        self.x_rect = self.x_surface.get_rect()
        self.x_rect.center = (WIDTH//2,400)

    def draw(self,screen):
        screen.blit(self.surface, self.rect)
        screen.blit(self.joystick_surface, self.joystick_rect)
        screen.blit(self.trigger_surface, self.trigger_rect)
        screen.blit(self.x_surface, self.x_rect)

class Button:
    def __init__(self, button,action):
        self.font = pygame.font.Font('assets/Xirod.otf',20)
        self.surface = self.font.render(f'Press {button} to {action}',1,(255,0,0))
        self.rect = self.surface.get_rect()
        self.rect.center = (WIDTH//2,HEIGHT//2)
    def draw(self,screen,y,x=0):
        screen.blit(self.surface, (self.rect[0]+x, self.rect[1]+y))
''' TO DO:
ASTEROIDS EXPLODE FROM LASER
TITLE SCREEN, GAME OVER SCREEN

'''