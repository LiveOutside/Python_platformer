import pygame
import sys
from settings import *
from level import Level
from game_data import level_0
from level_menu import LevelMenu
from UI import UI
import os
from PIL import Image


# Pygame setup
class Game:
	def __init__(self):
		self.last_level = 0
		self.health = 100
		self.current_health = 100
		self.coins_count = 0
		self.UI = UI(screen)

		self.level_menu = LevelMenu(0, self.last_level, screen, self.open_level)
		self.current_status = 'level_menu'

	def open_level(self, current_level):
		self.level = Level(current_level, screen, self.open_level_menu, self.count_coins)
		self.current_status = 'level'

	def open_level_menu(self, current_level, last_level):
		self.coins_count = 0
		if last_level > self.last_level:
			self.last_level = last_level
		self.level_menu = LevelMenu(current_level, self.last_level, screen, self.open_level)
		self.current_status = 'level_menu'

	def count_coins(self, coins):
		self.coins_count += coins

	def run(self):
		if self.current_status == 'level_menu':
			self.level_menu.run()
		else:
			self.level.run()
			self.UI.show_health_bar(self.current_health, self.health)
			self.UI.show_coin_bar(self.coins_count)


block = 1


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


pygame.init()
FPS = 50
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.K_e:
			block = 0
			pygame.display.flip()
	screen.fill((0, 0, 0))
	screen.blit(bg_main, (0, 0))
	screen.blit(bg_dark, (pos_d, 0))
	screen.blit(bg_dark, (additional_width_d + pos_d, 0))
	if pos_d == -additional_width_d:
		screen.blit(bg_dark, (additional_width_d + pos_d, 0))
		pos_d = 0
	pos_d -= 0.5
	screen.blit(bg_light, (pos_li, 0))
	screen.blit(bg_light, (additional_width_li + pos_li, 0))
	if pos_li == -additional_width_li:
		screen.blit(bg_light, (additional_width_li + pos_li, 0))
		pos_li = 0
	pos_li -= 1
	screen.blit(bg_w, (pos_wat, 0))
	screen.blit(bg_w, (additional_width_wat + pos_wat, 0))
	if pos_wat == -additional_width_wat:
		screen.blit(bg_w, (additional_width_l + pos_wat, 0))
		pos_wat = 0
	pos_wat -= 1
	screen.blit(bg_l, (pos_l, 0))
	screen.blit(bg_l, (additional_width_l + pos_l, 0))
	if pos_l == -additional_width_l:
		screen.blit(bg_l, (additional_width_l + pos_l, 0))
		pos_l = 0
	pos_l -= 1
	game.run()

	pygame.display.flip()
	clock.tick(FPS)
