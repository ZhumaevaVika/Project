import pygame as pg
from pygame.math import Vector2
import math
from random import randint, randrange, choice

class Player(pg.sprite.Sprite):
    def if_move(self):
        keys = pg.key.get_pressed()
        if keys:
            self.move(keys)

    def __init__(self):
        pos = (500, 375)
        super().__init__()
        self.image = pg.Surface((122, 70), pg.SRCALPHA)
        # A reference to the original image to preserve the quality.
        self.orig_image = pg.image.load('Sprites/Tank.png')
        self.size = self.orig_image.get_size()
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.rect = self.orig_image.get_rect()
        self.pos = Vector2(pos)  # The original center position/pivot point.
        self.offset = Vector2(9, 1)  # We shift the sprite 50 px to the right.
        self.angle = 0

        self.r = 20
        self.speed = 3

    def update(self, event):
        if event == (0, 0):
            self.angle = 0
            self.rotate()
        else:
            if event.pos[0] != self.pos.x:
                self.angle = math.atan((event.pos[1] - self.pos.y) / (event.pos[0] - self.pos.x))
            elif event.pos[0] == self.pos.x:
                self.angle = -80 * (event.pos[1] - self.pos.y) / abs(event.pos[1] - self.pos.y)
            self.angle = self.angle * 360 / 6.28
            if event.pos[0] < self.pos.x:
                self.angle += 180
            self.rotate()

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)

    def move(self, keys):
        if keys[pg.K_w]:
            self.pos.y -= self.speed
        if keys[pg.K_a]:
            self.pos.x -= self.speed
        if keys[pg.K_s]:
            self.pos.y += self.speed
        if keys[pg.K_d]:
            self.pos.x += self.speed
        # FIXME При движении по диагонали скорость увеличивается в 2 раза, надо чтобы она оставалась постоянной


class Food(pg.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        pos = (randint(50, 950), randint(50, 700))
        self.image = pg.Surface((122, 70), pg.SRCALPHA)
        # A reference to the original image to preserve the quality.
        self.orig_image = pg.image.load(filename)
        self.size = self.orig_image.get_size()
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.rect = self.orig_image.get_rect()
        self.pos = Vector2(pos)  # The original center position/pivot point.
        self.offset = Vector2(0, 0)  # We shift the sprite 50 px to the right.
        self.angle = randint(-180, 180)

        self.vx = randint(-10, 10) / 100
        self.vy = (0.0101 - self.vx ** 2) ** 0.5 * [-1, 1][randrange(2)]

    def update(self, event):
        self.angle += 0.35
        self.rotate()
        self.move()

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)

    def move(self):
        self.pos.x += self.vx
        self.pos.y += self.vy


class Square(Food):
    def __init__(self):
        filename = 'Sprites/Square.png'
        super().__init__(filename)


class Triangle(Food):
    def __init__(self):
        filename = 'Sprites/Triangle.png'
        super().__init__(filename)


class Pentagon(Food):
    def __init__(self):
        filename = 'Sprites/Pentagon.png'
        super().__init__(filename)

    def update(self, event):
        self.angle += 0.15
        self.rotate()
        self.move()


class Bullet(pg.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pg.Surface((122, 70), pg.SRCALPHA)
        # A reference to the original image to preserve the quality.
        self.orig_image = pg.image.load('Sprites/AlphaPentagon.png')
        self.size = self.orig_image.get_size()
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.rect = self.orig_image.get_rect()
        x, y = player.pos
        self.x = x
        self.y = y

        self.vx = 1
        self.vy = 1

    def update(self, event):
        self.move()

    def move(self):
        self.x += self.vx
        self.y += self.vy


class Generator:
    def generate_player(self):
        player = Player()
        all_sprites = pg.sprite.Group(player)
        return player, all_sprites

    def generate_food(self, all_sprites):
        N_max = 12
        N_prop = 1
        variants = [0, 1, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0] * N_prop
        for i in range(N_max):
            food = choice(variants)
            if food == 0:
                sq = Square()
                all_sprites.add(sq)
            elif food == 1:
                tr = Triangle()
                all_sprites.add(tr)
            else:
                pn = Pentagon()
                all_sprites.add(pn)
        return all_sprites
