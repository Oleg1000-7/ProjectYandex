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
        keys = [keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d]]

        if any((keys[0], keys[2])):
            if keys[0]:
                self.speed_y -= 0.5
            if keys[2]:
                self.speed_y += 0.5
        else:
            self.speed_y += 0.5 if self.speed_y < 0 else -0.5

        if any((keys[1], keys[3])):
            if keys[1]:
                self.speed_x -= 0.5
            if keys[3]:
                self.speed_x += 0.5
        else:
            self.speed_x += 0.5 if self.speed_x < 0 else -0.5

        if abs(self.speed_x) > max_speed:
            self.speed_x = max_speed if self.speed_x > 0 else -max_speed
        if abs(self.speed_y) > max_speed:
            self.speed_y = max_speed if self.speed_y > 0 else -max_speed

        move = [self.speed_x, self.speed_y]
        move[0] *= directions[0] if move[0] > 0 else directions[1]
        move[1] *= directions[2] if move[1] < 0 else directions[3]

        if (move[0] < 0 and screen_w / 10 * 4 > self.rect.centerx) or (move[0] > 0 and screen_w / 10 * 6 < self.rect.centerx):
            self.offset[0] += move[0]
        else:
            self.rect.x += move[0]

        if (move[1] < 0 and screen_h / 10 * 4 > self.rect.centery) or (move[1] > 0 and screen_h / 10 * 6 < self.rect.centery):
            self.offset[1] += move[1]
        else:
            self.rect.y += move[1]

        if directions[3]:
            self.rect.y += max_speed

    def get_screen_cords(self):
        return self.rect.x, self.rect.y

    def get_camera_cords(self):
        return tuple(map(round, self.offset))
