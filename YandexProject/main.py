import pygame
import Button
from Constants import *

pygame.init()

screen = pygame.display.set_mode((800, 600))

screen.fill(BLACK)

main_surface = pygame.Surface((200, 200))
main_surface.fill(WHITE)


while True:
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
