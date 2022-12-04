import pygame
from config import GREY, WHITE, RED, GREEN, ORANGE, PURPLE, DARK_PURPLE
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
    draw_bar_with_text(screen, Vector2(width // 2, height - 30), 200, 12, RED, player.HP, player.max_HP,
                       str(player.HP) + '/' + str(player.max_HP))
    draw_bar_with_text(screen, Vector2(width//2, height - 45), 150, 12, GREEN, player.XP, top_score,
                       "Score: " + str(player.XP))
    draw_text(screen, Vector2(width//2, height - 60), 20, "Name")  # FIXME поменять имя игрока
    draw_upgrade_bar(screen, Vector2(90, height - 150), 140, 12, ORANGE, player.regen_points, 7, "Health Regen", 1)
    draw_upgrade_bar(screen, Vector2(90, height - 135), 140, 12, PURPLE, player.max_HP_points, 7, "Max Health", 2)
    draw_upgrade_bar(screen, Vector2(90, height - 120), 140, 12, DARK_PURPLE, player.BD_points, 7, "Body Damage", 3)
