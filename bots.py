import pygame as pg
from pygame import Vector2
from player import Twin, TwinBullet, Sniper, Bullet, MachineGun, MachineGunBullet, FlankGuard, FlankGuardBulletBack, FlankGuardBulletFront
from random import randint, choice
import math


class BotTwin(Twin):
    def __init__(self, player):
        super().__init__(player)
        self.orig_image = pg.image.load('Sprites/twin_bot.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.pos = Vector2(randint(50, 9950), randint(50, 9950))
        self.pos_render = Vector2(self.pos.x - player.pos.x + 500, self.pos.y - player.pos.y + 375)
        self.type = 'bot'
        self.get_build()

    def get_build(self):
        self.level = randint(21, 45)
        self.XP = int(0.3562 * self.level ** 3 - 5.8423 * self.level ** 2 + 67.4898 * self.level - 60)//4
        if self.level < 30:
            self.skill_points = self.level
        else:
            self.skill_points = 30 + (self.level - 30) // 3
        self.glass_build()

    def glass_build(self):
        self.bullet_speed_points = self.skill_points // 5
        self.bullet_penetration_points = self.skill_points // 5
        self.bullet_damage_points = self.skill_points // 5
        self.reload_points = self.skill_points // 5
        self.speed_points = self.skill_points // 5

    def update(self, player, arr_bot):
        if player.pos.x != self.pos.x:
            self.angle = math.atan((player.pos.y - self.pos.y) / (player.pos.x - self.pos.x))
        elif player.pos.x == self.pos.x:
            try:
                self.angle = -80 * (player.pos.y - self.pos.y) / abs(player.pos.y - self.pos.y)
            except ZeroDivisionError:
                self.angle = 80*math.pi/180
        if player.pos.x < self.pos.x:
            self.angle += math.pi
        self.rotate()
        self.move(player)
        self.death(arr_bot, player)

        self.shoot_delay += 0.5
        self.regenerate()

    def move(self, player):
        x = 0
        y = 0
        k = self.speed / 160
        boost = 100 * k ** 2
        self.vx -= self.vx * k
        self.vy -= self.vy * k
        self.pos.x += self.vx
        self.pos.y += self.vy
        if ((self.pos.y - player.pos.y)**2 + (self.pos.x - player.pos.x)**2)**0.5 > 250:
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

        pass

    def shoot(self, bullet_sprites, bullets, player):
        try:
            if int(self.shoot_delay-0.5) % self.reload == 0:
                bullet = BotTwinBullet(self)
                bullets.append(bullet)
                bullet_sprites.add(bullet)
                bullet.angle_update(player)
                k = bullet.m * self.bullet_speed / self.m
                self.vx -= k * math.cos(bullet.angle)
                self.vy -= k * math.sin(bullet.angle)
                self.count += 1
        except AttributeError:
            pass

    def death(self, arr_bot, player, flag=0):
        if self.HP <= 0:
            self.kill()
            if flag == 1:
                player.XP += self.XP
            print(player.XP)  # FIXME player.XP каждый раз обнуляется
            if self in arr_bot:
                arr_bot.remove(self)
            generate_bot(player, 1, arr_bot)


class BotTwinBullet(TwinBullet):
    def __init__(self, bot_twin):
        super().__init__(bot_twin)
        self.orig_image = pg.image.load('Sprites/bullet_bot.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.20), int(self.size[1] * 0.20)))
        self.type = 'bot'

    def angle_update(self, player):
        if player.pos.x != self.pos.x:
            self.angle = math.atan((player.pos.y - self.pos.y) / (player.pos.x - self.pos.x))
        elif player.pos.x == self.pos.x:
            self.angle = -80 * (player.pos.y - self.pos.y) / abs(player.pos.y - self.pos.y)
        if player.pos.x < self.pos.x:
            self.angle += math.pi

    def damage_player(self, player, bot, bullets, arr_bot):
        if 0 < self.penetration < 7:
            if (self.pos_render.x + self.shift.x - player.pos_render.x) ** 2 + \
                    (self.pos_render.y + self.shift.y - player.pos_render.y) ** 2 <= (self.r + player.r) ** 2:
                self.penetration -= 6
                player.HP -= min(abs(self.damage), player.HP)
                player.death()
                self.death(bullets)


class BotSniper(Sniper):
    def __init__(self, player):
        super().__init__(player)
        self.orig_image = pg.image.load('Sprites/sniper_bot.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.4), int(self.size[1] * 0.36)))
        self.pos = Vector2(randint(50, 9950), randint(50, 9950))
        self.pos_render = Vector2(self.pos.x - player.pos.x + 500, self.pos.y - player.pos.y + 375)
        self.type = 'bot'
        self.get_build()

    def get_build(self):
        self.level = randint(21, 45)
        self.XP = int(0.3562 * self.level ** 3 - 5.8423 * self.level ** 2 + 67.4898 * self.level - 60)//4
        if self.level < 30:
            self.skill_points = self.level
        else:
            self.skill_points = 30 + (self.level - 30) // 3
        self.sniper_build()

    def sniper_build(self):
        self.bullet_speed_points = 7
        self.bullet_penetration_points = 7
        self.bullet_damage_points = 7
        if self.skill_points - 21 <= 7:
            self.speed_points = self.skill_points - 21
        else:
            self.speed_points = 7
            self.max_HP_points = self.skill_points - 28

    def update(self, player, arr_bot):
        if player.pos.x != self.pos.x:
            self.angle = math.atan((player.pos.y - self.pos.y) / (player.pos.x - self.pos.x))
        elif player.pos.x == self.pos.x:
            try:
                self.angle = -80 * (player.pos.y - self.pos.y) / abs(player.pos.y - self.pos.y)
            except ZeroDivisionError:
                self.angle = 80*math.pi/180
        if player.pos.x < self.pos.x:
            self.angle += math.pi
        self.rotate()
        self.move(player)
        self.death(arr_bot, player)

        self.shoot_delay += 1
        self.regenerate()

    def move(self, player):
        x = 0
        y = 0
        k = self.speed / 160
        boost = 100 * k ** 2
        self.vx -= self.vx * k
        self.vy -= self.vy * k
        self.pos.x += self.vx
        self.pos.y += self.vy
        if ((self.pos.y - player.pos.y)**2 + (self.pos.x - player.pos.x)**2)**0.5 > 400:
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

        pass

    def shoot(self, bullet_sprites, bullets, player):
        try:
            if int(self.shoot_delay) % self.reload == 0:
                bullet = BotSniperBullet(self)
                bullets.append(bullet)
                bullet_sprites.add(bullet)
                bullet.angle_update(player)
                k = bullet.m * self.bullet_speed / self.m
                self.vx -= k * math.cos(bullet.angle)
                self.vy -= k * math.sin(bullet.angle)
                self.count += 1
        except AttributeError:
            pass

    def death(self, arr_bot, player, flag=0):
        if self.HP <= 0:
            self.kill()
            if flag == 1:
                player.XP += self.XP
            print(player.XP)  # FIXME player.XP каждый раз обнуляется
            if self in arr_bot:
                arr_bot.remove(self)
            generate_bot(player, 1, arr_bot)


class BotSniperBullet(Bullet):
    def __init__(self, bot_twin):
        super().__init__(bot_twin)
        self.orig_image = pg.image.load('Sprites/bullet_bot.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.20), int(self.size[1] * 0.20)))
        self.type = 'bot'

    def angle_update(self, player):
        if player.pos.x != self.pos.x:
            self.angle = math.atan((player.pos.y - self.pos.y) / (player.pos.x - self.pos.x))
        elif player.pos.x == self.pos.x:
            self.angle = -80 * (player.pos.y - self.pos.y) / abs(player.pos.y - self.pos.y)
        if player.pos.x < self.pos.x:
            self.angle += math.pi

    def damage_player(self, player, bot, bullets, arr_bot):
        if 0 < self.penetration < 7:
            if (self.pos_render.x + self.shift.x - player.pos_render.x) ** 2 + \
                    (self.pos_render.y + self.shift.y - player.pos_render.y) ** 2 <= (self.r + player.r) ** 2:
                self.penetration -= 6
                player.HP -= min(abs(self.damage), player.HP)
                player.death()
                self.death(bullets)


class BotMachineGun(MachineGun):
    def __init__(self, player):
        super().__init__(player)
        self.orig_image = pg.image.load('Sprites/machinegun_bot.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.pos = Vector2(randint(50, 9950), randint(50, 9950))
        self.pos_render = Vector2(self.pos.x - player.pos.x + 500, self.pos.y - player.pos.y + 375)
        self.type = 'bot'
        self.get_build()

    def get_build(self):
        self.level = randint(21, 45)
        self.XP = int(0.3562 * self.level ** 3 - 5.8423 * self.level ** 2 + 67.4898 * self.level - 60) // 4
        if self.level < 30:
            self.skill_points = self.level
        else:
            self.skill_points = 30 + (self.level - 30) // 3
        self.ram_build()

    def ram_build(self):
        self.max_HP_points = self.skill_points // 5
        self.BD_points = self.skill_points // 5
        self.bullet_speed_points = self.skill_points // 5
        self.reload_points = self.skill_points // 5
        self.speed_points = self.skill_points // 5

    def update(self, player, arr_bot):
        if player.pos.x != self.pos.x:
            self.angle = math.atan((player.pos.y - self.pos.y) / (player.pos.x - self.pos.x))
        elif player.pos.x == self.pos.x:
            try:
                self.angle = -80 * (player.pos.y - self.pos.y) / abs(player.pos.y - self.pos.y)
            except ZeroDivisionError:
                self.angle = 80 * math.pi / 180
        if player.pos.x < self.pos.x:
            self.angle += math.pi
        self.angle *= -1
        self.rotate()
        self.move(player)
        self.death(arr_bot, player)

        self.shoot_delay += 1
        self.regenerate()

    def move(self, player):
        x = 0
        y = 0
        k = self.speed / 160
        boost = 100 * k ** 2
        self.vx -= self.vx * k
        self.vy -= self.vy * k
        self.pos.x += self.vx
        self.pos.y += self.vy
        if ((self.pos.y - player.pos.y) ** 2 + (self.pos.x - player.pos.x) ** 2) ** 0.5 > 20:
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

        pass

    def shoot(self, bullet_sprites, bullets, player):
        try:
            if int(self.shoot_delay) % self.reload == 0:
                bullet = BotMachineGunBullet(self)
                bullets.append(bullet)
                bullet_sprites.add(bullet)
                bullet.angle_update(player)
                k = bullet.m * self.bullet_speed / self.m
                self.vx -= k * math.cos(bullet.angle)
                self.vy -= k * math.sin(bullet.angle)
                self.count += 1
        except AttributeError:
            pass

    def death(self, arr_bot, player, flag=0):
        if self.HP <= 0:
            self.kill()
            if flag == 1:
                player.XP += self.XP
            print(player.XP)  # FIXME player.XP каждый раз обнуляется
            if self in arr_bot:
                arr_bot.remove(self)
            generate_bot(player, 1, arr_bot)


class BotMachineGunBullet(MachineGunBullet):
    def __init__(self, bot_twin):
        super().__init__(bot_twin)
        self.orig_image = pg.image.load('Sprites/bullet_bot.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.20), int(self.size[1] * 0.20)))
        self.type = 'bot'

    def angle_update(self, player):
        if player.pos.x != self.pos.x:
            self.angle = math.atan((player.pos.y - self.pos.y) / (player.pos.x - self.pos.x))
        elif player.pos.x == self.pos.x:
            self.angle = -80 * (player.pos.y - self.pos.y) / abs(player.pos.y - self.pos.y)
        if player.pos.x < self.pos.x:
            self.angle += math.pi
        self.angle *= -1

    def damage_player(self, player, bot, bullets, arr_bot):
        if 0 < self.penetration < 7:
            if (self.pos_render.x + self.shift.x - player.pos_render.x) ** 2 + \
                    (self.pos_render.y + self.shift.y - player.pos_render.y) ** 2 <= (self.r + player.r) ** 2:
                self.penetration -= 6
                player.HP -= min(abs(self.damage), player.HP)
                player.death()
                self.death(bullets)


class BotFlankGuard(FlankGuard):
    def __init__(self, player):
        super().__init__(player)
        self.orig_image = pg.image.load('Sprites/flankguard_bot.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.44), int(self.size[1] * 0.36)))
        self.pos = Vector2(randint(50, 9950), randint(50, 9950))
        self.pos_render = Vector2(self.pos.x - player.pos.x + 500, self.pos.y - player.pos.y + 375)
        self.type = 'bot'
        self.get_build()

    def get_build(self):
        self.level = randint(21, 45)
        self.XP = int(0.3562 * self.level ** 3 - 5.8423 * self.level ** 2 + 67.4898 * self.level - 60)//4
        if self.level < 30:
            self.skill_points = self.level
        else:
            self.skill_points = 30 + (self.level - 30) // 3
        self.smash_build()

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

    def update(self, player, arr_bot):
        if player.pos.x != self.pos.x:
            self.angle = math.atan((player.pos.y - self.pos.y) / (player.pos.x - self.pos.x))
        elif player.pos.x == self.pos.x:
            try:
                self.angle = -80 * (player.pos.y - self.pos.y) / abs(player.pos.y - self.pos.y)
            except ZeroDivisionError:
                self.angle = 80*math.pi/180
        if player.pos.x < self.pos.x:
            self.angle += math.pi
        self.rotate()
        self.move(player)
        self.death(arr_bot, player)

        self.shoot_delay += 1
        self.regenerate()

    def move(self, player):
        x = 0
        y = 0
        k = self.speed / 160
        boost = 100 * k ** 2
        self.vx -= self.vx * k
        self.vy -= self.vy * k
        self.pos.x += self.vx
        self.pos.y += self.vy
        if ((self.pos.y - player.pos.y)**2 + (self.pos.x - player.pos.x)**2)**0.5 > 50:
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

        pass

    def shoot(self, bullet_sprites, bullets, player):
        try:
            if int(self.shoot_delay) % self.reload == 0:
                bullet1 = BotFlankGuardBulletFront(self)
                bullet2 = BotFlankGuardBulletBack(self)
                bullets.append(bullet1)
                bullets.append(bullet2)
                bullet_sprites.add(bullet1)
                bullet_sprites.add(bullet2)
                bullet1.angle_update(player)
                bullet2.angle_update(player)
                self.count += 1
        except AttributeError:
            pass

    def death(self, arr_bot, player, flag=0):
        if self.HP <= 0:
            self.kill()
            if flag == 1:
                player.XP += self.XP
            print(player.XP)  # FIXME player.XP каждый раз обнуляется
            if self in arr_bot:
                arr_bot.remove(self)
            generate_bot(player, 1, arr_bot)


class BotFlankGuardBulletFront(FlankGuardBulletFront):
    def __init__(self, bot_twin):
        super().__init__(bot_twin)
        self.orig_image = pg.image.load('Sprites/bullet_bot.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.20), int(self.size[1] * 0.20)))
        self.type = 'bot'

    def angle_update(self, player):
        if player.pos.x != self.pos.x:
            self.angle = math.atan((player.pos.y - self.pos.y) / (player.pos.x - self.pos.x))
        elif player.pos.x == self.pos.x:
            self.angle = -80 * (player.pos.y - self.pos.y) / abs(player.pos.y - self.pos.y)
        if player.pos.x < self.pos.x:
            self.angle += math.pi

    def damage_player(self, player, bot, bullets, arr_bot):
        if 0 < self.penetration < 7:
            if (self.pos_render.x + self.shift.x - player.pos_render.x) ** 2 + \
                    (self.pos_render.y + self.shift.y - player.pos_render.y) ** 2 <= (self.r + player.r) ** 2:
                self.penetration -= 6
                player.HP -= min(abs(self.damage), player.HP)
                player.death()
                self.death(bullets)


class BotFlankGuardBulletBack(FlankGuardBulletBack):
    def __init__(self, bot_twin):
        super().__init__(bot_twin)
        self.orig_image = pg.image.load('Sprites/bullet_bot.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.20), int(self.size[1] * 0.20)))
        self.type = 'bot'

    def angle_update(self, player):
        if player.pos.x != self.pos.x:
            self.angle = math.atan((player.pos.y - self.pos.y) / (player.pos.x - self.pos.x))
        elif player.pos.x == self.pos.x:
            self.angle = -80 * (player.pos.y - self.pos.y) / abs(player.pos.y - self.pos.y)
        if player.pos.x < self.pos.x:
            self.angle += math.pi

    def damage_player(self, player, bot, bullets, arr_bot):
        if 0 < self.penetration < 7:
            if (self.pos_render.x + self.shift.x - player.pos_render.x) ** 2 + \
                    (self.pos_render.y + self.shift.y - player.pos_render.y) ** 2 <= (self.r + player.r) ** 2:
                self.penetration -= 6
                player.HP -= min(abs(self.damage), player.HP)
                player.death()
                self.death(bullets)


def generate_bot(player, num_bots, arr_bot=None):
    if arr_bot is None:
        arr_bot = []
    for i in range(num_bots):
        bot = choice([BotTwin(player), BotSniper(player), BotMachineGun(player), BotFlankGuard(player)])
        arr_bot.append(bot)
    return arr_bot

