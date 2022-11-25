import pygame as pg

from Objects import Generator, Bullet

# TODO Сделать карту, чтобы экран по ней перемещался, а игрок был в центре
# TODO Сделать игроку возможность стрелять
# TODO Заспавнить на карте еду

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

def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    generator = Generator()
    player, all_sprites = generator.generate_player()
    all_sprites = generator.generate_food(all_sprites)

    event_mouse = (0, 0)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.MOUSEMOTION:
                event_mouse = event
            elif event.type == pg.MOUSEBUTTONDOWN:
                bullet = Bullet(player)
                all_sprites.add(bullet)
                print(all_sprites)

        player.if_move()

        all_sprites.update(event_mouse)
        screen.fill(WHITE)
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()