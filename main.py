import pygame as pg
from player import generate_player
from bots import generate_bot
from food import generate_food
from hit_functions import food_hit, bot_hit
from visuals import draw_bottom_interface, create_upgrade_bars, update_upgrade_bars, draw_health_bars_for_food, \
    draw_background, create_class_sprites, draw_choose_class_menu, draw_die_screen, choose_class_menu_launcher
from config import FPS, HEIGHT, WIDTH, LIGHT_GREY
import copy

# TODO Добавить ботов (для начала с простым интеллектом,
#  по типу рандомный спавн со случайным уровнем и прокачкой, едут за игроком и стреляют в него) (Вика)
# TODO Документация (Максим, Ваня)
# TODO Презентация (Максим, Вика, Ваня)
# TODO При наведении мыши показывать прокачку (Вика)
# TODO Отскок пуль от еды (Ваня)


# FIXME При смене класса сбрасывается прокачка, skill points остаются (Ваня)
# FIXME player.XP каждый раз обнуляется (778 строка в player)
# FIXME иногда у ботов пропадает взаимодействие с пулями
# FIXME сделать урон игроку при столкновении с ботами


def main():
    arr_food = []
    arr_food_to_render = []
    arr_bot_to_render = []
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    player = None
    player, player_sprites = generate_player('Player', player)
    arr_bot = generate_bot(player, 30)
    bullet_sprites = pg.sprite.Group()
    arr_food = generate_food(arr_food, 1000)
    arr_upgrade_bars = create_upgrade_bars(HEIGHT, player)
    start_point = copy.copy(player.pos)
    class_sprites_to_render = create_class_sprites()

    choose_class_menu_on = False
    choose_class_menu_on_flag = 0
    event_mouse = (0, 0)
    time_click_passed = 0
    mouse_up = 1
    bullets = []
    alive = True

    while alive:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.MOUSEMOTION:
                event_mouse = event
            elif event.type == pg.KEYDOWN:
                event_keydown = event
                player.upgrade_on_key(event_keydown)
            elif event.type == pg.MOUSEBUTTONDOWN:
                event_mousedown = event
                player.upgrade_on_mouse(event_mousedown)
                player, player_sprites, choose_class_menu_on = player.chose_class(event_mousedown, player,
                                                                                  player_sprites, choose_class_menu_on)
            mouse_up, time_click_passed = player.get_shoot_delay(event, time_click_passed, mouse_up)
        if mouse_up:
            time_click_passed += 1

        if pg.mouse.get_pressed()[0]:
            player.shoot(bullet_sprites, bullets)

        bot_sprites_to_render = player.render_bot(arr_bot, arr_bot_to_render)
        for bot in arr_bot:
            if abs(bot.pos.x - player.pos.x) < 700 and abs(bot.pos.y - player.pos.y) < 700:
                bot.update(player, arr_bot)
                bot.shoot(bullet_sprites, bullets, player)
                bot.hit_food(arr_food, arr_food_to_render)

        player.if_keys()
        if bullets:
            for bul in bullets:
                for food in arr_food_to_render:
                    bul.damage_food(food, bullets, arr_food, arr_food_to_render, player, bul)
            for bul in bullets:
                for bot in arr_bot:
                    bul.damage_player(player, bot, bullets, arr_bot)

        alive = player.death()
        player.hit_food(arr_food, arr_food_to_render)
        food_hit(arr_food_to_render)
        bot_hit(arr_bot, player)
        player_sprites.update(event_mouse)
        food_sprite_to_render = player.render_food(arr_food, arr_food_to_render)
        food_sprite_to_render.update()
        bullet_sprites.update(event_mouse, player)
        upgrade_bars_to_render = update_upgrade_bars(arr_upgrade_bars, player)
        screen.fill(LIGHT_GREY)
        choose_class_menu_on, choose_class_menu_on_flag = \
            choose_class_menu_launcher(choose_class_menu_on, choose_class_menu_on_flag, player)
        draw_background(WIDTH, HEIGHT, screen, start_point, player.pos)
        bot_sprites_to_render.draw(screen)
        bullet_sprites.draw(screen)
        player_sprites.draw(screen)
        food_sprite_to_render.draw(screen)
        draw_health_bars_for_food(screen, arr_food_to_render)
        draw_bottom_interface(player, WIDTH, HEIGHT, screen, 50000, upgrade_bars_to_render)
        draw_choose_class_menu(screen, class_sprites_to_render, choose_class_menu_on)
        pg.display.flip()
        clock.tick(FPS)

    while not alive:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if (event.key == pg.K_RETURN) or (event.key == pg.K_KP_ENTER):
                    alive = True
                    main()

        food_hit(arr_food_to_render)
        food_sprite_to_render = player.render_food(arr_food, arr_food_to_render)
        food_sprite_to_render.update()
        bullet_sprites.update(event_mouse, player)
        bot_sprites_to_render.update(player, arr_bot)
        screen.fill(LIGHT_GREY)

        draw_background(WIDTH, HEIGHT, screen, start_point, player.pos)
        bullet_sprites.draw(screen)
        bot_sprites_to_render.draw(screen)
        food_sprite_to_render.draw(screen)
        draw_health_bars_for_food(screen, arr_food_to_render)
        draw_die_screen(screen, player.XP, player.level)
        pg.display.flip()
        clock.tick(FPS)
        pg.display.update()
    pg.quit()


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
