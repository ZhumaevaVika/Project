import pygame as pg
from pygame.math import Vector2
import math
from random import randint
from hit_functions import in_polygon, objects_hit


class Player(pg.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pg.Surface((122, 70), pg.SRCALPHA)
        # A reference to the original image to preserve the quality.
        self.orig_image = pg.image.load('Sprites/tank.png')
        self.size = self.orig_image.get_size()
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.rect = self.orig_image.get_rect()
        self.pos_render = Vector2(500, 375)
        self.pos = Vector2(randint(50, 9500), randint(50, 9500))
        self.offset = Vector2(9, 1)  # We shift the sprite 50 px to the right.
        self.angle = 0
        self.len_gun = 35
        self.shoot_delay = 0
        self.regen_time = 0

        self.class_type = 'Tank'
        self.type = 'player'

        self.regen = 3.12  # 3.12% per second
        self.max_HP = 50
        self.HP = 50
        self.BD = 5  # Body_damage 30 HP
        self.bullet_speed = 4
        self.bullet_penetration = 7
        self.bullet_damage = 7
        self.reload = 36  # Чем меньше reload, тем быстрее стреляет # FPS * время перезарядки # 36

        self.regen_points = 0
        self.max_HP_points = 0
        self.BD_points = 0
        self.bullet_speed_points = 0
        self.bullet_penetration_points = 0
        self.bullet_damage_points = 0
        self.reload_points = 0
        self.speed_points = 0

        self.vx = 0
        self.vy = 0
        self.m = 20
        self.impulse = 100
        self.speed = self.impulse / self.m
        self.r = 30
        self.delta_angle = 0

        if player is None:
            self.level = 1
            self.XP = 0  # Score
            self.skill_points = 0
        else:
            self.pos = player.pos
            self.level = player.level
            self.XP = player.XP
            self.skill_points = player.skill_points
            self.max_HP = player.max_HP
            self.HP = player.HP

    def hit_food(self, arr_food, arr_food_to_render):
        for food in arr_food_to_render:
            if in_polygon(self.pos.x, self.pos.y, food.generate_hitbox(self.r)[0], food.generate_hitbox(self.r)[1]):
                objects_hit(self, food)
                self.HP -= int(min(food.BD, food.HP))
                self.regen_time = 0
                food.HP -= min(self.BD, food.HP)
                food.death(arr_food_to_render, self)
                food.death(arr_food, self)

    def if_keys(self):
        keys = pg.key.get_pressed()
        if keys:
            self.move(keys)

    def upgrade_on_key(self, event):
        if event.key == pg.K_1:
            self.health_regen_up()
        if event.key == pg.K_2:
            self.max_health_up()
        if event.key == pg.K_3:
            self.body_damage_up()
        if event.key == pg.K_4:
            self.bullet_speed_up()
        if event.key == pg.K_5:
            self.bullet_penetration_up()
        if event.key == pg.K_6:
            self.bullet_damage_up()
        if event.key == pg.K_7:
            self.reload_up()
        if event.key == pg.K_8:
            self.speed_up()

    def upgrade_on_mouse(self, event):
        x1 = 136
        y1 = 601
        x2 = 166
        y2 = 613
        dy = 15
        if x1 <= event.pos[0] <= x2:
            if y1 <= event.pos[1] <= y2:
                self.health_regen_up()
            if y1 + dy <= event.pos[1] <= y2 + dy:
                self.max_health_up()
            if y1 + 2 * dy <= event.pos[1] <= y2 + 2 * dy:
                self.body_damage_up()
            if y1 + 3 * dy <= event.pos[1] <= y2 + 3 * dy:
                self.bullet_speed_up()
            if y1 + 4 * dy <= event.pos[1] <= y2 + 4 * dy:
                self.bullet_penetration_up()
            if y1 + 5 * dy <= event.pos[1] <= y2 + 5 * dy:
                self.bullet_damage_up()
            if y1 + 6 * dy <= event.pos[1] <= y2 + 6 * dy:
                self.reload_up()
            if y1 + 7 * dy <= event.pos[1] <= y2 + 7 * dy:
                self.speed_up()

    def chose_class(self, event, player, player_sprites, choose_class_menu_on):
        if choose_class_menu_on:
            if (79 <= event.pos[0] <= 121) and (213 <= event.pos[1] <= 226):
                player_sprites.remove(self)
                player, player_sprites = generate_player('Player', self)
                choose_class_menu_on = False
            if (20 <= event.pos[0] <= 95) and (50 <= event.pos[1] <= 125):
                player_sprites.remove(self)
                player, player_sprites = generate_player('Twin', self)
                choose_class_menu_on = False
            if (100 <= event.pos[0] <= 175) and (50 <= event.pos[1] <= 125):
                player_sprites.remove(self)
                player, player_sprites = generate_player('Sniper', self)
                choose_class_menu_on = False
            if (20 <= event.pos[0] <= 95) and (130 <= event.pos[1] <= 205):
                player_sprites.remove(self)
                player, player_sprites = generate_player('MachineGun', self)
                choose_class_menu_on = False
            if (100 <= event.pos[0] <= 175) and (130 <= event.pos[1] <= 205):
                player_sprites.remove(self)
                player, player_sprites = generate_player('FlankGuard', self)
                choose_class_menu_on = False
        return player, player_sprites, choose_class_menu_on

    def death(self):
        if self.HP <= 0:
            self.kill()
            return False
        return True

    def update(self, event):
        if event == (0, 0):
            self.angle = 0
            self.rotate()
        else:
            if event.pos[0] != self.pos_render.x:
                self.angle = math.atan((event.pos[1] - self.pos_render.y) / (event.pos[0] - self.pos_render.x)) + self.delta_angle
            elif event.pos[0] == self.pos_render.x:
                self.angle = -80 * (event.pos[1] - self.pos_render.y) / abs(event.pos[1] - self.pos_render.y) + self.delta_angle
            if event.pos[0] < self.pos_render.x:
                self.angle += math.pi
            self.rotate()
        self.shoot_delay += 1
        
        self.level_up()
        self.regenerate()

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        angle = self.angle * 180 / math.pi
        self.image = pg.transform.rotozoom(self.orig_image, -angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos_render + offset_rotated)

    def move(self, keys):
        x = 0
        y = 0
        k = self.speed / 160
        boost = 100 * k ** 2
        self.vx -= self.vx * k
        self.vy -= self.vy * k
        self.pos.x += self.vx
        self.pos.y += self.vy
        if keys[pg.K_w]:
            y -= 1
        if keys[pg.K_a]:
            x -= 1
        if keys[pg.K_s]:
            y += 1
        if keys[pg.K_d]:
            x += 1
        a = (x ** 2 + y ** 2) ** 0.5
        if a > 0:
            self.vx += boost * x / a - self.vx * k
            self.vy += boost * y / a - self.vy * k
            self.pos.x += self.vx
            self.pos.y += self.vy
        if self.pos.x >= 10000:
            self.pos.x = 10000
        if self.pos.y >= 10000:
            self.pos.y = 10000
        if self.pos.x <= 0:
            self.pos.x = 0
        if self.pos.y <= 0:
            self.pos.y = 0
        m = self.vx * math.sin(self.angle) - self.vy * math.cos(self.angle)
        self.delta_angle = m / 12

    def shoot(self, bullet_sprites, bullets):
        try:
            if self.shoot_delay % self.reload == 0:
                bullet = Bullet(self)
                bullets.append(bullet)
                bullet_sprites.add(bullet)
                bullet.angle_update(pg.mouse.get_pos())
                k = bullet.m * self.bullet_speed / self.m
                self.vx -= k * math.cos(bullet.angle)
                self.vy -= k * math.sin(bullet.angle)
        except AttributeError:
            pass

    def get_shoot_delay(self, event, time_click_passed, mouse_up):
        if event.type == pg.MOUSEBUTTONUP and (event.button == 1):
            self.shoot_delay = 0
            mouse_up = 1

        elif (event.type == pg.MOUSEBUTTONDOWN) and (event.button == 1):
            if time_click_passed > self.reload:
                self.shoot_delay = 0
                time_click_passed = 0
                mouse_up = 0
        return mouse_up, time_click_passed

    def level_up(self):
        score_func = 0.3562 * self.level ** 3 - 5.8423 * self.level ** 2 + 67.4898 * self.level - 60
        if (self.XP >= score_func) and (self.level < 45):
            self.level += 1
            self.max_HP = 50 + 2 * (self.level - 1)
            self.HP += 2
            self.m += 0.5
            self.speed = self.impulse / self.m
            if 2 <= self.level <= 28:
                self.skill_points += 1
            elif (self.level >= 30) and (self.level % 3 == 0):
                self.skill_points += 1

    def health_regen_up(self):
        if (self.regen_points < 7) and (self.skill_points > 0):
            regen_func = -0.0332 * self.regen_points ** 3 + 0.5029 * self.regen_points ** 2 \
                         - 0.1154 * self.regen_points + 3.12
            self.regen = int(regen_func * 100) // 100
            self.regen_points += 1
            self.skill_points -= 1

    def max_health_up(self):
        if (self.max_HP_points < 7) and (self.skill_points > 0):
            self.max_HP += 20
            self.HP += 20
            self.max_HP_points += 1
            self.skill_points -= 1

    def body_damage_up(self):
        if (self.BD_points < 7) and (self.skill_points > 0):
            self.BD += 3
            self.BD_points += 1
            self.skill_points -= 1

    def bullet_speed_up(self):
        if (self.bullet_speed_points < 7) and (self.skill_points > 0):
            self.bullet_speed += 0.5
            self.bullet_speed_points += 1
            self.skill_points -= 1

    def bullet_penetration_up(self):
        if (self.bullet_penetration_points < 7) and (self.skill_points > 0):
            self.bullet_penetration += 3
            self.bullet_penetration_points += 1
            self.skill_points -= 1

    def bullet_damage_up(self):
        if (self.bullet_damage_points < 7) and (self.skill_points > 0):
            self.bullet_damage += 3
            self.bullet_damage_points += 1
            self.skill_points -= 1

    def reload_up(self):
        if (self.reload_points < 7) and (self.skill_points > 0):
            if self.reload > 28:
                self.reload -= 2
            else:
                self.reload -= 3
            self.reload_points += 1
            self.skill_points -= 1

    def speed_up(self):
        if (self.speed_points < 7) and (self.skill_points > 0):
            self.impulse += 20
            self.speed = self.impulse / self.m
            self.speed_points += 1
            self.skill_points -= 1

    def regenerate(self):
        if self.HP < self.max_HP:
            self.regen_time += 1
        else:
            self.regen_time = 0
        if self.regen_time > 6000 / self.regen:
            self.HP += 1

    def render_food(self, arr_food, arr_food_to_render):
        food_sprite_to_render = pg.sprite.Group()
        for food in arr_food:
            if (abs(food.pos.x - self.pos.x) <= 550) and (abs(food.pos.y - self.pos.y) <= 425):
                food.pos_render = Vector2(food.pos.x - self.pos.x + 500, food.pos.y - self.pos.y + 375)
                food_sprite_to_render.add(food)
                if food not in arr_food_to_render:
                    arr_food_to_render.append(food)
            else:
                if food in arr_food_to_render:
                    arr_food_to_render.remove(food)
        return food_sprite_to_render

    def render_bot(self, arr_bot, arr_bot_to_render):
        bot_sprite_to_render = pg.sprite.Group()
        for bot in arr_bot:
            if (abs(bot.pos.x - self.pos.x) <= 500) and (abs(bot.pos.y - self.pos.y) <= 375):
                bot.pos_render = Vector2(bot.pos.x - self.pos.x + 500, bot.pos.y - self.pos.y + 375)
                bot_sprite_to_render.add(bot)
                if bot not in arr_bot_to_render:
                    arr_bot_to_render.append(bot)
            else:
                if bot in arr_bot_to_render:
                    arr_bot_to_render.remove(bot)
        return bot_sprite_to_render


class Bullet(pg.sprite.Sprite):
    def __init__(self, player):
        pos = player.pos
        super().__init__()
        self.image = pg.Surface((122, 70), pg.SRCALPHA)
        # A reference to the original image to preserve the quality.
        self.orig_image = pg.image.load('Sprites/bullet_m.png')
        self.size = self.orig_image.get_size()
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.20), int(self.size[1] * 0.20)))
        self.rect = self.orig_image.get_rect()
        self.pos = Vector2(pos)
        self.pos_render = Vector2(500, 375)
        self.shift = Vector2(0, 0)
        self.len = player.len_gun
        self.offset = Vector2(self.len * math.cos(player.angle),
                              self.len * math.sin(player.angle))
        self.angle = 0
        self.r = 10
        self.m = 3
        self.type = 'player'

        self.speed = player.bullet_speed  # Не точно
        self.penetration = player.bullet_penetration  # Не точно
        self.damage = player.bullet_damage  # 7 HP

    def update(self, event, player):
        self.rotate()
        self.move(player)
        self.penetration -= 0.04
        self.damage -= 0.04

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, 0.01, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(0.01)
        # Create a new rect with the center of the sprite + the offset.
        if (self.type == 'bot') and (self.penetration < 7):
            self.rect = self.image.get_rect(center=self.pos_render + self.shift + offset_rotated)
        else:
            self.rect = self.image.get_rect(center=self.pos_render + self.shift + offset_rotated)

    def angle_update(self, event):
        if event[0] != self.pos_render.x:
            self.angle = math.atan((event[1] - self.pos_render.y) / (event[0] - self.pos_render.x))
        elif event[0] == self.pos_render.x:
            self.angle = -80 * (event[1] - self.pos_render.y) / abs(event[1] - self.pos_render.y)
        if event[0] < self.pos_render.x:
            self.angle += math.pi

    def move(self, player):
        self.shift = self.pos - player.pos
        self.pos_render.x += self.speed * math.cos(self.angle)
        self.pos_render.y += self.speed * math.sin(self.angle)

    def damage_food(self, food, bullets, arr_food, arr_food_to_render, player, bul):
        if bul.type == 'player':
            player = player
        else:
            player = 'bot'
        if (self.pos_render.x + self.shift.x - food.pos_render.x) ** 2 + \
                (self.pos_render.y + self.shift.y - food.pos_render.y) ** 2 <= (self.r + food.r) ** 2:
            self.penetration -= min(abs(self.damage), food.HP)
            food.HP -= min(abs(self.damage), food.HP)
            food.death(arr_food, player)
            food.death(arr_food_to_render, player)
        if self in bullets:
            self.death(bullets)

    def damage_player(self, player, bot, bullets, arr_bot):
        if self.type == 'player':
            player = bot
            if self.penetration < 7:
                if (self.pos_render.x + self.shift.x - player.pos_render.x) ** 2 + \
                        (self.pos_render.y + self.shift.y - player.pos_render.y) ** 2 <= (self.r + player.r) ** 2:
                    self.penetration -= min(abs(self.damage), player.HP)
                    player.HP -= min(abs(self.damage), player.HP)
                    flag = 1
                    bot.death(arr_bot, player, flag)
                if self in bullets:
                    self.death(bullets)

    def death(self, bullets):
        if self.penetration <= 0:
            self.kill()
            if self in bullets:
                bullets.remove(self)


class Twin(Player):
    def __init__(self, player):
        super().__init__(player)
        self.pos = player.pos
        self.orig_image = pg.image.load('Sprites/twin.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.offset = Vector2(9, 1)
        self.len_gun = 35
        self.class_type = 'Twin'
        self.count = 0

        self.regen = player.regen
        self.max_HP = player.max_HP
        self.HP = player.HP
        self.BD = player.BD
        self.bullet_speed = player.bullet_speed
        self.bullet_penetration = player.bullet_penetration
        self.bullet_damage = player.bullet_damage
        self.reload = player.reload

        self.reload = 36 - player.reload_points * 3
        self.bullet_damage = player.bullet_damage
        self.bullet_speed = player.bullet_speed

        self.level = player.level
        self.XP = player.XP
        self.skill_points = player.skill_points
        self.max_HP = player.max_HP
        self.HP = player.HP

        self.regen_points = player.regen_points
        self.max_HP_points = player.max_HP_points
        self.BD_points = player.BD_points
        self.bullet_speed_points = player.bullet_speed_points
        self.bullet_penetration_points = player.bullet_penetration_points
        self.bullet_damage_points = player.bullet_damage_points
        self.reload_points = player.reload_points
        self.speed_points = player.speed_points

    def shoot(self, bullet_sprites, bullets):
        try:
            if self.shoot_delay % self.reload == 0:
                bullet = TwinBullet(self)
                bullets.append(bullet)
                bullet_sprites.add(bullet)
                bullet.angle_update(pg.mouse.get_pos())
                k = bullet.m * self.bullet_speed / self.m
                self.vx -= k * math.cos(bullet.angle)
                self.vy -= k * math.sin(bullet.angle)
                self.count += 1
        except AttributeError:
            pass

    def reload_up(self):
        if (self.reload_points < 7) and (self.skill_points > 0):
            self.reload -= 1
            self.reload_points += 1
            self.skill_points -= 1

    def bullet_damage_up(self):
        if (self.bullet_damage_points < 7) and (self.skill_points > 0):
            self.bullet_damage += 2.5
            self.bullet_damage_points += 1
            self.skill_points -= 1


class TwinBullet(Bullet):
    def __init__(self, player):
        super().__init__(player)
        self.offset1 = Vector2(
            self.len * math.cos(player.angle) - 12 * math.sin(player.angle),
            self.len * math.sin(player.angle) + 12 * math.cos(player.angle))
        self.offset2 = Vector2(
            self.len * math.cos(player.angle) + 12 * math.sin(player.angle),
            self.len * math.sin(player.angle) - 12 * math.cos(player.angle))
        if player.count % 2 == 0:
            self.offset = self.offset1
        if player.count % 2 == 1:
            self.offset = self.offset2
        self.level = player.level
        self.XP = player.XP
        self.skill_points = player.skill_points
        self.max_HP = player.max_HP
        self.HP = player.HP

        self.regen_points = player.regen_points
        self.max_HP_points = player.max_HP_points
        self.BD_points = player.BD_points
        self.bullet_speed_points = player.bullet_speed_points
        self.bullet_penetration_points = player.bullet_penetration_points
        self.bullet_damage_points = player.bullet_damage_points
        self.reload_points = player.reload_points
        self.speed_points = player.speed_points


class Sniper(Player):
    def __init__(self, player):
        super().__init__(player)
        self.pos = player.pos
        self.orig_image = pg.image.load('Sprites/sniper.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.4), int(self.size[1] * 0.36)))
        self.offset = Vector2(13, 1)
        self.len_gun = 35

        self.class_type = 'Sniper'

        self.regen = player.regen
        self.max_HP = player.max_HP
        self.HP = player.HP
        self.BD = player.BD
        self.bullet_speed = player.bullet_speed
        self.bullet_penetration = player.bullet_penetration
        self.bullet_damage = player.bullet_damage
        self.reload = player.reload

        self.bullet_speed = 6
        self.reload = 48

        self.level = player.level
        self.XP = player.XP
        self.skill_points = player.skill_points
        self.max_HP = player.max_HP
        self.HP = player.HP

        self.regen_points = player.regen_points
        self.max_HP_points = player.max_HP_points
        self.BD_points = player.BD_points
        self.bullet_speed_points = player.bullet_speed_points
        self.bullet_penetration_points = player.bullet_penetration_points
        self.bullet_damage_points = player.bullet_damage_points
        self.reload_points = player.reload_points
        self.speed_points = player.speed_points

    def bullet_speed_up(self):
        if (self.bullet_speed_points < 7) and (self.skill_points > 0):
            self.bullet_speed += 0.65
            self.bullet_speed_points += 1
            self.skill_points -= 1


class MachineGun(Player):
    def __init__(self, player):
        super().__init__(player)
        self.pos = player.pos
        self.orig_image = pg.image.load('Sprites/machine_gun.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.offset = Vector2(9, 1)
        self.len_gun = 35

        self.class_type = 'MachineGun'
        
        self.regen = player.regen
        self.max_HP = player.max_HP
        self.HP = player.HP
        self.BD = player.BD
        self.bullet_speed = player.bullet_speed
        self.bullet_penetration = player.bullet_penetration
        self.bullet_damage = player.bullet_damage
        self.reload = player.reload

        self.reload = 18
        self.bullet_damage = 6.5

        self.level = player.level
        self.XP = player.XP
        self.skill_points = player.skill_points
        self.max_HP = player.max_HP
        self.HP = player.HP

        self.regen_points = player.regen_points
        self.max_HP_points = player.max_HP_points
        self.BD_points = player.BD_points
        self.bullet_speed_points = player.bullet_speed_points
        self.bullet_penetration_points = player.bullet_penetration_points
        self.bullet_damage_points = player.bullet_damage_points
        self.reload_points = player.reload_points
        self.speed_points = player.speed_points

    def shoot(self, bullet_sprites, bullets):
        try:
            if self.shoot_delay % self.reload == 0:
                bullet = MachineGunBullet(self)
                bullets.append(bullet)
                bullet_sprites.add(bullet)
                bullet.angle_update(pg.mouse.get_pos())
                k = bullet.m * self.bullet_speed / self.m
                self.vx -= k * math.cos(bullet.angle)
                self.vy -= k * math.sin(bullet.angle)
        except AttributeError:
            pass

    def reload_up(self):
        if (self.reload_points < 7) and (self.skill_points > 0):
            self.reload -= 1
            self.reload_points += 1
            self.skill_points -= 1

    def bullet_damage_up(self):
        if (self.bullet_damage_points < 7) and (self.skill_points > 0):
            self.bullet_damage += 2.75
            self.bullet_damage_points += 1
            self.skill_points -= 1


class MachineGunBullet(Bullet):
    def __init__(self, player):
        super().__init__(player)

    def angle_update(self, event):
        if event[0] != self.pos_render.x:
            self.angle = math.atan((event[1] - self.pos_render.y) / (event[0] - self.pos_render.x))
        elif event[0] == self.pos_render.x:
            self.angle = -80 * (event[1] - self.pos_render.y) / abs(event[1] - self.pos_render.y)
        if event[0] < self.pos_render.x:
            self.angle += math.pi
        self.angle += randint(-15, 15) / 180 * math.pi


class FlankGuard(Player):
    def __init__(self, player):
        super().__init__(player)
        self.pos = player.pos
        self.orig_image = pg.image.load('Sprites/flank_guard.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.44), int(self.size[1] * 0.36)))
        self.offset = Vector2(4, 1)
        self.len_gun = 35

        self.class_type = 'FlankGuard'

        self.regen = player.regen
        self.max_HP = player.max_HP
        self.HP = player.HP
        self.BD = player.BD
        self.bullet_speed = player.bullet_speed
        self.bullet_penetration = player.bullet_penetration
        self.bullet_damage = player.bullet_damage
        self.reload = player.reload

        self.level = player.level
        self.XP = player.XP
        self.skill_points = player.skill_points

        self.regen_points = player.regen_points
        self.max_HP_points = player.max_HP_points
        self.BD_points = player.BD_points
        self.bullet_speed_points = player.bullet_speed_points
        self.bullet_penetration_points = player.bullet_penetration_points
        self.bullet_damage_points = player.bullet_damage_points
        self.reload_points = player.reload_points
        self.speed_points = player.speed_points

    def shoot(self, bullet_sprites, bullets):
        try:
            if self.shoot_delay % self.reload == 0:
                bullet_front = FlankGuardBulletFront(self)
                bullets.append(bullet_front)
                bullet_sprites.add(bullet_front)
                bullet_front.angle_update(pg.mouse.get_pos())

                bullet_back = FlankGuardBulletBack(self)
                bullets.append(bullet_back)
                bullet_sprites.add(bullet_back)
                bullet_back.angle_update(pg.mouse.get_pos())
        except AttributeError:
            pass


class FlankGuardBulletFront(Bullet):
    def __init__(self, player):
        super().__init__(player)
        self.offset = Vector2(self.len * math.cos(player.angle),
                              self.len * math.sin(player.angle))


class FlankGuardBulletBack(Bullet):
    def __init__(self, player):
        super().__init__(player)
        self.offset = Vector2(self.len * -math.cos(player.angle),
                              self.len * -math.sin(player.angle))

    def move(self, player):
        self.shift = self.pos - player.pos
        self.pos_render.x += self.speed * -math.cos(self.angle)
        self.pos_render.y += self.speed * -math.sin(self.angle)


def generate_player(type, player):
    player_sprites = None
    if type == 'Player':
        player = Player(player)
        player_sprites = pg.sprite.Group(player)
    if type == 'Twin':
        player = Twin(player)
        player_sprites = pg.sprite.Group(player)
    if type == 'Sniper':
        player = Sniper(player)
        player_sprites = pg.sprite.Group(player)
    if type == 'MachineGun':
        player = MachineGun(player)
        player_sprites = pg.sprite.Group(player)
    if type == 'FlankGuard':
        player = FlankGuard(player)
        player_sprites = pg.sprite.Group(player)
    return player, player_sprites


if __name__ == "__main__":
    print("This module is not for direct call!")
