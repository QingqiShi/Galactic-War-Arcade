# import required modules
import math
import pygame
import time

class Weapon(object):
    weaponNum = 0
    coolDown = 0.0
    bulletSpeed = 0.0
    bullets = []
    lastFired = 0
    def __init__(self, groups, weaponNum):
        self.groups = groups
        self.weaponNum = weaponNum
        self.groups = groups

        if weaponNum == 0:
            self.coolDown = 0.3
            self.bulletSpeed = 500

    def fire(self, position, direction):
        if time.time() - self.lastFired > self.coolDown:
            newBullet = Bullet(self.groups, self.bulletSpeed, self.weaponNum, position, direction)
            self.bullets.append(newBullet)
            self.lastFired = time.time()

    def clearBullets(self):
        for bullet in self.bullets:
            bullet_x = bullet.rect.center[0]
            bullet_y = bullet.rect.center[1]
            if bullet_x < 0 or bullet_x > 1024 or bullet_y < 0 or bullet_y > 768:
                bullet.kill()
                self.bullets.remove(bullet)


class Bullet(pygame.sprite.Sprite):
    bulletSpeed = 0.0
    position = (0, 0)
    direction = 0
    weaponNum = 0
    def __init__(self, groups, bulletSpeed, weaponNum, position, direction):
        super(Bullet, self).__init__(groups)
        self.image = pygame.image.load('img/bullet' + str(weaponNum) + '.png')
        self.originImage = self.image
        self.image = pygame.transform.rotate(self.originImage, math.degrees(self.direction) * -1)

        self.rect = pygame.rect.Rect((position[0] - self.image.get_size()[0] * 0.5, position[1] - self.image.get_size()[1] * 0.5), self.image.get_size())
        
        self.rect = self.image.get_rect(center=self.rect.center)

        self.bulletSpeed = bulletSpeed
        self.position = position
        self.direction = direction
        self.weaponNum = weaponNum

    def update(self, tickReturn):
        # rotate image
        self.image = pygame.transform.rotate(self.originImage, math.degrees(self.direction) * -1)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.weaponNum == 0:
            self.rect.x -= math.ceil(math.sin(self.direction) * self.bulletSpeed * tickReturn * -1)
            self.rect.y -= math.ceil(math.cos(self.direction) * self.bulletSpeed * tickReturn)
        else:
            print("Incorrect Weapon")