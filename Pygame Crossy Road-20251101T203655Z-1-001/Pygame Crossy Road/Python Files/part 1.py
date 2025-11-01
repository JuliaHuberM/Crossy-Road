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
        self.rect.center = (self.x, self.y)

    def movement(self):
        keys = p.key.get_pressed()
        if keys[p.K_LEFT]:
            self.x -= self.vel

        elif keys[p.K_RIGHT]:
            self.x += self.vel

        if keys[p.K_UP]:
            self.y -= self.vel

        elif keys[p.K_DOWN]:
            self.y += self.vel


WIDTH = 640
HEIGHT = 480

p.init()

win = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption('Crossy Road')
clock = p.time.Clock()

cat = Cat()
cat_group = p.sprite.Group()
cat_group.add(cat)

run = True
while run:
    clock.tick(60)
    for event in p.event.get():
        if event.type == p.QUIT:
            run = False

    win.fill((0, 255, 0))

    cat_group.draw(win)
    cat_group.update()

    p.display.update()

p.quit()
