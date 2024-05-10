from constants import *
from menu import Menu
from game import Game
from player import Player

clock = pygame.time.Clock()
pygame.init()

game = Game()
menu = Menu()
scene = "MENU"
level = 1

keys = list()
events = list()
mouse = tuple()
running = True

while running:
    clock.tick(60)
    pygame.display.flip()
    screen.fill(BLACK)

    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_k = pygame.mouse.get_pressed()
    events = pygame.event.get()

    if scene == "MENU":
        scene = menu(mouse_pos, mouse_k)

    elif scene == "GAME":
        scene = game(keys, mouse_pos, mouse_k)

    running = not keys[pygame.K_ESCAPE] and scene != "EXIT"

    for event in events:
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
