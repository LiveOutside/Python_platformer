import pygame, sys
from settings import *
from level import Level

pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
FPS = 60
level = Level(level_map, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(pygame.Color('black'))
    level.run()
    pygame.display.flip()
    clock.tick(FPS)