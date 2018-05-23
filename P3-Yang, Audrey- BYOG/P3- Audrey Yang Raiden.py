import pygame, os, sys, time, random, math

os.environ['SDL_VIDEO_CENTERED'] = "1"
#`pygame.mixer.pre_init(44100,-16,2,2048)

#Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 53)
BLUE = (35, 185, 255)
YELLOW = (255, 232, 89)
GREEN = (154,205,50)
ORANGE = (255, 165, 0)
PURPLE = (153, 50, 204)
SKY = (193, 235, 249)
DAWN = (255, 210, 222)
NIGHT = (16, 18, 29)
FILL = WHITE

WIDTH = 22 * 32
HEIGHT = 33 * 32

SHIPW = WIDTH/10
SHIPH = HEIGHT/10

TIMER = 0
COUNT = 0
SCORE = 0

LEVEL = 1

intro = True
win = False
lose = False
play = False
next = False
htp = False

#Classes

def Load(name, x, y):
    image = pygame.image.load(name).convert_alpha()
    image = pygame.transform.scale(image, (x, y))
    return image

class Background(pygame.sprite.Sprite):
    def __init__(self,pic):
        self.images = []
        self.images.append(Load(pic, WIDTH, HEIGHT))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(0,0,  WIDTH, HEIGHT)
        self.time = 0
    def update(self):
        self.time += 1
        if self.time % 3 == 0:
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.index = 0
        self.images = []
        pygame.sprite.Sprite.__init__(self)
        #.image = pygame.Surface ((210, 150)).convert()
        #self.image = pygame.image.load("images/clouds2.gif").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (210, 150))
        #self.rect = pygame.Rect(x, y, 420, 300)
        if LEVEL == 1:
            self.images = []
            self.images.append(Load('images/clouds1a.png', 336, 240))
            self.images.append(Load('images/clouds2a.png', 336, 240))
            self.images.append(Load('images/clouds3a.png', 336, 240))
            self.images.append(Load('images/clouds4a.png', 336, 240))
            self.index = 0
            self.image = self.images[self.index]
            self.rect = pygame.Rect(x, y, 336, 240)
        if LEVEL == 2:
            self.images = []
            self.images.append(Load('images/clouds1.png', 336, 240))
            self.images.append(Load('images/clouds2.png', 336, 240))
            self.images.append(Load('images/clouds3.png', 336, 240))
            self.images.append(Load('images/clouds4.png', 336, 240))
            self.index = 0
            self.image = self.images[self.index]
            self.rect = pygame.Rect(x, y, 336, 240)
        if LEVEL == 3:
            self.images = []
            self.images.append(Load('images/clouds1c.png', 672, 480))
            self.images.append(Load('images/clouds2c.png', 672, 480))
            self.images.append(Load('images/clouds3c.png', 672, 480))
            self.images.append(Load('images/clouds4c.png', 672, 480))
            self.index = 0
            self.image = self.images[self.index]
            self.rect = pygame.Rect(x, y, 672, 480)

    def update(self):
        '''This method iterates through the elements inside self.images and
        displays the next one each tick. For a slower animation, you may want to
        consider using a timer of some sort so it updates slower.'''
        if TIMER % 5 == 0:
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

'''
class Lives(pygame.sprite.Sprite):
    def __init__(self, container, ship, x, group):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.ship = ship
        self.x = 20
        self.hp = ship.hp
        self.group = group
        self.image = pygame.Surface((20, 20)).convert()
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = container.right + x
        self.rect.top = container.top + 10

    def update(self, lives_group):
        self.x += 20
        for l in (0, self.hp):
            life = Lives(self.container, self.ship, self.x, self.group)
            self.group.add(life)
'''

class Ship(pygame.sprite.Sprite):
    def __init__(self, container):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.side_speed = 6
        self.top_speed = 6
        self.hp = 15
        self.pwr_count = 0
        self.image = pygame.Surface((58, 51)).convert()
        #self.image = Load("images/ship.png", 58, 51)
        self.images = []
        self.images.append(Load('images/ship1.png', 81, 51))
        self.images.append(Load('images/ship2.png', 81, 51))
        self.images.append(Load('images/ship3.png', 81, 51))
        self.index = 0
        self.image = self.images[self.index]
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = container.centerx
        self.rect.bottom = container.bottom - self.rect.height * 3
        if self.rect.bottom >= container.bottom - self.rect.height:
            self.rect.top = container.bottom - self.rect.height
        if self.rect.top <= self.rect.height:
            self.rect.top = self.rect.height

    def update(self,cam_ent, camera, container, bullet_group, enemy_bullet_group, powerup_group, hpup_group, enemy_group):
        global TIMER, COUNT, SCORE
        key = pygame.key.get_pressed()
        #target = random.choice(enemy_group.sprites())
        #target = (enemy_group.get_top_sprite())

        if TIMER % 4 == 0:
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

        if (cam_ent.is_moving == True) or (self.rect.bottom < self.container.bottom - self.rect.height * 3):
            if key[pygame.K_w]:
                self.rect.y -= self.top_speed
            if key[pygame.K_s]:
                self.rect.y += self.top_speed
            if key[pygame.K_a]:
                self.rect.x -= self.side_speed
            if key[pygame.K_d]:
                self.rect.x += self.side_speed

            if TIMER % 10 == 0: #and COUNT < 10:
                if key[pygame.K_SPACE]:
                    bullet_l = Bullet()
                    bullet_r = Bullet()
                    bullet_l.set_pos(self, "left", "ship", None)
                    bullet_r.set_pos(self, "right", "ship", None)
                    bullet_group.add(bullet_l, bullet_r)
                    if self.pwr_count >= 1:
                        bullet_c = Bullet()
                        bullet_c.set_pos(self, "center", "ship", None)
                        bullet_group.add(bullet_c)
                    if self.pwr_count >= 2:
                        bullet_l2 = Bullet()
                        bullet_l2.set_pos(self,"left2", "ship", None)
                        bullet_group.add(bullet_l2)
                    if self.pwr_count >= 3:
                        bullet_r2 = Bullet()
                        bullet_r2.set_pos(self, "right2", "ship", None)
                        bullet_group.add(bullet_r2)

                    COUNT += 1

            #print (self.rect.top, camera.y_offset)
            # Stop at bottom
            if self.rect.bottom > HEIGHT - camera.y_offset:
                self.rect.bottom = HEIGHT - camera.y_offset
            # Stop at top
            if self.rect.top < -camera.y_offset:
                self.rect.top = -camera.y_offset
            # Stop at right
            if self.rect.right > WIDTH - camera.x_offset:
                self.rect.right = WIDTH - camera.x_offset
            # Stop at left
            if self.rect.left < -camera.x_offset:
                self.rect.left = -camera.x_offset

            pwrup = pygame.sprite.spritecollide(self, powerup_group, True)
            for p in pwrup:
                pygame.mixer.Sound("sound/up.ogg").play(0)
                self.pwr_count += 1
                SCORE += 25
            hpup = pygame.sprite.spritecollide(self, hpup_group, True)
            for h in hpup:
                pygame.mixer.Sound("sound/hp.ogg").play(0)
                self.hp += 1
                SCORE += 50

            collisions = pygame.sprite.spritecollide(self, enemy_bullet_group, True)
            for b in collisions:
                self.hp -= 1
                pygame.mixer.Sound("sound/hit.ogg").play(0)
            if self.hp <= 0:
                self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,5)).convert()
        self.image = Load("images/bullet_ora.png", 12,12)
        self.rect = self.image.get_rect()
        self.side = None
        self.type = None
        self.speed = 12

    def set_pos(self, ship, side, type, target):
        if side == "right":
            self.side = "right"
            self.rect.centerx = ship.rect.centerx - self.rect.height * 2
            self.side_speed = 3
            self.speed = 12
        if side == "left":
            self.side = "left"
            self.rect.centerx = ship.rect.centerx + self.rect.height * 2
            self.side_speed = 3
            self.speed = 12
        if side == "center":
            self.side = "center"
            self.rect.centerx = ship.rect.centerx
            self.speed = 12
            self.side_speed = 0
        if side == "right2":
            self.side = "right2"
            self.rect.centerx = ship.rect.centerx - self.rect.height * 3
            self.side_speed = 6
            self.speed = 12
        if side == "left2":
            self.side = "left2"
            self.rect.centerx = ship.rect.centerx + self.rect.height * 3
            self.side_speed = 6
            self.speed = 12
        if side == "homing":
            self.side = "homing"
            self.rect.centerx = ship.rect.centerx
            x1 = self.rect.x
            y1 = self.rect.y
            x2 = target.rect.x
            y2 = target.rect.y
            x = math.fabs(x2-x1)
            y = math.fabs(y2-y1)
            self.speed = math.sqrt(y)/2.5
            self.side_speed = math.sqrt(x)/2.5

        if type == "ship":
            self.rect.bottom = ship.rect.top + self.rect.height * 3
            self.image = Load("images/bullet_red.png", 12,12)
        if type == "huey":
            self.rect.top = ship.rect.bottom
        if type == "heli":
            self.rect.top = ship.rect.bottom
            self.image = Load("images/bullet_pur.png", 12, 12)

    def update(self, h, ship):
        global COUNT
        if h == ship == None:
            self.rect.y -= self.speed
            if self.side == "left":
                self.rect.x -= self.side_speed
            if self.side == "right":
                self.rect.x += self.side_speed
            if self.rect.y <= 0:
                self.kill()
                COUNT -= 1
        if h == "h":
            self.rect.y += self.speed
            if self.side == "left" or self.side == "left2":
                self.rect.x += self.side_speed
            if self.side == "right" or self.side == "right2":
                self.rect.x -= self.side_speed
            if self.side == "homing":
                if ship.rect.x <= self.rect.x:
                    self.rect.x -= self.side_speed
                if ship.rect.x >= self.rect.x:
                    self.rect.x += self.side_speed
            if self.rect.y >= HEIGHT * 2.5:
                self.kill()

class Powerup(pygame.sprite.Sprite):
    def __init__(self, container):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.image = pygame.Surface((38, 29)).convert()
        self.images = []
        self.images.append(Load('images/powerup1.png', 38, 29))
        self.images.append(Load('images/powerup2.png', 38, 29))
        self.images.append(Load('images/powerup3.png', 38, 29))
        self.index = 0
        self.image = self.images[self.index]
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = container.centerx + random.randrange(-432, 433)
        self.rect.top = container.top + 500
        if TIMER > 1000:
            self.rect.top = container.top
    def update(self, ship):
        self.rect.y += 3
        if TIMER % 2 == 0:
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        if self.rect.y >= HEIGHT * 2:
            self.kill()
            

class Hpup(pygame.sprite.Sprite):
    def __init__(self, container):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.image = pygame.Surface((38, 29)).convert()
        self.images = []
        self.images.append(Load('images/hpup1.png', 38, 29))
        self.images.append(Load('images/hpup2.png', 38, 29))
        self.images.append(Load('images/hpup3.png', 38, 29))
        self.index = 0
        self.image = self.images[self.index]
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = container.centerx + random.randrange(-432, 433)
        self.rect.top = container.top + 500
        if TIMER > 1000:
            self.rect.top = container.top
    def update(self, ship):
        self.rect.y += 3
        if TIMER % 2 == 0:
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        if self.rect.y >= HEIGHT * 2:
            self.kill()

class Huey(pygame.sprite.Sprite):
    def __init__(self, container):
        global TIMER
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.side_speed = 3
        self.top_speed = 6
        if LEVEL == 1:
            self.hp = 6
        if LEVEL == 2:
            self.hp = 7
        if LEVEL == 3:
            self.hp = 8
        self.path = random.randrange(0,2)
        self.time = -20 + TIMER/2
        self.image = pygame.Surface((89, 54)).convert()
        #self.image = Load("images/huey.png", SHIPW, SHIPH)
        self.images = []
        self.images.append(Load('images/huey1.png', 89, 54))
        self.images.append(Load('images/huey2.png', 89, 54))
        self.images.append(Load('images/huey3.png', 89, 54))
        self.index = 0
        self.image = self.images[self.index]
        #self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.centerx = container.centerx
        self.rect.top = container.top + 700
        if TIMER > 1000:
            self.rect.top = container.top
        if self.rect.bottom >= container.bottom - self.rect.height:
            self.rect.top = container.bottom - self.rect.height
        if self.rect.top <= self.rect.height:
            self.rect.top = self.rect.height

    def update(self, ship_bullet_group, enemy_bullet_group, huey_group, container, camera):
        global SCORE
        self.time += 1
        if TIMER % 4 == 0:
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

        if self.path == 0:
            if self.time <= 100 and self.rect.x > WIDTH/2:
                self.rect.y += self.top_speed
            if 100 < self.time <= random.randrange(250,300) and self.rect.left > container.left + 50:
                self.top_speed = 2
                self.rect.y += self.top_speed
                self.rect.x -= self.side_speed
                if self.rect.left < container.left + 50:
                    self.time = 300
            if 300 < self.time <= random.randrange(400,500) and self.rect.right < container.right - 50:
                self.rect.y += self.top_speed
                self.rect.x += self.side_speed
                if  self.rect.right > container.right - 50:
                    self.time = 500
            if 500 < self.time <= random.randrange(600,800) and self.rect.left > container.left + 50:
                self.rect.y += self.top_speed
                self.rect.x -= self.side_speed
                if self.rect.left < container.left + 50:
                    self.time = 800
            if 800 < self.time:
                self.rect.y += self.top_speed
                self.rect.x += self.side_speed
        if self.path == 1:
            if self.time <= 100:
                self.rect.y += self.top_speed
            if 100 < self.time <= random.randrange(250,300) and self.rect.right < container.right - 50:
                self.top_speed = 2
                self.rect.y += self.top_speed
                self.rect.x += self.side_speed
                if self.rect.right > container.right - 50:
                    self.time = 300
            if 300 < self.time <= random.randrange(400,500) and self.rect.left > container.left + 50:
                self.rect.y += self.top_speed
                self.rect.x -= self.side_speed
                if self.rect.left < container.left + 50:
                    self.time = 500
            if 500 < self.time <= random.randrange(600,800) and self.rect.right < container.right - 50:
                self.rect.y += self.top_speed
                self.rect.x += self.side_speed
                if self.rect.right > container.right - 50:
                    self.time = 800
            if 800 < self.time:
                self.rect.y += self.top_speed
                self.rect.x -= self.side_speed
        if self.rect.bottom > container.top - camera.y_offset:
            if self.time % 40 == 0 and self.time > 0:
                bullet_l = Bullet()
                bullet_c = Bullet()
                bullet_r = Bullet()
                bullet_l.set_pos(self, "left", "huey", None)
                bullet_c.set_pos(self, "center", "huey", None)
                bullet_r.set_pos(self, "right", "huey", None)
                enemy_bullet_group.add(bullet_l, bullet_c, bullet_r)
            collisions = pygame.sprite.spritecollide (self, ship_bullet_group, True)
            for b in collisions:
                self.hp -= 1
                SCORE += 5

        if self.rect.y >= HEIGHT*2.5:
            self.kill()
        if self.hp <= 0:
            pygame.mixer.Sound("sound/score.ogg").play(0)
            self.kill()
            SCORE += 75

class Helicopter(pygame.sprite.Sprite):
    def __init__(self, container):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.side_speed = 6
        self.top_speed = 40
        if LEVEL == 1:
            self.hp = 4
        if LEVEL == 2:
            self.hp = 5
        if LEVEL == 3:
            self.hp = 6
        self.time = -100
        self.path = random.randrange(0,2)
        self.image = pygame.Surface((84, 50)).convert()
        #self.image = Load("images/heli.png", SHIPH, SHIPH)
        self.images = []
        self.images.append(Load('images/heli1.png', 84, 50))
        self.images.append(Load('images/heli2.png', 84, 50))
        self.images.append(Load('images/heli3.png', 84, 50))
        self.index = 0
        self.image = self.images[self.index]
        #self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.centerx = container.centerx
        self.rect.top = container.top
        if self.rect.bottom >= container.bottom - self.rect.height:
            self.rect.top = container.bottom - self.rect.height
        if self.rect.top <= self.rect.height:
            self.rect.top = self.rect.height
    def update(self, container, ship_bullet_group, enemy_bullet_group, ship, camera):
        global SCORE
        self.time += 1
        if TIMER % 2 == 0:
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

        if self.path == 0:
            if self.time <= 200:
                self.top_speed = 2
                self.rect.y += self.top_speed
            if 200 < self.time <= random.randrange(350, 450) and self.rect.right < container.right - 50:
                self.rect.y += self.top_speed
                self.rect.x += self.side_speed
                if self.rect.right > container.right - 50:
                    self.time = 450
            if 450 < self.time <= random.randrange(550,650) and self.rect.left > container.left + 50:
                self.rect.y -= self.top_speed
                self.rect.x -= self.side_speed
                if self.rect.left < container.left + 50:
                    self.time = 650
            if 650 < self.time <= random.randrange(750,850) and self.rect.right < container.right - 50:
                self.rect.y += self.top_speed
                self.rect.x += self.side_speed
                if self.rect.right > container.right - 50:
                    self.time = 850
            if 850 < self.time:
                self.rect.y -= self.top_speed
                self.rect.x -= self.side_speed
        if self.path == 1:
            if self.time <= 200:
                self.top_speed = 2
                self.rect.y += self.top_speed
            if 200 < self.time <= random.randrange(400,500) and self.rect.left > container.left + 50:
                self.top_speed = 2
                self.rect.y += self.top_speed
                self.rect.x -= self.side_speed
                if self.rect.left < container.left + 50:
                    self.time = 500
            if 500 < self.time <= random.randrange(600,700) and self.rect.right < container.right - 50:
                self.rect.y -= self.top_speed
                self.rect.x += self.side_speed
                if self.rect.right > container.right - 50:
                    self.time = 700
            if 700 < self.time <= random.randrange(800,950) and self.rect.left > container.left + 50:
                self.rect.y -= self.top_speed
                self.rect.x -= self.side_speed
                if self.rect.left < container.left + 50:
                    self.time = 950
            if 950 < self.time:
                self.rect.y -= self.top_speed
                self.rect.x += self.side_speed
        if self.rect.bottom > container.top - camera.y_offset:
            if self.time % 180 == 0 and self.time > 0:
                bullet_c = Bullet()
                bullet_c.set_pos(self, "homing", "heli", ship)
                enemy_bullet_group.add(bullet_c)
            collisions = pygame.sprite.spritecollide(self, ship_bullet_group, True)
            for b in collisions:
                self.hp -= 1
                SCORE += 5


        if self.rect.y >= HEIGHT*2:
            self.kill()
        if self.hp <= 0:
            pygame.mixer.Sound("sound/score.ogg").play(0)
            self.kill()
            SCORE += 100

class Boss(pygame.sprite.Sprite):
    def __init__ (self, container):
        global LEVEL
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.side_speed = 1
        self.top_speed = .25
        if LEVEL == 1:
            self.hp = 20
        if LEVEL == 2:
            self.hp = 30
        if LEVEL == 3:
            self.hp = 40
        self.time = 0
        self.image = pygame.Surface((102, 67)).convert()
        self.images = []
        self.images.append(Load('images/boss1.png', 102, 67))
        self.images.append(Load('images/boss2.png', 102, 67))
        self.images.append(Load('images/boss3.png', 102, 67))
        self.index = 0
        self.image = self.images[self.index]
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = container.centerx
        self.rect.top = container.top + 50
        if self.rect.bottom >= container.bottom - self.rect.height:
            self.rect.top = container.bottom - self.rect.height
        if self.rect.top <= self.rect.height:
            self.rect.top = self.rect.height
    def update(self, ship_bullet_group, enemy_bullet_group, ship, container):
        global SCORE, LEVEL
        if TIMER % 4 == 0:
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        if self.hp >= 0:
            self.time += 1
            print(self.time)
            if self.time <= random.randrange(50,350) and self.rect.right < container.right - 50:
                self.rect.x += self.side_speed
                self.rect.y += self.top_speed
                if self.rect.right > container.right - 50:
                    self.time = 350
            if 350 < self.time <= random.randrange(500,650) and self.rect.left > container.left + 50:
                self.rect.x -= self.side_speed
                if self.rect.left < container.left + 50:
                    self.time = 650
            if 650 < self.time <= random.randrange(800,950) and self.rect.right < container.right - 50:
                self.rect.x += self.side_speed
                self.rect.y -= self.top_speed
                if self.rect.right > container.right - 50:
                    self.time = 950
            if 950 < self.time <= random.randrange(950,1100) and self.rect.right < container.right - 50:
                self.rect.x += self.side_speed
                self.rect.y -= self.top_speed
                if self.rect.right > container.right - 50:
                    self.time = 1100
            if 1100 < self.time and self.rect.left > container.left + 50:
                self.rect.x -= self.side_speed
            if 1100 < self.time and self.rect.right < container.right - 50:
                self.rect.x += self.side_speed
            if self.time > 1250:
                self.time = 0

        if self.hp > 50:
            if TIMER % 30 == 0 and TIMER > 0:
                bullet_l = Bullet()
                bullet_c = Bullet()
                bullet_r = Bullet()
                bullet_l.set_pos(self, "left", "huey", None)
                bullet_c.set_pos(self, "center", "huey", None)
                bullet_r.set_pos(self, "right", "huey", None)
                enemy_bullet_group.add(bullet_l, bullet_c, bullet_r)
            if TIMER % 60 == 0 and TIMER > 0:
                bullet_c1 = Bullet()
                bullet_c2 = Bullet()
                bullet_c1.set_pos(self, "homing", "heli", ship)
                bullet_c2.set_pos(self, "homing", "heli", ship)
                enemy_bullet_group.add(bullet_c1, bullet_c2)
        if self.hp < 50:
            if TIMER % 20 == 0 and TIMER > 0:
                bullet_l = Bullet()
                bullet_c = Bullet()
                bullet_r = Bullet()
                bullet_l.set_pos(self, "left", "huey", None)
                bullet_c.set_pos(self, "center", "huey", None)
                bullet_r.set_pos(self, "right", "huey", None)
                enemy_bullet_group.add(bullet_l, bullet_c, bullet_r)
            if TIMER % 50 == 0 and TIMER > 0:
                bullet_c1 = Bullet()
                bullet_c2 = Bullet()
                bullet_c1.set_pos(self, "homing", "heli", ship)
                bullet_c2.set_pos(self, "homing", "heli", ship)
                enemy_bullet_group.add(bullet_c1, bullet_c2)
        collisions = pygame.sprite.spritecollide (self, ship_bullet_group, True)
        for b in collisions:
            self.hp -= 1
            print (self.hp)
            print b
        if self.rect.y >= HEIGHT*2:
            pygame.mixer.Sound("sound/score.ogg").play(0)
            self.kill()
        if self.hp <= 0:
            self.kill()
            SCORE += 500
            ship.hp = 10
            pygame.mixer.music.fadeout(100)

class Respawn:
    def __init__(self, container):
        global TIMER
        self.time = 0
        self.boss = Boss(container)
    def update(self, ship, container, cament, pwr, hu, he, bg, hp):
        global TIMER
        if cament.is_moving:
            if TIMER % 450 == 0 and TIMER > 0:
                hpup = Hpup(container)
                hp.add(hpup)
                print("hp")
            if TIMER % 300 == 0 and TIMER > 0:
                pwrup = Powerup(container)
                pwr.add(pwrup)
                print("new")
            if TIMER % 180 == 0 and TIMER > 0:
                huey = Huey(container)
                hu.add(huey)
                print("huey")
            if TIMER % 250 == 0 and TIMER > 0:
                heli = Helicopter(container)
                he.add(heli)
                print("heli")
        if not cament.is_moving and TIMER > 100 and self.time == 0:
            self.time = TIMER
            bg.add(self.boss)
            for h in (0,2):
                huey = Huey(container)
                hu.add(huey)
                heli = Helicopter(container)
                he.add(heli)

class Camera:
    def __init__(self, width, height):
        self.x_offset = 0
        self.y_offset = 0
        self.width = width
        self.height = height

    def apply(self,obj):
        return pygame.Rect(obj.rect.x + self.x_offset, obj.rect.y + self.y_offset, obj.rect.width, obj.rect.height)

    def update(self, ship, camera_entity):
        self.x_offset = -ship.rect.x + WIDTH / 2
        self.y_offset = -camera_entity.rect.y + HEIGHT / 2

        # Stop scrolling at left edge
        if self.x_offset > 0:
            self.x_offset = 0
        # Stop scrolling at the right edge
        elif self.x_offset < -(self.width - WIDTH):
            self.x_offset = -(self.width - WIDTH)
        # Stop scrolling at top
        if self.y_offset > 0:
            self.y_offset = 0
        # Stop scrolling at the bottom
        elif self.y_offset < -(self.height - HEIGHT):
            self.y_offset = -(self.height - HEIGHT)

class Camera_Entity(pygame.sprite.Sprite):
    def __init__(self, container):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.image = pygame.Surface((10, 10)).convert()
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = container.centerx
        self.rect.y = container.bottom - HEIGHT/2.2
        self.is_moving = False
        
    def update(self,camera):
        self.rect.y -= 1

        if self.rect. y <= self.container.bottom - HEIGHT/2:
            self.is_moving = True
        if self.rect.y <= HEIGHT/2:
            self.is_moving = False

class Text(pygame.sprite.Sprite):
    def __init__(self,container, size, color, xpos, font, type):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.type = type
        self.color = color
        self.xpos = xpos
        self.font = pygame.font.Font(font, size)

    def update(self):
        self.image = self.font.render(self.type)
        self.rect = self.image.get_rect()
        self.rect = self.container.centerx

class Lives(pygame.sprite.Sprite):
    def __init__(self,container, ship):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.color = RED
        self.font = pygame.font.Font("DK Nanuk.otf", 40)
    def update(self, ship, cament):
        self.image = self.font.render(str("HP: " + str(ship.hp)) + "     SCORE: " + str(SCORE), 1, self.color)
        self.rect = self.image.get_rect()
        self.hold = 0
        if not cament.is_moving and TIMER < 100:
            self.rect = self.rect.move(self.container.centerx - 190, self.container.bottom - HEIGHT * .99)
        if cament.is_moving:
            self.rect = self.rect.move(self.container.centerx - 190, self.container.bottom - HEIGHT * .99 + 47 - TIMER)
            self.hold = TIMER
        if not cament.is_moving and TIMER > 100:
            self.rect = self.rect.move(self.container.centerx - 190, self.container.top + 10)

def main():

    #Initialize variables
    global TIMER, SCORE, LEVEL, FILL, intro, win, lose, play, next, htp
    pygame.init()
    fps = 30
    clock = pygame.time.Clock()
    play = True
    lose = win = False
    pygame.display.set_caption('Raiden!')
    screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.SRCALPHA)

    # Load Level
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P  C                       P",
        "P                          P",
        "P                      PPPPP",
        "P                          P",
        "PPPPPPPP             C     P",
        "P                          P",
        "P                          P",
        "C                          P",
        "P                      PPPPP",
        "P                          P",
        "PPPP                    C  P",
        "P                          P",
        "P   C                  PPPPP",
        "PPPPP                      P",
        "P                          P",
        "P                          P",
        "P          C         PPPPPPP",
        "P                          P",
        "PPPPPP                     P",
        "P                          P",
        "P                          P",
        "PPPP                       P",
        "P                          P",
        "PC                      PPPC",
        "PPPPP                      P",
        "P                          P",
        "P                          P",
        "P            C       PPPPPPP",
        "P                          P",
        "PPPPPP                     P",
        "P                          C",
        "P                          P",
        "P                          P",
        "P                      PPPPP",
        "P                          P",
        "PPPPPPPP                   P",
        "P                          P",
        "P                          P",
        "PC                         P",
        "P                      PPPPP",
        "P                          P",
        "PPPP              C        P",
        "P                          P",
        "P                       PPPP",
        "PPPPPP                     P",
        "P                          P",
        "C                          P",
        "P                    PPPPPPP",
        "P                          P",
        "PPPPPP                     P",
        "P                          C",
        "P                          P",
        "PPPP   C                   P",
        "P                          P",
        "P                       PPPP",
        "P                          P",
        "P                          P",
        "PC                         P",
        "P                      PPPPP",
        "P                          P",
        "PPPP              C        P",
        "P                          P",
        "P                       PPPP",
        "PPPPPP                     P",
        "P                          P",
        "C                          P",
        "P                    PPPPPPP",
        "P                          P",
        "PPPPPP                     P",
        "P                          C",
        "P                          P",
        "PPPP   C                   P",
        "P                          P",
        "P                       PPPP",
        "PPPPP                      P",
        "P                          C",
        "P                          P",
        "P                    PPPPPPP",
        "P                          C",
        "PPPPPP                     P",
        "P             C            P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP", ]

    # Create Groups
    platform_group = pygame.sprite.Group()
    ship_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    enemy_bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.LayeredUpdates()
    huey_group = pygame.sprite.Group()
    heli_group = pygame.sprite.Group()
    pwrup_group = pygame.sprite.Group()
    hpup_group = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()
    lives_group = pygame.sprite.Group()

    # Create Game Objects
    container = pygame.Rect(0,0, len(level[0]) * 32, len(level) * 32)
    camera = Camera(container.width, container.height)
    cam_ent = Camera_Entity(container)
    ship = Ship(container)
    huey = Huey(container)
    heli = Helicopter(container)
    respawn = Respawn(container)
    lives = Lives(container, ship)
    #shipcontainer = pygame.Rect(ship.rect.centerx - WIDTH/2, ship.rect.centery - HEIGHT/2, WIDTH/2 - 100, ship.rect.width * 9)

    #Add Objects
    ship_group.add(ship)
    huey_group.add(huey)
    heli_group.add(heli)
    enemy_group.add(huey, heli)
    lives_group.add(lives)

    # Build Level
    x = y = 0
    for row in level:
        for col in row:
            if col == "C":
                p = Platform(x,y)
                platform_group.add(p)
            x += 32
        y += 32
        x = 0

    if LEVEL == 0 or LEVEL == 4:
        pygame.mixer.music.load("sound/dawn.ogg")
        pygame.mixer.music.set_volume(.2)
        pygame.mixer.music.play(-1)
    if LEVEL == 1:
        FILL = DAWN
        pygame.mixer.music.load("sound/dawn.ogg")
        pygame.mixer.music.set_volume(.2)
        pygame.mixer.music.play(-1)
    if LEVEL == 2:
        FILL = SKY
        pygame.mixer.music.load("sound/day.ogg")
        pygame.mixer.music.set_volume(.2)
        pygame.mixer.music.play(-1)
    if LEVEL == 3:
        FILL = NIGHT
        pygame.mixer.music.load("sound/night.ogg")
        pygame.mixer.music.set_volume(.2)
        pygame.mixer.music.play(-1)


    # Gameplay

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    TIMER = 0
                    #LEVEL = 1
                    #pygame.mixer.music.fadeout(100)
                    intro = False
                if event.key == pygame.K_w:
                    htp = True
                    intro = False

        introtitle = Text(container, 80, BLUE, 10, "DK Nanuk.otf", None)
        introsub = Text(container, 40, RED, 10, "DK Nanuk.otf", None)
        introsub2 = Text(container, 32, BLUE, 10, "DK Nanuk.otf", None)


        introtitle.image = introtitle.font.render(("RAIDEN"), 1, introtitle.color)
        introtitle.rect = introtitle.image.get_rect()
        introtitle.rect = introtitle.rect.move(container.centerx - introtitle.rect.width/1.15, HEIGHT / 3)
        introsub.image = introsub.font.render(("Press SPACE to start!"), 1, introsub.color)
        introsub.rect = introsub.image.get_rect()
        introsub.rect = introsub.rect.move(container.centerx - introsub.rect.width/1.3, HEIGHT / 3 + 100)
        introsub2.image = introsub2.font.render(("Press W for instructions!"), 1, introsub2.color)
        introsub2.rect = introsub2.image.get_rect()
        introsub2.rect = introsub2.rect.move(container.centerx - introsub2.rect.width/1.3, HEIGHT / 3 + 160)


        bgd = Background('images/screen.png')

        bgd.update()

        screen.blit(bgd.image, bgd.rect)
        screen.blit(introtitle.image, introtitle.rect)
        screen.blit(introsub.image, introsub.rect)
        screen.blit(introsub2.image, introsub2.rect)

        clock.tick(fps)
        pygame.display.flip()

    while htp:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    TIMER = 0
                    # LEVEL = 1
                    # pygame.mixer.music.fadeout(100)
                    htp = False

        bgd = Background('images/instructions.png')
        bgd.update()
        screen.blit(bgd.image, bgd.rect)

        clock.tick(fps)
        pygame.display.flip()

    while play:
        # Checks if exit button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        next = True
        if ship.hp <= 0:
            lose = True
            play = False

        if respawn.boss.hp <= 0 and LEVEL < 4:
            hold = TIMER
            if TIMER < hold + 25:
                pygame.mixer.fadeout(100)
                enemy_bullet_group.empty()
                ship.rect.y -= 5
            if ship.rect.y <= 10:
                next = True
                LEVEL += 1
                play = False

        if respawn.boss.hp <= 0 and LEVEL >= 4:
            hold = TIMER
            if TIMER < hold + 25:
                enemy_bullet_group.empty()
                ship.rect.y -= 5
            if ship.rect.y <= 10:
                win = True
                play = intro = lose = next = False

        # Update groups
        screen.fill(FILL)
        platform_group.update()
        ship_group.update(cam_ent, camera, container, bullet_group, enemy_bullet_group, pwrup_group, hpup_group,
                          enemy_group)
        camera.update(ship, cam_ent)
        cam_ent.update(ship)
        bullet_group.update(None, None)
        huey_group.update(bullet_group, enemy_bullet_group, huey_group, container, camera)
        heli_group.update(container, bullet_group, enemy_bullet_group, ship, camera)
        boss_group.update(bullet_group, enemy_bullet_group, ship, container)
        enemy_bullet_group.update("h", ship)
        pwrup_group.update(ship_group)
        hpup_group.update(ship_group)
        lives_group.update(ship, cam_ent)
        respawn.update(ship, container, cam_ent, pwrup_group, huey_group, heli_group, boss_group, hpup_group)

        # Draw objects
        # screen.blit(cam_ent.image, camera.apply(cam_ent))

        for p in platform_group:
            screen.blit(p.image, camera.apply(p))
        for b in bullet_group:
            screen.blit(b.image, camera.apply(b))
        for s in ship_group:
            screen.blit(s.image, camera.apply(s))
        for h in huey_group:
            screen.blit(h.image, camera.apply(h))
        for h in heli_group:
            screen.blit(h.image, camera.apply(h))
        for b in boss_group:
            screen.blit(b.image, camera.apply(b))

        for b in enemy_bullet_group:
            screen.blit(b.image, camera.apply(b))
        for p in pwrup_group:
            screen.blit(p.image, camera.apply(p))
        for l in lives_group:  # this is the score up top
            screen.blit(l.image, camera.apply(l))
        for h in hpup_group:
            screen.blit(h.image, camera.apply(h))

        # Limits frames per iteration of while loop
        clock.tick(fps)
        TIMER += 1
        # Writes to main surface
        pygame.display.flip()

    while lose:
        #Checks if exit button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    TIMER = 0
                    SCORE = 0
                    pygame.mixer.music.fadeout(100)
                    main()
        losetitle = Text(container, 80, BLUE, 10, "DK Nanuk.otf", None)
        losesub = Text(container, 40, RED, 10, "DK Nanuk.otf", None)

        losetitle.image = losetitle.font.render(("GAME OVER"), 1, losetitle.color)
        losetitle.rect = losetitle.image.get_rect()
        losetitle.rect = losetitle.rect.move(container.centerx - losetitle.rect.width/1.33, HEIGHT / 3)
        losesub.image = losesub.font.render(("Press SPACE to play again."), 1, losesub.color)
        losesub.rect = losesub.image.get_rect()
        losesub.rect = losesub.rect.move(container.centerx - losesub.rect.width/1.45, HEIGHT / 3 + 100)

        bgd = Background('images/screen.png')

        bgd.update()

        screen.blit(bgd.image, bgd.rect)
        screen.blit(losetitle.image, losetitle.rect)
        screen.blit(losesub.image, losesub.rect)

        clock.tick(fps)
        pygame.display.flip()

    while next:
        #Checks if exit button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    TIMER = 0
                    play = True
                    intro = False
                    next = False
                    main()

        wintitle = Text(container, 80, BLUE, 10, "DK Nanuk.otf", None)
        winsub = Text(container, 40, RED, 10, "DK Nanuk.otf", None)

        wintitle.image = wintitle.font.render(("Level " + str(LEVEL-1) + " Complete!"), 1, wintitle.color)
        wintitle.rect = wintitle.image.get_rect()
        wintitle.rect = wintitle.rect.move(container.centerx - wintitle.rect.width/1.45, HEIGHT / 3 - 50)
        winsub.image = winsub.font.render(str("Press SPACE to continue."), 1, winsub.color)
        winsub.rect = winsub.image.get_rect()
        winsub.rect = winsub.rect.move(container.centerx - winsub.rect.width/1.45, HEIGHT / 3 + 100)

        bgd = Background('images/screen.png')

        bgd.update()

        screen.blit(bgd.image, bgd.rect)
        screen.fill(WHITE)
        screen.blit(wintitle.image, wintitle.rect)
        screen.blit(winsub.image, winsub.rect)

        clock.tick(fps)
        pygame.display.flip()

    while win:
        #Checks if exit button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    TIMER = 0
                    SCORE = 0
                    LEVEL = 1
                    main()
        wintitle = Text(container, 80, BLUE, 10, "DK Nanuk.otf", None)
        winsub = Text(container, 30, RED, 10, "DK Nanuk.otf", None)

        wintitle.image = wintitle.font.render(("YOU WIN"), 1, wintitle.color)
        wintitle.rect = wintitle.image.get_rect()
        wintitle.rect = wintitle.rect.move(container.centerx - wintitle.rect.width/1.33, HEIGHT / 3)
        winsub.image = winsub.font.render(str("Final score: " + str(SCORE) + "  Press SPACE to play again."), 1, winsub.color)
        winsub.rect = winsub.image.get_rect()
        winsub.rect = winsub.rect.move(container.centerx - winsub.rect.width/1.5, HEIGHT / 3 + 100)

        bgd = Background('images/screen.png')

        bgd.update()

        screen.blit(bgd.image, bgd.rect)
        screen.blit(wintitle.image, wintitle.rect)
        screen.blit(winsub.image, winsub.rect)

        clock.tick(fps)
        pygame.display.flip()

if __name__ == "__main__":
    main()

'''        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                          P",
        "P                          P",
        "P                    PPPPPPP",
        "P                          P",
        "PPPPPPPPPPPPPPPP           P",
        "P                          P",
        "P                          P",
        "PPPP                       P",
        "P                          P",
        "P       PPPPPPPPPPPPPPPPPPPP",
        "PPPPP                      P",
        "P                          P",
        "P                          P",
        "P                    PPPPPPP",
        "P                          P",
        "PPPPPP         PPPPPPPPPPPPP",
        "P                          P",
        "P                          P",
        "P                          P",
        "P                      PPPPP",
        "P                          P",
        "PPPPPPPP                   P",
        "P                          P",
        "P                          P",
        "P                          P",
        "P PPPPPPPPPPPPPPPP     PPPPP",
        "P                          P",
        "PPPP                       P",
        "P                          P",
        "P                       PPPP",
        "PPPPP                      P",
        "P                          P",
        "P                          P",
        "P                    PPPPPPP",
        "P                          P",
        "PPPPPP                     P",
        "P                          P",
        "P                          P",
        "PPPPPPPPPPPPPPPPP          P",
        "P                          P",
        "P                       PPPP",
        "PPPPP                      P",
        "P                          P",
        "P                          P",
        "P           PPPPPPPPPPPPPPPP",
        "PPPPPP                     P",
        "P                          P",
        "P                          P",
        "P                          P",
        "P                      PPPPP",
        "P                          P",
        "PPPPPPPP                   P",
        "P                          P",
        "P                          P",
        "PPPPPPPPPPPPPPPPPP         P",
        "P                      PPPPP",
        "P                          P",
        "PPPP                       P",
        "P                          P",
        "P                       PPPP",
        "PPPPP                      P",
        "P                          P",
        "P                          P",
        "P                    PPPPPPP",
        "P                          P",
        "PPPPPP                     P",
        "P          PPPPPPPPPPPPPPPPP",
        "P                          P",
        "PPPP                       P",
        "P                          P",
        "P                       PPPP",
        "PPPPP                      P",
        "P                          P",
        "P                          P",
        "PPPPPPPPPPPPPPPP     PPPPPPP",
        "P                          P",
        "PPPPPP                     P",
        "P                          P",
        "PPPPPPPPPPPPPPPPP          P",
        "P                      PPPPP",
        "P                          P",
        "PPPPPPPP                   P",
        "P                          P",
        "P                          P",
        "P                          P",
        "P                      PPPPP",
        "P                          P",
        "PPPP                       P",
        "P                          P",
        "P                      PPPPP",
        "PPPPP                      P",
        "P                          P",
        "P                          P",
        "P                    PPPPPPP",
        "P                          P",
        "PPPPPPPPPPPPPPPP           P",
        "P                          P",
        "P                          P",
        "PPPP                       P",
        "P                          P",
        "P       PPPPPPPPPPPPPPPPPPPP",
        "PPPPP                      P",
        "P                          P",
        "P                          P",
        "P                    PPPPPPP",
        "P                          P",
        "PPPPPP         PPPPPPPPPPPPP",
        "P                          P",
        "P                          P",
        "P                          P",
        "P                      PPPPP",
        "P                          P",
        "PPPPPPPP                   P",
        "P                          P",
        "P                          P",
        "P                          P",
        "P PPPPPPPPPPPPPPPP     PPPPP",
        "P                          P",
        "PPPP                       P",
        "P                          P",
        "P                       PPPP",
        "PPPPP                      P",
        "P                          P",
        "P                          P",
        "P                    PPPPPPP",
        "P                          P",
        "PPPPPP                     P",
        "P                          P",
        "P                          P",
        "PPPPPPPPPPPPPPPPP          P",
        "P                          P",
        "P                       PPPP",
        "PPPPP                      P",
        "P                          P",
        "P                          P",
        "P           PPPPPPPPPPPPPPPP",
        "P                          P",
        "PPPPPP                     P",
        "P                          P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP", ]'''


