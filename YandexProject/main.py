import pygame
from constants import *
from menu import menu
from game import game

pygame.init()

h, w = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((h, w))
screen_w, screen_h = screen.get_size()

scene = "MENU"
level = 1

keys = list()
events = list()
mouse = tuple()
Running = True
while Running:
    pygame.display.flip()
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()
    events = pygame.event.get()

    if scene == "MENU":
        scene = menu()

    elif scene == "GAME":
        scene = game()

    Running = not keys[pygame.K_ESCAPE]

    for event in events:
        if event.type == pygame.QUIT:
            Running = False

pygame.quit()
