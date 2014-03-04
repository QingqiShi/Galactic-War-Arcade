#!/usr/bin/env python

# import required modules
import pygame
from pygame.sprite import Sprite

# global variables
WIDTH = 1080
HEIGHT = 720

# define objects
class Spaceship(Sprite):
    def __init__(self, color, position):
        shipHeight = HEIGHT/18
        shipWidth = shipHeight*0.6
        Sprite.__init__(self)
        self.image = pygame.Surface([shipWidth, shipHeight])
        self.rect = pygame.Rect(0, 0, shipWidth, shipHeight)
        pygame.draw.lines(self.image, pygame.Color(color), True, [(1, 1), (shipWidth/2, shipHeight-1), (shipWidth-1, 1), (shipWidth/2, 7)], 2)
        self.rect.center = position

# main function
def main():
    # set window properties
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Galactic War")

    # setup sprites
    playerShip = Spaceship("#00CCFF", (WIDTH/2, HEIGHT/2))

    # list sprites to render
    sprites = pygame.sprite.RenderPlain([playerShip])

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
