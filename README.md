# Destroy Asteroids 
"Destroy Asteroids" é um jogo criado com Python e a biblioteca Pygame. O objetivo do jogo é dirigir uma nave espacial e destruir o maior número de asteroides possível, mantendo-se ao mesmo tempo em um caminho diferente para evitar colisões. Ao usar os tiros da nave para destruir os asteroides, o jogador ganha pontos. Quando a nave colide com um asteroide, o jogo termina. Em cada tentativa, o jogador pode tentar superar seu próprio recorde.
## Imagens

<p align="center">
<img src="https://img.itch.zone/aW1hZ2UvMjQxNDc3MC8xNDI5MjU3Mi5wbmc=/original/%2B7Alr6.png" alt="drawing" style="width:600px;"/>
<img src="https://img.itch.zone/aW1hZ2UvMjQxNDc3MC8xNDI5MjU3My5wbmc=/original/CulrRW.png" alt="drawing" style="width:600px;"/>
<img src="https://img.itch.zone/aW1hZ2UvMjQxNDc3MC8xNDI5MjU3NC5wbmc=/original/C%2BW%2Bbc.png" style="width:600px;"/>
</p>

## Jogabilidade

- Use as teclas de seta (ou W, S, A, D) para mover a nave para a esquerda, direita, cima e baixo.
- Pressione a tecla de espaço para atirar mísseis da nave.
- Evite colidir com os asteroides em movimento.
- Destrua os asteroides atirando neles para ganhar pontos.
- O jogo termina quando a nave colide com um asteroide.
- Pressione a tecla "x" para continuar após o fim do jogo e reiniciar.
## Componentes Principais
### Nave (Classe: Nave)
- Responsável por representar a nave que o jogador controla.
- É capaz de movimentar a nave em direções vertical e horizontal.
- Possui sprites que podem animar a nave em várias direções.
Exemplo de código fonte:
```python
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_nave = []
        for i in range(3):
            img = sprite_sheet.subsurface((i*32, 0), (32, 32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_nave.append(img)

        self.index_lista = 0
        self.image = self.imagens_nave[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA/2.1, ALTURA/1.4)
        self.velocidade = 20

    def mover_nave(self):
        keys = pygame.key.get_pressed()
        if keys[K_a] and comeca_jogo == True:
            self.rect.x -= self.velocidade
            if self.rect.x < 0 : self.rect.x = 0
        if keys[K_d] and comeca_jogo == True:
            self.rect.x += self.velocidade
            if self.rect.x > (LARGURA-95) : self.rect.x = (LARGURA-95)
        if keys[K_w] and comeca_jogo == True:
            self.rect.y -= self.velocidade
            if self.rect.y < ALTURA/2.5 : self.rect.y = ALTURA/2.5
        if keys[K_s] and comeca_jogo == True:
            self.rect.y += self.velocidade
            if self.rect.y > (ALTURA-95) : self.rect.y = (ALTURA-95)

    def update(self):
        self.mover_nave()
        if self.index_lista > 1:
            self.index_lista = 0
        self.index_lista += 0.5
        self.image = self.imagens_nave[int(self.index_lista)]

class Asteroide(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32*2, 0), (32, 32))
        self.image =   pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect =  self.image.get_rect()
        self.rect.center = (int(randint(25, LARGURA-25)), 0)
        self.mostrar_asteroide = int(randint(0, 20))
        self.velocidade = velocidade
        self.angulo = 40


    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y >= ALTURA:
            self.kill()
        self.mostrar_asteroide = int(randint(10, 40))

```
### Asteroide (Classe: Asteroide)

- Representa os asteroides que se movem na tela em direção à nave.
- Gera novos asteroides periodicamente durante o jogo.
- Colide com a nave, resultando no fim do jogo.
```python
class Missil(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32*3, 0), (32, 32))
        self.image =   pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect =  self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.velocidade = 20
    
    def update(self):
    
        self.rect.y -= self.velocidade
        if self.rect.y < 20:
            self.kill()
```
### Míssil (Classe: Missil)
- Representa os mísseis disparados pela nave para destruir os asteroides.
- Movimenta-se na direção vertical e colide com os asteroides.
```python
class Missil(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32*3, 0), (32, 32))
        self.image =   pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect =  self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.velocidade = 20
    
    def update(self):
    
        self.rect.y -= self.velocidade
        if self.rect.y < 20:
            self.kill()
```
