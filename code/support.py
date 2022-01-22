from csv import reader
from settings import tile_size
from os import walk, listdir
import pygame


# loading files from folder using given path
def import_folder(path):
	surface_list = []

	for _, _, image_files in walk(path):
		for image in image_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list


# creating level layout
def import_csv_layout(path):
	terrain_map = []
	with open(path) as map:
		level = reader(map, delimiter=',')
		for row in level:
			terrain_map.append(list(row))
		return terrain_map


# cuts tile sheet into rect objects / returns list of rect objects
def import_cut_graphics(path):
	surface = pygame.image.load(path).convert_alpha()
	tile_num_x = int(surface.get_size()[0] / tile_size)
	tile_num_y = int(surface.get_size()[1] / tile_size)

	cut_tiles = []
	for row in range(tile_num_y):
		for col in range(tile_num_x):
			x = col * tile_size
			y = row * tile_size
			new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
			new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
			cut_tiles.append(new_surf)

	return cut_tiles


# function for testing .png, not tile sets
def create_surface_list(path):
	result = []
	list = []
	for i in listdir(path):
		list.append(i)
	for j in list:
		r = path + f'/{j}'
		surface = pygame.image.load(r)
		new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
		new_surf.blit(surface, (0, 0), pygame.Rect(0, 0, tile_size, tile_size))
		result.append(new_surf)

	return result


def path_finder(path):
	paths_list = []
	list = []
	for i in listdir(path):
		list.append(i)
	for j in list:
		img_path = path + f'/{j}'
		paths_list.append(img_path)

	return paths_list
