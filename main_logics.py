from visuals import draw_background, draw_health_bars_for_food, draw_health_bars_for_bots, draw_choose_class_menu,\
    draw_die_screen


def bot_actions(arr_bot, player, bullet_sprites, bullets, arr_food, arr_food_to_render):
    """Process bot actions

    :return: Process bot actions
    """
    for bot in arr_bot:
        if abs(bot.pos.x - player.pos.x) < 700 and abs(bot.pos.y - player.pos.y) < 700:
            bot.update(player, arr_bot)
            bot.shoot(bullet_sprites, bullets, player)
            bot.hit_food(arr_food, arr_food_to_render)


def bullet_interaction(bullets, arr_food_to_render, arr_food, player, arr_bot, arr_bot_to_render):
    """Process bullet interaction

    :return: Process bullet interaction
    """
    if bullets:
        for bul in bullets:
            for food in arr_food_to_render:
                bul.damage_food(food, bullets, arr_food, arr_food_to_render, player, bul)
        for bul in bullets:
            for bot in arr_bot:
                bul.damage_player(player, bot, bullets, arr_bot, arr_bot_to_render)


def draw_game(width, height, screen, start_point, player, bot_sprites_to_render, bullet_sprites, player_sprites,
              food_sprite_to_render, arr_food_to_render, arr_bot_to_render, class_sprites_to_render,
              choose_class_menu_on, alive):
    """Draws game interface

    :return: Draws game interface
    """
    draw_background(width, height, screen, start_point, player.pos)
    bullet_sprites.draw(screen)
    bot_sprites_to_render.draw(screen)
    food_sprite_to_render.draw(screen)
    draw_health_bars_for_food(screen, arr_food_to_render)
    draw_health_bars_for_bots(screen, arr_bot_to_render)
    if alive:
        player_sprites.draw(screen)
        draw_choose_class_menu(screen, class_sprites_to_render, choose_class_menu_on)
    else:
        draw_die_screen(screen, player.XP, player.level)


if __name__ == "__main__":
    print("This module is not for direct call!")
