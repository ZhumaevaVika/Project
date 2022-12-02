import pygame as pg

from Objects import Generator
from Visuals import draw_bottom_interface  # подключил функцию из нового файлика (коммит с health bar)

# TODO Сделать столкновения объектов (Ваня)
# TODO Добавить регенерацию (Вика)
# TODO Графический интерфейс (Максим)
# TODO Добавить ботов (для начала с простым интеллектом,
#  по типу рандомный спавн со случайным уровнем и прокачкой, едут за игроком и стреляют в него)

# FIXME Танк слишком медленный, надо подобрать значения массы и скорости. При движении по диагонали скорость
#  маленькая (Ваня)
# FIXME Сделать, чтобы Twin по очереди стрелял из пушек (395 строка в Objects) (Ваня)
# FIXME Если зажать левую кнопку мыши и нажимать правую, ломается перезарядка (Вика)
# FIXME При смене класса сбрасывается прокачка, skill points остаются (Вика)
# FIXME Если набрать много очков, при отрисовке зеленая линия выходит за границы (Максим)

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
    arr_food_to_render = []
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    generator = Generator()
    player = None
    player, player_sprites = generator.generate_player('Player', player)
    # player_sprites.add(Player())
    bullet_sprites = pg.sprite.Group()
    arr_food = generator.generate_food(arr_food)

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
                player, player_sprites = player.chose_class(event_keydown, player, player_sprites)
            mouse_up, time_click_passed = player.get_shoot_delay(event, time_click_passed, mouse_up)
        if mouse_up:
            time_click_passed += 1

        if pg.mouse.get_pressed()[0]:
            player.shoot(bullet_sprites, bullets)

        player.if_keys()
        if bullets:
            for bul in bullets:
                for food in arr_food_to_render:
                    bul.damage_food(food, bullets, arr_food, arr_food_to_render, player)

        player.hit_food(arr_food, arr_food_to_render)
        player_sprites.update(event_mouse)
        food_sprite_to_render = player.render_food(arr_food, arr_food_to_render)
        food_sprite_to_render.update(event_mouse)
        bullet_sprites.update(event_mouse, player)
        screen.fill(WHITE)

        bullet_sprites.draw(screen)
        player_sprites.draw(screen)
        food_sprite_to_render.draw(screen)
        draw_bottom_interface(player, WIDTH, HEIGHT, screen, 5000)  # вот что добавлено (коммит с health bar)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
