import pygame
from game_data import levels


class LevelMenu:
    def __init__(self, level, unlocked, surface, open_level):

        # setting parameters
        self.unlocked_levels = unlocked
        self.current_level = level
        self.open_level = open_level
        self.display_surface = surface

        # player
        self.icon = pygame.sprite.GroupSingle()

        # movement
        self.movement_in_progress = False
        self.movement_direction = pygame.math.Vector2(0, 0)
        self.speed = 8

        # sprites
        self.setup_level_pos()
        self.setup_player_icon()

    # setting class LevelIcon in specified position
    def setup_level_pos(self):
        self.levels = pygame.sprite.Group()

        for id, level_data in enumerate(levels.values()):
            if id <= self.unlocked_levels:
                level_sprite = LevelIcon(level_data['pos'], 'available', self.speed)
            else:
                level_sprite = LevelIcon(level_data['pos'], 'unavailable', self.speed)
            self.levels.add(level_sprite)

    # setting class PlayerIcon in specified position (connected to current level position)
    def setup_player_icon(self):
        icon_sprite = PlayerIcon(self.levels.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    # creating lines between different LevelIcons
    def create_paths(self):
        cords = []
        if self.unlocked_levels > 0:
            for id, level_data in enumerate(levels.values()):
                if id <= self.unlocked_levels:
                    cords.append(level_data['pos'])

            pygame.draw.lines(self.display_surface, 'grey', False, cords, 6)

    # responding to player keyboard input in level menu
    def player_input(self):
        keys = pygame.key.get_pressed()

        if not self.movement_in_progress:
            if keys[pygame.K_d] and self.current_level < self.unlocked_levels:
                self.movement_direction = self.movement('next')
                self.current_level += 1
                self.movement_in_progress = True
            elif keys[pygame.K_a] and self.current_level > 0:
                self.movement_direction = self.movement('last')
                self.current_level -= 1
                self.movement_in_progress = True
            elif keys[pygame.K_SPACE]:
                self.open_level(self.current_level)

    # moving PlayerIcon in level menu
    def movement(self, level_pos):
        # "level 1"(pos) - "level 2"(pos) = direction
        start_point = pygame.math.Vector2(self.levels.sprites()[self.current_level].rect.center)
        if level_pos == 'next':
            final_point = pygame.math.Vector2(self.levels.sprites()[self.current_level + 1].rect.center)
        else:
            final_point = pygame.math.Vector2(self.levels.sprites()[self.current_level - 1].rect.center)
        return (final_point - start_point).normalize()

    # checking PlayerIcon status
    def get_player_pos(self):
        if self.movement_in_progress and self.movement_direction:
            self.icon.sprite.pos += self.movement_direction * self.speed
            level_path = self.levels.sprites()[self.current_level]
            if level_path.block.collidepoint(self.icon.sprite.pos):
                self.movement_in_progress = False
                self.movement_direction = pygame.math.Vector2(0, 0)

    # activation
    def run(self):
        self.player_input()
        self.get_player_pos()
        self.icon.update()
        self.create_paths()
        self.levels.draw(self.display_surface)
        self.icon.draw(self.display_surface)


# creating level surface in level menu
class LevelIcon(pygame.sprite.Sprite):
    def __init__(self, pos, status, player_speed):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        if status == 'available':
            self.image.fill('#8054E8')
        else:
            self.image.fill('grey')
        self.rect = self.image.get_rect(center=pos)

        self.block = pygame.Rect(self.rect.centerx - (player_speed / 2),
                                 self.rect.centery - (player_speed / 2),
                                 player_speed, player_speed)


# creating player surface in level menu
class PlayerIcon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((20, 20))
        self.image.fill('#FFFFFF')
        self.rect = self.image.get_rect(center=pos)

    # updating current rect.center pos of PlayerIcon
    def update(self):
        self.rect.center = self.pos
