import pygame as pg
from pygame import Vector2
from player import Twin, TwinBullet, Sniper, Bullet, MachineGun, MachineGunBullet, FlankGuard, FlankGuardBulletBack, \
    FlankGuardBulletFront
from random import randint, choice
import math


class BotTwin(Twin):
    def __init__(self, player):
        super().__init__(player)
        self.bot_type = 'twin'
        init_bot(self, player)

    def update(self, player, arr_bot):
        update_bot(self, player, arr_bot)

    def move(self, player):
        move_bot(self, player)

    def shoot(self, bullet_sprites, bullets, player):
        shoot_bot(self, bullet_sprites, bullets, player)

    def death(self, arr_bot, player, flag=0):
        death_bot(self, arr_bot, player, flag)


class BotTwinBullet(TwinBullet):
    def __init__(self, bot_twin):
        super().__init__(bot_twin)
        self.bot_type = 'twin'
        init_bot_bullet(self)

    def angle_update(self, player):
        angle_update_bot_bullet(self, player)

    def damage_player(self, player, bot, bullets, arr_bot, arr_bot_to_render):
        damage_player_bot_bullet(self, player, bullets)


class BotSniper(Sniper):
    def __init__(self, player):
        super().__init__(player)
        self.bot_type = 'sniper'
        init_bot(self, player)

    def update(self, player, arr_bot):
        update_bot(self, player, arr_bot)

    def move(self, player):
        move_bot(self, player)

    def shoot(self, bullet_sprites, bullets, player):
        shoot_bot(self, bullet_sprites, bullets, player)

    def death(self, arr_bot, player, flag=0):
        death_bot(self, arr_bot, player, flag)


class BotSniperBullet(Bullet):
    def __init__(self, bot_twin):
        super().__init__(bot_twin)
        self.bot_type = 'sniper'
        init_bot_bullet(self)

    def angle_update(self, player):
        angle_update_bot_bullet(self, player)

    def damage_player(self, player, bot, bullets, arr_bot, arr_bot_to_render):
        damage_player_bot_bullet(self, player, bullets)


class BotMachineGun(MachineGun):
    def __init__(self, player):
        super().__init__(player)
        self.bot_type = 'machine_gun'
        init_bot(self, player)

    def update(self, player, arr_bot):
        update_bot(self, player, arr_bot)

    def move(self, player):
        move_bot(self, player)

    def shoot(self, bullet_sprites, bullets, player):
        shoot_bot(self, bullet_sprites, bullets, player)

    def death(self, arr_bot, player, flag=0):
        death_bot(self, arr_bot, player, flag)


class BotMachineGunBullet(MachineGunBullet):
    def __init__(self, bot_twin):
        super().__init__(bot_twin)
        self.bot_type = 'machine_gun'
        init_bot_bullet(self)

    def angle_update(self, player):
        angle_update_bot_bullet(self, player)

    def damage_player(self, player, bot, bullets, arr_bot, arr_bot_to_render):
        damage_player_bot_bullet(self, player, bullets)


class BotFlankGuard(FlankGuard):
    def __init__(self, player):
        super().__init__(player)
        self.bot_type = 'flank_guard'
        init_bot(self, player)

    def update(self, player, arr_bot):
        update_bot(self, player, arr_bot)

    def move(self, player):
        move_bot(self, player)

    def shoot(self, bullet_sprites, bullets, player):
        shoot_bot(self, bullet_sprites, bullets, player)

    def death(self, arr_bot, player, flag=0):
        death_bot(self, arr_bot, player, flag)


class BotFlankGuardBulletFront(FlankGuardBulletFront):
    def __init__(self, bot_twin):
        super().__init__(bot_twin)
        self.bot_type = 'flank_guard'
        init_bot_bullet(self)

    def angle_update(self, player):
        angle_update_bot_bullet(self, player)

    def damage_player(self, player, bot, bullets, arr_bot, arr_bot_to_render):
        damage_player_bot_bullet(self, player, bullets)


class BotFlankGuardBulletBack(FlankGuardBulletBack):
    def __init__(self, bot_twin):
        super().__init__(bot_twin)
        self.bot_type = 'flank_guard'
        init_bot_bullet(self)

    def angle_update(self, player):
        angle_update_bot_bullet(self, player)

    def damage_player(self, player, bot, bullets, arr_bot, arr_bot_to_render):
        damage_player_bot_bullet(self, player, bullets)


def generate_bot(player, num_bots, arr_bot=None):
    if arr_bot is None:
        arr_bot = []
    for i in range(num_bots):
        bot = choice([BotTwin(player), BotSniper(player), BotMachineGun(player), BotFlankGuard(player)])
        arr_bot.append(bot)
    return arr_bot


def init_bot(self, player):
    if self.bot_type == 'twin':
        self.orig_image = pg.image.load('Sprites/twin_bot.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
    elif self.bot_type == 'sniper':
        self.orig_image = pg.image.load('Sprites/sniper_bot.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.4), int(self.size[1] * 0.36)))
    elif self.bot_type == 'machine_gun':
        self.orig_image = pg.image.load('Sprites/machine_gun_bot.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
    elif self.bot_type == 'flank_guard':
        self.orig_image = pg.image.load('Sprites/flank_guard_bot.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.44), int(self.size[1] * 0.36)))
    self.pos = Vector2(randint(50, 9950), randint(50, 9950))
    self.pos_render = Vector2(self.pos.x - player.pos.x + 500, self.pos.y - player.pos.y + 375)
    self.type = 'bot'
    get_build(self)


def get_build(self):
    self.level = randint(21, 45)
    self.XP = int(0.3562 * self.level ** 3 - 5.8423 * self.level ** 2 + 67.4898 * self.level - 60) // 4
    if self.level < 30:
        self.skill_points = self.level
    else:
        self.skill_points = 30 + (self.level - 30) // 3
    if self.bot_type == 'twin':
        glass_build(self)
    elif self.bot_type == 'sniper':
        sniper_build(self)
    elif self.bot_type == 'machine_gun':
        ram_build(self)
    elif self.bot_type == 'flank_guard':
        smash_build(self)


def glass_build(self):
    self.bullet_speed_points = self.skill_points // 5
    self.bullet_penetration_points = self.skill_points // 5
    self.bullet_damage_points = self.skill_points // 5
    self.reload_points = self.skill_points // 5
    self.speed_points = self.skill_points // 5


def sniper_build(self):
    self.bullet_speed_points = 7
    self.bullet_penetration_points = 7
    self.bullet_damage_points = 7
    if self.skill_points - 21 <= 7:
        self.speed_points = self.skill_points - 21
    else:
        self.speed_points = 7
        self.max_HP_points = self.skill_points - 28


def ram_build(self):
    self.max_HP_points = self.skill_points // 5
    self.BD_points = self.skill_points // 5
    self.bullet_speed_points = self.skill_points // 5
    self.reload_points = self.skill_points // 5
    self.speed_points = self.skill_points // 5


def smash_build(self):
    self.bullet_penetration_points = 7
    self.bullet_damage_points = 7
    self.reload_points = 7
    if self.skill_points - 21 <= 5:
        self.max_HP_points = self.skill_points - 21
    elif self.skill_points - 21 <= 9:
        self.max_HP_points = 5
        self.speed_points = self.skill_points - 26
    else:
        self.max_HP_points = 5
        self.speed_points = 4
        self.BD_points = self.skill_points - 30


def update_bot(self, player, arr_bot):
    if player.pos.x != self.pos.x:
        self.angle = math.atan((player.pos.y - self.pos.y) / (player.pos.x - self.pos.x))
    elif player.pos.x == self.pos.x:
        try:
            self.angle = -80 * (player.pos.y - self.pos.y) / abs(player.pos.y - self.pos.y)
        except ZeroDivisionError:
            self.angle = 80 * math.pi / 180
    if player.pos.x < self.pos.x:
        self.angle += math.pi
    if self.bot_type == 'machine_gun':
        self.angle *= -1
    self.rotate()
    self.move(player)
    self.death(arr_bot, player)
    self.regenerate()
    if self.bot_type == 'twin':
        self.shoot_delay += 0.5
    else:
        self.shoot_delay += 1


def move_bot(self, player):
    x = 0
    y = 0
    k = self.impulse / self.m / 160
    boost = 100 * k ** 2
    self.vx -= self.vx * k
    self.vy -= self.vy * k
    self.pos.x += self.vx
    self.pos.y += self.vy
    f1 = False
    f2 = False
    f3 = False
    f4 = False
    if self.bot_type == 'twin':
        f1 = ((self.pos.y - player.pos.y) ** 2 + (self.pos.x - player.pos.x) ** 2) ** 0.5 > 250
    elif self.bot_type == 'sniper':
        f2 = ((self.pos.y - player.pos.y) ** 2 + (self.pos.x - player.pos.x) ** 2) ** 0.5 > 400
    elif self.bot_type == 'machine_gun':
        f3 = ((self.pos.y - player.pos.y) ** 2 + (self.pos.x - player.pos.x) ** 2) ** 0.5 > 20
    elif self.bot_type == 'flank_guard':
        f4 = ((self.pos.y - player.pos.y) ** 2 + (self.pos.x - player.pos.x) ** 2) ** 0.5 > 50
    if ((self.bot_type == 'twin') and f1) or ((self.bot_type == 'sniper') and f2) \
            or ((self.bot_type == 'machine_gun') and f3) or ((self.bot_type == 'flank_guard') and f4):
        if self.pos.y > player.pos.y:
            y -= 1
        if self.pos.x > player.pos.x:
            x -= 1
        if self.pos.y < player.pos.y:
            y += 1
        if self.pos.x < player.pos.x:
            x += 1
    else:
        if self.pos.y > player.pos.y:
            y += 1
        if self.pos.x > player.pos.x:
            x += 1
        if self.pos.y < player.pos.y:
            y -= 1
        if self.pos.x < player.pos.x:
            x -= 1
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


def shoot_bot(self, bullet_sprites, bullets, player):
    try:
        if ((int(self.shoot_delay - 0.5) % self.reload == 0) and (self.bot_type == 'twin')) or (
                (int(self.shoot_delay) % self.reload == 0) and (self.bot_type != 'twin')):
            if self.bot_type == 'twin':
                bullet = BotTwinBullet(self)
            elif self.bot_type == 'sniper':
                bullet = BotSniperBullet(self)
            elif self.bot_type == 'machine_gun':
                bullet = BotMachineGunBullet(self)
            elif self.bot_type == 'flank_guard':
                bullet = BotFlankGuardBulletBack(self)
                bullets.append(bullet)
                bullet_sprites.add(bullet)
                bullet.angle_update(player)
                bullet = BotFlankGuardBulletFront(self)
            else:
                bullet = None
            bullets.append(bullet)
            bullet_sprites.add(bullet)
            bullet.angle_update(player)
            if self.bot_type != 'flank_guard':
                k = bullet.m * self.bullet_speed / self.m
                self.vx -= k * math.cos(bullet.angle)
                self.vy -= k * math.sin(bullet.angle)
                if self.bot_type == 'twin':
                    self.count += 1
    except AttributeError:
        pass


def death_bot(self, arr_bot, player, flag=0):
    if self.HP <= 0:
        self.kill()
        if flag == 1:
            player.XP += self.XP
        print(player.XP)  # FIXME player.XP каждый раз обнуляется
        if self in arr_bot:
            arr_bot.remove(self)
        generate_bot(player, 1, arr_bot)


def init_bot_bullet(self):
    self.orig_image = pg.image.load('Sprites/bullet_bot.png')
    self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.20), int(self.size[1] * 0.20)))
    self.type = 'bot'


def angle_update_bot_bullet(self, player):
    if player.pos.x != self.pos.x:
        self.angle = math.atan((player.pos.y - self.pos.y) / (player.pos.x - self.pos.x))
    elif player.pos.x == self.pos.x:
        self.angle = -80 * (player.pos.y - self.pos.y) / abs(player.pos.y - self.pos.y)
    if player.pos.x < self.pos.x:
        self.angle += math.pi
    if self.bot_type == 'machine_gun':
        self.angle += randint(-15, 15) / 180 * math.pi
        self.angle *= -1


def damage_player_bot_bullet(self, player, bullets):
    if 0 < self.penetration < 7:
        if (self.pos_render.x + self.shift.x - player.pos_render.x) ** 2 + \
                (self.pos_render.y + self.shift.y - player.pos_render.y) ** 2 <= (self.r + player.r) ** 2:
            self.penetration -= 6
            player.HP -= min(abs(self.damage), player.HP)
            player.death(bullets, player)
            self.death(bullets)
