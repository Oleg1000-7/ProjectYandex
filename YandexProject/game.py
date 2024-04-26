import pygame
from main import screen
from button import Button
from constants import*

def game():
    scene = "GAME"
    screen.fill(WHITE)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        scene = "MENU"

    return scene