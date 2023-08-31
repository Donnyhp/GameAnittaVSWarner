import pygame
import random
import math

from pygame import mixer

#Inicialização
pygame.init()

#Tela do jogo
screen = pygame.display.set_mode((800, 600))
s_background = pygame.image.load('background.jpg') #carregar imagem de fundo na variável

#Música de fundo
mixer.music.load('fundo.wav')
mixer.music.play(-1)

#Título e ícone
pygame.display.set_caption("Anitta VS Warner")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#Jogador
jogadorImg = pygame.image.load('icon.png')
jogadorX = 370
jogadorY = 510
jogadorX_Movimento = 0

#Inimigos
inimigosImg = []
inimigosX = []
inimigosY = []
inimigosX_Movimento = []
inimigosY_Movimento = []
numero_inimigos = 8

for i in range(numero_inimigos):
    inimigosImg.append(pygame.image.load('enemy.png'))
    inimigosX.append(random.randint(0, 724))
    inimigosY.append(random.randint(15, 200))
    inimigosX_Movimento.append(0.3)
    inimigosY_Movimento.append(40)

#Bala
# Ready - você não pode ver a bala
# Fire - bala está se movendo

balaImg = pygame.image.load('bullet.png')
balaX = 0
balaY = 510
balaX_Movimento = 0
balaY_Movimento = 2
estado_Bala = "ready"

# Placar
valor_placar = 0
fonte = pygame.font.Font('freesansbold.ttf', 32)

textoX = 10
textoY = 10

#Texto Game Over
fonte_over = pygame.font.Font('freesansbold.ttf', 72)

def mostrar_Placar(x, y):
    placar = fonte.render("Placar: " + str(valor_placar), True, (188,81,135))
    screen.blit(placar, (x, y))

def game_over_text():
    over_text = fonte_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (185, 280))
def jogador(x, y):
    screen.blit(jogadorImg, (x,y))

def inimigos(x, y, i):
    screen.blit(inimigosImg[i], (x,y))

def tiro_Bala(x,y):
    global estado_Bala
    estado_Bala = "fire"
    screen.blit(balaImg, (x + 35, y + 10))

def colidiu(inimigosX,inimigosY,balaX,balaY):
    distancia = math.sqrt((math.pow(inimigosX-balaX, 2)) + (math.pow(inimigosY-balaY, 2)))
    if distancia < 27:
        return True
    else:
        return False

#Game Loop
running = True
while running:
    screen.blit(s_background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #verificar se tecla está pressionada
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jogadorX_Movimento = -0.5

            if event.key == pygame.K_RIGHT:
                jogadorX_Movimento = 0.5

            if event.key == pygame.K_SPACE:
                som_Bala = mixer.Sound('laser.wav')
                som_Bala.play()
                if estado_Bala is "ready":
                    balaX = jogadorX
                    tiro_Bala(balaX,balaY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jogadorX_Movimento = 0


    #Verificar bordas Anitta
    jogadorX += jogadorX_Movimento

    if jogadorX <= -15:
        jogadorX = -15

    elif jogadorX >= 715:
        jogadorX = 715

    #Movimento dos inimigos

    for i in range(numero_inimigos):

        #Game Over
        if inimigosY[i] > 460:
            for j in range(numero_inimigos):
                inimigosY[j] = 2000
            game_over_text()
            break

        inimigosX[i] += inimigosX_Movimento[i]

        if inimigosX[i] <= -15:
            inimigosX_Movimento[i] = 0.5
            inimigosY[i] += inimigosY_Movimento[i]

        elif inimigosX[i] >= 725:
            inimigosX_Movimento[i] = -0.5
            inimigosY[i] += inimigosY_Movimento[i]

        # Colisão
        colisao = colidiu(inimigosX[i], inimigosY[i], balaX, balaY)
        if colisao:
            som_Colisao = mixer.Sound('explosion.wav')
            som_Colisao.play()
            balaY = 510
            estado_Bala = "ready"
            valor_placar += 100
            inimigosX[i] = random.randint(0, 724)
            inimigosY[i] = random.randint(15, 200)

        inimigos(inimigosX[i], inimigosY[i], i)

    # Movimento Bala
    if balaY <= 0:
        balaY = 510
        estado_Bala = "ready"

    if estado_Bala is "fire":
        tiro_Bala(balaX,balaY)
        balaY -= balaY_Movimento



    jogador(jogadorX, jogadorY)
    mostrar_Placar(textoX, textoY)
    pygame.display.update()



