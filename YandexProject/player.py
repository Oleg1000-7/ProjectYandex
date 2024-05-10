import pygame.sprite

from constants import *


def collided_rects(rec, other_rects):
    res = list()
    for i in map(lambda x: x.rect, other_rects):
        if i.colliderect(rec):
            res.append(i)
    return res


def blocked_sides(moving, other_rects):
    res = [True] * 4

    for o in other_rects:
        if not any(res):
            break

        if moving.y < o.centery < moving.bottomright[1]:
            if o.centerx > moving.centerx:
                res[0] = False
            else:
                res[1] = False

        if moving.x < o.centerx < moving.bottomright[0]:
            if o.centery < moving.centery:
                res[2] = False
            else:
                res[3] = False

    return tuple(res)


def correcting(moving, other):
    pass


class Player(pygame.sprite.Sprite):
    def __init__(self, offset=(0, 0)):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_w / 2, screen_h / 2)
        self.offset = list(offset)
        self.speed_x = 0
        self.speed_y = 0

    def update(self, keys, map_objects):
        max_speed = 5
        collided = collided_rects(self.rect, map_objects)
        directions = blocked_sides(self.rect, collided)

        if directions[3]:
            self.speed_y += 0.2

        if any((keys[pygame.K_w], keys[pygame.K_s])):
            if abs(self.speed_y) < max_speed:
                if keys[pygame.K_w] and directions[2]:
                    self.speed_y -= 0.5
                    #if screen_h / 5 < self.rect.centery and self.offset[1] < screen_h:
                    #    self.rect.y -= self.speed_y
                    #else:
                    #    self.offset[1] -= self.speed_y
                if keys[pygame.K_s] and directions[3]:
                    self.speed_y += 0.5
                    #if screen_h / 5 * 4 > self.rect.centery and self.offset[1] < screen_h:
                    #    self.rect.y += self.speed_y
                    #else:
                    #    self.offset[1] += self.speed_y
        else:
            self.speed_y = 0

        if any((keys[pygame.K_a], keys[pygame.K_d])):
            if abs(self.speed_x) < max_speed:
                if keys[pygame.K_a] and directions[1]:
                    self.speed_x -= 0.5
                    #if screen_w / 10 * 4 < self.rect.centerx:
                    #    self.rect.x -= self.speed_x
                    #elif self.offset[0] >= 0:
                    #    self.offset[0] -= self.speed_x
                    #elif self.rect.x > 0:
                    #    self.rect.x -= self.speed_x
                if keys[pygame.K_d] and directions[0]:
                    self.speed_x += 0.5
                    #if screen_w / 10 * 6 > self.rect.centerx:
                    #    self.rect.x += self.speed_x
                    #else:
                    #    self.offset[0] += self.speed_x
        else:
            self.speed_x = 0

        if self.speed_x > 0 and not directions[0]:
            self.speed_x = 0
        if self.speed_x < 0 and not directions[1]:
            self.speed_x = 0
        if self.speed_y > 0 and not directions[2]:
            self.speed_y = 0
        if self.speed_y > 0 and not directions[3]:
            self.speed_y = 0

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def get_screen_cords(self):
        return self.rect.x, self.rect.y

    def get_camera_cords(self):
        return tuple(self.offset)
