import pygame as pg
from pygame.math import Vector2
import math
from random import randint, randrange, choice


class Food(pg.sprite.Sprite):
    def __init__(self, filename):
        """Class Food constructor

        :return: New food dummy
        """
        super().__init__()
        pos = (randint(50, 9500), randint(50, 9500))
        self.image = pg.Surface((122, 70), pg.SRCALPHA)
        self.orig_image = pg.image.load(filename)
        self.size = self.orig_image.get_size()
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.rect = self.orig_image.get_rect()
        self.pos = Vector2(pos)
        self.pos_render = Vector2(-1000, -1000)
        self.offset = Vector2(0, 0)
        self.angle = randint(-180, 180) * math.pi / 180
        self.a = 30
        self.n = 3
        self.delta = 0
        self.rotate_speed = 6.11 / 1000
        self.speed = 0.1
        self.vx = randint(-10, 10) / 100
        self.vy = (0.0101 - self.vx ** 2) ** 0.5 * [-1, 1][randrange(2)]
        self.vx = self.speed * math.cos(self.angle)
        self.vy = self.speed * math.sin(self.angle)
        self.HP = 10
        self.max_HP = 10
        self.XP = 10
        self.m = 10
        self.has_not_health_bar = True
        self.tpx = []
        self.tpy = []

    def update(self):
        """Move, rotate and check hit box

        :return: Updates food parameters
        """
        self.move()
        self.angle += self.rotate_speed
        self.rotate()
        self.generate_hit_box()

    def rotate(self):
        """Rotate the image of the sprite around a pivot point

        :return: Sprite position
        """
        angle = self.angle * 180 / math.pi
        self.image = pg.transform.rotozoom(self.orig_image, -angle, 1)
        offset_rotated = self.offset.rotate(angle)
        self.rect = self.image.get_rect(center=self.pos_render + offset_rotated)

    def move(self):
        """Moves food according to its speed, slows down food, if its speed is more than speed of generation

        :return: Change food speed vector. Food have acceleration and force of viscous friction
        """
        speed = (self.vx ** 2 + self.vy ** 2) ** 0.5
        if speed > self.speed:
            self.vx -= self.vx * 0.01
            self.vy -= self.vy * 0.01
        self.pos.x += self.vx
        self.pos.y += self.vy 
        if self.pos.x >= 10000 or self.pos.x <= 0:
            self.vx *= -1
        if self.pos.y >= 10000 or self.pos.y <= 0:
            self.vy *= -1

    def death(self, arr_food, player):
        """Checks if food is dead

        :return: Delete sprite of food, if it was killed, remove food from array with food, generates new food,
        increase player's XP
        """
        if self.HP <= 0:
            self.kill()
            if self in arr_food:
                arr_food.remove(self)
                if player == 'bot':
                    pass
                else:
                    player.XP += self.XP
            generate_food(arr_food, 1)

    def generate_hit_box(self, r=0):
        """Generates x and y coordinates of tops of hit box

        :return: x and y coordinates of tops of hit box
        """
        angle = self.angle + self.delta
        x = self.pos.x
        y = self.pos.y
        n = self.n
        a = self.a + r
        for i in range(n):
            self.tpx[i] = x + a * math.cos(angle + i * 2 * math.pi / n) 
            self.tpy[i] = y + a * math.sin(angle + i * 2 * math.pi / n)
        return self.tpx, self.tpy


class Square(Food):
    def __init__(self):
        """Subclass Square constructor from Food

        :return: New Square
        """
        filename = 'Sprites/square.png'
        super().__init__(filename)
        self.HP = 10
        self.max_HP = 10
        self.BD = 8
        self.XP = 10
        self.r = 19
        self.a = 26
        self.n = 4
        self.delta = 13.96 / 1000
        self.tpx = [0, 0, 0, 0]
        self.tpy = [0, 0, 0, 0]
        self.rotate_speed = 6.11 / 1000
        self.m = 10


class Triangle(Food):
    def __init__(self):
        """Subclass Triangle constructor from Food

        :return: New Triangle
        """
        filename = 'Sprites/triangle.png'
        super().__init__(filename)
        self.HP = 30
        self.max_HP = 30
        self.BD = 8
        self.XP = 25
        self.r = 15
        self.a = 22
        self.n = 3
        self.delta = 8.72 / 1000
        self.tpx = [0, 0, 0]
        self.tpy = [0, 0, 0]
        self.rotate_speed = 6.11 / 1000
        self.m = 15


class Pentagon(Food):
    def __init__(self):
        """Subclass Pentagon constructor from Food

        :return: New Pentagon
        """
        filename = 'Sprites/pentagon.png'
        super().__init__(filename)
        self.HP = 100
        self.max_HP = 100
        self.BD = 12
        self.XP = 130
        self.r = 27
        self.a = 33
        self.n = 5
        self.delta = -5.59 / 1000
        self.tpx = [0, 0, 0, 0, 0]
        self.tpy = [0, 0, 0, 0, 0]
        self.rotate_speed = 2.62 / 1000
        self.m = 30


class AlphaPentagon(Food):
    def __init__(self):
        """Subclass AlphaPentagon constructor from Food

        :return: New AlphaPentagon
        """
        filename = 'Sprites/alpha_pentagon.png'
        super().__init__(filename)
        self.HP = 3000
        self.max_HP = 3000
        self.BD = 20
        self.XP = 1000
        self.r = 69
        self.a = 85
        self.n = 5
        self.delta = -5.59 / 1000
        self.tpx = [0, 0, 0, 0, 0]
        self.tpy = [0, 0, 0, 0, 0]
        self.rotate_speed = 1.74 / 1000
        self.m = 100


def generate_food(arr_food, n_max):
    """Generates food on the screen
    
    :return: Array with all food existing
    """
    variants = [0, 1, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0]
    for i in range(n_max):
        food = choice(variants)
        if food == 0:
            sq = Square()
            arr_food.append(sq)
        elif food == 1:
            tr = Triangle()
            arr_food.append(tr)
        else:
            pn = Pentagon()
            arr_food.append(pn)
    return arr_food


if __name__ == "__main__":
    print("This module is not for direct call!")
