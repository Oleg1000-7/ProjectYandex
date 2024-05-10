import pygame.sprite

from constants import *


def collided_rects(rec, other_rects):
    res = list()
    for i in map(lambda x: x.rect, other_rects):
        if i.colliderect(rec):
            res.append(i)
    return res


class Player(pygame.sprite.Sprite):
    def __init__(self, offset=(0, 0)):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_w / 2, screen_h / 2)
        self.offset = list(offset)

    def update(self, keys, map_objects):
        speed = 5
        collided = collided_rects(self.rect, map_objects)

        if keys[pygame.K_w]:
            if screen_h / 5 < self.rect.centery and self.offset[1] < screen_h:
                self.rect.y -= speed
            else:
                self.offset[1] -= speed
        if keys[pygame.K_s]:
            if screen_h / 5 * 4 > self.rect.centery and self.offset[1] < screen_h:
                self.rect.y += speed
            else:
                self.offset[1] += speed
        if keys[pygame.K_a]:
            if screen_w / 10 * 4 < self.rect.centerx:
                self.rect.x -= speed
            elif self.offset[0] >= 0:
                self.offset[0] -= speed
            elif self.rect.x > 0:
                self.rect.x -= speed
        if keys[pygame.K_d]:
            if screen_w / 10 * 6 > self.rect.centerx:
                self.rect.x += speed
            else:
                self.offset[0] += speed

    def get_screen_cords(self):
        return self.rect.x, self.rect.y

    def get_camera_cords(self):
        return tuple(self.offset)
