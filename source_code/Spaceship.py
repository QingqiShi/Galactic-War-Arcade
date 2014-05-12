# import required modules
import math
import pygame

class Spaceship(pygame.sprite.Sprite):
    velocity = [0, 0]
    speed = 0.0
    acceleration = 0.0
    maxSpeed = 0
    direction = 0
    center = [0, 0]
    bullets = []

    def __init__(self, groups, position, acceleration, maxSpeed, weapon, image_path):
        super(Spaceship, self).__init__(groups)
        self.image = pygame.image.load(image_path)
        self.originImage = self.image
        self.rect = pygame.rect.Rect((position[0], position[1]), self.image.get_size())

        self.acceleration = acceleration
        self.maxSpeed = maxSpeed
        self.weapon = weapon

        self.calculateCenter()

    def update(self, tickReturn):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= math.ceil(600 * tickReturn)
        if key[pygame.K_RIGHT]:
            self.rect.x += math.ceil(600 * tickReturn)
        if key[pygame.K_UP]:
            self.rect.y -= math.ceil(600 * tickReturn)
        if key[pygame.K_DOWN]:
            self.rect.y += math.ceil(600 * tickReturn)

    def updateDirection(self, position):
        # Calculate a new direction for spaceship pointing to a position (in radians)
        x = position[0] - self.center[0]
        y = position[1] - self.center[1]
        if (x >= 0 and y < 0):
            # top right quadrum
            self.direction = math.atan(float(x)/float(-y))
        elif (x <= 0 and y > 0):
            # bottom left quadrum
            self.direction = math.pi + math.atan(float(-x)/float(y))
        elif (x > 0 and y >= 0):
            # bottom right quadrum
            self.direction = (math.pi / 2.0) + math.atan(float(y)/float(x))
        elif (x < 0 and y <= 0):
            # top left quadrum
            self.direction = (math.pi * 1.5) + math.atan(float(-y)/float(-x))

    def accelerate(self, tickReturn):
        newSpeed =  self.speed + (self.acceleration * tickReturn)

        # test for maxSpeed
        if newSpeed > self.maxSpeed:
            newSpeed = self.maxSpeed
        
        # calculate velocity vector
        self.velocity[0] = math.sin(self.direction) * newSpeed
        self.velocity[1] = math.cos(self.direction) * newSpeed * -1

        self.speed = newSpeed
            
    def deccelerate(self, tickReturn):
        # test for maxSpeed
        if self.speed > 0.5:

            newSpeed =  self.speed - (self.acceleration * tickReturn)

            # Find the factor
            factor = newSpeed / self.speed
            self.velocity[0] *= factor
            self.velocity[1] *= factor

            self.speed = newSpeed

        else:
            self.velocity[0] = 0
            self.velocity[1] = 0

            self.speed = 0

    def changeWeapon(self, weaponNum):
        self.weapon = weaponNum

    def calculateCenter(self):
        self.center = self.rect.center

    def fire(self):
        self.weapon.fire(self.rect.center, self.direction)

class PlayerShip(Spaceship):
    def __init__(self, groups, position, acceleration, maxSpeed, weapon, image_path):
        super(PlayerShip, self).__init__(groups, position, acceleration, maxSpeed, weapon, image_path)

    def update(self, tickReturn):
        oldDirection = self.direction
        super(PlayerShip, self).updateDirection(pygame.mouse.get_pos())

        if (oldDirection != self.direction):
            # rotate image
            self.image = pygame.transform.rotate(self.originImage, math.degrees(self.direction) * -1)
            self.rect = self.image.get_rect(center=self.rect.center)

            super(PlayerShip, self).calculateCenter()

        

        mouseDistance = math.hypot(pygame.mouse.get_pos()[0] - self.center[0], pygame.mouse.get_pos()[1] - self.center[1])

        if (pygame.mouse.get_pressed()[2] and mouseDistance > 5):
            super(PlayerShip, self).accelerate(tickReturn)
        elif (mouseDistance < 5):
            self.velocity = [0, 0]
        else:
            super(PlayerShip, self).deccelerate(tickReturn)

        if (pygame.mouse.get_pressed()[0]):
            super(PlayerShip, self).fire()

        self.rect.move_ip(self.velocity[0], self.velocity[1])

        self.weapon.clearBullets()

class EnemyShip(Spaceship):
    def __init__(self, groups, position, acceleration, maxSpeed, weapon, image_path, playership):
        super(EnemyShip, self).__init__(groups, position, acceleration, maxSpeed, weapon, image_path)
        self.playership = playership

    def update(self, tickReturn):
        oldDirection = self.direction
        super(EnemyShip, self).updateDirection(self.playership.center)

        if (oldDirection != self.direction):
            # rotate image
            self.image = pygame.transform.rotate(self.originImage, math.degrees(self.direction) * -1)
            self.rect = self.image.get_rect(center=self.rect.center)

            super(EnemyShip, self).calculateCenter()

        super(EnemyShip, self).fire()