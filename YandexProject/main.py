from constants import *
from menu import Menu
from game import Game
from settings import Settings

clock = pygame.time.Clock()
pygame.init()

menu = Menu()
settings = Settings()
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
        game = Game()
        scene = game(keys, mouse_pos, mouse_k)

    elif scene == "SETTINGS":
        scene = settings(mouse_pos, mouse_k)

    running = not keys[pygame.K_ESCAPE] and scene != "EXIT"

    for event in events:
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
