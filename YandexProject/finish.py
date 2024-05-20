from constants import *


class Finish(pygame.sprite.Sprite):
    def __init__(self, cords):
        super().__init__()
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = cords
        self.x, self.y = cords

    def damage(self):
        pass

    def update(self, **kwargs):
        offset = kwargs["offset"]
        self.rect.x = self.x - offset[0]
        self.rect.y = self.y - offset[1]
