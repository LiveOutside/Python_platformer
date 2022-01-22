import pygame


class UI:
    def __init__(self, surface):

        self.display_surface = surface

        self.font = pygame.font.Font('../graphics/UI/font/Pixellettersfull-BnJ5.ttf', 30)

        self.health_bar = pygame.image.load('../graphics/UI/healthbar_emp.png')
        self.health_bar_top_left = (38, 32)
        self.health_bar_width = 108
        self.health_bar_height = 8

        self.coin_bar = pygame.image.load('../graphics/UI/Coini.png')
        self.coin_bar_rect = self.coin_bar.get_rect(topleft=(20, 50))

    def show_health_bar(self, current_hp, full_hp):
        self.display_surface.blit(self.health_bar, (20, 10))
        health_status = current_hp / full_hp
        health_bar_width = self.health_bar_width * health_status
        health_bar_rect = pygame.Rect(self.health_bar_top_left, (health_bar_width, self.health_bar_height))
        pygame.draw.rect(self.display_surface, 'red', health_bar_rect)

    def show_coin_bar(self, coins):
        self.display_surface.blit(self.coin_bar, self.coin_bar_rect)
        coins_amount = self.font.render(str(coins), False, 'white')
        coins_amount_rect = coins_amount.get_rect(midleft=(self.coin_bar_rect.right + 4,
                                                           self.coin_bar_rect.centery))
        self.display_surface.blit(coins_amount, coins_amount_rect)