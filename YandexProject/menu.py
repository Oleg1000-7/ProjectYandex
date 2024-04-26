import pygame
from main import screen
from button import Button

screen_w, screen_h = screen.get_size()
main_surface = pygame.Surface((screen_w, screen_h))
main_surface_w, main_surface_h = main_surface.get_size()

btn_play = Button(main_surface, main_surface_w, main_surface_h,  100, 50, text="Play")
btn_info = Button(main_surface, main_surface_w, main_surface_h + 60, 100, 50, text="Information")
btn = Button(main_surface, main_surface_w, main_surface_h + 60, 100, 50, text="Play")


def menu():
    scene = "MENU"
    screen.blit(main_surface, (0, 0))

    btn.draw()
    events = pygame.event.get()
    mouse = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and btn.rect.collidepoint(mouse):
            scene = "GAME"

            break

    return scene
