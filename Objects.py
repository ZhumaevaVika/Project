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
        self.orig_image = pg.image.load('Sprites/Tank.png')
        self.size = self.orig_image.get_size()
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.rect = self.orig_image.get_rect()
        if player is None:
            self.pos = Vector2(500, 375)
        else:
            self.pos = Vector2(player.pos)
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
        self.m = 50
        self.impulse = 200

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

    def hit_food(self, arr_food):
        def inPolygon(x, y, tpx, tpy):
            c=0
            for i in range(len(tpx)):
                if (((tpy[i]<=y and y<tpy[i-1]) or (tpy[i-1]<=y and y<tpy[i])) and (x > (tpx[i-1] - tpx[i]) * (y - tpy[i]) / (tpy[i-1] - tpy[i]) + tpx[i])): 
                    c = 1 - c    
            if c == 1: 
                return True
        for food in arr_food:
            if inPolygon(self.pos.x, self.pos.y, food.tpx, food.tpy):
                food.HP -= min(self.BD, food.HP)
                food.death(arr_food, self)
                print(food.HP)
                print("obama")


    def if_keys(self):
        keys = pg.key.get_pressed()
        if keys:
            self.move(keys)

    def upgrade(self, event):
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

    def choose_class(self, event, player, player_sprites):
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
            if event.pos[0] != self.pos.x:
                self.angle = math.atan((event.pos[1] - self.pos.y) / (event.pos[0] - self.pos.x))
            elif event.pos[0] == self.pos.x:
                self.angle = -80 * (event.pos[1] - self.pos.y) / abs(event.pos[1] - self.pos.y)
            self.angle = self.angle * 360 / 6.28
            if event.pos[0] < self.pos.x:
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
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)

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
            self.pos.x += self.speed * x / (x ** 2 + y ** 2) ** 0.5
            self.pos.y += self.speed * y / (x ** 2 + y ** 2) ** 0.5

    def shoot(self, all_sprites, bullets):
        try:
            if self.shoot_delay % self.reload == 0:
                bullet = Bullet(self)
                bullets.append(bullet)
                all_sprites.add(bullet)
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
            self.m += 5
            print(self.speed)
            self.speed = self.impulse / self.m
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
            self.impulse += 50
            self.speed_points += 1
            self.skill_points -= 1


class Bullet(pg.sprite.Sprite):
    def __init__(self, player):
        pos = player.pos
        super().__init__()
        self.image = pg.Surface((122, 70), pg.SRCALPHA)
        # A reference to the original image to preserve the quality.
        self.orig_image = pg.image.load('Sprites/BulletM.png')
        self.size = self.orig_image.get_size()
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.20), int(self.size[1] * 0.20)))
        self.rect = self.orig_image.get_rect()
        self.pos = Vector2(pos)  # The original center position/pivot point.
        self.len = player.len_gun
        self.offset = Vector2(self.len * math.cos(player.angle * 6.28 / 360),
                              self.len * math.sin(player.angle * 6.28 / 360))
        self.angle = 0
        self.r = 10

        self.speed = player.bullet_speed  # Не точно
        self.penetration = player.bullet_penetration  # Не точно
        self.damage = player.bullet_damage  # 7 HP

    def update(self, event):
        self.rotate()
        self.move()
        self.penetration -= 0.04
        self.damage -= 0.04

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, 0.01, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(0.01)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)

    def angle_update(self, event):
        if event[0] != self.pos.x:
            self.angle = math.atan((event[1] - self.pos.y) / (event[0] - self.pos.x))
        elif event[0] == self.pos.x:
            self.angle = -80 * (event[1] - self.pos.y) / abs(event[1] - self.pos.y)
        self.angle = self.angle * 360 / 6.28
        if event[0] < self.pos.x:
            self.angle += 180

    def move(self):
        self.pos.x += self.speed * math.cos(self.angle * 6.28 / 360)
        self.pos.y += self.speed * math.sin(self.angle * 6.28 / 360)

    def damage_food(self, food, bullets, arr_food, player):
        # FIXME Ваня, хитбоксы у еды при контакте с пулей круглые, ты вроде хотел сделать их по спрайту,
        #  а при соударениях друг с другом круглыми
        def inPolygon(x, y, tpx, tpy):
            c=0
            for i in range(len(tpx)):
                if (((tpy[i]<=y and y<tpy[i-1]) or (tpy[i-1]<=y and y<tpy[i])) and (x > (tpx[i-1] - tpx[i]) * (y - tpy[i]) / (tpy[i-1] - tpy[i]) + tpx[i])): 
                    c = 1 - c    
            if c == 1: 
                return True
        if inPolygon(self.pos.x, self.pos.y, food.tpx, food.tpy):
            self.penetration -= min(self.damage, food.HP)
            food.HP -= min(self.damage, food.HP)
            food.death(arr_food, player)
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
        self.orig_image = pg.image.load('Sprites/Twin.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.offset = Vector2(9, 1)
        self.len_gun = 35

        self.reload = 18
        self.bullet_damage = 6

        self.level = player.level
        self.XP = player.XP
        self.skill_points = player.skill_points

    def shoot(self, all_sprites, bullets):
        try:
            if self.shoot_delay % self.reload == 0:
                bullet = TwinBullet(self)
                bullets.append(bullet)
                all_sprites.add(bullet)
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
        self.orig_image = pg.image.load('Sprites/Sniper.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.4), int(self.size[1] * 0.36)))
        self.offset = Vector2(13, 1)
        self.len_gun = 35

        self.bullet_speed = 6
        self.reload = 48

        self.level = player.level
        self.XP = player.XP
        self.skill_points = player.skill_points

    def bullet_speed_up(self):
        if (self.bullet_speed_points < 7) and (self.skill_points > 0):
            self.bullet_speed += 0.65
            self.bullet_speed_points += 1
            self.skill_points -= 1


class MachineGun(Player):
    def __init__(self, player):
        super().__init__(player)
        self.pos = player.pos
        self.orig_image = pg.image.load('Sprites/MachineGun.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.offset = Vector2(9, 1)
        self.len_gun = 35

        self.reload = 18
        self.bullet_damage = 6.5

        self.level = player.level
        self.XP = player.XP
        self.skill_points = player.skill_points

    def shoot(self, all_sprites, bullets):
        try:
            if self.shoot_delay % self.reload == 0:
                bullet = MachineGunBullet(self)
                bullets.append(bullet)
                all_sprites.add(bullet)
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
        if event[0] != self.pos.x:
            self.angle = math.atan((event[1] - self.pos.y) / (event[0] - self.pos.x))
        elif event[0] == self.pos.x:
            self.angle = -80 * (event[1] - self.pos.y) / abs(event[1] - self.pos.y)
        self.angle = self.angle * 360 / 6.28
        if event[0] < self.pos.x:
            self.angle += 180
        self.angle += randint(-20, 20)


class FlankGuard(Player):
    def __init__(self, player):
        super().__init__(player)
        self.pos = player.pos
        self.orig_image = pg.image.load('Sprites/FlankGuard.png')
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.44), int(self.size[1] * 0.36)))
        self.offset = Vector2(4, 1)
        self.len_gun = 35

        self.level = player.level
        self.XP = player.XP
        self.skill_points = player.skill_points

    def shoot(self, all_sprites, bullets):
        try:
            if self.shoot_delay % self.reload == 0:
                bullet_front = FlankGuardBulletFront(self)
                bullets.append(bullet_front)
                all_sprites.add(bullet_front)
                bullet_front.angle_update(pg.mouse.get_pos())

                bullet_back = FlankGuardBulletBack(self)
                bullets.append(bullet_back)
                all_sprites.add(bullet_back)
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

    def move(self):
        self.pos.x += self.speed * -math.cos(self.angle * 6.28 / 360)
        self.pos.y += self.speed * -math.sin(self.angle * 6.28 / 360)


class Food(pg.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.screen = pg.display.set_mode((1000, 750))
        pos = (randint(50, 950), randint(50, 700))
        self.image = pg.Surface((122, 70), pg.SRCALPHA)
        # A reference to the original image to preserve the quality.
        self.orig_image = pg.image.load(filename)
        self.size = self.orig_image.get_size()
        self.orig_image = pg.transform.scale(self.orig_image, (int(self.size[0] * 0.36), int(self.size[1] * 0.36)))
        self.rect = self.orig_image.get_rect()
        self.pos = Vector2(pos)  # The original center position/pivot point.
        self.offset = Vector2(0, 0)  # We shift the sprite 50 px to the right.
        self.angle = randint(-180, 180)
        self.a = 30

        self.vx = randint(-10, 10) / 100
        self.vy = (0.0101 - self.vx ** 2) ** 0.5 * [-1, 1][randrange(2)]
        self.HP = 10
        self.XP = 10

    def update(self, event):
        self.angle += 0.35
        self.rotate()
        self.move()


    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)


    def move(self):
        self.pos.x += self.vx
        self.pos.y += self.vy

    def death(self, arr_food, player):
        if self.HP <= 0:
            self.kill()
            arr_food.remove(self)
            player.XP += self.XP

    def hit(self, arr_food, player):
        pass


class Square(Food):
    def __init__(self):
        filename = 'Sprites/Square.png'
        super().__init__(filename)
        self.HP = 10
        self.BD = 8  # Body_damage 8 HP
        self.XP = 10  # Score
        self.r = 19
        self.a = 26 + 10
        self.tpx = []
        self.tpy = []

    def update(self, event):
        self.angle += 0.35
        self.rotate()
        self.move()       
        angle = self.angle * math.pi / 180 + 0.8
        x = self.pos.x
        y = self.pos.y
        self.tpx = [x + self.a * math.cos(angle), 
                    x + self.a * math.cos(angle + 1 * 2*math.pi/4),
                    x + self.a * math.cos(angle + 2 * 2*math.pi/4),
                    x + self.a * math.cos(angle + 3 * 2*math.pi/4)
                    ]
        self.tpy = [y + self.a * math.sin(angle),
                    y + self.a * math.sin(angle + 1 * 2*math.pi/4),
                    y + self.a * math.sin(angle + 2 * 2*math.pi/4),
                    y + self.a * math.sin(angle + 3 * 2*math.pi/4)
                    ]


class Triangle(Food):
    def __init__(self):
        filename = 'Sprites/Triangle.png'
        super().__init__(filename)
        self.HP = 30
        self.BD = 8  # Body_damage 8 HP
        self.XP = 25  # Score
        self.r = 22
        self.a = 22 + 10
        self.tpx = []
        self.tpy = []
        
    def update(self, event):
        self.angle += 0.35
        self.rotate()
        self.move()
        angle = self.angle * math.pi / 180 + 0.5
        x = self.pos.x
        y = self.pos.y
        self.tpx = [x +self.a * math.cos(angle),
                    x +self.a * math.cos(angle + 1 * 2*math.pi/3),
                    x +self.a * math.cos(angle + 2 * 2*math.pi/3)
                    ]
        self.tpy = [y + self.a * math.sin(angle), 
                    y + self.a * math.sin(angle + 1 * 2*math.pi/3), 
                    y + self.a * math.sin(angle + 2 * 2*math.pi/3)
                    ]


class Pentagon(Food):
    def __init__(self):
        filename = 'Sprites/Pentagon.png'
        super().__init__(filename)
        self.HP = 100
        self.BD = 12  # Body_damage
        self.XP = 130
        self.r = 33
        self.a = 33 + 10
        self.tpx = []
        self.tpy = []

    def update(self, event):
        self.angle += 0.15
        self.rotate()
        self.move()
        angle = self.angle * math.pi / 180 - 0.32
        x = self.pos.x
        y = self.pos.y
        self.tpx = [x + self.a * math.cos(angle),
                    x + self.a * math.cos(angle + 1 * 2*math.pi/5),
                    x + self.a * math.cos(angle + 2 * 2*math.pi/5),
                    x + self.a * math.cos(angle + 3 * 2*math.pi/5),
                    x + self.a * math.cos(angle + 4 * 2*math.pi/5)
                    ]
        self.tpy = [y + self.a * math.sin(angle),
                    y + self.a * math.sin(angle + 1 * 2*math.pi/5),
                    y + self.a * math.sin(angle + 2 * 2*math.pi/5),
                    y + self.a * math.sin(angle + 3 * 2*math.pi/5),
                    y + self.a * math.sin(angle + 4 * 2*math.pi/5)
                    ]


class AlphaPentagon(Food):
    def __init__(self):
        filename = 'Sprites/AlphaPentagon.png'
        super().__init__(filename)
        self.HP = 3000
        self.BD = 20  # Body_damage
        self.XP = 3000
        self.r = 85
        self.a = 85 + 10
        self.tpx = []
        self.tpy = []

    def update(self, event):
        self.angle += 0.10
        self.rotate()
        self.move()       
        angle = self.angle * math.pi / 180 - 0.32
        x = self.pos.x
        y = self.pos.y
        self.tpx = [x + self.a * math.cos(angle),
                    x + self.a * math.cos(angle + 1 * 2*math.pi/5),
                    x + self.a * math.cos(angle + 2 * 2*math.pi/5),
                    x + self.a * math.cos(angle + 3 * 2*math.pi/5),
                    x + self.a * math.cos(angle + 4 * 2*math.pi/5)
                    ]
        self.tpy = [y + self.a * math.sin(angle),
                    y + self.a * math.sin(angle + 1 * 2*math.pi/5),
                    y + self.a * math.sin(angle + 2 * 2*math.pi/5),
                    y + self.a * math.sin(angle + 3 * 2*math.pi/5),
                    y + self.a * math.sin(angle + 4 * 2*math.pi/5)
                    ]


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

    def generate_food(self, all_sprites, arr_food):
        n_max = 12
        variants = [0, 1, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0]
        for i in range(n_max):
            food = choice(variants)
            if food == 0:
                sq = Square()
                arr_food.append(sq)
                all_sprites.add(sq)
            elif food == 1:
                tr = Triangle()
                arr_food.append(tr)
                all_sprites.add(tr)
            else:
                pn = Pentagon()
                arr_food.append(pn)
                all_sprites.add(pn)
        return all_sprites, arr_food


if __name__ == "__main__":
    print("This module is not for direct call!")
