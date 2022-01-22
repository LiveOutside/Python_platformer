import pygame

pygame.init()


def musicplayer(musicname):
    pygame.mixer.music.load(musicname)
    pygame.mixer.music.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
