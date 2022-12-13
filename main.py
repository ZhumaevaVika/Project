import pygame as pg
import pygame.math
from player import generate_player
from food import generate_food
from hit_functions import food_hit
from visuals import draw_bottom_interface, create_upgrade_bars, update_upgrade_bars, draw_health_bars_for_food, draw_background
from config import FPS, HEIGHT, WIDTH, LIGHT_GREY
import copy

# TODO Графический интерфейс (Максим)
# TODO Отрисовывать границы карты, потому что не понятно где она кончается (Максим)
# TODO Добавить ботов (для начала с простым интеллектом,
#  по типу рандомный спавн со случайным уровнем и прокачкой, едут за игроком и стреляют в него) (Вика)

# FIXME Танк слишком медленный, надо подобрать значения массы и скорости. При движении по диагонали скорость
#  маленькая (Ваня)
# FIXME Сделать, чтобы Twin по очереди стрелял из пушек (395 строка в Objects) (Ваня)
# FIXME При смене класса сбрасывается прокачка, skill points остаются (Вика)
# FIXME Если набрать много очков, при отрисовке зеленая линия выходит за границы (Максим)


def main():
    arr_food = []
    arr_food_to_render = []
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    player = None
    player, player_sprites = generate_player('Player', player)
    bullet_sprites = pg.sprite.Group()
    arr_food = generate_food(arr_food, 1000)
    arr_upgrade_bars = create_upgrade_bars(HEIGHT, player)
    start_point = copy.copy(player.pos)

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
                player.upgrade_on_key(event_keydown)
                player, player_sprites = player.chose_class(event_keydown, player, player_sprites)
            elif event.type == pg.MOUSEBUTTONDOWN:
                event_mousedown = event
                player.upgrade_on_mouse(event_mousedown)
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
        food_hit(arr_food_to_render)
        player_sprites.update(event_mouse)
        food_sprite_to_render = player.render_food(arr_food, arr_food_to_render)
        food_sprite_to_render.update()
        bullet_sprites.update(event_mouse, player)
        upgrade_bars_to_render = update_upgrade_bars(arr_upgrade_bars, player)
        screen.fill(LIGHT_GREY)

        draw_background(WIDTH, HEIGHT, screen, start_point, player.pos)
        bullet_sprites.draw(screen)
        player_sprites.draw(screen)
        food_sprite_to_render.draw(screen)
        if player.HP > 0:
            draw_bottom_interface(player, WIDTH, HEIGHT, screen, 5000, upgrade_bars_to_render)
        draw_health_bars_for_food(screen, arr_food_to_render)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
