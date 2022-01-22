import pygame, sys
from settings import *
from PIL import Image


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
image = Image.open('../graphics/start screen/img.png')


def start_screen():
    intro_text = ["SIMPLE PLATFORMER", "",
                  "CREATORS:",
                  "Владислав Маслихов",
                  "Георгий Чистяков",
                  "Торлопов Николай"]

    fon = pygame.transform.scale(pygame.image.load('../graphics/start screen/img.png'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


while True:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.K_SPACE:
            terminate()

    screen.fill(pygame.Color('black'))
    start_screen()
    pygame.display.flip()
