# Не делала солнечную систему, поэтому пока хз как импортировать классы из других файлов

import pygame
from pygame.draw import line, circle, rect

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

class Player:
    global keys

    def __init__(self):
        self.x = 500
        self.y = 375
        self.r = 20
        self.speed = 3

    def move(self):
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        #FIXME При движении по диагонали скорость увеличивается в 2 раза, надо чтобы она оставалась постоянной


    def draw(self):
        circle(screen, BLUE, (self.x, self.y), self.r)
        #FIXME Надо отрисовывать спрайт


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False

player = Player()

while not finished:
    screen.fill(WHITE)
    player.draw()
    pygame.display.update()

    clock.tick(FPS)

    keys = pygame.key.get_pressed()  # checking pressed keys
    if keys:
        player.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True


pygame.quit()