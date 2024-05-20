import pygame.sprite

from player import Player
from object import Object
from enemy import Enemy
from finish import Finish
from constants import *

world_map = pygame.sprite.Group()
for line in range(len(MAP)):
    for char in range(len(MAP[line])):
        if MAP[line][char] == "X":
            world_map.add(Object(((char - 1) * BLOCK_WIDTH, (line) * BLOCK_HEIGHT)))
        if MAP[line][char] == "E":
            world_map.add(Enemy(((char - 1) * BLOCK_WIDTH, (line) * BLOCK_HEIGHT)))
        if MAP[line][char] == "F":
            world_map.add(Finish(((char - 1) * BLOCK_WIDTH, (line) * BLOCK_HEIGHT)))

all_sprites = pygame.sprite.Group()
all_objects = pygame.sprite.Group()
player = Player()
all_sprites.add(world_map)
all_sprites.add(player)

for i in all_sprites:
    if type(i) != Player:
        all_objects.add(i)

main_surface = pygame.Surface((screen_w, screen_h))


class Game:
    def __init__(self):
        pass

    def __call__(self, keys, mouse_pos, mouse_k):
        screen.blit(main_surface, (0, 0))
        main_surface.fill(SKYBLUE)

        scene = "GAME"
        if keys[pygame.K_q] or player.get_screen_cords()[
            1] >= screen_h or player.touched_finish() or player.get_hp() <= 0:
            scene = "MENU"

        text = pygame.font.SysFont("Arial", 30).render(f"ОЧКИ ЗДОРОВЬЯ: {player.get_hp()}", True, WHITE)
        main_surface.blit(text, (100, 100))

        for i in all_sprites:
            new_objects = i.update(offset=player.get_camera_cords(), keys=keys, mouse_k=mouse_k,
                                   map_objects=all_sprites, player=player, finish=type(Finish((0, 0))))
            if new_objects is not None:
                for i in new_objects:
                    all_sprites.add(i)

        all_sprites.draw(main_surface)
        return scene
