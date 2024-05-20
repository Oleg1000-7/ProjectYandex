from constants import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, cords, camera, parent, size=(30, 10), color=RED,
                 move_pattern=lambda x: x):
        super().__init__()
        self.move_pattern = move_pattern
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cords
        self.x, self.y = cords
        self.x += camera[0]
        self.y += camera[1]
        self.tick = pygame.time.get_ticks()
        self.parent = parent

    def damage(self):
        pass

    def update(self, **kwargs):
        offset = kwargs["offset"]
        map_objects = kwargs["map_objects"]

        self.rect.x = self.x - offset[0] + self.move_pattern(pygame.time.get_ticks() - self.tick)
        self.rect.y = self.y - offset[1]

        for i in pygame.sprite.spritecollide(self, map_objects, False):
            if i not in (self.parent, self):
                i.damage()
                self.kill()
