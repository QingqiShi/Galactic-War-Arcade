#!/usr/bin/env python

# import required modules
import math
import pygame

def main():
    screen = pygame.display.set_mode((1024, 768))
    startGame(screen, 1)

def startGame(screen, level):
    background = pygame.image.load('img/bg.jpg')

    sprites = pygame.sprite.Group()
    playerShip = PlayerShip(sprites, [320, 480], 6.8, 13, 0, 'img/playership1.png')

    clock = pygame.time.Clock()
    while True:
        tickReturn = clock.tick(120) / 1000.0
        pygame.display.set_caption("Galactic War v0.1.0 - {0:.3f} fps - {1:.4f}".format(clock.get_fps(), tickReturn))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        
        sprites.update(tickReturn)
        screen.fill((0,0,0))
        screen.blit(background, (-500, -500))
        sprites.draw(screen)
        pygame.display.flip()

class Spaceship(pygame.sprite.Sprite):
    velocity = [0, 0]
    speed = 0.0
    acceleration = 0.0
    maxSpeed = 0
    direction = 0
    weapon = 0
    center = [0, 0]

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
        oldSpeed = self.speed
        newSpeed =  oldSpeed - (self.acceleration * tickReturn * 2)

        # test for maxSpeed
        if newSpeed > 0.5:

            # Find the factor
            factor = newSpeed / oldSpeed
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


class PlayerShip(Spaceship):
    def __init__(self, groups, position, acceleration, maxSpeed, weapon, image_path):
        super(PlayerShip, self).__init__(groups, position, acceleration, maxSpeed, weapon, image_path)

    def update(self, tickReturn):
        super(PlayerShip, self).updateDirection(pygame.mouse.get_pos())

        # rotate image
        self.image = pygame.transform.rotate(self.originImage, math.degrees(self.direction) * -1)
        self.rect = self.image.get_rect(center=self.rect.center)

        super(PlayerShip, self).calculateCenter()

        

        mouseDistance = math.hypot(pygame.mouse.get_pos()[0] - self.center[0], pygame.mouse.get_pos()[1] - self.center[1])

        print(self.speed)

        if (pygame.mouse.get_pressed()[2] and mouseDistance > 5):
            super(PlayerShip, self).accelerate(tickReturn)
        elif (mouseDistance < 5):
            self.velocity = [0, 0]
        else:
            super(PlayerShip, self).deccelerate(tickReturn)

        self.rect.move_ip(self.velocity[0], self.velocity[1]) 

    # self.rect.move_ip(int(self.velocity[0]), int(self.velocity[1]))
    # self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
    # self.rect.center = self.position


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
