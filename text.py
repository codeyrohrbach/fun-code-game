import pygame
class Text:
    def __init__(self):
        self.score_font = pygame.font.Font('assets/Xirod.otf', 40)
        self.score_surface = self.score_font.render('Score: 0',1,(255,0,0))
    def draw(self, screen):
        screen.blit(self.score_surface, (20,20))
    def update_score(self, score):
        self.score_surface = self.score_font.render(f"Score: {score}",1,(255,0,0))