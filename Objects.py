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
        self.len_gun = 35
        self.speed = 3
        self.shoot_delay = 0
        self.reload = 50 # Чем меньше reload, тем быстрее стреляет

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
        self.shoot_delay += 1

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)

    def move(self, keys):
        x = 0
        y = 0
        if keys[pg.K_w]:
            y -= 1
        if keys[pg.K_a]:
            x -= 1
        if keys[pg.K_s]:
            y += 1
        if keys[pg.K_d]:
            x += 1
        if (x ** 2 + y ** 2) > 0:
            self.pos.x += self.speed * x / (x ** 2 + y ** 2) ** 0.5
            self.pos.y += self.speed * y / (x ** 2 + y ** 2) ** 0.5

    def shoot(self, all_sprites):
        try:
            if self.shoot_delay % self.reload == 0:
                bullet = Bullet(self)
                all_sprites.add(bullet)
                bullet.angle_update(pg.mouse.get_pos())
        except AttributeError:
            pass

    def get_shoot_delay(self, event, time_click_passed, mouse_up):
        if event.type == pg.MOUSEBUTTONUP:
            self.shoot_delay = 0
            mouse_up = 1

        elif event.type == pg.MOUSEBUTTONDOWN:
            if time_click_passed > self.reload:
                self.shoot_delay = 0
                time_click_passed = 0
                mouse_up = 0
        return mouse_up, time_click_passed


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
        pos = player.pos
        super().__init__()
        self.image = pg.Surface((122, 70), pg.SRCALPHA)
        # A reference to the original image to preserve the quality.
        self.orig_image = pg.image.load('Sprites/BulletM.png')
        self.size = self.orig_image.get_size()
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.20), int(self.size[1] * 0.20)))
        self.rect = self.orig_image.get_rect()
        self.pos = Vector2(pos)  # The original center position/pivot point.
        self.l = player.len_gun
        self.offset = Vector2(self.l*math.cos(player.angle*6.28/360), self.l*math.sin(player.angle*6.28/360))  # We shift the sprite 50 px to the right.
        self.angle = 0

        self.r = 20
        self.speed = 6

    def update(self, event):
        self.rotate()
        self.move()

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, 0.01, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(0.01)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)

    def angle_update(self, event):
        if event[0] != self.pos.x:
            self.angle = math.atan((event[1] - self.pos.y) / (event[0] - self.pos.x))
        elif event[0] == self.pos.x:
            self.angle = -80 * (event[1] - self.pos.y) / abs(event[1] - self.pos.y)
        self.angle = self.angle * 360 / 6.28
        if event[0] < self.pos.x:
            self.angle += 180

    def move(self):
        self.pos.x += self.speed * math.cos(self.angle*6.28/360)
        self.pos.y += self.speed * math.sin(self.angle*6.28/360)


class Generator:

    def generate_player(self):
        player = Player()
        player_sprites = pg.sprite.Group(player)
        return player, player_sprites

    def generate_food(self, all_sprites):
        N_max = 12
        variants = [0, 1, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0]
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


