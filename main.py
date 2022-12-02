import pygame as pg

from Objects import Generator

# TODO Сделать столкновения объектов, добавить танку хитбокс.
#  При контакте игрока с едой оба получают урон (body_damage/BD) (Ваня)
# TODO Сделать health bar, показатели уровня и счета в нижней части экрана (Максим)
# TODO Сделать возможность выбора класса танка (Вика)
# TODO Добавить ботов (для начала с простым интеллектом,
#  по типу рандомный спавн со случайным уровнем и прокачкой, едут за игроком и стреляют в него)

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
    player = None
    player, player_sprites = generator.generate_player('Player', player)
    # player_sprites.add(Player())
    all_sprites = pg.sprite.Group()
    all_sprites, arr_food = generator.generate_food(all_sprites, arr_food)

    event_mouse = (0, 0)
    time_click_passed = 0
    mouse_up = 1
    bullets = []

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.MOUSEMOTION:
                event_mouse = event
            elif event.type == pg.KEYDOWN:
                event_keydown = event
                player.upgrade(event_keydown)
                player, player_sprites = player.choose_class(event_keydown, player, player_sprites)
            mouse_up, time_click_passed = player.get_shoot_delay(event, time_click_passed, mouse_up)
        if mouse_up:
            time_click_passed += 1

        if pg.mouse.get_pressed()[0]:
            player.shoot(all_sprites, bullets)

        player.if_keys()
        if bullets:
            for bul in bullets:
                for food in arr_food:
                    bul.damage_food(food, bullets, arr_food, player)

        player_sprites.update(event_mouse)
        screen.fill(WHITE)
        all_sprites.update(event_mouse)
        all_sprites.draw(screen)
        player_sprites.draw(screen)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
