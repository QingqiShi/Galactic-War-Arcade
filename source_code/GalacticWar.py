#!/usr/bin/env python

# import required modules
import math
import pygame
from pygame.sprite import Sprite

# global variables
WIDTH = 1080
HEIGHT = 720

# define objects
class Spaceship(Sprite):
    def __init__(self, color, width, height, position):
        Sprite.__init__(self)
        self.velocity = [0, 0]     # velocity vector of spaceship
        self.direction = 0         # spaceship rotation, north is 0, anti-clock
        self.shipHeight = height
        self.shipWidth = width
        self.position = position
        self.image = pygame.Surface([self.shipWidth, self.shipHeight])
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.originImage = self.image

class Playership(Spaceship):
    def __init__(self, color, position):
        Spaceship.__init__(self, color, HEIGHT/16*0.6, HEIGHT/16, position)

        # draw player spaceship
        pygame.draw.lines(self.image, pygame.Color(color), True, [(1, self.shipHeight-1), (self.shipWidth/2, 1), (self.shipWidth-1, self.shipHeight-1), (self.shipWidth/2, self.shipHeight-8)], 1)

    def updateDirection(self):
        mousePosition = pygame.mouse.get_pos()
        # calculate direction
        if (self.position[1] - mousePosition[1] != 0):
            self.direction = math.degrees(math.atan(float(self.position[0] - mousePosition[0]) / float(self.position[1] - mousePosition[1])))
        if (self.position[1] - mousePosition[1] < 0):
            self.direction += 180
        # rotate image
        self.image = pygame.transform.rotate(self.originImage, self.direction)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.updateDirection()

# main function
def main():
    # set window properties
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Galactic War v0.0.7")

    # background
    background = pygame.Surface([WIDTH, HEIGHT])
    background.fill(pygame.Color("black"))
    screen.blit(background, (0, 0))

    # setup sprites
    player = Playership("#00CCFF", (WIDTH/2, HEIGHT/2))

    # list sprites to render
    sprites = pygame.sprite.RenderPlain([player])

    # game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(120)
        pygame.display.set_caption("Galactic War v0.0.7 - {0:.3f} fps".format(clock.get_fps()))

        sprites.update()
        sprites.draw(screen)
        pygame.display.flip()
        sprites.clear(screen, background)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# if executed as a script, run main()
if __name__ == "__main__":
    main()
