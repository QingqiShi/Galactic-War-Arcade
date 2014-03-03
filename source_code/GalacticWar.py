#!/usr/bin/env python

# import required modules
import pygame


# main function
def main():
    # set window properties
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Galactic War")

    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# if executed as a script, run main()
if __name__ == "__main__":
    main()