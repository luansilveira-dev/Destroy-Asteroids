import pygame
from random import randint
from pygame.locals import *
from db_utils import *
from sys import exit
import os

dados = verDados()
record = dados[0][0]

pygame.init()

pasta_principal = os.path.dirname(__file__)
pasta_imagens = os.path.join(pasta_principal, "imagens")
pasta_sons = os.path.join(pasta_principal, "sons")


# LARGURA = 720 , ALTURA = 560
LARGURA = 670
ALTURA = 560

print(LARGURA)
print(ALTURA)

BRANCO = (255, 255, 255)


janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Destroy Asteroids")

## Sprite do Jogo
sprite_sheet = pygame.image.load(
    os.path.join(pasta_imagens, "naveSpritesheet.png")
).convert_alpha()
spriteFundo = pygame.image.load(os.path.join(pasta_imagens, "fundo.png"))

## Esfeitos Sonoros do Jogo
sons_shot = pygame.mixer.Sound(os.path.join(pasta_sons, "retroShot.wav"))
sons_shot.set_volume(0.2)
sons_collide = pygame.mixer.Sound(os.path.join(pasta_sons, "death_sound.wav"))
sons_collide.set_volume(1)

## Musicas do jogo ###
musicaBatalha = pygame.mixer.Sound(os.path.join(pasta_sons, "m2.mp3"))
pygame.mixer.music.load(os.path.join(pasta_sons, "m3.mp3"))
pygame.mixer.music.play(-1)

## Icon do Jogo
icon = sprite_sheet.subsurface((64, 0), (32, 32))
pygame.display.set_icon(icon)

musica = False
batalha = False
comeca_jogo = False
velocidade = 10
pontos = 0
nave_colidiu = False
conte_tempo = 0
tempo_maximo = 500


def reiniciar_jogo():
    global velocidade, pontos, nave_colidiu, conte_tempo, colm, musica, batalha
    musica = False
    batalha = False
    velocidade = 10
    pontos = 0
    nave_colidiu = False
    conte_tempo = 0
    nave.rect.center = (LARGURA / 2.1, ALTURA / 1.4)


def mensagens(msg, tamanho_fonte, cor, negrito):
    fonte = pygame.font.SysFont("comicsansms", tamanho_fonte, negrito, False)
    mensagem = f"{msg}"
    texto = fonte.render(mensagem, True, cor)
    return texto


class Nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_nave = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_nave.append(img)

        self.index_lista = 0
        self.image = self.imagens_nave[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA / 2.1, ALTURA / 1.4)
        self.velocidade = 20

    def mover_nave(self):
        keys = pygame.key.get_pressed()
        if keys[K_a] and comeca_jogo == True:
            self.rect.x -= self.velocidade
            if self.rect.x < 0:
                self.rect.x = 0
        if keys[K_d] and comeca_jogo == True:
            self.rect.x += self.velocidade
            if self.rect.x > (LARGURA - 95):
                self.rect.x = LARGURA - 95
        if keys[K_w] and comeca_jogo == True:
            self.rect.y -= self.velocidade
            if self.rect.y < ALTURA / 2.5:
                self.rect.y = ALTURA / 2.5
        if keys[K_s] and comeca_jogo == True:
            self.rect.y += self.velocidade
            if self.rect.y > (ALTURA - 95):
                self.rect.y = ALTURA - 95

    def update(self):
        self.mover_nave()
        if self.index_lista > 1:
            self.index_lista = 0
        self.index_lista += 0.5
        self.image = self.imagens_nave[int(self.index_lista)]


class Asteroide(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32 * 2, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.center = (int(randint(25, LARGURA - 25)), 0)
        self.mostrar_asteroide = int(randint(0, 20))
        self.velocidade = velocidade
        self.angulo = 40

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y >= ALTURA:
            self.kill()
        self.mostrar_asteroide = int(randint(10, 40))


class Missil(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32 * 3, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.velocidade = 20

    def update(self):

        self.rect.y -= self.velocidade
        if self.rect.y < 20:
            self.kill()


class Fundo(pygame.sprite.Sprite):
    def __init__(self, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = spriteFundo
        self.image = pygame.transform.scale(self.image, (160 * 5, 160 * 5))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = pos_y
        self.velocidade = velocidade

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y >= ALTURA:
            self.rect.y = -self.rect.height


todas_as_sprite = pygame.sprite.Group()
grupo_inimigos = pygame.sprite.Group()
grupo_missil = pygame.sprite.Group()
grupoMenu = pygame.sprite.Group()


fundo1 = Fundo(0)
fundo2 = Fundo(-ALTURA)


todas_as_sprite.add(fundo1, fundo2)
nave = Nave()
todas_as_sprite.add(nave)

grupoMenu.add(fundo1, fundo2, nave)

relogio = pygame.time.Clock()
while True:
    relogio.tick(30)
    janela.fill(BRANCO)

    asteroide = Asteroide()
    missil = Missil(nave.rect.x + 45, nave.rect.y)
    grupo_inimigos.add(asteroide)

    if asteroide.mostrar_asteroide == 0 and nave_colidiu == False:
        todas_as_sprite.add(asteroide)

    elif nave_colidiu:
        for inimigo in grupo_inimigos:
            inimigo.kill()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and nave_colidiu == False:
                if len(grupo_missil) < 4:
                    sons_shot.play()
                    todas_as_sprite.add(missil)
                    grupo_missil.add(missil)
                    for asteroide in grupo_inimigos:
                        for missil in grupo_missil:
                            if missil.rect.colliderect(asteroide.rect):
                                pontos += 1
                                asteroide.kill()
                                missil.kill()
                                sons_collide.play()

            if event.key == pygame.K_x and nave_colidiu == True:
                reiniciar_jogo()
                if comeca_jogo == False:
                    comeca_jogo = True
                    nave_colidiu = False
            elif event.key == pygame.K_z and nave_colidiu == True:
                reiniciar_jogo()
                comeca_jogo = False

    if comeca_jogo == False:
        grupoMenu.draw(janela)
        tituloJogo = mensagens("Destroy Asteroids", 45, (0, 0, 0), True)
        comeca = mensagens("Start - x", 35, (0, 0, 0), False)
        janela.blit(comeca, (LARGURA / 2.5, ALTURA / 2.5))
        janela.blit(tituloJogo, (LARGURA / 4.3, ALTURA / 6.5))
        nave_colidiu = True
        grupoMenu.update()

    if comeca_jogo:
        for asteroide in grupo_inimigos:
            if nave.rect.colliderect(asteroide.rect):
                nave_colidiu = True

        texto_pontos = mensagens(f"Score : {pontos}", 35, (0, 0, 0), False)
        texto_record = mensagens(f"HI : {record}", 30, (0, 0, 0), False)

        if not batalha:
            pygame.mixer.music.pause()
            musicaBatalha.play(-1)
            batalha = True

        if nave_colidiu:
            atualizarDados([record, pontos])
            game_over = mensagens("GAME OVER", 70, (0, 0, 0), True)
            continuar = mensagens("Continue - x", 35, (0, 0, 0), False)
            sair = mensagens("Quit - y", 33, (0, 0, 0), False)
            janela.blit(game_over, (LARGURA / 4.9, ALTURA / 3))

            janela.blit(continuar, ((LARGURA / 4.5) + 100, (ALTURA / 3) + 120))
            janela.blit(sair, ((LARGURA / 4.5) + 135, (ALTURA / 3) + 180))
            janela.blit(texto_pontos, (LARGURA - 250, 10))
            janela.blit(texto_record, (50, 10))
            if not musica:
                musicaBatalha.stop()
                pygame.mixer.music.play(-1)
                musica = True

        else:
            todas_as_sprite.draw(janela)
            janela.blit(texto_pontos, (LARGURA - 250, 10))
            janela.blit(texto_record, (50, 10))
        todas_as_sprite.update()
        conte_tempo += 1
        if conte_tempo % tempo_maximo == 0:
            if velocidade >= 30:
                velocidade += 0
            else:
                velocidade += 2
            conte_tempo = 0

        if pontos >= record:
            record = pontos

    pygame.display.flip()
