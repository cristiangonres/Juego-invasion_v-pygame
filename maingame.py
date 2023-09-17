import pygame
import random
import math
from pygame import mixer
import io

pygame.init()

# Crea pantalla
display = pygame.display.set_mode((800, 600))

# Título e icono
pygame.display.set_caption("Invasion vaginal")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
bg = pygame.image.load("Fondo.jpg")

# Musica
mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.1)
mixer.music.play(-1)

# fuente a bytes
def font_bytes(font):
    with open(font, 'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)

# Score
score = 0
font_as_bytes = font_bytes('freesansbold.ttf')
font = pygame.font.Font(font_as_bytes, 32)
text_x = 10
text_y = 10

def show_score(x, y):
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))
    display.blit(score_value, (x, y))

# Texto final juego
def text_end():
    end_game = font.render("Fin del juego", True, (255, 255, 255))
    score_value =  font.render(f"Tu puntuación es de {score} puntos" , True, (255, 255, 255))
    display.blit(end_game, (250, 250))                          
    display.blit(score_value, (150, 290))


# Jugador
player_img = pygame.image.load("cohete.png")
player_x = 368
player_y = 520
speed_player = 0
def player_mov(x,y):
    display.blit(player_img, (x, y))
    
    
# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
speed_enemy_x = []
speed_enemy_y = []
num_enemies = 9

for e in range(num_enemies):
    enemy_img.append(pygame.image.load("enemigo.png"))
    enemy_x.append(random.randint(0, 723))
    enemy_y.append(random.randint(50, 200))
    speed_enemy_x.append(1)
    speed_enemy_y.append(50)
    
def enemy_mov(x, y, ene):
    display.blit(enemy_img[ene], (x, y))


# Bullet
bullet_img = pygame.image.load("bala4.png")
bullet_x = 0
bullet_y = 520
speed_bullet_x = 0
speed_bullet_y = 2
bullet_shot = False
def bullet_mov(x,y):
    global bullet_shot
    bullet_shot = True
    display.blit(bullet_img, (x + 16, y + 10))
    
# Detectar colisiones
def detect_collision(x_b, x_e, y_b, y_e):
    distance = math.sqrt(math.pow(x_e - x_b, 2) + math.pow(y_e - y_b, 2))
    if distance < 25:
        return True
    else:
        return False

# Loop del juego
play = True
while play:
    
    # Fondo
    display.fill((0, 0, 51))
    display.blit(bg, (0, 0))
    
    # Controles jugador
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            play = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_a:
                speed_player = -5
            if ev.key == pygame.K_d:
                speed_player = 5
            if ev.key == pygame.K_SPACE:
                if not bullet_shot:
                    shot = mixer.Sound('disparo.mp3')
                    shot.play()
                    bullet_x = player_x
                    bullet_mov(bullet_x, player_y)
                
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_a or ev.key == pygame.K_d:
                speed_player = 0

    # Modificar posición jugador
    player_x += speed_player
    
    # Mantener jugador en los bordes
    if player_x < 0:
        player_x = 0
    elif player_x > 736:
        player_x = 736    
    
    # Movimiento bala
    if bullet_y <= -24:
        bullet_y = 520
        bullet_shot = False   
    if bullet_shot:
        bullet_mov(bullet_x, bullet_y)
        bullet_y -= speed_bullet_y
    
    
    
    # Modificar posición enemigo
    for e in range(num_enemies):
        
        # fin del juego
        if enemy_y[e] > 490:
            for k in range(num_enemies):
                enemy_y[k] = 1000
            text_end()
            break
        
        enemy_x[e] += speed_enemy_x[e]    
    # Mantener enemigo en los bordes
        if enemy_x[e] <= 0:
            enemy_x[e] = 0
            speed_enemy_x[e] = speed_enemy_x[e] * -1
            enemy_y[e] += speed_enemy_y[e]
        elif enemy_x[e] >= 736:
            enemy_x[e] = 736
            speed_enemy_x[e] = speed_enemy_x[e] * -1
            enemy_y[e] += speed_enemy_y[e]
        enemy_mov(enemy_x[e], enemy_y[e], e)
        # Colisión
        collision = detect_collision(bullet_x, enemy_x[e], bullet_y, enemy_y[e])
        if collision:
            bullet_y = 500
            bullet_shot = False
            enemy_img[e] = pygame.image.load("baby.png")
            score += 1
            hit = mixer.Sound('Golpe.mp3')
            hit.play()
            enemy_x[e] = random.randint(0, 723)
            enemy_y[e] = random.randint(50, 200)
        
    player_mov(player_x, player_y)
    show_score(text_x, text_y)
    
    
    pygame.display.update()