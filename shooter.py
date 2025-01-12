from pygame import *
from random import randint

window = display.set_mode((700, 500))
clock = time.Clock()
display.set_caption('Космический Шутер')
background = transform.scale(image.load('space.png'), (700, 500))
game = True
font.init()
lost_count = 0
lost = font.SysFont('Arial', 40)
kill_count = 0
kill = font.SysFont('Arial', 40)
lose = font.SysFont('Arial', 100)
win = font.SysFont('Arial', 100)
class GamesSprite(sprite.Sprite):
    def __init__(self, x, y, image_player, speed, size):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(image_player), size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GamesSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < 640:
           self.rect.x += self.speed 
        if keys[K_a] and self.rect.x > 5:
           self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet(self.rect.centerx - 15, self.rect.top, 'bullet.png', 7, (30, 30))
        bullets.add(bullet)
class Enemy(GamesSprite):
    def update(self):
        global lost_count
        self.rect.y += self.speed
        if self.rect.y > 500:
            lost_count += 1
            self.rect.y = 0
            self.rect.x = randint(0, 600)
class Bullet(GamesSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

monsters = sprite.Group()
rocket = Player(300, 420, 'rocket.png', 10, (80, 80))
bullets = sprite.Group()
for i in range(6):
    enemy = Enemy(randint(0, 600), 0, 'UFO.png', randint(1, 3), (80, 80))
    monsters.add(enemy)
finish = False
while game:
    if finish == False:

        window.blit(background, (0, 0))
        sprite_collide = sprite.spritecollide(rocket, monsters, False)
        if len(sprite_collide) > 0:
            finish = True
            lose_txt = lose.render('Поражение!', True, (255, 0, 0))
            window.blit(lose_txt, (150, 200))
        if lost_count > 20:
            finish = True
            lose_txt = lose.render('Поражение!', True, (255, 0, 0))
            window.blit(lose_txt, (150, 200))
        group_collide = sprite.groupcollide(bullets, monsters, True, True)
        for i in group_collide:
            enemy = Enemy(randint(0, 600), 0, 'UFO.png', randint(1, 3), (80, 80))
            monsters.add(enemy)
            kill_count += 1
        if kill_count > 50:
            finish = True
            win_txt = win.render('Победа!', True, (0, 255, 0))
            window.blit(win_txt, (150, 200))
        kill_txt = kill.render('Сбито: ' + str(kill_count), True, (255, 255, 255))    
        lost_txt = lost.render('Пропущено: ' + str(lost_count), True, (255, 255, 255))
        window.blit(lost_txt, (0, 0))
        window.blit(kill_txt, (0, 30))
        rocket.reset()
        rocket.update()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
    display.update()
    clock.tick(60)