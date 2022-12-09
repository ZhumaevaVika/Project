import pygame
from config import GREY, WHITE, RED, GREEN, ORANGE, PURPLE, DARK_PURPLE, YELLOW, BLUE, ANOTHER_GREEN, CYAN
from pygame.math import Vector2


def draw_text(screen, pos, size, text):
    font = pygame.font.Font('freesansbold.ttf', size)
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
    value_to_px = int((value / max_value) * width)
    font = pygame.font.Font('freesansbold.ttf', height - 2)
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
    value_to_px = int((value / max_value) * width)
    font = pygame.font.Font('freesansbold.ttf', height - 2)
    text_main = font.render(text, True, WHITE)
    text_add = font.render(text, True, GREY)
    # Gray borders of health bar line
    pygame.draw.line(screen, GREY, (pos.x - width//2, pos.y),
                     (pos.x + width//2, pos.y), height)
    pygame.draw.circle(screen, GREY, (pos.x - width//2, pos.y + 1), height//2)
    pygame.draw.circle(screen, GREY, (pos.x + width//2, pos.y + 1), height//2)
    # Health bar line
    pygame.draw.line(screen, color, (pos.x - width//2, pos.y),
                     (pos.x - width//2 + value_to_px, pos.y), height - 2)
    pygame.draw.circle(screen, color, (pos.x - width//2, pos.y + 1), (height - 2)//2)
    pygame.draw.circle(screen, color, (pos.x - width//2 + value_to_px, pos.y + 1), (height - 2)//2)
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
    value_to_px = int((value / max_value) * (5 * width//6))
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
    text_main_rect.center = (pos.x - width//10, pos.y + 1)
    text_add_rect.center = (pos.x - width//10, pos.y + 1 - 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (pos.x - width//10, pos.y + 1 + 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (pos.x - 1 - width//10, pos.y + 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (pos.x + 1 - width//10, pos.y + 1)
    screen.blit(text_add, text_add_rect)
    # Main gray text
    screen.blit(text_main, text_main_rect)
    draw_text(screen, Vector2(pos.x + width//4 + 5, pos.y), 6, '[' + str(number_button) + ']')
    pygame.draw.rect(screen, GREY, pygame.Rect(pos.x + width//2 - 14, pos.y - 1, 9, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(pos.x + width // 2 - 14 + 3, pos.y - 1 - 3, 3, 9))


def draw_bottom_interface(player, width, height, screen, top_score):
    score_func = 0.3562 * player.level ** 3 - 5.8423 * player.level ** 2 + 67.4898 * player.level - 60
    if player.level != 1:
        score_func_1 = 0.3562 * (player.level - 1) ** 3 - 5.8423 * (player.level - 1) ** 2 + 67.4898 * \
                       (player.level - 1) - 60
        draw_bar_with_text(screen, Vector2(width // 2, height - 30), 200, 12, YELLOW, player.XP - score_func_1,
                           score_func - score_func_1, 'Lvl ' + str(player.level) + ' ' + player.class_type)
    else:
        draw_bar_with_text(screen, Vector2(width // 2, height - 30), 200, 12, YELLOW, player.XP,
                           score_func, 'Lvl ' + str(player.level) + ' ' + player.class_type)

    if player.XP <= top_score:
        draw_bar_with_text(screen, Vector2(width//2, height - 45), 150, 12, GREEN, player.XP, top_score,
                           "Score: " + str(player.XP))
    else:
        draw_bar_with_text(screen, Vector2(width // 2, height - 45), 150, 12, GREEN, 1, 1,
                           "Score: " + str(player.XP))
    if player.skill_points > 0:
        draw_text(screen, Vector2(width // 2, height - 60), 20, "Name")  # FIXME поменять имя игрока
        draw_upgrade_bar(screen, Vector2(90, height - 150), 140, 12, ORANGE, player.regen_points, 7, "Health Regen", 1)
        draw_upgrade_bar(screen, Vector2(90, height - 135), 140, 12, PURPLE, player.max_HP_points, 7, "Max Health", 2)
        draw_upgrade_bar(screen, Vector2(90, height - 120), 140, 12, DARK_PURPLE, player.BD_points, 7, "Body Damage", 3)
        draw_upgrade_bar(screen, Vector2(90, height - 105), 140, 12, BLUE, player.bullet_speed_points, 7,
                         "Bullet Speed", 4)
        draw_upgrade_bar(screen, Vector2(90, height - 90), 140, 12, YELLOW, player.bullet_penetration_points, 7,
                         "Bullet Penetration", 5)
        draw_upgrade_bar(screen, Vector2(90, height - 75), 140, 12, RED, player.bullet_damage_points, 7,
                         "Bullet Damage", 6)
        draw_upgrade_bar(screen, Vector2(90, height - 60), 140, 12, ANOTHER_GREEN, player.reload_points, 7, "Reload", 7)
        draw_upgrade_bar(screen, Vector2(90, height - 45), 140, 12, CYAN, player.speed_points, 7, "Movement Speed", 8)

    if player.HP < player.max_HP:
        if player.HP >= 0:
            draw_bar(screen, Vector2(width // 2, height // 2 + 50), 50, 8, ANOTHER_GREEN, player.HP, player.max_HP)
        else:
            draw_bar(screen, Vector2(width // 2, height // 2 + 50), 50, 8, ANOTHER_GREEN, 0, player.max_HP)
