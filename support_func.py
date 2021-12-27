import pygame
from os import walk


def open_folder(path):
    img_list = []

    for _, _, img_files in walk(path):
        for image in img_files:
            img_path = path + '/' + image
            img_surface = pygame.image.load(img_path).convert_alpha()
            img_list.append(img_surface)

    return img_list
