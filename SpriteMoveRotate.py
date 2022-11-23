import pygame as pg
from pygame.math import Vector2
import math

#TODO Сделать карту, чтобы экран по ней перемещался, а игрок был в центре
#TODO Сделать игроку возможность стрелять
#TODO Заспавнить на карте еду

FPS = 60
WIDTH = 1000
HEIGHT = 750

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Player(pg.sprite.Sprite):
    global keys

    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((122, 70), pg.SRCALPHA)
        # A reference to the original image to preserve the quality.
        self.orig_image = pg.image.load('Sprites/Tank.png')
        self.size = self.orig_image.get_size()
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.3), int(self.size[1] * 0.3)))
        self.rect = self.orig_image.get_rect()
        self.pos = Vector2(pos)  # The original center position/pivot point.
        self.offset = Vector2(8, 2)  # We shift the sprite 50 px to the right.
        self.angle = 0

        self.rect.x = 500
        self.rect.y = 375
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
                self.angle = -80*(event.pos[1] - self.pos.y)/abs(event.pos[1] - self.pos.y)
            self.angle = self.angle*360/6.28
            if event.pos[0]<self.pos.x:
                self.angle += 180
            self.rotate()

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos+offset_rotated)


    def move(self):
        if keys[pg.K_w]:
            self.pos.y -= self.speed
        if keys[pg.K_a]:
            self.pos.x -= self.speed
        if keys[pg.K_s]:
            self.pos.y += self.speed
        if keys[pg.K_d]:
            self.pos.x += self.speed
        # FIXME При движении по диагонали скорость увеличивается в 2 раза, надо чтобы она оставалась постоянной


def main():
    global keys
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    player = Player((500, 375))
    all_sprites = pg.sprite.Group(player)
    event_mouse = (0, 0)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.MOUSEMOTION:
                event_mouse = event

        keys = pg.key.get_pressed()
        if keys:
            player.move()

        all_sprites.update(event_mouse)
        screen.fill(WHITE)
        all_sprites.draw(screen)
        pg.draw.circle(screen, (255, 128, 0), [int(i) for i in player.pos], 3)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()