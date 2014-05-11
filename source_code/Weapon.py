# import required modules
import math
import pygame

class Weapon(object):
    weaponNum = 0
    coolDown = 0
    bullets = []
    def __init__(self, groups, weaponNum, coolDown):
        self.groups = groups
        self.weaponNum = weaponNum
        self.coolDown = coolDown

# class Bullet(pygame.sprite.Sprite):
