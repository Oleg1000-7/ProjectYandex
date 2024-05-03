from button import Button
from player import Player
from constants import *

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

main_surface = pygame.Surface((screen_w, screen_h))

class Game:
    def __init__(self):
        pass

    def __call__(self, keys, mouse_pos, mouse_k):
        screen.blit(main_surface, (0, 0))
        main_surface.fill(BLACK)

        scene = "GAME"
        if keys[pygame.K_q]:
            scene = "MENU"

        all_sprites.update(keys)
        all_sprites.draw(main_surface)

        return scene
