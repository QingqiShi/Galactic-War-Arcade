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

class Bullet(pygame.sprite.Sprite):
    bulletSpeed = 0.0
    def __init__(self, groups, bulletSpeed, weaponNum):
        self.bulletSpeed = bulletSpeed