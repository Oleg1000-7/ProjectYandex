from collections import namedtuple

import pygame.sprite

from constants import *

Keys = namedtuple("Keys", ["W", "A", "S", "D", "CTRL"])


def collided_rects(rec, other_rects):
    res = list()
    for i in map(lambda x: x.rect, other_rects):
        if i.colliderect(rec):
            res.append(i)
    return res


def blocked_sides(moving, other_rects):
    res = [True] * 4
    res1 = []

    for o in other_rects:
        if not any(res):
            break

        if moving.y < o.y < moving.bottomleft[1] or moving.y < o.bottomleft[1] < moving.bottomleft[1]:
            if o.centerx > moving.centerx:
                res[0] = False
                res1.append((o, 0))
            else:
                res[1] = False
                res1.append((o, 1))

        if moving.x < o.x < moving.topright[0] or moving.x < o.topright[0] < moving.topright[0]:
            if o.centery < moving.centery:
                res[2] = False
                res1.append((o, 2))
            else:
                res[3] = False
                res1.append((o, 3))

    return tuple(res), tuple(res1)


def correcting(moving, collided):
    for o in collided:
        if o[1] == 0:
            moving.x = o[0].x - moving.width
        elif o[1] == 1:
            moving.x = o[0].topright[0]
        elif o[1] == 2:
            moving.y = o[0].bottomleft[1]
        else:
            moving.y = o[0].y - moving.height


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

        self.hp = 100

    def move(self, keys, map_objects):
        max_speed = 5
        collided = collided_rects(self.rect, map_objects)
        collided_sides = blocked_sides(self.rect, collided)
        directions = collided_sides[0]

        if keys.W or keys.S:
            if keys.W:
                self.speed_y -= 0.5
            if keys.S:
                self.speed_y += 0.5
        else:
            self.speed_y += 0.5 if self.speed_y < 0 else -0.5

        if keys.A or keys.D:
            if keys.A:
                self.speed_x -= 0.5
            if keys.D:
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

        if (move[0] < 0 and screen_w / 10 * 4 > self.rect.centerx) or (
                move[0] > 0 and screen_w / 10 * 6 < self.rect.centerx):
            self.offset[0] += move[0]
        else:
            self.rect.x += move[0]

        if (move[1] < 0 and screen_h / 10 * 4 > self.rect.centery) or (
                move[1] > 0 and screen_h / 10 * 6 < self.rect.centery):
            self.offset[1] += move[1]
        else:
            self.rect.y += move[1]

        # oif directions[3]:
        # o    self.rect.y += max_speed

        correcting(self.rect, collided_sides[1])

    def events(self, keys):
        if keys.CTRL:
            self.rect.height = 40
            self.image = pygame.Surface((40, 40))
            self.image.fill(GREEN)
        else:
            self.rect.height = 80
            self.image = pygame.Surface((40, 80))
            self.image.fill(GREEN)

    def update(self, keys, map_objects):
        keys = Keys(W=keys[pygame.K_w],
                    A=keys[pygame.K_a],
                    S=keys[pygame.K_s],
                    D=keys[pygame.K_d],
                    CTRL=keys[pygame.K_LCTRL])
        self.move(keys, map_objects)
        self.events(keys)

    def get_screen_cords(self):
        return self.rect.x, self.rect.y

    def get_camera_cords(self):
        return tuple(map(round, self.offset))
