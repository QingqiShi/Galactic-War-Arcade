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
        Spaceship.__init__(self, color, HEIGHT/16*0.6, HEIGHT/16, position, 0.5, 10)

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
        # calculate velocity based on initial velocity
        #u = math.hypot(self.velocity[0], self.velocity[1])
        #v = math.hypot(self.velocity[0], self.velocity[1]) + self.acceleration)
        # test for maximum velocity
        #if v > self.topSpeed:
        #    v -= (self.acceleration /2.0)
        
        mousePosition = pygame.mouse.get_pos()

        accel = self.acceleration
        #dist = math.hypot((mousePosition[0] - self.position[0]),(mousePosition[1] - self.position[1]))
        #if (dist < 1000):
        #    accel = (self.acceleration / 1000) * dist

        v = [0, 0]
        b = math.hypot(self.velocity[0], self.velocity[1])
        if b == 0:
            b = 1
        beta = self.direction - math.acos(self.velocity[1]/b)
        a = math.sqrt(b*b+accel*accel-2*b*accel*math.cos(beta))
        alpha = math.asin((math.sin(beta)*b)/a)

        v[0] = self.velocity[0] - math.sin(math.radians(180 - self.direction - alpha)) * accel
        v[1] = self.velocity[1] + math.cos(math.radians(180 - self.direction - alpha)) * accel

        if v[0] > 0:
            v[0] - AIRRESISTANCE
        elif v[0] < 0:
            v[0] + AIRRESISTANCE

        if v[1] > 0:
            v[1] - AIRRESISTANCE
        elif v[1] < 0:
            v[1] + AIRRESISTANCE

        print math.hypot(v[0], v[1])
        if (math.hypot((self.position[0] - mousePosition[0]), (self.position[1] - mousePosition[1])) < 50):
            # if mouse is within 10 pixel radius, don't move
            self.velocity = [0, 0]
        else:
            # calculate velocity vector and move the rect and image
            if math.hypot(v[0], v[1]) <= self.topSpeed:
                self.velocity[0] = v[0]
                self.velocity[1] = v[1]
            self.rect.move_ip(int(self.velocity[0]), int(self.velocity[1]))
            self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
            self.rect.center = self.position

    def update(self):
        self.updateDirection()
        self.move()

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
