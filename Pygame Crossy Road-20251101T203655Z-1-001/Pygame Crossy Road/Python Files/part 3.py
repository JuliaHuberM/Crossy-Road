import pygame as p


class Cat(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 50
        self.y = HEIGHT / 2
        self.vel = 4
        self.width = 100
        self.height = 50

        # IMAGES

        self.cat1 = p.image.load('cat1.png')
        self.cat2 = p.image.load('cat2.png')
        self.cat1 = p.transform.scale(self.cat1, (self.width, self.height))
        self.cat2 = p.transform.scale(self.cat2, (self.width, self.height))

        self.image = self.cat1
        self.rect = self.image.get_rect()

    def update(self):
        self.movement()
        self.correction()
        self.rect.center = (self.x, self.y)

    def movement(self):
        keys = p.key.get_pressed()
        if keys[p.K_LEFT]:
            self.x -= self.vel
            self.image = self.cat2

        elif keys[p.K_RIGHT]:
            self.x += self.vel
            self.image = self.cat1

        if keys[p.K_UP]:
            self.y -= self.vel

        elif keys[p.K_DOWN]:
            self.y += self.vel

    def correction(self):
        if self.x - self.width / 2 < 0:
            self.x = self.width / 2

        elif self.x + self.width / 2 > WIDTH:
            self.x = WIDTH - self.width / 2

        if self.y - self.height / 2 < 0:
            self.y = self.height / 2

        elif self.y + self.height / 2 > HEIGHT:
            self.y = HEIGHT - self.height / 2


class Car(p.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        if number == 1:
            self.x = 190
            self.image = p.image.load('Slow Car.png')
            self.vel = -4

        else:
            self.x = 460
            self.image = p.image.load('Fast Car.png')
            self.vel = 5

        self.y = HEIGHT / 2
        self.width = 100
        self.height = 150
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

    def update(self):
        self.movement()
        self.rect.center = (self.x, self.y)

    def movement(self):
        self.y += self.vel

        if self.y - self.height / 2 < 0:
            self.y = self.height / 2
            self.vel *= -1

        elif self.y + self.height / 2 > HEIGHT:
            self.y = HEIGHT - self.height / 2
            self.vel *= -1


class Screen(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img1 = p.image.load('Scene.png')
        self.img2 = p.image.load('You Win.png')
        self.img3 = p.image.load('You lose.png')

        self.img1 = p.transform.scale(self.img1, (WIDTH, HEIGHT))
        self.img2 = p.transform.scale(self.img2, (WIDTH, HEIGHT))
        self.img3 = p.transform.scale(self.img3, (WIDTH, HEIGHT))

        self.image = self.img1
        self.x = 0
        self.y = 0

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = (self.x, self.y)


class Flag(p.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.number = number

        if self.number == 1:
            self.image = p.image.load('green flag.png')
            self.visible = False
            self.x = 50

        else:
            self.image = p.image.load('white flag.png')
            self.visible = True
            self.x = 580

        self.y = HEIGHT / 2
        self.image = p.transform.scale2x(self.image)
        self.rect = self.image.get_rect()

    def update(self):
        if self.visible:
            self.rect.center = (self.x, self.y)


def ScoreDisplay():
    score_text = score_font.render(str(SCORE) + ' / 5', True, (0, 0, 0))
    win.blit(score_text, (255, 10))


WIDTH = 640
HEIGHT = 480

p.init()

win = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption('Crossy Road')
clock = p.time.Clock()

SCORE = 0
score_font = p.font.SysFont('comicsans', 80, True)

bg = Screen()
screen_group = p.sprite.Group()
screen_group.add(bg)

cat = Cat()
cat_group = p.sprite.Group()
cat_group.add(cat)

slow_car = Car(1)
fast_car = Car(2)
car_group = p.sprite.Group()
car_group.add(slow_car, fast_car)

run = True
while run:
    clock.tick(60)
    for event in p.event.get():
        if event.type == p.QUIT:
            run = False

    screen_group.draw(win)

    cat_group.draw(win)
    car_group.draw(win)

    cat_group.update()
    car_group.update()

    screen_group.update()
    ScoreDisplay()

    p.display.update()

p.quit()
