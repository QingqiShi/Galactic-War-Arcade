#!/usr/bin/env python

# import required modules
import pygame
import random
import math
import time

# import different modules
from Spaceship  import *
from Weapon import *
from Menu import *
from HUD import *

def main():

    screen = pygame.display.set_mode((1024, 768))
    quit = False
    while not quit:
        quit = startGame(screen)

def startGame(screen):
    pygame.mixer.init()
    # create sprite groups
    sprites = pygame.sprite.Group()
    enemy = pygame.sprite.Group()
    playerDeadly = pygame.sprite.Group()
    enemyDeadly = pygame.sprite.Group()

    spritesList = [sprites, enemy, playerDeadly, enemyDeadly]

    gameStartTime = time.time()
    pauseTime = 0
    pauseStartTime = time.time()
    score = 0
    timeCounter = 0

    f = open('highScore', 'a+')
    temp = f.read()
    if temp != "":
        highScore = int(temp)
    else:
        highScore = 0
    f.close()

    # create player ship
    playerShip = PlayerShip(sprites, [512, 384], 6.8, 13, Weapon(enemyDeadly, 0), 'img/playership1.png')
    alive = True
    pause = False
    

    # create HUD
    hud = HUD(screen)

    explodeSound = pygame.mixer.Sound('explosion.ogg')
    bgMusic = pygame.mixer.Sound('bgloop.ogg')
    wooshSound = pygame.mixer.Sound('woosh.ogg')
    bgMusic.play(-1)

    # start game loop
    clock = pygame.time.Clock()
    while True:
        tickReturn = clock.tick(60) / 1000.0
        timeCounter += tickReturn
        pygame.display.set_caption("Galactic War v1.0.0 - {0:.3f} fps".format(clock.get_fps()))

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f = open('highScore', 'w')
                f.write(str(highScore))
                f.close()
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and alive:
                if pause:
                    pause = False
                    pauseTime += time.time() - pauseStartTime
                    bgMusic.play(-1)
                else:
                    pause = True
                    pauseStartTime = time.time()
                    bgMusic.stop()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a and alive:
                if playerShip.autoShoot:
                    playerShip.autoShoot = False
                else:
                    playerShip.autoShoot = True
            
        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            f = open('highScore', 'w')
            f.write(str(highScore))
            f.close()
            return False
        

        # calculate random tick
        randomTick = random.randint(0, 4 * int(clock.get_fps())) == 1 and True or False

        # handle randomTick action
        if randomTick:
            if alive and (not pause):
                timePassed = time.time() - gameStartTime
                if (timePassed < 15 + pauseTime):
                    difficulty = 1
                elif (timePassed < 30 + pauseTime):
                    difficulty = 2
                elif (timePassed < 45 + pauseTime):
                    difficulty = 3
                else:
                    difficulty = 4

            if alive and (not pause) and len(enemy.sprites()) < difficulty:
                wooshSound.play()
                enemyShip = EnemyShip(enemy, [random.randint(10, 1000), random.randint(10, 750)], 6.8, 13, Weapon(playerDeadly, 0), 'img/enemyship1.png', playerShip)

        if alive and (not pause):

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
                explodeSound.play()
                bgMusic.stop()

            for deadEnemy in deadEnemyList:
                score += 10
                explodeSound.play()
                if score > highScore:
                    highScore = score

        updateScreen(spritesList, screen, hud, score, highScore, alive, pause)

def updateScreen(spritesList, screen, hud, score, highScore, alive, pause):
    # background = pygame.image.load('img/bg.jpg')
    screen.fill((0,0,0))
    # screen.blit(background, (-500, -500))

    drawSpriteGroups(spritesList, screen)
    hud.updateScore(score)
    if not alive:
        Menu().displayMenu(screen, 3, score, highScore)
    elif pause:
        Menu().displayMenu(screen, 2)

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
