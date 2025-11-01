# ===== inicialização =====
import pygame
import random

pygame.init()

width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('crossy road')

# cores
gray = (100, 100, 100)
green = (76, 208, 56)
red = (255, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# configurações
gameover = False
speed = 2
score = 0

# marcações
marker_width = 10
marker_height = 50
road = (100, 0, 300, height)
left = (95, 0, marker_width, height)
right = (395, 0, marker_width, height)

# pista
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]
lane_anim = 0

# classe carro
class carro(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        rect = image.get_rect()
        image_scale = (45 / rect.width)*2.5
        new_width = int(rect.width * image_scale)
        new_height = int(rect.height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class playerc(carro):
    def __init__(self, x, y):
        image = pygame.image.load('audi.png')  
        super().__init__(image, x, y)

# jogador
player_x = 250
player_y = 400

player_group = pygame.sprite.Group()
player = playerc(player_x, player_y)
player_group.add(player)

#outros carros



# loop principal
clock = pygame.time.Clock()
fps = 120
running = True
while running:
    clock.tick(fps)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

        # movimentos carro
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif evento.key == pygame.K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100

    # fundo
    screen.fill(green)
    pygame.draw.rect(screen, gray, road)
    pygame.draw.rect(screen, yellow, left)
    pygame.draw.rect(screen, yellow, right)

    # animação das faixas
    lane_anim += speed * 2
    if lane_anim >= marker_height * 2:
        lane_anim = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, ((150 + 45), y + lane_anim, marker_width, marker_height))
        pygame.draw.rect(screen, white, ((250 + 45), y + lane_anim, marker_width, marker_height))

    # desenha carro do jogador
    player_group.draw(screen)

    pygame.display.update()

pygame.quit()