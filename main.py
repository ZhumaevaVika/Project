import pygame as pg
from main_logics import bot_actions, bullet_interaction, draw_game
from player import generate_player
from bots import generate_bot
from food import generate_food
from hit_functions import hit_interaction, food_hit
from visuals import draw_bottom_interface, create_upgrade_bars, update_upgrade_bars, create_class_sprites, \
    choose_class_menu_launcher, check_mouse_for_upgrade_bars
from config import FPS, HEIGHT, WIDTH, LIGHT_GREY
import copy


def main():
    arr_food = []
    arr_food_to_render = []
    arr_bot_to_render = []
    bullets = []
    bot_sprites_to_render = pg.sprite.Group()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    player, player_sprites = generate_player('Player', None)
    arr_bot = generate_bot(player, 30)
    bullet_sprites = pg.sprite.Group()
    arr_food = generate_food(arr_food, 1000)
    arr_upgrade_bars = create_upgrade_bars(HEIGHT, player)
    start_point = copy.copy(player.pos)
    class_sprites_to_render = create_class_sprites()

    upgrade_bars_flag = 0
    choose_class_menu_on = False
    choose_class_menu_on_flag = 0
    event_mouse = (0, 0)
    time_click_passed = 0
    mouse_up = 1
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
                event_mouse_down = event
                player.upgrade_on_mouse(event_mouse_down)
                player, player_sprites, choose_class_menu_on = player.choose_class(event_mouse_down, player,
                                                                                   player_sprites, choose_class_menu_on)
            mouse_up, time_click_passed = player.get_shoot_delay(event, time_click_passed, mouse_up)
        if mouse_up:
            time_click_passed += 1

        if pg.mouse.get_pressed()[0]:
            player.shoot(bullet_sprites, bullets, player)
        upgrade_bars_flag = check_mouse_for_upgrade_bars(event_mouse, upgrade_bars_flag, player, HEIGHT)

        alive = player.death(arr_bot, player)
        bot_sprites_to_render, arr_bot_to_render = player.render_bot(arr_bot, arr_bot_to_render)
        food_sprite_to_render = player.render_food(arr_food, arr_food_to_render)
        upgrade_bars_to_render = update_upgrade_bars(arr_upgrade_bars, player)
        choose_class_menu_on, choose_class_menu_on_flag = \
            choose_class_menu_launcher(choose_class_menu_on, choose_class_menu_on_flag, player)

        bot_actions(arr_bot, player, bullet_sprites, bullets, arr_food, arr_food_to_render)
        player.if_keys()
        bullet_interaction(bullets, arr_food_to_render, arr_food, player, arr_bot, arr_bot_to_render)
        hit_interaction(player, arr_food, arr_food_to_render, arr_bot)

        player_sprites.update(event_mouse, arr_bot)
        food_sprite_to_render.update()
        bullet_sprites.update(player)

        screen.fill(LIGHT_GREY)
        draw_game(WIDTH, HEIGHT, screen, start_point, player, bot_sprites_to_render, bullet_sprites, player_sprites,
                  food_sprite_to_render, arr_food_to_render, arr_bot_to_render, class_sprites_to_render,
                  choose_class_menu_on, alive)
        upgrade_bars_flag = draw_bottom_interface(player, WIDTH, HEIGHT, screen, 50000, upgrade_bars_to_render,
                                                  upgrade_bars_flag)
        pg.display.flip()
        clock.tick(FPS)

    while not alive:
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
        bullet_sprites.update(player)
        bot_sprites_to_render.update(player, arr_bot)

        screen.fill(LIGHT_GREY)
        draw_game(WIDTH, HEIGHT, screen, start_point, player, bot_sprites_to_render, bullet_sprites, player_sprites,
                  food_sprite_to_render, arr_food_to_render, arr_bot_to_render, class_sprites_to_render,
                  choose_class_menu_on, alive)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
