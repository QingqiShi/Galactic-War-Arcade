# import required modules
import math
import pygame

class Weapon(object):
    weaponNum = 0
    coolDown = 0.0
    bulletSpeed = 0.0
    bullets = []
    def __init__(self, groups, weaponNum, coolDown, bulletSpeed):
        self.groups = groups
        self.weaponNum = weaponNum
        self.coolDown = coolDown
        self.bulletSpeed = bulletSpeed
        self.groups = groups

    def fire(self, position, direction):
        newBullet = Bullet(self.groups, self.bulletSpeed, self.weaponNum, position, direction)
        self.bullets.append(newBullet)


class Bullet(pygame.sprite.Sprite):
    bulletSpeed = 0.0
    position = (0, 0)
    direction = 0
    weaponNum = 0
    def __init__(self, groups, bulletSpeed, weaponNum, position, direction):
        super(Bullet, self).__init__(groups)
        self.image = pygame.image.load('img/bullet' + str(weaponNum) + '.png')
        self.rect = pygame.rect.Rect(position, self.image.get_size())

        self.originImage = self.image
        
        # rotate image
        self.image = pygame.transform.rotate(self.originImage, math.degrees(self.direction) * -1)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.bulletSpeed = bulletSpeed
        self.position = position
        self.direction = direction
        self.weaponNum = weaponNum

    def update(self, tickReturn):
        if self.weaponNum == 0:
            self.rect.x -= math.ceil(200 * tickReturn)
            self.rect.y -= math.ceil(200 * tickReturn)
        else:
            print("Incorrect Weapon")