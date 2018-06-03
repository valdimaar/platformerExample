import pygame, sys, random
pygame.init()

X = 900
Y = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 155, 0)

screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Leikur prufa")
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT + 1, 10000)

acc = 2


class Platform():
    def __init__(self, sizex, sizey, posx, posy, color):
        self.surf = pygame.surface.Surface((sizex, sizey))
        self.rect = self.surf.get_rect(midbottom=(posx, posy))
        self.surf.fill(color)

    def draw(self):
        screen.blit(self.surf, self.rect)


class Player():
    def __init__(self):
        self.jump = False
        self.left = False
        self.right = False
        self.lives = 5
        self.heart = pygame.image.load('heart.png').convert()
        self.surf = pygame.image.load('player.jpg').convert()
        self.rect = self.surf.get_rect(midbottom=(X//2, Y - 100))
        self.y_speed = 0

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.on_ground():
                    self.jump = True
            elif event.type == pygame.USEREVENT + 1:
                enemy.timer = True

        self.left = False
        self.right = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.left = True
        if keys[pygame.K_RIGHT]:
            self.right = True

    def move(self):
        if self.jump:
            self.y_speed = -18
            self.jump = False
        self.rect.bottom += self.y_speed

        if self.left and self.rect.left > 0:
            self.rect.centerx -= 5
        if self.right and self.rect.right < X:
            self.rect.centerx += 5

        if self.on_ground():
            if self.y_speed >= 0:
                self.rect.bottom = p_rects[self.rect.collidelist(p_rects)].top + 1
                self.y_speed = 0
            else:
                self.rect.top = p_rects[self.rect.collidelist(p_rects)].bottom
                self.y_speed = 2
        else:
            self.y_speed += acc

    def on_ground(self):
        collision = self.rect.collidelist(p_rects)
        if collision > -1:
            return True
        else:
            return False

    def draw(self):
        screen.blit(self.surf, self.rect)
        for i in range(self.lives):
            screen.blit(self.heart, [i*20 + 20, 20])


class Enemy():
    def __init__(self):
        self.surf = pygame.image.load('enemy.jpg').convert()
        self.rect = self.surf.get_rect(midtop=(X//2, 0))
        self.x_speed = random.randint(3, 7)
        self.y_speed = 0
        self.timer = False

    def move(self):
        self.rect.centerx += self.x_speed
        if self.rect.left <= 0 or self.rect.right >= X:
            self.x_speed *= -1

        if self.on_ground():
            self.rect.bottom = p_rects[self.rect.collidelist(p_rects)].top + 1
            self.y_speed = 0
        else:
            self.y_speed += acc
        self.rect.bottom += self.y_speed

        self.hit()

        if self.timer:
            self.timer = False
            self.rect.midtop = (X//2, 0)
            self.x_speed = random.randint(3, 7) * ((self.x_speed > 0) - (self.x_speed < 0))

    def on_ground(self):
        collision = self.rect.collidelist(p_rects)
        if collision > -1:
            return True
        else:
            return False

    def hit(self):
        if player.rect.colliderect(self.rect):
            player.lives -= 1
            player.rect.midbottom = (X//2, Y - 100)
        # if lives == 0:
            # do something..

    def draw(self):
        screen.blit(self.surf, self.rect)


class Coin():
    def __init__(self):
        self.positions = [(600, 245), (250, 325), (40, 500), (850, 500), (830, 245), (800, 325)]
        self.surf = pygame.image.load('coin.png').convert()
        self.rect = self.surf.get_rect(midbottom=random.choice(self.positions))
        self.count = 0
        self.small_surf = pygame.transform.scale(self.surf, (20, 20))

    def hit(self):
        if player.rect.colliderect(self.rect):
            self.rect.midbottom = random.choice(self.positions)
            self.count += 1
        elif enemy.rect.colliderect(self.rect):
            self.rect.midbottom = random.choice(self.positions)
        # if self.count > value:
            # do something

    def draw(self):
        screen.blit(self.surf, self.rect)
        for i in range(self.count):
            screen.blit(self.small_surf, [850 - i*20, 20])


platforms = []
platforms.append(Platform(X, 100, X//2, Y, GREEN))
platforms.append(Platform(200, 15, 500, Y-180, BLUE))
platforms.append(Platform(300, 15, 200, 340, BLUE))
platforms.append(Platform(250, 15, 480, 260, BLUE))
platforms.append(Platform(300, 15, 150, 180, BLUE))
platforms.append(Platform(300, 15, 500, 100, BLUE))
platforms.append(Platform(80, 15, 830, 260, BLUE))
platforms.append(Platform(80, 15, 800, 340, BLUE))
p_rects = [p.rect for p in platforms]

player = Player()
enemy = Enemy()
coin = Coin()

while True:
    clock.tick(30)
    screen.fill(WHITE)

    player.event()
    player.move()
    enemy.move()
    coin.hit()

    player.draw()
    enemy.draw()
    coin.draw()
    for p in platforms:
        p.draw()

    pygame.display.flip()
