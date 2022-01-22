import pygame


vertical_tile_number = 16
tile_size = 32

screen_height = vertical_tile_number * tile_size
screen_width = 1200


# creating background
# setting images
bg_image_main = pygame.image.load('../graphics/decoration/sky/1.png')
bg_dark_forest = pygame.image.load('../graphics/decoration/sky/2.png')
bg_light_forest = pygame.image.load('../graphics/decoration/sky/3.png')
bg_water = pygame.image.load('../graphics/decoration/sky/4.png')
bg_log = pygame.image.load('../graphics/decoration/sky/5.png')

# rescaling images
bg_main = pygame.transform.scale(bg_image_main, (screen_width, screen_height))
bg_dark = pygame.transform.scale(bg_dark_forest, (screen_width, screen_height))
bg_light = pygame.transform.scale(bg_light_forest, (screen_width, screen_height))
bg_w = pygame.transform.scale(bg_water, (screen_width, screen_height))
bg_l = pygame.transform.scale(bg_log, (screen_width, screen_height))

pos_d = 0
pos_li = 0
pos_l = 0
pos_wat = 0

additional_width_d = screen_width
additional_width_li = screen_width
additional_width_l = screen_width
additional_width_wat = screen_width



