import pygame
from config import GREY, WHITE, RED, GREEN, ORANGE, PURPLE, DARK_PURPLE, YELLOW, BLUE, ANOTHER_GREEN, CYAN, ANOTHER_GREY
from pygame.math import Vector2


class IgnoreButton(pygame.sprite.Sprite):
    def __init__(self, pos):
        """Creates ignore button

        :return: Button sprite
        """
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((70, 70), pygame.SRCALPHA)

        draw_bar_with_text(self.image, Vector2(30, 10), 30, 15, ANOTHER_GREY, 1, 1, 'Ignore')

        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


class PlayerClassSprite(pygame.sprite.Sprite):
    def __init__(self, class_type, pos):
        """Creates player class sprites

        :return: Player class sprites
        """
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((75, 75))
        self.image.set_colorkey((0, 0, 0))
        if class_type == 'Twin':
            self.orig_image = pygame.image.load('Sprites/twin_upgrade.png').convert()
        elif class_type == 'Sniper':
            self.orig_image = pygame.image.load('Sprites/sniper_upgrade.png').convert()
        elif class_type == 'MachineGun':
            self.orig_image = pygame.image.load('Sprites/machine_gun_upgrade.png').convert()
        else:
            self.orig_image = pygame.image.load('Sprites/flank_guard_upgrade.png').convert()
        self.image.blit(self.orig_image, (0, 0), (0, 0, 75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


class UpgradeBar(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, color, value, max_value, text, number_button):
        """Creates upgrade bar sprite

        :return: Upgrade bar sprite
        """
        super().__init__()
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color
        self.value = value
        self.max_value = max_value
        self.text = text
        self.number_button = number_button

        self.image = pygame.Surface((self.width + 20, self.height + 5), pygame.SRCALPHA)

        draw_upgrade_bar(self.image, Vector2(self.width // 2 + 10, self.height // 2), self.width, self.height,
                         self.color, self.value, self.max_value, self.text, self.number_button)

        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def update(self, new_value):
        """Updates value of upgrade bar

        :return: Draw value of upgrade bar
        """
        if self.value != new_value:
            self.value = new_value
            self.image = pygame.Surface((self.width + 20, self.height + 5), pygame.SRCALPHA)

            draw_upgrade_bar(self.image, Vector2(self.width // 2 + 10, self.height // 2), self.width, self.height,
                             self.color, self.value, self.max_value, self.text, self.number_button)

            self.rect = self.image.get_rect()
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y


def draw_text(screen, pos, size, text, font='freesansbold.ttf'):
    """Draws text on screen

    :return: Draws text on screen
    """
    font = pygame.font.Font(font, size)
    text_main = font.render(text, True, WHITE)
    text_add = font.render(text, True, GREY)
    # text render
    text_main_rect = text_main.get_rect()
    text_add_rect = text_add.get_rect()
    # White borders of text
    text_main_rect.center = (pos.x, pos.y)
    text_add_rect.center = (pos.x, pos.y - 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (pos.x, pos.y + 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (pos.x - 1, pos.y)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (pos.x + 1, pos.y)
    screen.blit(text_add, text_add_rect)
    # Main gray text
    screen.blit(text_main, text_main_rect)


def draw_bar(screen, pos, width, height, color, value, max_value):
    """Draws bar

    :return: Draws bar
    """
    value_to_px = int((value / max_value) * width)
    # Gray borders of health bar line
    pygame.draw.line(screen, GREY, (pos.x - width // 2, pos.y),
                     (pos.x + width // 2, pos.y), height)
    pygame.draw.circle(screen, GREY, (pos.x - width // 2, pos.y + 1), height // 2)
    pygame.draw.circle(screen, GREY, (pos.x + width // 2, pos.y + 1), height // 2)
    # Health bar line
    pygame.draw.line(screen, color, (pos.x - width // 2, pos.y),
                     (pos.x - width // 2 + value_to_px, pos.y), height - 2)
    pygame.draw.circle(screen, color, (pos.x - width // 2, pos.y + 1), (height - 2) // 2)
    pygame.draw.circle(screen, color, (pos.x - width // 2 + value_to_px, pos.y + 1), (height - 2) // 2)


def draw_bar_with_text(screen, pos, width, height, color, value, max_value, text):
    """Draws bar with text

    :return: Draws bar with text
    """
    value_to_px = int((value / max_value) * width)
    font = pygame.font.Font('freesansbold.ttf', height - 2)
    text_main = font.render(text, True, WHITE)
    text_add = font.render(text, True, GREY)
    # Gray borders of health bar line
    pygame.draw.line(screen, GREY, (pos.x - width // 2, pos.y),
                     (pos.x + width // 2, pos.y), height)
    pygame.draw.circle(screen, GREY, (pos.x - width // 2, pos.y + 1), height // 2)
    pygame.draw.circle(screen, GREY, (pos.x + width // 2, pos.y + 1), height // 2)
    # Health bar line
    pygame.draw.line(screen, color, (pos.x - width // 2, pos.y),
                     (pos.x - width // 2 + value_to_px, pos.y), height - 2)
    pygame.draw.circle(screen, color, (pos.x - width // 2, pos.y + 1), (height - 2) // 2)
    pygame.draw.circle(screen, color, (pos.x - width // 2 + value_to_px, pos.y + 1), (height - 2) // 2)
    # text render
    text_main_rect = text_main.get_rect()
    text_add_rect = text_add.get_rect()
    # White borders of text
    text_main_rect.center = (pos.x, pos.y + 1)
    text_add_rect.center = (pos.x, pos.y + 1 - 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (pos.x, pos.y + 1 + 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (pos.x - 1, pos.y + 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (pos.x + 1, pos.y + 1)
    screen.blit(text_add, text_add_rect)
    # Main gray text
    screen.blit(text_main, text_main_rect)


def draw_upgrade_bar(screen, pos, width, height, color, value, max_value, text, number_button):
    """Draws upgrade bar

    :return: Draws upgrade bar
    """
    value_to_px = int((value / max_value) * (5 * width // 6))
    font = pygame.font.Font('freesansbold.ttf', height - 2)
    text_main = font.render(text, True, WHITE)
    text_add = font.render(text, True, GREY)
    # Gray borders of health bar line
    pygame.draw.line(screen, GREY, (pos.x - width // 2, pos.y),
                     (pos.x + width // 2, pos.y), height)
    pygame.draw.circle(screen, GREY, (pos.x - width // 2, pos.y + 1), height // 2)
    pygame.draw.circle(screen, GREY, (pos.x + width // 2, pos.y + 1), height // 2)
    # Health bar line
    pygame.draw.line(screen, color, (pos.x - width // 2 + 5 * width // 6, pos.y),
                     (pos.x + width // 2, pos.y), height - 2)
    # pygame.draw.circle(screen, color, (pos.x - width // 2, pos.y + 1), (height - 2) // 2)
    pygame.draw.circle(screen, color, (pos.x + width // 2, pos.y + 1), (height - 2) // 2)
    if value != 0:
        pygame.draw.line(screen, color, (pos.x - width // 2, pos.y),
                         (pos.x - width // 2 + value_to_px, pos.y), height - 2)
        pygame.draw.circle(screen, color, (pos.x - width // 2, pos.y + 1), (height - 2) // 2)
    # pygame.draw.circle(screen, color, (pos.x - width // 2 + value_to_px, pos.y + 1), (height - 2) // 2)
    for i in range(max_value):
        pygame.draw.line(screen, GREY, (pos.x - width // 2 + (i + 1) * (5 * width // 6) // 7 - 1, pos.y),
                         (pos.x - width // 2 + (i + 1) * (5 * width // 6) // 7, pos.y), height - 2)

    # text render
    text_main_rect = text_main.get_rect()
    text_add_rect = text_add.get_rect()
    # White borders of text
    text_main_rect.center = (pos.x - width // 10, pos.y + 1)
    text_add_rect.center = (pos.x - width // 10, pos.y + 1 - 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (pos.x - width // 10, pos.y + 1 + 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (pos.x - 1 - width // 10, pos.y + 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (pos.x + 1 - width // 10, pos.y + 1)
    screen.blit(text_add, text_add_rect)
    # Main gray text
    screen.blit(text_main, text_main_rect)
    draw_text(screen, Vector2(pos.x + width // 4 + 5, pos.y), 6, '[' + str(number_button) + ']')
    pygame.draw.rect(screen, GREY, pygame.Rect(pos.x + width // 2 - 14, pos.y - 1, 9, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(pos.x + width // 2 - 14 + 3, pos.y - 1 - 3, 3, 9))


def create_upgrade_bars(height, player):
    """Creates upgrade bars

    :return: health_regen, max_health, body_damage, bullet_speed, bullet_penetration, bullet_damage, reload,
            movement_speed
    """
    health_regen = UpgradeBar(Vector2(10, height - 150), 140, 12, ORANGE, player.regen_points, 7, "Health Regen", 1)
    max_health = UpgradeBar(Vector2(10, height - 135), 140, 12, PURPLE, player.max_HP_points, 7, "Max Health", 2)
    body_damage = UpgradeBar(Vector2(10, height - 120), 140, 12, DARK_PURPLE, player.BD_points, 7, "Body Damage", 3)
    bullet_speed = UpgradeBar(Vector2(10, height - 105), 140, 12, BLUE, player.bullet_speed_points, 7,
                              "Bullet Speed", 4)
    bullet_penetration = UpgradeBar(Vector2(10, height - 90), 140, 12, YELLOW, player.bullet_penetration_points, 7,
                                    "Bullet Penetration", 5)
    bullet_damage = UpgradeBar(Vector2(10, height - 75), 140, 12, RED, player.bullet_damage_points, 7, "Bullet Damage",
                               6)
    reload = UpgradeBar(Vector2(10, height - 60), 140, 12, ANOTHER_GREEN, player.reload_points, 7, "Reload", 7)
    movement_speed = UpgradeBar(Vector2(10, height - 45), 140, 12, CYAN, player.speed_points, 7, "Movement Speed", 8)
    return [health_regen, max_health, body_damage, bullet_speed, bullet_penetration, bullet_damage, reload,
            movement_speed]


def update_upgrade_bars(upgrade_bar_list, player):
    """Updates upgrade bars

    :return: bars_to_render
    """
    upgrade_bar_list[0].update(player.regen_points)
    upgrade_bar_list[1].update(player.max_HP_points)
    upgrade_bar_list[2].update(player.BD_points)
    upgrade_bar_list[3].update(player.bullet_speed_points)
    upgrade_bar_list[4].update(player.bullet_penetration_points)
    upgrade_bar_list[5].update(player.bullet_damage_points)
    upgrade_bar_list[6].update(player.reload_points)
    upgrade_bar_list[7].update(player.speed_points)
    bars_to_render = pygame.sprite.Group(*upgrade_bar_list)
    return bars_to_render


def check_mouse_for_upgrade_bars(event, upgrade_bars_flag, player, height):
    """Changes upgrade_bars_flag when mouse is located in left-bottom part of the screen

    :return: upgrade_bars_flag
    """
    if event == (0, 0):
        pass
    else:
        if (upgrade_bars_flag == 0) and (0 <= event.pos[0] <= 170) and (height - 200 <= event.pos[1] <= height) and \
                (player.skill_points == 0):
            upgrade_bars_flag = 50
    return upgrade_bars_flag


def draw_bottom_interface(player, width, height, screen, top_score, bars_to_render, upgrade_bars_flag):
    """Draws player's nickname, score bar, level bar, upgrade bars, health bar

    :return: upgrade_bars_flag
    """
    # yellow level bar
    score_func = 0.3562 * player.level ** 3 - 5.8423 * player.level ** 2 + 67.4898 * player.level - 60
    if player.level != 1:
        score_func_1 = 0.3562 * (player.level - 1) ** 3 - 5.8423 * (player.level - 1) ** 2 + 67.4898 * \
                       (player.level - 1) - 60
        if player.level != 45:
            draw_bar_with_text(screen, Vector2(width // 2, height - 30), 200, 12, YELLOW, player.XP - score_func_1,
                               score_func - score_func_1, 'Lvl ' + str(player.level) + ' ' + player.class_type)
        else:
            draw_bar_with_text(screen, Vector2(width // 2, height - 30), 200, 12, YELLOW, 1,
                               1, 'Lvl ' + str(player.level) + ' ' + player.class_type)
    else:
        draw_bar_with_text(screen, Vector2(width // 2, height - 30), 200, 12, YELLOW, player.XP,
                           score_func, 'Lvl ' + str(player.level) + ' ' + player.class_type)
    # green score bar
    if player.XP <= top_score:
        draw_bar_with_text(screen, Vector2(width // 2, height - 45), 150, 12, GREEN, player.XP, top_score,
                           "Score: " + str(player.XP))
    else:
        draw_bar_with_text(screen, Vector2(width // 2, height - 45), 150, 12, GREEN, 1, 1,
                           "Score: " + str(player.XP))
    # Name
    draw_text(screen, Vector2(width // 2, height - 60), 20, "Name")  # FIXME поменять имя игрока
    # upgrade bars
    if (player.skill_points > 0) or (upgrade_bars_flag > 0):
        bars_to_render.draw(screen)
        if player.skill_points > 0:
            draw_text(screen, Vector2(180, height - 160), 20, 'x' + str(player.skill_points))
        if upgrade_bars_flag > 0:
            upgrade_bars_flag = upgrade_bars_flag - 1
    # player health bar
    if player.HP < player.max_HP:
        if player.HP >= 0:
            draw_bar(screen, Vector2(width // 2, height // 2 + 30), 50, 8, ANOTHER_GREEN, player.HP, player.max_HP)
        else:
            draw_bar(screen, Vector2(width // 2, height // 2 + 30), 50, 8, ANOTHER_GREEN, 0, player.max_HP)
    return upgrade_bars_flag


def draw_health_bars_for_bots(screen, arr_bot_to_render):
    """Draws health bars for bots

    :return: Draws health bars for bots
    """
    for bot in arr_bot_to_render:
        if (bot.HP < bot.max_HP) and (bot.HP > 0):
            draw_bar(screen, Vector2(bot.pos_render.x, bot.pos_render.y + 40), 50, 8, ANOTHER_GREEN, bot.HP,
                     bot.max_HP)


def draw_health_bars_for_food(screen, arr_food_to_render):
    """Draws health bars for food

    :return: Draws health bars for food
    """
    for food in arr_food_to_render:
        if (food.HP >= 0) and (food.HP < food.max_HP):
            draw_bar(screen, Vector2(food.pos_render.x, food.pos_render.y + 40), 50, 8, ANOTHER_GREEN, food.HP,
                     food.max_HP)


def draw_background(width, height, screen, start_point, pos):
    """Draws background

    :return: Draws background
    """
    shift_x = - (pos.x - start_point.x) % 25
    shift_y = - (pos.y - start_point.y) % 25
    for i in range(40):
        pygame.draw.line(screen, ANOTHER_GREY, (i * (width // 40) + shift_x, 0), (i * (width // 40) + shift_x, height),
                         2)
    for i in range(30):
        pygame.draw.line(screen, ANOTHER_GREY, (0, i * (height // 30) + shift_y), (width, i * (height // 30) + shift_y),
                         2)

    if 10000 - pos.x <= width // 2:
        pygame.draw.rect(screen, GREY, pygame.Rect(width // 2 + 10000 - pos.x, 0, width // 2 - 10000 + pos.x, height))
    elif pos.x <= width // 2:
        pygame.draw.rect(screen, GREY, pygame.Rect(0, 0, width // 2 - pos.x, height))
    if 10000 - pos.y <= height // 2:
        pygame.draw.rect(screen, GREY, pygame.Rect(0, height // 2 + 10000 - pos.y, width, height // 2 - 10000 + pos.y))
    elif pos.y <= height // 2:
        pygame.draw.rect(screen, GREY, pygame.Rect(0, 0, width, height // 2 - pos.y))


def draw_die_screen(screen, score, level):
    """Draws level and score of player after his death

    :return: Draws level and score of player after his death
    """
    text1 = 'Score: ' + str(score)
    text2 = 'Level: ' + str(level)

    draw_text(screen, Vector2(500, 230), 32, 'You were killed')
    draw_text(screen, Vector2(500, 280), 32, text1)
    draw_text(screen, Vector2(500, 315), 32, text2)
    draw_text(screen, Vector2(500, 365), 32, 'Press enter to continue')


def create_class_sprites():
    """Creates four player class sprites (PlayerClassSprite) for each player class

    :return: class_sprites_to_render
    """
    twin = PlayerClassSprite('Twin', Vector2(20, 50))
    sniper = PlayerClassSprite('Sniper', Vector2(100, 50))
    machine_gun = PlayerClassSprite('MachineGun', Vector2(20, 130))
    flank_guard = PlayerClassSprite('FlankGuard', Vector2(100, 130))
    ignore_button = IgnoreButton(Vector2(70, 210))
    class_sprites_to_render = pygame.sprite.Group()
    class_sprites_to_render.add(twin)
    class_sprites_to_render.add(sniper)
    class_sprites_to_render.add(machine_gun)
    class_sprites_to_render.add(flank_guard)
    class_sprites_to_render.add(ignore_button)
    return class_sprites_to_render


def choose_class_menu_launcher(choose_class_menu_on, choose_class_menu_on_flag, player):
    """Activates class menu when player's level reaches 15

    :return: choose_class_menu_on, choose_class_menu_on_flag
    """
    if player.level == 15:
        if choose_class_menu_on_flag == 0:
            choose_class_menu_on = True
            choose_class_menu_on_flag = 1
    return choose_class_menu_on, choose_class_menu_on_flag


def draw_choose_class_menu(screen, class_sprites_to_render, choose_class_menu_on):
    """Draws class menu

    :return: Draws class menu
    """
    if choose_class_menu_on:
        draw_text(screen, Vector2(100, 30), 20, 'Upgrades')
        class_sprites_to_render.draw(screen)


if __name__ == "__main__":
    print("This module is not for direct call!")
