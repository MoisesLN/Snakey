import pygame
from pygame.locals import *  
from sys import exit
import random

pygame.init()

# Tela
largura = 640
altura = 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snakey")  # Título do jogo

# Arena
largura_arena = 320
altura_arena = 320
x_arena = 160
y_arena = 80
fim_x_arena = 480
fim_y_arena = 400

# Imagens
img_menu = pygame.image.load('sprites/tela_inicio.png')
img_gameover = pygame.image.load('sprites/tela_fim.png')
img_arena = pygame.image.load('sprites/mapa.png')
img_rabo = pygame.image.load('sprites/rabo.png').convert_alpha()
img_corpo = pygame.image.load('sprites/corpo.png').convert_alpha()
img_cabeca = pygame.image.load('sprites/cabeca.png').convert_alpha()
img_maca = pygame.image.load('sprites/chao_frutav2.png').convert_alpha()
img_ranking = pygame.image.load('sprites/leaderboard.png')
img_creditos = pygame.image.load('sprites/dev_lock_in.png')
img_nome = pygame.image.load('sprites/Nome.png')

# Música
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.load("musica_fundo.mp3")
pygame.mixer.music.play(-1)
moeda_colisao = pygame.mixer.Sound("moeda_coletar.mp3")
moeda_colisao.set_volume(0.5)

# Fonte p renderizar texto:
fonte = pygame.font.Font('PressStart2P_font.ttf', 24)
fonte_nome = pygame.font.Font('PressStart2P_font.ttf', 30)
fonte_creditos = pygame.font.Font('PressStart2P_font.ttf', 12)
# FPS do jogo
relogio = pygame.time.Clock()

def aumenta_cobra(lista_cobra):
    for i in range(len(lista_cobra)):
        # Cabeça
        if i == len(lista_cobra) - 1:
            

            # Rotacionar a cabeça
            if x_controle > 0:
                cabeca_virada = pygame.transform.rotate(img_cabeca, 0) # Direita
            elif x_controle < 0:
                cabeca_virada = pygame.transform.rotate(img_cabeca, 180) # Esquerda
            elif y_controle > 0:
                cabeca_virada = pygame.transform.rotate(img_cabeca, 270) # Baixo
            else:
                cabeca_virada = pygame.transform.rotate(img_cabeca, 90) # Cima
            tela.blit(cabeca_virada, (lista_cobra[i][0], lista_cobra[i][1]))

        # Rabo
        elif i == 0:
            x_antigo, y_antigo = lista_cobra[i + 1]
            
            x_atual, y_atual = lista_cobra[i]

            #O rabo precisa das coordenadas invertidas
            if x_atual > x_antigo:
                angulo = 180 # direita
            elif x_atual < x_antigo:
                angulo = 0 # esquerda
            elif y_atual > y_antigo:
                angulo = 90 # baixo
            else:
                angulo = 270 # cima
            rabo_virado = pygame.transform.rotate(img_rabo, angulo)
            tela.blit(rabo_virado, (lista_cobra[i][0], lista_cobra[i][1]))

        # Corpo
        else:
            # A rotação do corpo depende da direção entre o segmento anterior e o segmento atual
            x_antigo, y_antigo = lista_cobra[i + 1]
            
            x_atual, y_atual = lista_cobra[i]

            if x_atual > x_antigo:
                angulo = 180 # esquerda
            elif x_atual < x_antigo:
                angulo = 0 # direita
            elif y_atual > y_antigo:
                angulo = 270 # baixo
            else:
                angulo = 90 # cima
            corpo_virado = pygame.transform.rotate(img_corpo, angulo)
            tela.blit(corpo_virado, (lista_cobra[i][0], lista_cobra[i][1]))

def adicionar_ranking():
    # Adicionar dados ao ranking
    with open("ranking.txt", "a") as arquivo: # "a" é para append, adicionar items
        arquivo.write(f"{nome_texto} - {pontos} pontos\n")

# Estado do jogo (menu, jogo, ranking, game over ou créditos)
estado = "menu"

# Variáveis do jogo
x_cobra = (altura_arena / 2) - 16
y_cobra = (largura_arena / 2) - 16
x_maca = random.randrange(x_arena, fim_x_arena - 16, 16)
y_maca = random.randrange(y_arena, fim_y_arena - 16, 16)
x_controle = 16
y_controle = 0
velocidade = 16
comprimento = 3
lista_cobra = []
pontos = 0
nome_texto = ''

while True:
    relogio.tick(10) # Velocidade do jogo
    

    # Tela de menu
    if estado == "menu":
        tela.fill((0, 0, 0))
        tela.blit(img_menu, (0, 0))


    # Input de nome, vem antes do jogo
    elif estado == "nome":
        tela.blit(img_nome, (0, 0))
        input = pygame.draw.rect(tela, (255, 0, 0), (208, 252, 245, 60))
        nome_format = fonte_nome.render(nome_texto, 0, (255, 150, 5))
        tela.blit(nome_format, (212, 265))

    # Quando o jogo estiver rodando
    elif estado == "jogo":
        tela.fill((0, 0, 0))
        tela.blit(img_arena, (0,0))
        # Exibe a pontuação
        mensagem = f"Pontos: {pontos}"
        texto_formatado = fonte.render(mensagem, 0, (255, 255, 255))
        tela.blit(texto_formatado, (10, 20))
        
        # Atualiza a posição da cobra
        x_cobra += x_controle
        y_cobra += y_controle
        
        #cobra = pygame.draw.rect(tela, (0, 255, 0), (x_cobra, y_cobra, 16, 16))
        #maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, 16, 16))
        cobra = tela.blit(img_corpo, (x_cobra, y_cobra))
        maca = tela.blit(img_maca, (x_maca, y_maca))
        
        # Colisão com a maçã
        if cobra.colliderect(maca):
            moeda_colisao.play()
            pontos += 1
            comprimento += 1
            # Loop para a maçã não ser gerada no corpo da cobra:
            while True:
                x_maca = random.randrange(x_arena, fim_x_arena, 16)
                y_maca = random.randrange(y_arena, fim_y_arena, 16)
                if [x_maca, y_maca] not in lista_cobra:
                    break
        # Atualiza a lista do corpo da cobra
        lista_cabeca = (x_cobra, y_cobra)
        lista_cobra.append(lista_cabeca)
        if len(lista_cobra) > comprimento:
            lista_cobra.pop(0)
        # Verifica colisão com o próprio corpo ou com as bordas
        if (lista_cobra.count(lista_cabeca) > 1 or x_cobra >= fim_x_arena or x_cobra < x_arena or y_cobra >= fim_y_arena or y_cobra < y_arena):
            estado = "game_over"
            adicionar_ranking() # Adicionar dados ao ranking
        aumenta_cobra(lista_cobra)


    # Game over
    elif estado == "game_over":
        tela.fill((0, 0, 0))
        tela.blit(img_gameover, (0,0))

        # Exibe a pontuação
        pontuacao = f'Pontuação: {pontos}'
        pontuacao_texto = fonte.render(pontuacao, 0, (0, 255, 0))
        tela.blit(pontuacao_texto, (250, 120))

        # Adicionarei dados ao ranking qnd apertar alguma tecla, se for no loop adiciona vários dados repetidos

    elif estado == "ranking":
        tela.blit(img_ranking, (0,0)) # Mostra a imagem do ranking

        #ler arquivo
        with open("ranking.txt", "r") as arquivo: # r de read, ler o arquivo
            linhas = arquivo.readlines()

        # Mostrar as linhas
        y_rank = 200
        for linha in linhas:
            linha_format = fonte.render(linha, 0, (255, 150, 5))
            tela.blit(linha_format, (120, y_rank))
            y_rank += 40

        
    elif estado == "creditos":
        tela.blit(img_creditos, (0, 0)) # mostra creditos na tela
        msg = "Pressione espaço para voltar ao menu!"
        msg_format = fonte_creditos.render(msg, 0, (0, 255, 0))
        tela.blit(msg_format, (110, 375))



    # Eventos (teclas, etc)
    for event in pygame.event.get():
        if event.type == QUIT:   # Quita do jogo se apertar no X
            pygame.quit()
            exit()

        if estado == "menu": # Teclas do menu
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    estado = "nome"
                    nome_texto = ''
                elif event.key == K_x:
                    estado = "creditos"
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
        
        # Nome do jogador (para o ranking)
        elif estado == "nome":
            if event.type == KEYDOWN:
                if event.key == K_RETURN: # Enter
                    estado = "jogo"
                    # Reinicializa as variáveis do jogo
                    x_cobra = (altura_arena / 2) - 16
                    y_cobra = (largura_arena / 2) - 16
                    x_maca = random.randrange(x_arena, fim_x_arena, 16)
                    y_maca = random.randrange(y_arena, fim_y_arena, 16)
                    x_controle = 16
                    y_controle = 0
                    velocidade = 16
                    comprimento = 3
                    lista_cobra = []
                    pontos = 0
                elif event.key == K_BACKSPACE:
                    nome_texto = nome_texto [:-1] # Remove ultima letra do nome se segurar backspace
                elif len(nome_texto) < 8:
                    nome_texto += event.unicode # adiciona qualquer outra tecla ao texto


        elif estado == "jogo": # Teclas do jogo
            if event.type == KEYDOWN:
                if event.key == K_a or event.key == K_LEFT:
                    if x_controle == velocidade:
                        pass
                    else:
                        x_controle = -velocidade # Velocidade negativa pois vai no sentido contrário do X
                        y_controle = 0
                        break
                elif event.key == K_d or event.key == K_RIGHT:
                    if x_controle == -velocidade:
                        pass
                    else:
                        x_controle = velocidade
                        y_controle = 0
                        break
                elif event.key == K_w or event.key == K_UP:
                    if y_controle == velocidade:
                        pass
                    else:
                        x_controle = 0
                        y_controle = -velocidade
                        break
                elif event.key == K_s or event.key == K_DOWN:
                    if y_controle == -velocidade:
                        pass
                    else:
                        x_controle = 0
                        y_controle = velocidade
                        break
        
        elif estado == "game_over": # Teclas da tela de game over
            if event.type == KEYDOWN:
                
                if event.key == K_r:
                    estado = "nome"
                    nome_texto = '' # Reinicia o nome

                elif event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                
                elif event.key == K_l:
                    estado = "ranking"

        elif estado == "ranking": # Teclas da tela de ranking
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    estado = "menu"
                elif event.key == K_BACKSPACE:
                    with open("ranking.txt", "w") as arquivo: # w = write, vai sobreescrever oq tem
                        arquivo.write("") # escreve nada, esvazia o arquivo
                

        elif estado == "creditos": # Teclas dos créditos
            if event.type == KEYDOWN and event.key == K_SPACE:
                estado = "menu"
    
    pygame.display.update()
