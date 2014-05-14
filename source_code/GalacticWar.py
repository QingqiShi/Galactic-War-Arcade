#!/usr/bin/env python

# import required modules
import pygame
import random
import math
import time

# import different modules
from Spaceship  import *
from Weapon import *
from Meteoroid import *
from Menu import *
from HUD import *

def main():
    screen = pygame.display.set_mode((1024, 768))
    quit = False
    while not quit:
        quit = startGame(screen)

def startGame(screen):
    # create sprite groups
    sprites = pygame.sprite.Group()
    enemy = pygame.sprite.Group()
    playerDeadly = pygame.sprite.Group()
    enemyDeadly = pygame.sprite.Group()

    spritesList = [sprites, enemy, playerDeadly, enemyDeadly]

    gameStartTime = time.time()
    score = 0
    timeCounter = 0

    f = open('highScore', 'r')
    temp = f.read()
    if temp != "":
        highScore = int(temp)
    else:
        highScore = 0
    f.close()

    # create player ship
    playerShip = PlayerShip(sprites, [512, 384], 6.8, 13, Weapon(enemyDeadly, 0), 'img/playership1.png')
    alive = True

    # create HUD
    hud = HUD(screen)

    # start game loop
    clock = pygame.time.Clock()
    while True:
        tickReturn = clock.tick(60) / 1000.0
        timeCounter += tickReturn
        pygame.display.set_caption("Galactic War v0.1.2 - {0:.3f} fps".format(clock.get_fps()))

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f = open('highScore', 'w')
                f.write(str(highScore))
                f.close()
                return True
        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            f = open('highScore', 'w')
            f.write(str(highScore))
            f.close()
            return False
        if key[pygame.K_ESCAPE]:
            f = open('highScore', 'w')
            f.write(str(highScore))
            f.close()
            return True

        # calculate random tick
        randomTick = random.randint(0, 4 * int(clock.get_fps())) == 1 and True or False

        # handle randomTick action
        if randomTick:
            if alive:
                timePassed = time.time() - gameStartTime
                if (timePassed < 15):
                    difficulty = 1
                elif (timePassed < 30):
                    difficulty = 2
                elif (timePassed < 45):
                    difficulty = 3
                else:
                    difficulty = 4

            if alive and len(enemy.sprites()) < difficulty:
                enemyShip = EnemyShip(enemy, [random.randint(10, 1000), random.randint(10, 750)], 6.8, 13, Weapon(playerDeadly, 0), 'img/enemyship1.png', playerShip)

        if alive:

            if timeCounter > 5:
                timeCounter = 0
                score += 1
                if score > highScore:
                    highScore = score

            # update sprites
            updateSpriteGroups(spritesList, tickReturn)

            # test collision
            pygame.sprite.groupcollide(sprites, enemy, False, True, pygame.sprite.collide_rect_ratio(0.4))
            deadEnemyList = pygame.sprite.groupcollide(enemy, enemyDeadly, True, True, pygame.sprite.collide_rect_ratio(0.4))
            deadPlayerList = pygame.sprite.groupcollide(sprites, playerDeadly, True, True, pygame.sprite.collide_rect_ratio(0.4))

            for deadPlayer in deadPlayerList:
                alive = False

            for deadEnemy in deadEnemyList:
                score += 10
                if score > highScore:
                    highScore = score

        updateScreen(spritesList, screen, hud, score, highScore, alive)


def updateScreen(spritesList, screen, hud, score, highScore, alive):
    # background = pygame.image.load('img/bg.jpg')
    screen.fill((0,0,0))
    # screen.blit(background, (-500, -500))

    drawSpriteGroups(spritesList, screen)
    hud.updateScore(score)
    if not alive:
        Menu().displayMenu(screen, 3, score, highScore)

    pygame.display.flip()

def updateSpriteGroups(spriteGroups, tickReturn):
    for group in spriteGroups:
        group.update(tickReturn)

def drawSpriteGroups(spriteGroups, screen):
    for group in spriteGroups:
        group.draw(screen)

if __name__ == "__main__":
    pygame.init()
    main()


    



# import required modules
# import math
# import pygame
# from pygame.sprite import Sprite

# # global variables
# WIDTH = 1280
# HEIGHT = 720
# FPS = 60

# # define objects
# class Spaceship(Sprite):
#     def __init__(self, color, width, height, position, accel, maxSpeed):
#         Sprite.__init__(self)
#         self.velocity = [0.0, 0.0]        # velocity vector of spaceship
#         self.acceleration = float(accel)  # acceleration in both direction
#         self.topSpeed = maxSpeed          # maximum speed of spaceship
#         self.direction = 0                # spaceship rotation, north is 0, anti-clock
#         self.shipHeight = height
#         self.shipWidth = width
#         self.position = position
#         self.image = pygame.Surface([self.shipWidth, self.shipHeight])
#         self.rect = self.image.get_rect()
#         self.rect.center = self.position
#         self.originImage = self.image

# class Playership(Spaceship):
#     def __init__(self, color, position):
#         Spaceship.__init__(self, color, HEIGHT/16*0.6, HEIGHT/16, position, 1, 15)

#         self.coolDown = 0

#         # draw player spaceship
#         lines = [(1, self.shipHeight-1), (self.shipWidth/2, 1), (self.shipWidth-1, self.shipHeight-1), (self.shipWidth/2, self.shipHeight-8)]
#         pygame.draw.lines(self.image, pygame.Color(color), True, lines, 2)

#     def updateDirection(self):
#         mousePosition = pygame.mouse.get_pos()
#         # calculate direction
#         if (self.position[1] - mousePosition[1] != 0):
#             self.direction = math.degrees(math.atan(float(self.position[0] - mousePosition[0]) / float(self.position[1] - mousePosition[1])))
#         if (self.position[1] - mousePosition[1] < 0):
#             self.direction += 180
#         # rotate image
#         self.image = pygame.transform.rotate(self.originImage, self.direction)
#         self.rect = self.image.get_rect(center=self.rect.center)

#     def move(self):
#         print self.direction
#         if pygame.mouse.get_pressed()[2]:
#             # accelerate if right mouse id down
#             # calculate velocity based on initial velocity
#             v = math.hypot(self.velocity[0], self.velocity[1]) + (self.acceleration / (FPS*0.1))
#             # test for maximum velocity
#             if v > self.topSpeed:
#                 v -= (self.acceleration /2.0)
            
#             mousePosition = pygame.mouse.get_pos()
#             if (math.hypot((self.position[0] - mousePosition[0]), (self.position[1] - mousePosition[1])) < 10):
#                 # if mouse is within 10 pixel radius, don't move
#                 self.velocity = [0, 0]
#             else:
#                 # calculate velocity vector and move the rect and image
#                 angle = self.direction
#                 self.velocity[0] = math.sin(math.radians(angle)) * v * -1
#                 self.velocity[1] = math.cos(math.radians(angle)) * v * -1
                
#         else:
#             # decelerate if right mouse is up
#             if self.velocity[0] != 0:
#                 self.velocity[0] *= 0.95
#             if self.velocity[1] != 0:
#                 self.velocity[1] *= 0.95
#             if -0.001 < self.velocity[0] < 0.001:
#                 self.velocity[0] = 0
#             if -0.001 < self.velocity[1] < 0.001:
#                 self.velocity[1] = 0

#         self.rect.move_ip(int(self.velocity[0]), int(self.velocity[1]))
#         self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
#         self.rect.center = self.position

#     def shoot(self, screen):

#         if self.coolDown == 0:
#             self.coolDown = 5
#             bullet = Bullet(1, (self.position[0], self.position[1]), self.direction)
#             return bullet
#         else:
#             self.coolDown-=1
#             return None

#     def update(self):
#         self.updateDirection()
#         self.move()

# class Bullet(Sprite):
#     def __init__(self, bullet_id, position, angle):
#         Sprite.__init__(self)
#         # draw bullet
#         self.position = position
#         self.direction = angle
#         self.speed = 25
#         self.image = pygame.Surface([4, 20])
#         self.originImage = self.image
#         self.rect = self.image.get_rect()
#         self.rect.center = self.position
#         pygame.draw.line(self.image, pygame.Color("white"), (1, 1), (1, 19),2)

#         # rotate image
#         self.image = pygame.transform.rotate(self.originImage, self.direction)
#         self.rect = self.image.get_rect(center=self.rect.center)

#     def move(self):
#         v = [0, 0]
#         v[0] = int(math.sin(math.radians(self.direction)) * self.speed)
#         v[1] = int(math.cos(math.radians(self.direction)) * self.speed)
#         self.rect.move_ip(v[0] * -1, v[1] * -1)
#         self.position = (self.position[0] - v[0], self.position[1] - v[1])
#         self.rect.center = self.position
        
#     def update(self):
#         self.move()

# # main function
# def main():
#     # set window properties
#     pygame.init()
#     infoObject = pygame.display.Info()
#     WIDTH = infoObject.current_w
#     HEIGHT = infoObject.current_h
#     screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
#     pygame.display.set_caption("Galactic War v0.0.2")

#     # background
#     background = pygame.Surface([WIDTH, HEIGHT])
#     background.fill(pygame.Color("black"))
#     screen.blit(background, (0, 0))

#     #bgimg = pygame.Surface([2560, 1600])
#     #bgimg = pygame.image.load('img/bg.png')
#     #screen.blit(bgimg, (0, 0))

#     # setup sprites
#     player = Playership("#00CCFF", (WIDTH/2, HEIGHT/2))

#     bullet = player.shoot(screen)
#     bulletArray = [bullet]

#     # list sprites to render
#     spriteArray = [player]
#     sprites = pygame.sprite.RenderPlain(spriteArray)

#     # game loop
#     running = True
#     clock = pygame.time.Clock()
    
#     while running:
#         clock.tick(FPS)
#         pygame.display.set_caption("Galactic War v0.0.2 - {0:.3f} fps".format(clock.get_fps()))
        
#         sprites.update()

#         if pygame.mouse.get_pressed()[0]:
#             bullet = player.shoot(screen)
#             if bullet != None:
#                 bulletArray.append(bullet)
#                 sprites.add(bullet)
#         for temp_bullet in bulletArray:
#             if temp_bullet.position[0] < 0 or temp_bullet.position[0] > WIDTH:
#                 sprites.remove(temp_bullet)
#                 bulletArray.remove(temp_bullet)
#             elif temp_bullet.position[1] < 0 or temp_bullet.position[1] > HEIGHT:
#                 sprites.remove(temp_bullet)
#                 bulletArray.remove(temp_bullet)

#         sprites.draw(screen)
#         pygame.display.flip()
#         sprites.clear(screen, background)
#         #sprites.clear(screen, bgimg)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     running = False

# # if executed as a script, run main()
# if __name__ == "__main__":
#     main()
