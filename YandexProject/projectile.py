import object
from constants import *


class Projectile(object.Object):
    def __init__(self, cords, move_pattern, size=(BLOCK_WIDTH, BLOCK_HEIGHT), color=RED):
        super().__init__(cords)
        self.move_pattern = move_pattern
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.tick = pygame.time.get_ticks()

    def update(self, offset):
        self.rect.x = self.move_pattern(pygame.time.get_ticks() - self.tick)
        self.rect.x = self.x - offset[0]
        self.rect.y = self.y - offset[1]




