import sys
import pygame
from support import import_csv_layout, import_cut_graphics, create_surface_list, import_folder
from support import path_finder
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, AnimatedCoin, Ridge, Ladder
from player import Player
from particles import ParticleEffect
from game_data import levels


class Level:
	def __init__(self, current_level, surface, open_level_menu, count_coins):
		# world setup
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None

		# level_menu connection
		self.open_level_menu = open_level_menu
		self.current_level = current_level
		level_data = levels[self.current_level]
		self.new_last_level = level_data['unlock']

		# player setup
		player_layout = import_csv_layout(level_data['spawn'])
		self.player = pygame.sprite.GroupSingle()
		self.finish_line = pygame.sprite.GroupSingle()
		self.player_setup(player_layout)
		self.count_coins = count_coins

		# dust sprites
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		# terrain setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

		# grass setup
		grass_layout = import_csv_layout(level_data['grass'])
		self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

		# ridges setup
		# ridges_layout = import_csv_layout(level_data['ridges'])
		# self.ridges_sprites = self.create_tile_group(ridges_layout, 'ridges')

		# crates setup
		crates_layout = import_csv_layout(level_data['crates'])
		self.crates_sprites = self.create_tile_group(crates_layout, 'crates')

		# start setup
		start_layout = import_csv_layout(level_data['start'])
		self.start_sprites = self.create_tile_group(start_layout, 'start')

		# finish setup
		finish_layout = import_csv_layout(level_data['finish'])
		self.finish_sprites = self.create_tile_group(finish_layout, 'finish')

		# coins setup
		coins_layout = import_csv_layout(level_data['coins'])
		self.coins_sprites = self.create_tile_group(coins_layout, 'coins')

		# ladder setup
		ladder_layout = import_csv_layout(level_data['ladder'])
		self.ladder_sprites = self.create_tile_group(ladder_layout, 'ladder')

	# setting images on objects (based on TILED layout .CSV)
	def create_tile_group(self, layout, type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index, val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('../graphics/terrain/Tileset.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)

					if type == 'grass':
						grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png')
						tile_surface = grass_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)

					if type == 'ladder':
						if val == '0':
							sprite = Ladder('../graphics/decoration/ladder/1.png', tile_size, x, y)
						if val == '1':
							sprite = Ladder('../graphics/decoration/ladder/2.png', tile_size, x, y)
						if val == '2':
							sprite = Ladder('../graphics/decoration/ladder/3.png', tile_size, x, y)

					# if type == 'ridges':
					# 	if val == '1':
					# 		sprite = Ridge(tile_size, x, y, '../graphics/decoration/ridges/1', 120)
					# 	if val == '2':
					# 		sprite = Ridge(tile_size, x, y, '../graphics/decoration/ridges/2', 120)
					# 	if val == '3':
					# 		sprite = Ridge(tile_size, x, y, '../graphics/decoration/ridges/3', 120)
					# 	if val == '4':
					# 		sprite = Ridge(tile_size, x, y, '../graphics/decoration/ridges/4', 120)
					# 	if val == '5':
					# 		sprite = Ridge(tile_size, x, y, '../graphics/decoration/ridges/5', 120)
					# 	if val == '6':
					# 		sprite = Ridge(tile_size, x, y, '../graphics/decoration/ridges/6', 120)
					# 	if val == '7':
					# 		sprite = Ridge(tile_size, x, y, '../graphics/decoration/ridges/7', 120)
					# 	if val == '8':
					# 		sprite = Ridge(tile_size, x, y, '../graphics/decoration/ridges/8', 120)
					# 	if val == '9':
					# 		sprite = Ridge(tile_size, x, y, '../graphics/decoration/ridges/9', 120)
					# 	if val == '10':
					# 		sprite = Ridge(tile_size, x, y, '../graphics/decoration/ridges/10', 120)
					# 	if val == '11':
					# 		sprite = Ridge(tile_size, x, y, '../graphics/decoration/ridges/11', 120)
					# 	if val == '12':
					# 		sprite = Ridge(tile_size, x, y, '../graphics/decoration/ridges/12', 120)

					if type == 'coins':
						sprite = AnimatedCoin(tile_size, x, y, '../graphics/coins')

					if type == 'crates':
						sprite = Crate('../graphics/decoration/crates/4.png', tile_size, x, y)

					if type == 'start':
						sprite = Crate('../graphics/decoration/start/5.png', tile_size, x, y)

					if type == 'finish':
						sprite = Crate('../graphics/decoration/finish/1.png', tile_size, x, y)
						self.finish_line.add(sprite)

					sprite_group.add(sprite)
		
		return sprite_group

	# setting the player on the surface
	def player_setup(self, layout):
		for row_index, row in enumerate(layout):
			for col_index, val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val != '-1':
					sprite = Player((x, y), self.display_surface, self.create_jump_particles)
					self.player.add(sprite)

	# creating particle effect for jumps
	def create_jump_particles(self, pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(1, 5)
		else:
			pos += pygame.math.Vector2(10, -5)
		jump_particle_sprite = ParticleEffect(pos, 'jump')
		self.dust_sprite.add(jump_particle_sprite)

	# collision axis(x)
	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		collidable_sprites = self.terrain_sprites.sprites() + self.crates_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	# collision axis(y)
	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()
		collidable_sprites = self.terrain_sprites.sprites() + self.crates_sprites.sprites()

		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	# camera movement
	def camera(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0

		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0

		else:
			self.world_shift = 0
			player.speed = 8

	# additional player info
	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def death_info(self):
		player = self.player.sprite.rect.top
		if player > screen_height:
			self.open_level_menu(self.current_level, 0)

	def level_complete(self):
		if pygame.sprite.spritecollide(self.player.sprite, self.finish_line, False) and not self.coins_sprites:
			self.open_level_menu(self.current_level, self.new_last_level)

	def ladder_mechanic(self):
		keys = pygame.key.get_pressed()
		player = self.player.sprite
		if keys[pygame.K_w] and pygame.sprite.spritecollide(self.player.sprite, self.ladder_sprites, False):
			player.direction.y -= 1
		elif keys[pygame.K_s] and pygame.sprite.spritecollide(self.player.sprite, self.ladder_sprites, False):
			player.direction.y += 1

	def coin_pickup(self):
		picked_coins = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)
		if picked_coins:
			for coin in picked_coins:
				self.count_coins(1)

	def run(self):

		# terrain
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)

		# # ridges
		# self.ridges_sprites.update(self.world_shift)
		# self.ridges_sprites.draw(self.display_surface)

		# start stone
		self.start_sprites.update(self.world_shift)
		self.start_sprites.draw(self.display_surface)

		# finish stone
		self.finish_sprites.update(self.world_shift)
		self.finish_sprites.draw(self.display_surface)

		# crates
		self.crates_sprites.update(self.world_shift)
		self.crates_sprites.draw(self.display_surface)

		# ladder
		self.ladder_sprites.update(self.world_shift)
		self.ladder_sprites.draw(self.display_surface)

		# player sprites
		self.player.update()
		self.horizontal_movement_collision()

		self.get_player_on_ground()
		self.vertical_movement_collision()

		self.camera()
		self.player.draw(self.display_surface)

		# coins
		self.coins_sprites.update(self.world_shift)
		self.coins_sprites.draw(self.display_surface)

		# grass
		self.grass_sprites.update(self.world_shift)
		self.grass_sprites.draw(self.display_surface)

		# level reactions
		self.death_info()
		self.level_complete()
		self.ladder_mechanic()
		self.coin_pickup()

		# dust particles
		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)

