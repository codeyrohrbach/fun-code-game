import pygame
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