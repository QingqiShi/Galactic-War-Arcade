#!/usr/bin/env python

# import required modules
import math
import pygame
from pygame.sprite import Sprite

# global variables
WIDTH = 1080
HEIGHT = 720
FPS = 30

AIRRESISTANCE = 2

# define objects
class Spaceship(Sprite):
    def __init__(self, color, width, height, position, accel, maxSpeed):
        Sprite.__init__(self)
        self.velocity = [0.0, 0.0]     # velocity vector of spaceship
        self.acceleration = float(accel)      # acceleration in both direction
        self.topSpeed = maxSpeed          # maximum speed of spaceship
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
        Spaceship.__init__(self, color, HEIGHT/16*0.6, HEIGHT/16, position, 1, 15)

        # draw player spaceship
        pygame.draw.lines(self.image, pygame.Color(color), True, [(1, self.shipHeight-1), (self.shipWidth/2, 1), (self.shipWidth-1, self.shipHeight-1), (self.shipWidth/2, self.shipHeight-8)], 2)

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

    def move(self):
        if pygame.mouse.get_pressed()[2]:
            # calculate velocity based on initial velocity
            v = math.hypot(self.velocity[0], self.velocity[1]) + (self.acceleration / (FPS*0.1))
            # test for maximum velocity
            if v > self.topSpeed:
                v -= (self.acceleration /2.0)
            
            mousePosition = pygame.mouse.get_pos()
            if (math.hypot((self.position[0] - mousePosition[0]), (self.position[1] - mousePosition[1])) < 10):
                # if mouse is within 10 pixel radius, don't move
                self.velocity = [0, 0]
            else:
                # calculate velocity vector and move the rect and image
                angle = self.direction
                self.velocity[0] = math.sin(math.radians(angle)) * v * -1
                self.velocity[1] = math.cos(math.radians(angle)) * v * -1
                
        else:
            if self.velocity[0] != 0:
                self.velocity[0] *= 0.9
            if self.velocity[1] != 0:
                self.velocity[1] *= 0.9
            if -0.001 < self.velocity[0] < 0.001:
                self.velocity[0] = 0
            if -0.001 < self.velocity[1] < 0.001:
                self.velocity[1] = 0

        self.rect.move_ip(int(self.velocity[0]), int(self.velocity[1]))
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        self.rect.center = self.position

    def update(self):
        self.updateDirection()
        self.move()

class bullet(object):
    def __init__(self):
        pass

# main function
def main():
    # set window properties
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Galactic War v0.0.2")

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
        clock.tick(FPS)
        pygame.display.set_caption("Galactic War v0.0.2 - {0:.3f} fps".format(clock.get_fps()))

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
