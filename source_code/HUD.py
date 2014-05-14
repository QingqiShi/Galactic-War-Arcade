# import required modules
import pygame

class HUD(object):
    def __init__(self, screen):
        self.screen = screen

    def updateScore(self, score):
        self.screen.blit(pygame.font.SysFont("monospace", 72, True).render(str(score), 1, (91, 109, 131)), (900, 50))