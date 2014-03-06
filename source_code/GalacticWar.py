#!/usr/bin/env python

# import required modules
import math
import pygame
from pygame.sprite import Sprite

# global variables
WIDTH = 1080
HEIGHT = 720
FPS = 30

# define objects
class Spaceship(Sprite):
    def __init__(self, color, width, height, position, accel, maxSpeed):
        Sprite.__init__(self)
        self.velocity = [0.0, 0.0]        # velocity vector of spaceship
        self.acceleration = float(accel)  # acceleration in both direction
        self.topSpeed = maxSpeed          # maximum speed of spaceship
        self.direction = 0                # spaceship rotation, north is 0, anti-clock
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
        lines = [(1, self.shipHeight-1), (self.shipWidth/2, 1), (self.shipWidth-1, self.shipHeight-1), (self.shipWidth/2, self.shipHeight-8)]
        pygame.draw.lines(self.image, pygame.Color(color), True, lines, 2)

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
            # accelerate if right mouse id down
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
            # decelerate if right mouse is up
            if self.velocity[0] != 0:
                self.velocity[0] *= 0.95
            if self.velocity[1] != 0:
                self.velocity[1] *= 0.95
            if -0.001 < self.velocity[0] < 0.001:
                self.velocity[0] = 0
            if -0.001 < self.velocity[1] < 0.001:
                self.velocity[1] = 0

        self.rect.move_ip(int(self.velocity[0]), int(self.velocity[1]))
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        self.rect.center = self.position

    def shoot(self, screen):
        bullet = Bullet(1, (self.position[0], self.position[1]), self.direction)
        return bullet

    def update(self):
        self.updateDirection()
        self.move()

class Bullet(Sprite):
    def __init__(self, bullet_id, position, angle):
        Sprite.__init__(self)
        # draw bullet
        self.position = position
        self.direction = angle
        self.speed = 1
        self.image = pygame.Surface([1, 20])
        self.originImage = self.image
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        pygame.draw.line(self.image, pygame.Color("white"), (0, 0), (0, 19))

        # rotate image
        self.image = pygame.transform.rotate(self.originImage, self.direction)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self):
        v = [0, 0]
        v[0] = int(-1 * (math.sin(self.direction) * 20 + 20) * self.speed)
        v[1] = int(-1 * (math.cos(self.direction) * 20 + 20) * self.speed)
        self.rect.move_ip(v[0], v[1])
        self.position = (self.position[0] + v[0], self.position[1] + v[1])
        self.rect.center = self.position
        
    def update(self):
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

    bullet = player.shoot(screen)
    bulletArray = [bullet]

    # list sprites to render
    spriteArray = [player]
    sprites = pygame.sprite.RenderPlain(spriteArray)

    # game loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        clock.tick(FPS)
        pygame.display.set_caption("Galactic War v0.0.2 - {0:.3f} fps".format(clock.get_fps()))
        
        sprites.update()

        if pygame.mouse.get_pressed()[0]:
            bullet = player.shoot(screen)
            bulletArray.append(bullet)
            sprites.add(bullet)
        for temp_bullet in bulletArray:
            if temp_bullet.position[0] < 0 or temp_bullet.position[0] > WIDTH:
                sprites.remove(temp_bullet)
                bulletArray.remove(temp_bullet)
            elif temp_bullet.position[1] < 0 or temp_bullet.position[1] > HEIGHT:
                sprites.remove(temp_bullet)
                bulletArray.remove(temp_bullet)

        sprites.draw(screen)
        pygame.display.flip()
        sprites.clear(screen, background)
        print bulletArray.__len__()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# if executed as a script, run main()
if __name__ == "__main__":
    main()
