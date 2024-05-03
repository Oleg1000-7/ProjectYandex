import pygame

pygame.init()

h, w = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((h, w))
screen_w, screen_h = screen.get_size()
FPS = 60
# COLORS
BLACK = pygame.Color(0, 0, 0, 255)
WHITE = pygame.Color(255, 255, 255, 255)
RED = pygame.Color(255, 0, 0, 255)
GREEN = pygame.Color(0, 255, 0, 255)
BLUE = pygame.Color(0, 0, 255, 255)
# MAIN MENU CONSTANTS
