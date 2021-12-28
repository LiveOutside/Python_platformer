import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player


class Level:
    def __init__(self, level_data, surface):
        #level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x_pos = 0

    def setup_level(self, layout):
        self.tile_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                x, y = column_index * tile_size, row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tile_group.add(tile)
                if cell == 'P':
                    player_model = Player((x, y))
                    self.player_group.add(player_model)

    def scroll_x(self):
        player = self.player_group.sprite
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

    def horizontal_movement_collision(self):
        player = self.player_group.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tile_group.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x_pos = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x_pos = player.rect.right

        if player.on_left and (player.rect.left < self.current_x_pos or player.direction.x >= 0):
            player.on_left = False
        elif player.on_right and (player.rect.right < self.current_x_pos or player.direction.x < 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player_group.sprite
        player.apply_gravity()

        for sprite in self.tile_group.sprites():
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
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
    def run(self):

        # level tiles
        self.tile_group.update(self.world_shift)
        self.tile_group.draw(self.display_surface)

        # player
        self.player_group.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player_group.draw(self.display_surface)
        self.scroll_x()


