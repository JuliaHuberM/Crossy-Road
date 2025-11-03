# ===== inicialização =====
import pygame
import random

pygame.init()
pygame.mixer.init()  # Inicializa o mixer de áudio

width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('crossy road')

# Carregar música de fundo (adicione o arquivo 'musica_fundo.mp3' na pasta do projeto)
try:
    pygame.mixer.music.load('trilha.mp3')
    pygame.mixer.music.play(-1)  # Loop infinito
except pygame.error as e:
    print(f"Erro ao carregar música de fundo: {e}")

# Carregar som de colisão (adicione o arquivo 'som_colisao.wav' na pasta do projeto)
try:
    crash_sound = pygame.mixer.Sound('batida.mp3')
except pygame.error as e:
    print(f"Erro ao carregar som de colisão: {e}")
    crash_sound = None  # Fallback: sem som

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
class Carro(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        rect = image.get_rect()
        # Ajuste a escala para reduzir a largura e evitar sobreposição entre lanes
        # Novo: image_scale reduzido para ~60-70 pixels de largura (menor que 100 pixels entre lanes)
        image_scale = (30 / rect.width) * 2.5  # Reduzido de 45 para 30 para estreitar
        new_width = int(rect.width * image_scale)
        new_height = int(rect.height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerCar(Carro):
    def __init__(self, x, y):
        image = pygame.image.load('imagens/car.png')
        super().__init__(image, x, y)

# jogador
player_x = 250
player_y = 400

player_group = pygame.sprite.Group()
player = PlayerCar(player_x, player_y)
player_group.add(player)

# outros carros
image_file = ['police.png', 'ambulance.png', 'mini_van.png', 'taxi.png']
carros_images = []
for file in image_file:
    try:
        image = pygame.image.load('imagens/' + file)
        carros_images.append(image)
    except pygame.error as e:
        print(f"Erro ao carregar imagem {file}: {e}")
        image = pygame.Surface((60, 100))  # Ajustado para largura 60
        image.fill(red)
        carros_images.append(image)

carro_grupo = pygame.sprite.Group()

# batida dos carros
try:
    crash = pygame.image.load('imagens/explosion4.png').convert_alpha()
except pygame.error as e:
    print(f"Erro ao carregar imagem explosion4.png: {e}")
    # fallback simples
    crash = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.circle(crash, red, (30, 30), 30)
crash_rect = crash.get_rect()

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
        if not gameover:
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

    # adicionar carros
    if not gameover and len(carro_grupo) < 2:
        # espaço entre os carros
        add_carro = True
        for car in carro_grupo:
            if car.rect.top < car.rect.height * 1.5:
                add_carro = False
                
        if add_carro:
            lane = random.choice(lanes)
            image = random.choice(carros_images)
            veiculo = Carro(image, lane, height / -2)
            carro_grupo.add(veiculo)

    # movimentação dos carros
    if not gameover:
        for veiculo in carro_grupo:
            veiculo.rect.y += speed

            # remove o que vai pra fora da tela
            if veiculo.rect.top >= height:
                veiculo.kill()
                score += 1
                
                # aumento da velocidade após 5 carros
                if score > 0 and score % 5 == 0:
                    speed += 1

    # desenhar carros
    carro_grupo.draw(screen)

    # score
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score:' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 450)
    screen.blit(text, text_rect)

    # confere se tem colisão
    if not gameover and pygame.sprite.spritecollide(player, carro_grupo, False):
        gameover = True
        crash_rect.center = player.rect.center
        # Tocar som de colisão
        if crash_sound:
            crash_sound.play()

    if gameover:
        # Parar música de fundo na tela de game over (opcional, para "durante todo jogo" pode remover)
        pygame.mixer.music.stop()
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Press Y to play again or N to quit.', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)

        # play again
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_y:
                    # reset
                    gameover = False
                    speed = 2
                    score = 0
                    carro_grupo.empty()
                    player.rect.center = [player_x, player_y]
                    # Reiniciar música de fundo
                    pygame.mixer.music.play(-1)
                elif evento.key == pygame.K_n:
                    running = False

    pygame.display.update()

pygame.quit()
