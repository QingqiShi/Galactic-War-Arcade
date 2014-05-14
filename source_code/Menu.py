# import required modules
import pygame

class Menu(object):

    def displayMenu(self, screen, menuID, score = 0, highScore = 0):
        # menuID 1 = Instruction
        #        2 = Pause
        #        3 = Game Over

        if menuID == 2:
        elif menuID == 3:
            screen.blit(pygame.font.SysFont("monospace", 72, True).render("Game Over", 1, (91, 109, 131)), (320, 300))
            screen.blit(pygame.font.SysFont("monospace", 16, True).render("Press R to restart", 1, (91, 109, 131)), (420, 370))
            screen.blit(pygame.font.SysFont("monospace", 16, True).render("Score", 1, (91, 109, 131)), (380, 420))
            screen.blit(pygame.font.SysFont("monospace", 16, True).render("Best", 1, (91, 109, 131)), (590, 420))
            screen.blit(pygame.font.SysFont("monospace", 72, True).render(str(score), 1, (91, 109, 131)), (380, 440))
            screen.blit(pygame.font.SysFont("monospace", 72, True).render(str(highScore), 1, (91, 109, 131)), (590, 440))