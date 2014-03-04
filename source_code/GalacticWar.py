#!/usr/bin/env python

# import required modules
import pygame
from pygame.sprite import Sprite

# global variables
WIDTH = 1080
HEIGHT = 720

# define objects
class Spaceship(Sprite):
    def __init__(self, color, width, height):
        Sprite.__init__(self)
        self.velocity = [0, 0]
        self.direction = 0
        self.shipHeight = height
        self.shipWidth = width
        self.image = pygame.Surface([self.shipWidth, self.shipHeight])

class Playership(Spaceship):
    def __init__(self, color, position):
        Spaceship.__init__(self, color, HEIGHT/20*0.6, HEIGHT/20)
        Spaceship.rect = pygame.Rect(0, 0, self.shipWidth, self.shipHeight)
        pygame.draw.lines(self.image, pygame.Color(color), True, [(1, 1), (self.shipWidth/2, self.shipHeight-1), (self.shipWidth-1, 1), (self.shipWidth/2, 7)], 2)
        Spaceship.rect.center = position
        
        

# main function
def main():
    # set window properties
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Galactic War")

    # setup sprites
    player = Playership("#00CCFF", (WIDTH/2, HEIGHT/2))

    # list sprites to render
    sprites = pygame.sprite.RenderPlain([player])

    # game loop
    running = True
    while running:
        sprites.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# if executed as a script, run main()
if __name__ == "__main__":
    main()
