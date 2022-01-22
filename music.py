import pygame

pygame.init()


def musicplayer():
    pygame.mixer.music.load("")  # вставить название музыки, музыка должна быть в одной папке с основным кодом
    pygame.mixer.music.play()
    #
    W, H = 500, 300                       # стереть т.к. функция встанет
    sc = pygame.display.set_mode((W, H))  # в готовый дисплей

    clock = pygame.time.Clock  # вставить параметры из main
    FPS = 60                   #

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
