import pygame, sys
from settings import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()

while True:
    # event loop logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)


    #Drawing logic
    pygame.display.update()
    clock.tick(60)        