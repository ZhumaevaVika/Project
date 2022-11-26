import pygame as pg

from Objects import Generator

# TODO Сделать столкновения объектов
# TODO Проработать level up

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
    arr_food = []
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    generator = Generator()
    player, player_sprites = generator.generate_player()
    all_sprites = pg.sprite.Group()
    all_sprites, arr_food = generator.generate_food(all_sprites, arr_food)

    event_mouse = (0, 0)
    time_click_passed = 0
    mouse_up = 1
    bullets = []
    bullets_arr = []

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.MOUSEMOTION:
                event_mouse = event
            mouse_up, time_click_passed = player.get_shoot_delay(event, time_click_passed, mouse_up)
        if mouse_up:
            time_click_passed += 1

        if pg.mouse.get_pressed()[0]:
            player.shoot(all_sprites, bullets)

        player.if_move()
        if bullets:
            for bul in bullets:
                for food in arr_food:
                    print(food.pos.x, food.pos.y, bul.pos.x, bul.pos.y)
                    bul.damage_food(food, bullets, arr_food)

        player_sprites.update(event_mouse)
        all_sprites.update(event_mouse)
        screen.fill(WHITE)
        all_sprites.draw(screen)
        player_sprites.draw(screen)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()