from collections import namedtuple

import pygame.sprite
from projectile import Projectile

from constants import *

Keys = namedtuple("Keys", ["W", "A", "S", "D", "CTRL", "SPACE", "LMB"])


def collided_rects(moving, other):
    res = list()
    rec = moving.rect
    for i in map(lambda x: x.rect, other):
        if i.colliderect(rec) and moving != other:
            res.append(i)

    return res


def blocked_sides(moving, other_rects):
    res = [True] * 4
    res1 = []

    for o in other_rects:
        if not any(res):
            break
        if abs(moving.centerx - o.centerx) > abs(moving.centery - o.centery):
            if moving.centerx < o.centerx:
                res[0] = False
                res1.append((o, 0))
            elif moving.centerx > o.centerx:
                res[1] = False
                res1.append((o, 1))
        else:
            if moving.centery > o.centery:
                res[2] = False
                res1.append((o, 2))
            elif moving.centery < o.centery:
                res[3] = False
                res1.append((o, 3))
    return tuple(res), tuple(res1)


def correcting(moving, collided):
    for o in collided:
        if o[1] == 0:
            moving.rect.x = o[0].x - moving.rect.width
            if moving.speed_x >= 0:
                moving.speed_x = 0
        elif o[1] == 1:
            moving.rect.x = o[0].topright[0]
            if moving.speed_x <= 0:
                moving.speed_x = 0
        elif o[1] == 2:
            moving.rect.y = o[0].bottomleft[1]
            if moving.speed_y < 0:
                moving.speed_y = 0
        elif o[1] == 3:
            moving.rect.y -= moving.rect.bottom - o[0].y - 1
            if moving.speed_y > 0:
                moving.speed_y = 0


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
        self.direction = True
        self.sides = [True] * 4
        self.fire_cooldown = 0
        self.finish = False

        self.hp = 100

    def move(self, keys, map_objects):
        collided = collided_rects(self, map_objects)
        collided_sides = blocked_sides(self.rect, collided)
        correcting(self, collided_sides[1])

        self.sides = collided_sides
        sides = collided_sides[0]
        max_speed = MAX_SPEED

        if keys.W or keys.S:
            if keys.W and not sides[3]:
                self.speed_y = -10
            if keys.S and self.speed_y < max_speed:
                self.speed_y += 0.5
        if sides[3] and self.speed_y < max_speed:
            self.speed_y += 0.5

        if keys.A or keys.D:
            if keys.A:
                self.direction = False
                if self.speed_x > -max_speed:
                    self.speed_x -= 0.5
            if keys.D:
                self.direction = True
                if self.speed_x < max_speed:
                    self.speed_x += 0.5
        elif self.speed_x:
            self.speed_x += 0.5 if self.speed_x < 0 else -0.5

        move = [self.speed_x, self.speed_y]
        move[0] *= sides[0] if move[0] > 0 else sides[1]
        move[1] *= sides[2] if move[1] < 0 else sides[3]

        if (move[0] < 0 and screen_w / 10 * 4 > self.rect.centerx) or (
                move[0] > 0 and screen_w / 10 * 6 < self.rect.centerx):
            if move[0] > 0 or (move[0] < 0 < self.offset[0]):
                self.offset[0] += move[0]
            elif self.offset[0] <= 0:
                self.rect.x += move[0]
        else:
            self.rect.x += move[0]

        if (move[1] < 0 and screen_h / 10 * 4 > self.rect.centery) or (
                move[1] > 0 and screen_h / 10 * 6 < self.rect.centery):
            if move[1] < 0 or (move[1] > 0 > self.offset[1]):
                self.offset[1] += move[1]
            elif self.offset[1] >= 0:
                self.rect.y += move[1]
        else:
            self.rect.y += move[1]

    def events(self, keys):
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        res = []
        if keys.CTRL:
            self.rect.height = 50
            self.image = pygame.Surface((40, 50))
            self.image.fill(GREEN)

        elif self.rect.height == 50:
            self.speed_y = -5
            self.rect.height = 80

        else:
            self.image = pygame.Surface((40, 80))
            self.image.fill(GREEN)

        if keys.SPACE and self.fire_cooldown <= 0:
            if self.direction:
                proj = Projectile((self.rect.midright[0], self.rect.midright[1] - 10), self.offset, self, move_pattern=lambda x: x)
            else:
                proj = Projectile((self.rect.midleft[0] - 50, self.rect.midleft[1] - 10), self.offset, self,
                                  move_pattern=lambda x: -x)
            self.fire_cooldown = 80
            res.append(proj)
        return res

    def damage(self):
        self.hp -= 20

    def update(self, **kwargs):
        map_objects = kwargs["map_objects"]
        mouse_k = kwargs["mouse_k"]
        keys = kwargs["keys"]
        finish = kwargs["finish"]

        if finish in map(type, pygame.sprite.spritecollide(self, map_objects, False)):
            self.finish = True

        p_keys = Keys(W=keys[pygame.K_w],
                      A=keys[pygame.K_a],
                      S=keys[pygame.K_s],
                      D=keys[pygame.K_d],
                      CTRL=keys[pygame.K_LCTRL],
                      SPACE=keys[pygame.K_SPACE],
                      LMB=mouse_k[0])
        self.move(p_keys, map_objects)
        obj_arr = self.events(p_keys)

        return obj_arr

    def get_direction(self):
        return self.direction

    def get_screen_cords(self):
        return self.rect.x, self.rect.y

    def get_camera_cords(self):
        return tuple(map(round, self.offset))

    def get_hp(self):
        return self.hp

    def touched_finish(self):
        return self.finish
