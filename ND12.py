from pygame import*
import random

#Шлях до зображення
img_back = "galaxy.jpg" # фон
img_hero = "rocket.png" #Спрайт гравця
img_enemy = "ufo.png" #Спрайт ворога
img_bullet = "bullet.png" #Спрайт куль
img_ast = "asteroid.png" # Спрайт астероїда

#Своримо вікно
win_w = 700
win_h = 500

score = 0 # Кількість збитих ворогів
lost = 0 # Кількість пропущених кораблів
max_score = 20 # Кількість збитих воргів для перемоги
max_lost = 5 # Кількість пропущених воргів для програшу
life = 3 # Кількість життів гравця


window = display.set_mode((win_w, win_h))
background = transform.scale(image.load(img_back),(win_w, win_h))

#Створимо батьківський клас для інших спрайтів
# sprite.Sprite - клас із модуля pygame для створення спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, size_x,size_y, player_speed):
        sprite.Sprite.__init__(self)
        #Завантажимо та маштабуємо спрайти
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        # Всатовимо початкові координати спрайтів
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #Метод для виведення спрайтів на екран
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

#Клас головного гравця(дочірній)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        #get_pressed() - повертає список де кожен елемент вказує чи була натиснута
        # відповідна клавіша
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):

        #  self.rect.centerx - координата X середина спрайта
        #  self.rect.top - координата Y верхньою точкою спрайту
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15,20,-15)
        bullets.add(bullet)


        

#Клас для НЛО(дочірній)
class Enemy(GameSprite):
    #рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # Зникає коли дійде до кінця
        if self.rect.y > win_h:
            self.rect.x = random.randint(80, win_w - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Rock(GameSprite):
    def update(self):
        self.rect.y += self.speed # переміщуємо наш спрайт вниз
        global lost 
        if self.rect.y > win_h:
            spawn_chance = random.randint(1,100)
            if spawn_chance <=17: # Шанс спавну астероїда 17%
                self.rect.y = 0
                self.rect.x = random.randint(50, win_w - 80)






#Створимо спрайти
ship = Player(img_hero, 5, win_h-100, 80, 100, 10)
#Створення групи спрайтів
monsters = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()

for i in range(1,6):
    monster = Enemy(img_enemy, random.randint(80, win_w - 80), -40, 80,30,random.randint(1,5))
    monsters.add(monster)

for i in range(1,2):
    asteroid = Rock(img_ast, random.randint(80, win_w - 80), -40, 80,30,random.randint(1,5))
    asteroids.add(asteroid)


# підключемо музику
mixer.init()
#mixer.music.load("space.ogg")
#mixer.music.play()
#fire_sound = mixer.Sound("fire.ogg")

#Підключити текст
font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
# None - стандартний шрифт(просто шрифт), 36 - розмір
win = font1.render("Ти переміг!",True,(255,255,255))
lose = font1.render("Ти програв!",True,(180,0,0))
# True - згладжування тексту

finish = False
run = True

def restart_game():
    global score, lost, life, finish

    #Скидання данних
    score = 0
    lost = 0
    life = 5
    finish = False

    # Скидання положення гравця та монстрів
    ship.rect.x = 5 #
    ship.rect.y = win_h - 100#
    monsters.empty()#
    bullets.empty()#

    #Створимо нових монстрів
    for i in range(1,6):
        monster = Enemy(img_enemy, random.randint(80, win_w - 80), -40, 80,30,random.randint(1,5))
        monsters.add(monster)

    for i in range(1,2):
        asteroid = Rock(img_ast, random.randint(80, win_w - 80), -40, 80,30,random.randint(1,5))
        asteroids.add(asteroid)



while run:
    # event.get - повертає список подій, які вже відбулися
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:#
                ship.fire()
            elif e.key == K_RETURN and finish:
                restart_game()
    if not finish:
        # Розмістимо фон
        window.blit(background, (0,0))
        # Розмістимо текст на екрані
        text = font2.render("Рахунок: " +str(score), 1,(255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render("НЛО пропущено: " +str(lost), 1,(255,255,255))
        window.blit(text_lose, (10,50))

        #Оновлення руху гравця
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        # Виведемо спрайти на екран
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        # Перевіримо чи зіткнулися кулі та монстри
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # цикл який повторюєється стільки разів, скільки монстів збито
            score = score + 1
            monster = Enemy(img_enemy, random.randint(80, win_w - 80), -40, 80,30,random.randint(1,5))
            monsters.add(monster)

        collides2 = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides2:
            # цикл який повторюєється стільки разів, скільки монстів збито
            score = score + 5
            asteroid = Rock(img_ast, random.randint(80, win_w - 80), -40, 80,30,random.randint(1,5))
            asteroids.add(asteroid)

        #Зіткнення корабля з НЛО 
        if sprite.spritecollide(ship, monsters, False):
            for c in sprite.spritecollide(ship, monsters, False):
                c.rect.x = random.randint(80, win_w-80)
                c.rect.y = -40
                life = life - 1
        # Зіткнення астероїда з гравцем

        elif sprite.spritecollide(ship, asteroids, False):
            for c in sprite.spritecollide(ship, asteroids, False):
                c.rect.x = random.randint(80, win_w-80)
                c.rect.y = -40
                life = life - life
        
        #Ситуація програшу
        if life ==0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        #Ситуація виграшу
        if score >= max_score:
            finish = True
            window.blit(win,(200,200))
        display.update()
    #затримка для визначення частоти оновллення
    time.delay(50)