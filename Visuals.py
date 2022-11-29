import pygame


def draw_text(screen, position, size, text):
    font = pygame.font.Font('freesansbold.ttf', size)
    color_gray = (50, 50, 50)
    color_white = (255, 255, 255)
    text_main = font.render(text, True, color_white)
    text_add = font.render(text, True, color_gray)
    # text render
    text_main_rect = text_main.get_rect()
    text_add_rect = text_add.get_rect()
    # White borders of text
    text_main_rect.center = (position[0], position[1])
    text_add_rect.center = (position[0], position[1] - 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (position[0], position[1] + 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (position[0] - 1, position[1])
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (position[0] + 1, position[1])
    screen.blit(text_add, text_add_rect)
    # Main gray text
    screen.blit(text_main, text_main_rect)


def draw_bar_with_text(screen, position, width, height, color, value, max_value, text):
    value_to_px = int((value / max_value) * width)
    color_gray = (50, 50, 50)
    color_white = (255, 255, 255)
    font = pygame.font.Font('freesansbold.ttf', height - 2)
    text_main = font.render(text, True, color_white)
    text_add = font.render(text, True, color_gray)
    # Gray borders of health bar line
    pygame.draw.line(screen, color_gray, (position[0] - width//2, position[1]), (position[0] + width//2, position[1]), height)
    pygame.draw.circle(screen, color_gray, (position[0] - width//2, position[1] + 1), height//2)
    pygame.draw.circle(screen, color_gray, (position[0] + width//2, position[1] + 1), height//2)
    # Health bar line
    pygame.draw.line(screen, color, (position[0] - width//2, position[1]),
                     (position[0] - width//2 + value_to_px, position[1]), height - 2)
    pygame.draw.circle(screen, color, (position[0] - width//2, position[1] + 1), (height - 2)//2)
    pygame.draw.circle(screen, color, (position[0] - width//2 + value_to_px, position[1] + 1), (height - 2)//2)
    # text render
    text_main_rect = text_main.get_rect()
    text_add_rect = text_add.get_rect()
    # White borders of text
    text_main_rect.center = (position[0], position[1] + 1)
    text_add_rect.center = (position[0], position[1] + 1 - 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (position[0], position[1] + 1 + 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (position[0] - 1, position[1] + 1)
    screen.blit(text_add, text_add_rect)
    text_add_rect.center = (position[0] + 1, position[1] + 1)
    screen.blit(text_add, text_add_rect)
    # Main gray text
    screen.blit(text_main, text_main_rect)


def draw_bottom_interface(player, width, height, screen, top_score):
    draw_bar_with_text(screen, (width // 2, height - 30), 200, 12, (255, 58, 58), player.HP, player.max_HP,
                       str(player.HP) + '/' + str(player.max_HP))
    draw_bar_with_text(screen, (width//2, height - 45), 150, 12, (151, 255, 158), player.XP, top_score,
                       "Score: " + str(player.XP))
    draw_text(screen, (width//2, height - 60), 20, "Name")  # FIXME поменять имя игрока

