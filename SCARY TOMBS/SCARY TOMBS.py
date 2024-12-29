import pyxel as px
import random
import time
x = 92
y = 102
velocidade = 1
direcao = 1
pose = 0
morcegos = []
zumbis = []  
chancezb = 130
chancemor = 130
t = 100
espada = 0
cooldown = 0
estado = "basico"
pontos = 10
score = 0
#para fazer o menu
menu = 0
game = 1 
gameover = 2
estado_game = menu 


boss = False
boss2 = False
 
#SISTEMA DE COLISÃO

def espadacolisao():
    global score, pontos
    cor = [2, 3, 8]

    # Verifique a direção do ataque
    if estado == "direita":
        espada_x = x + 10  # Posição da espada quando atacando para a direita
    elif estado == "esquerda":
        espada_x = x - 10  # Posição da espada quando atacando para a esquerda
    elif estado == "cima":
        espada_x = y - 5 # Posição da espada quando atacando para cima
        espada_y = y - 10  # Posição da espada quando atacando para cima
    else:
        return False  # Se não estiver atacando na direção correta, não há colisão

    for c in cor:
        for zumbi in zumbis:
            if (estado == "direita" and zumbi["x"] > espada_x) or (estado == "esquerda" and zumbi["x"] < espada_x):
                continue

            if (espada_x < zumbi["x"] + 12 and espada_x + 10 > zumbi["x"] and y < 118 and y + 16 > 102):
                zumbis.remove(zumbi)
                score += pontos  # Ganhe pontos ao colidir com um zumbi

        for morcego in morcegos:
            if (estado == "cima" and espada_x < 108 and espada_x + 10 > 92 and espada_y < morcego["y"] + 20 and espada_y + 10 > morcego["y"]):
                morcegos.remove(morcego)
                score += pontos  # Ganhe pontos ao colidir com um morcego

    return False  # Não houve colisão com nenhum zumbi ou morcego



def colisao():
    cor = [2, 3, 8]
    for c in cor:
        if (px.pget(x + 7, y) == c or px.pget(x+2, y + 9) == c or px.pget(x + 7, y) == c or px.pget(x + 8, y + 8) == c or px.pget(x , y + 8) == c or px.pget(x + 7, y-1) == c or px.pget(x + 7, y+1) == c):
            return True
    
#PROCESSO PARA CRIAR ZUMBIS / MORCEGOS
def criar_morcego():
    y = -12
    morcegos.append({"y": y})

def criar_zumbi(direcao):
    global zumbiativo
    if direcao == -1:
        x = 202
    else:
        x = -12
    zumbi = {"x": x, "direcao": direcao}
    zumbis.append(zumbi)

def update():
    global velocidade, zumbis, morcegos, chancezb, chancemor, estado, cooldown, espada, boss, t, boss2, x, y, direcao, direita, zumbiativo, score, pontos, estado_game, menu, gameover, game, tempo_inicial
#FIM DE JOGO
    # FIM DE JOGO
    if estado_game == gameover:
        velocidade = 0
        if px.btn(px.KEY_R):
            estado_game = game
            x = 92
            y = 102
            morcegos.clear()
            zumbis.clear()
            score = 0
            tempo_inicial = time.time()
            t = 0
            boss = False
            boss2 = False
            velocidade = 1
            chancezb = 140
            chancemor = 140
            pontos = 10
            

    if estado_game == menu:
        morcegos.clear()
        zumbis.clear()
        if px.btn(px.KEY_E):
            estado_game = game
            x = 92
            y = 102
            # Defina 'tempo_inicial' como zero quando o jogo começar
            tempo_inicial = time.time()
            t = 0

    if estado_game == game:
        t = time.time() - tempo_inicial  # Atualize o tempo apenas quando o jogo começar
            

#AJUDAR A POSIÇÃO (VELOCIDADE)
    for morcego in morcegos:
        morcego["y"] += velocidade

    for zumbi in zumbis:
        if zumbi["direcao"] == -1:
            zumbi["x"] -= velocidade
        else:
            zumbi["x"] += velocidade

#REMOVER OS ZUMBIS / MORCEGOS
    zumbis = [zumbi for zumbi in zumbis if zumbi["x"] > -12 and zumbi["x"] < 202]
    morcegos = [morcego for morcego in morcegos if morcego["y"] < 150]
       
#VER SE TA NA HORA DE CRIAR OUTRO ZUMBI / MORCEGO
    if random.randint(0, chancezb) == 0:
        direcao_zumbi = random.choice([-1, 1])
        criar_zumbi(direcao_zumbi)
    if random.randint(0, chancemor) == 0:    
        criar_morcego()
        
#BGL DOS ATAQUES       
    if (px.btnp(px.KEY_RIGHT) or px.btnp(px.KEY_D)):
        estado = "direita"
        cooldown = 10  
        espada = 1
        direcao = 1
        if not espadacolisao():
            for zumbi in zumbis:
                if zumbi['x'] > 93 and zumbi['x'] < 114:
                    zumbi['x'] = 1000
                    score += pontos
                    
        
    elif px.btnp(px.KEY_LEFT) or px.btnp(px.KEY_A):
        estado = "esquerda"
        cooldown = 10
        espada = 1
        direcao = -1
        if not espadacolisao():
            for zumbi in zumbis:
                if zumbi['x'] > 68 and zumbi['x'] < 90:
                    zumbi['x'] = 1000
                    score += pontos
                    
        
    elif px.btnp(px.KEY_UP) or px.btnp(px.KEY_W):
        estado = "cima"
        cooldown = 10
        espada = 1
        if not espadacolisao():
            for morcego in morcegos:
                if morcego["y"] > 150 and morcego["y"] < 80:
                    morcegos.remove(morcego)
                    score += pontos
                    

#REDUZIR O COOLDOWN
    if cooldown > 0:
        cooldown -= 1
    else:
        estado = "basico"

    if t > 30:
        boss = True
        velocidade = 1.5
        chancezb = 75
        chancemor = 90
        pontos = 20
        
    if t > 60:
        velocidade = 1.5
        chancezb = 45
        chancemor = 65  
        pontos = 40
        
    if t > 90:
        boss2 = True
        boss = False
        velocidade = 2
        chancezb = 30
        chancemor = 50
        pontos = 60
        
    if t > 120:
        boss2 = True
        velocidade = 2
        chancezb = 15
        chancemor = 35
        pontos = 80
        
    if t > 150:
        boss2 = True
        velocidade = 2.5
        chancezb = 10
        chancemor = 25
        pontos = 100
        
    if t > 180:
        boss2 = True
        velocidade = 3
        chancezb = 7
        chancemor = 18
        pontos = 130
        
    if t > 210:
        boss2 = True
        velocidade = 3.5
        chancezb = 5
        chancemor = 15
        pontos = 150
        
        
        
#T0IRAR O BONECO DO MAPA CASO ALGM BATA NELE
        
        
    if colisao():
        x = -1000  
        y = -1000
        estado_game = gameover
        morcegos.clear()
        zumbis.clear()

def draw():
    global pose, direcao, x, y, estado, espada, t, boss, pontos, score, estado_game
    
    if estado_game == menu:
        px.cls(0)
        px.text(px.width // 2 - 22, 30, "SCARY TOMBS", 7)
        px.text(px.width // 2 - 46, 100, "APERTE 'E' PARA INICIAR", 7)
    if estado_game == game:
    
        if boss2 == False:
            px.blt(0, 0, 0, 0, 0, 192, 150)  # fundo
        else:
            px.cls(0)
        
    #BOSS 1 FASE
        if boss == True:

    # DESENHO DOS MORCEGOS DO BOSS
            for morcego in morcegos:
                if int(pose) == 0:
                    #      x,             y, img, u, v,  w,  h, transp
                    px.blt(89, morcego["y"],   1, 0, 17, 16, 16, 1)
                else:
                    px.blt(89, morcego["y"],   1,16, 16, 16, 16, 1)
                
    # DESENHO DOS ZUMBIS DO BOSS
            for zumbi in zumbis:
                if int(pose) == 0:
                    px.blt(zumbi["x"], 102, 1, 32, 16, 12*(-zumbi["direcao"]), 16, 1) 
                else:
                    px.blt(zumbi["x"], 102, 1, 44, 16, 12*(-zumbi["direcao"]), 16, 1)
            px.blt(56, 27, 1, 56, 16, 16, 16, 1)
            px.blt(120, 27, 1, 56, 16, -16, 16, 1)

            pose = pose + 0.2
            if pose > 2:
                pose = 0
                
    #BOSS FINAL
        elif boss2 == True:

            for morcego in morcegos:
                if int(pose) == 0:
                    #      x,             y, img, u, v,  w,  h, transp
                    px.blt(89, morcego["y"],   1, 0, 16, 16, 16, 1)
                else:
                    px.blt(89, morcego["y"],   1,16, 16, 16, 16, 1)
                
            for zumbi in zumbis:
                if int(pose) == 0:
                    px.blt(zumbi["x"], 102, 1, 32, 16, 12*(-zumbi["direcao"]), 16, 1) 
                else:
                    px.blt(zumbi["x"], 102, 1, 44, 16, 12*(-zumbi["direcao"]), 16, 1)
            px.blt(56, 27, 1, 56, 16, 16, 16, 1)
            px.blt(120, 27, 1, 56, 16, -16, 16, 1)
            px.blt(49, 60,1,17,49,96,26,1) 

            pose = pose + 0.25
            if pose > 2:
                pose = 0
        else:
    # DESENHO DOS MORCEGOS
            for morcego in morcegos:
                if int(pose) == 0:
                    px.blt(89, morcego["y"], 1, 0, 0, 16, 16, 1)
                else:
                    px.blt(89, morcego["y"], 1, 16, 0, 16, 16, 1)
                
    # DESENHO DOS ZUMBIS
            for zumbi in zumbis:
                if int(pose) == 0:
                    px.blt(zumbi["x"], 102, 1, 32, 0, 12*(-zumbi["direcao"]), 16, 1) 
                else:
                    px.blt(zumbi["x"], 102, 1, 44, 0, 12*(-zumbi["direcao"]), 16, 1)
            pose = pose + 0.1
            if pose > 2:
                pose = 0
                
                
                

    # ATAQUES
        if estado == "direita":
            px.blt(x, y, 1, 56, 0, 10, 16, 1)  # personagem

            if espada == 1:
                px.blt(x + 10, y + 1, 1, 96, 1, 10, 12, 1)  
            elif espada > 1:
                px.blt(x + 10, y + 1, 1, 106, 1, 10, 12, 1)
                
            espada += 0.1
            if espada > 3:
                espada = 0
                
        elif estado == "esquerda":
            px.blt(x, y, 1, 56, 0, -10, 16, 1)  # personagem  

            if espada == 1:
                px.blt(x-10, y + 1, 1, 96, 1, -10, 12, 1) 
            elif espada > 1:
                px.blt(x-10, y + 1, 1, 106, 1, -10, 12, 1)  

            espada += 0.1
            if espada > 5:
                espada = 0
                
        elif estado == "cima":

            if espada == 1:
                px.blt(x, y-4, 1, 76, 0, 10, 16, 1)  # personagem
                px.blt(x + 7, y - 14, 1, 86, 0, 6, 12, 1)
            elif espada == 2:
                px.blt(x, y-8, 1, 76, 0, 10, 16, 1)  # personagem
                px.blt(x + 7, y - 14, 1, 86, 0, 6, 12, 1)
            elif espada == 3:
                px.blt(x, y-4, 1, 76, 0, 10, 16, 1)  # personagem
                px.blt(x + 7, y - 14, 1, 86, 0, 6, 12, 1) 
            else:
                px.blt(x, y-1, 1, 76, 0, 10, 16, 1)  # personagem
                px.blt(x +9, y -6, 1, 93, 0, 3, 12, 1)  

            espada += 0.1
            if espada > 4:
                espada = 0
                
                
        elif estado == "basico":
            if direcao == -1:
                #      x, y, img, u, v, w, h, transp
                px.blt(x, y, 1, 66, 0, -10, 16, 1)  # personagem
                px.blt(x-3, y, 1, 93, 0, -3, 10, 1)  # espada
            else:
                px.blt(x, y, 1, 66, 0, 10, 16, 1)  # personagem
                px.blt(x+10, y, 1, 93, 0, 3, 10, 1)  # espada
            
        px.text(20, 6, 'Time = ' + str(round(t,1)), 7)
        px.text(130, 6, 'Score = ' + str(round(score,1)),7)
        
    if estado_game == gameover:
        px.cls(0)
        px.text(px.width // 2 - 22, px.height // 2 - 50, "FIM DE JOGO", 8)
        px.text(px.width // 2 - 50, px.height // 2 + 20 , "APERTE 'R' PARA REINICIAR", 7)
        px.text(px.width // 2 - 55, px.height // 2 , 'SEU SCORE FOI DE ' + str(round(score,1)) + ' PONTOS',  7)

px.init(192, 150, title='SCARY TOMBS', fps=60)
px.image(0).load(0, 0, 'cenario.png')
px.image(1).load(0, 0, 'sprites.png')
px.run(update, draw)
