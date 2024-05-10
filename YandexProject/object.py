from constants import *


class Object(pygame.sprite.Sprite):
    def __init__(self, cords):
        super().__init__()
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = cords
        self.x, self.y = cords

    def update(self, offset):
        self.rect.x = self.x - offset[0]
        self.rect.y = self.y - offset[1]
