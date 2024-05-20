from constants import *
from projectile import Projectile


def collided_rects(moving, other, ex):
    res = list()
    rec = moving.rect
    for i in map(lambda x: x.rect, other):
        if i.colliderect(rec) and type(moving) != type(i) and i != ex:
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, cords):
        super().__init__()
        self.image = pygame.Surface((50, 100))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.center = cords
        self.x, self.y = cords
        self.direction = False
        self.speed_x, self.speed_y = 0, 0
        self.fire_cooldown = 0

    def damage(self):
        self.kill()

    def update(self, **kwargs):
        offset = kwargs["offset"]
        self.rect.x = self.x - offset[0]
        self.rect.y = self.y - offset[1]
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
        return self.move(kwargs["player"], kwargs["map_objects"])

    def shoot(self, player):
        if self.fire_cooldown <= 0:
            if self.direction:
                proj = Projectile(self.rect.midright, player.get_camera_cords(), self, move_pattern=lambda c: c)
            else:
                proj = Projectile((self.rect.midleft[0] - 50, self.rect.midleft[1]), player.get_camera_cords(),
                                  self, move_pattern=lambda c: -c)
            self.fire_cooldown = 100
            return proj
        return []

    def move(self, player, map_objects):
        collided = collided_rects(self, map_objects, player)
        collided_sides = blocked_sides(self.rect, collided)
        correcting(self, collided_sides[1])
        self.sides = collided_sides
        sides = collided_sides[0]

        res = []
        x, y = player.rect.center
        r = ((x - self.rect.centerx) ** 2 + (y - self.rect.centery) ** 2) ** 0.5

        self.direction = 0 if x < self.rect.x else 1

        if screen_w // 5 < r < screen_w // 3:
            if x < self.rect.x and sides[1]:
                self.speed_x -= 0.5
            elif x > self.rect.x and sides[0]:
                self.speed_x += 0.5
            else:
                self.speed_x = 0

            if not sides[0] or not sides[1]:
                self.speed_y = -7

        else:
            self.speed_x = 0

        if r < screen_w // 5:
            res.append(self.shoot(player))

        if sides[3] and self.speed_y < MAX_SPEED:
            self.speed_y += 0.5

        move = [self.speed_x, self.speed_y]
        move[0] *= sides[0] if move[0] > 0 else sides[1]
        move[1] *= sides[2] if move[1] < 0 else sides[3]
        self.x += move[0] if abs(move[0]) < MAX_SPEED / 2 else (MAX_SPEED / 2 if move[0] > 0 else -MAX_SPEED / 2)
        self.y += move[1]



        return res
