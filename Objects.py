import pygame as pg
from pygame.math import Vector2
import math
from random import randint, randrange, choice


# FIXME (не баг, а фича)) При смене класса сбрасывается прокачка, skill points остаются


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

        self.regen = 3.12  # 3.12% per second
        self.max_HP = 50
        self.HP = 50
        self.BD = 30  # Body_damage 30 HP
        self.bullet_speed = 4
        self.bullet_penetration = 7
        self.bullet_damage = 7
        self.reload = 36  # Чем меньше reload, тем быстрее стреляет # FPS * время перезарядки # 36
        self.speed = 3.5  # С увеличением уровня падает скорость

        self.regen_points = 0
        self.max_HP_points = 0
        self.BD_points = 0
        self.bullet_speed_points = 0
        self.bullet_penetration_points = 0
        self.bullet_damage_points = 0
        self.reload_points = 0
        self.speed_points = 0

        if player is None:
            self.level = 1
            self.XP = 0  # Score
            self.skill_points = 0
        else:
            self.level = player.level
            self.XP = player.XP
            self.skill_points = player.skill_points

    def if_keys(self):
        keys = pg.key.get_pressed()
        if keys:
            self.move(keys)

    def upgrade(self, event):
        # FIXME При смене класса танка сбрасывается прокачка
        if event.key == pg.K_1:
            self.health_regen_up()
            print('regen ', self.regen_points, ' skill points ', self.skill_points)
        if event.key == pg.K_2:
            self.max_health_up()
            print('max HP ', self.max_HP_points, ' skill points ', self.skill_points)
        if event.key == pg.K_3:
            self.body_damage_up()
            print('body damage ', self.BD_points, ' skill points ', self.skill_points)
        if event.key == pg.K_4:
            self.bullet_speed_up()
            print('bullet speed ', self.bullet_speed_points, ' skill points ', self.skill_points)
        if event.key == pg.K_5:
            self.bullet_penetration_up()
            print('bullet penetration ', self.bullet_penetration_points, ' skill points ', self.skill_points)
        if event.key == pg.K_6:
            self.bullet_damage_up()
            print('bullets damage ', self.bullet_damage_points, ' skill points ', self.skill_points)
        if event.key == pg.K_7:
            self.reload_up()
            print('reload ', self.reload_points, ' skill points ', self.skill_points)
        if event.key == pg.K_8:
            self.speed_up()
            print('speed ', self.speed_points, ' skill points ', self.skill_points)

    def chose_class(self, event, player, player_sprites):
        generator = Generator()
        if event.key == pg.K_g:
            player_sprites.remove(self)
            player, player_sprites = generator.generate_player('Player', self)
        if event.key == pg.K_h:
            player_sprites.remove(self)
            player, player_sprites = generator.generate_player('Twin', self)
        if event.key == pg.K_j:
            player_sprites.remove(self)
            player, player_sprites = generator.generate_player('Sniper', self)
        if event.key == pg.K_k:
            player_sprites.remove(self)
            player, player_sprites = generator.generate_player('MachineGun', self)
        if event.key == pg.K_l:
            player_sprites.remove(self)
            player, player_sprites = generator.generate_player('FlankGuard', self)
        return player, player_sprites

    def update(self, event):
        if event == (0, 0):
            self.angle = 0
            self.rotate()
        else:
            if event.pos[0] != self.pos_render.x:
                self.angle = math.atan((event.pos[1] - self.pos_render.y) / (event.pos[0] - self.pos_render.x))
            elif event.pos[0] == self.pos_render.x:
                self.angle = -80 * (event.pos[1] - self.pos_render.y) / abs(event.pos[1] - self.pos_render.y)
            self.angle = self.angle * 360 / 6.28
            if event.pos[0] < self.pos_render.x:
                self.angle += 180
            self.rotate()
        self.shoot_delay += 1

        self.level_up()

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos_render + offset_rotated)

    def move(self, keys):
        x = 0
        y = 0
        if keys[pg.K_w]:
            y -= 1
        if keys[pg.K_a]:
            x -= 1
        if keys[pg.K_s]:
            y += 1
        if keys[pg.K_d]:
            x += 1
        if (x ** 2 + y ** 2) > 0:
            self.pos.x += int(self.speed * x / (x ** 2 + y ** 2) ** 0.5)
            self.pos.y += int(self.speed * y / (x ** 2 + y ** 2) ** 0.5)
        if self.pos.x >= 10000:
            self.pos.x = 10000
        if self.pos.y >= 10000:
            self.pos.y = 10000
        if self.pos.x <= 0:
            self.pos.x = 0
        if self.pos.y <= 0:
            self.pos.y = 0

    def shoot(self, bullet_sprites, bullets):
        try:
            if self.shoot_delay % self.reload == 0:
                bullet = Bullet(self)
                bullets.append(bullet)
                bullet_sprites.add(bullet)
                bullet.angle_update(pg.mouse.get_pos())
        except AttributeError:
            pass

    def get_shoot_delay(self, event, time_click_passed, mouse_up):
        if event.type == pg.MOUSEBUTTONUP:
            self.shoot_delay = 0
            mouse_up = 1

        elif event.type == pg.MOUSEBUTTONDOWN:
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
            if 2 <= self.level <= 28:
                self.skill_points += 1
            elif (self.level >= 30) and (self.level % 3 == 0):
                self.skill_points += 1
            print('level ', self.level, ' skill points ', self.skill_points)

    def health_regen_up(self):
        if (self.regen_points < 7) and (self.skill_points > 0):
            regen_func = -0.0332 * self.regen_points ** 3 + 0.5029 * self.regen_points ** 2\
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
            self.BD += 6
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
            self.speed += 0.5
            self.speed_points += 1
            self.skill_points -= 1

    def render_food(self, arr_food, arr_food_to_render):
        food_sprite_to_render = pg.sprite.Group()
        for food in arr_food:
            if (abs(food.pos.x - self.pos.x) <= 500) and (abs(food.pos.y - self.pos.y) <= 375):
                food.pos_render = Vector2(food.pos.x - self.pos.x + 500, food.pos.y - self.pos.y + 375)
                food_sprite_to_render.add(food)
                if food not in arr_food_to_render:
                    arr_food_to_render.append(food)
            else:
                if food in arr_food_to_render:
                    arr_food_to_render.remove(food)
        return food_sprite_to_render


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
        self.offset = Vector2(self.len * math.cos(player.angle * 6.28 / 360),
                              self.len * math.sin(player.angle * 6.28 / 360))
        self.angle = 0
        self.r = 10

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
        self.rect = self.image.get_rect(center=self.pos_render + self.shift + offset_rotated)

    def angle_update(self, event):
        if event[0] != self.pos_render.x:
            self.angle = math.atan((event[1] - self.pos_render.y) / (event[0] - self.pos_render.x))
        elif event[0] == self.pos_render.x:
            self.angle = -80 * (event[1] - self.pos_render.y) / abs(event[1] - self.pos_render.y)
        self.angle = self.angle * 360 / 6.28
        if event[0] < self.pos_render.x:
            self.angle += 180

    def move(self, player):
        self.shift = self.pos - player.pos
        self.pos_render.x += self.speed * math.cos(self.angle * 6.28 / 360)
        self.pos_render.y += self.speed * math.sin(self.angle * 6.28 / 360)

    def damage_food(self, food, bullets, arr_food, arr_food_to_render, player):
        # FIXME Ваня, хитбоксы у еды при контакте с пулей круглые, ты вроде хотел сделать их по спрайту,
        #  а при соударениях друг с другом круглыми
        if (self.pos_render.x + self.shift.x - food.pos_render.x) ** 2 +\
                (self.pos_render.y + self.shift.y - food.pos_render.y) ** 2 <= (self.r + food.r) ** 2:
            self.penetration -= min(self.damage, food.HP)
            food.HP -= min(self.damage, food.HP)
            food.death(arr_food, player)
            food.death(arr_food_to_render, player)
        if self in bullets:
            self.death(bullets)

    def death(self, bullets):
        if self.penetration <= 0:
            self.kill()
            bullets.remove(self)


class Twin(Player):
    def __init__(self, player):
        super().__init__(player)
        self.pos = player.pos
        self.orig_image = pg.image.load('Sprites/twin.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.offset = Vector2(9, 1)
        self.len_gun = 35

        self.reload = 18
        self.bullet_damage = 6

        self.level = player.level
        self.XP = player.XP
        self.skill_points = player.skill_points
        self.max_HP = player.max_HP
        self.HP = player.HP

    def shoot(self, bullet_sprites, bullets):
        try:
            if self.shoot_delay % self.reload == 0:
                bullet = TwinBullet(self)
                bullets.append(bullet)
                bullet_sprites.add(bullet)
                bullet.angle_update(pg.mouse.get_pos())
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
            self.len * math.cos(player.angle * 6.28 / 360) - 12 * math.sin(player.angle * 6.28 / 360),
            self.len * math.sin(player.angle * 6.28 / 360) + 12 * math.cos(player.angle * 6.28 / 360))
        self.offset2 = Vector2(
            self.len * math.cos(player.angle * 6.28 / 360) + 12 * math.sin(player.angle * 6.28 / 360),
            self.len * math.sin(player.angle * 6.28 / 360) - 12 * math.cos(player.angle * 6.28 / 360))
        self.offset = choice([self.offset1, self.offset2])  # FIXME Сделать, чтоб по очереди стрелял из пушек


class Sniper(Player):
    def __init__(self, player):
        super().__init__(player)
        self.pos = player.pos
        self.orig_image = pg.image.load('Sprites/sniper.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.4), int(self.size[1] * 0.36)))
        self.offset = Vector2(13, 1)
        self.len_gun = 35

        self.bullet_speed = 6
        self.reload = 48

        self.level = player.level
        self.XP = player.XP
        self.skill_points = player.skill_points
        self.max_HP = player.max_HP
        self.HP = player.HP

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

        self.reload = 18
        self.bullet_damage = 6.5

        self.level = player.level
        self.XP = player.XP
        self.skill_points = player.skill_points
        self.max_HP = player.max_HP
        self.HP = player.HP

    def shoot(self, bullet_sprites, bullets):
        try:
            if self.shoot_delay % self.reload == 0:
                bullet = MachineGunBullet(self)
                bullets.append(bullet)
                bullet_sprites.add(bullet)
                bullet.angle_update(pg.mouse.get_pos())
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
        self.angle = self.angle * 360 / 6.28
        if event[0] < self.pos_render.x:
            self.angle += 180
        self.angle += randint(-20, 20)


class FlankGuard(Player):
    def __init__(self, player):
        super().__init__(player)
        self.pos = player.pos
        self.orig_image = pg.image.load('Sprites/flank_guard.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.44), int(self.size[1] * 0.36)))
        self.offset = Vector2(4, 1)
        self.len_gun = 35

        self.level = player.level
        self.XP = player.XP
        self.skill_points = player.skill_points
        self.max_HP = player.max_HP
        self.HP = player.HP

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
        self.offset = Vector2(self.len * math.cos(player.angle * 6.28 / 360),
                              self.len * math.sin(player.angle * 6.28 / 360))


class FlankGuardBulletBack(Bullet):
    def __init__(self, player):
        super().__init__(player)
        self.offset = Vector2(self.len * -math.cos(player.angle * 6.28 / 360),
                              self.len * -math.sin(player.angle * 6.28 / 360))

    def move(self, player):
        self.shift = self.pos - player.pos
        self.pos.x += self.speed * -math.cos(self.angle * 6.28 / 360)
        self.pos.y += self.speed * -math.sin(self.angle * 6.28 / 360)
        self.pos_render.x += self.speed * -math.cos(self.angle * 6.28 / 360)
        self.pos_render.y += self.speed * -math.sin(self.angle * 6.28 / 360)


class Food(pg.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        pos = (randint(50, 9500), randint(50, 9500))
        self.image = pg.Surface((122, 70), pg.SRCALPHA)
        # A reference to the original image to preserve the quality.
        self.orig_image = pg.image.load(filename)
        self.size = self.orig_image.get_size()
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.rect = self.orig_image.get_rect()
        self.pos = Vector2(pos)  # The original center position/pivot point.
        self.pos_render = Vector2(0, 0)   # Vector2(0, 0) player.pos - self.pos
        self.offset = Vector2(0, 0)  # We shift the sprite 50 px to the right.
        self.angle = randint(-180, 180)

        self.vx = randint(-10, 10) / 100
        self.vy = (0.0101 - self.vx ** 2) ** 0.5 * [-1, 1][randrange(2)]
        self.HP = 10
        self.XP = 10

    def update(self, event):
        self.move()
        self.angle += 0.35
        self.rotate()

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos_render + offset_rotated)

    def move(self):
        self.pos.x += self.vx
        self.pos.y += self.vy
        if self.pos.x >= 10000 or self.pos.x <= 0:
            self.vx *= -1
        if self.pos.y >= 10000 or self.pos.y <= 0:
            self.vy *= -1

    def death(self, arr_food, player):
        if self.HP <= 0:
            self.kill()
            arr_food.remove(self)
            player.XP += self.XP


class Square(Food):
    def __init__(self):
        filename = 'Sprites/square.png'
        super().__init__(filename)
        self.HP = 10
        self.BD = 8  # Body_damage 8 HP
        self.XP = 10  # Score
        self.r = 19


class Triangle(Food):
    def __init__(self):
        filename = 'Sprites/triangle.png'
        super().__init__(filename)
        self.HP = 30
        self.BD = 8  # Body_damage 8 HP
        self.XP = 25  # Score
        self.r = 22


class Pentagon(Food):
    def __init__(self):
        filename = 'Sprites/pentagon.png'
        super().__init__(filename)
        self.HP = 100
        self.BD = 12  # Body_damage
        self.XP = 130
        self.r = 33

    def update(self, event):
        self.move()
        self.angle += 0.15
        self.rotate()


class AlphaPentagon(Food):
    def __init__(self):
        filename = 'Sprites/alpha_pentagon.png'
        super().__init__(filename)
        self.HP = 3000
        self.BD = 20  # Body_damage
        self.XP = 3000
        self.r = 85

    def update(self, event):
        self.move()
        self.angle += 0.10
        self.rotate()


class Generator:
    def generate_player(self, type, player):
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

    def generate_food(self, arr_food):
        n_max = 1000
        variants = [0, 1, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0]
        for i in range(n_max):
            food = choice(variants)
            if food == 0:
                sq = Square()
                arr_food.append(sq)
            elif food == 1:
                tr = Triangle()
                arr_food.append(tr)
            else:
                pn = Pentagon()
                arr_food.append(pn)
        return arr_food


if __name__ == "__main__":
    print("This module is not for direct call!")
