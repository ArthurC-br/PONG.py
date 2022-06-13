import pygame
from pygame.locals import *
from random import randint
import neat

pygame.init()

ia_jogando = True
geracao = 0

widht = 500
height = 400

fonte = pygame.font.SysFont('arial', 10, bold=True, italic=True)
pygame.display.set_caption('Pong do Turjin')
current = True

class Pong:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 60
        self.speed = 5
        self.altura = self.y

    def moveup(self):
        if self.x >= 0:
            self.x -= self.speed

    def movedown(self):
        if self.x <= widht - self.size:
            self.x += self.speed

    def make(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.size, 10))

class Ball:

    SIZE = 15

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = self.SIZE
        self.speedx = 0
        self.speedy = 5

    def move(self):
        self.y += self.speedy

    def make(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.size, self.size))

    def colide_height(self):
        if self.y >= height + 20:
            return True

    def colide_pong(self, pong):
        if self.x >= pong.x and self.x <= pong.x + 60 and self.y >= 385:
            self.y = -10
            self.x = randint(15, 385)
            return True

def make_screen(screen, pongs, balls, pontos):
    screen.fill((0, 0, 0))
    for pong in pongs:
        pong.make(screen)
    for ball in balls:
        ball.make(screen)

    mensagem = f'Pontos = {pontos}'
    texto_formatado = fonte.render(mensagem, True, (255, 255, 255))
    screen.blit(texto_formatado, (435, 10))
    if ia_jogando:
        mensagem = f'Geracao = {geracao}'
        texto_formatado = fonte.render(mensagem, True, (255, 255, 255))
        screen.blit(texto_formatado, (10, 10))
    pygame.display.flip()

def main(genomas, config):
    global screen, pong, ball, geracao, lista_genomas, redes
    geracao += 1

    if ia_jogando:
        redes = []
        lista_genomas = []
        pongs = []
        balls = []
        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            lista_genomas.append(genoma)
            pongs.append(Pong(widht // 2, 395))
            balls.append(Ball(randint(15, 385), 0))
    else:
        pongs = [Pong(widht // 2, 395)]
        balls = [Ball(randint(15, 385), 0)]
    screen = pygame.display.set_mode((widht, height))
    pontos = 0
    tick = pygame.time.Clock()


    current = True
    while current:
        tick.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if not ia_jogando:
            if pygame.key.get_pressed()[K_LEFT]:
                pong.moveup()
            if pygame.key.get_pressed()[K_RIGHT]:
                pong.movedown()
        if len(balls) > 0:
            pass
        else:
            current = False
            break

        for ball in balls:
            ball.move()

        for ball in balls:
            for i, pong in enumerate(pongs):
                if ball.colide_height():
                    pontos -= 2
                    if ia_jogando:
                        lista_genomas[i].fitness -= 5
                        lista_genomas.pop(i)
                        redes.pop(i)
                        balls.pop(i)
                        pongs.pop(i)
            for i, pong in enumerate(pongs):

                if ball.x >= pong.x and ball.x+15 <= pong.x + 60:
                    if ia_jogando:
                        lista_genomas[i].fitness += 0.1


                if ia_jogando:
                    output = redes[i].activate((pong.x, abs(pong.x - ball.x), abs(pong.y - ball.y)))
                    if output[0] > 0.5:
                            pong.moveup()
                    if output[0] < 0.5:
                        pong.movedown()

                if ball.colide_pong(pong):
                    if ia_jogando:
                        for genoma in lista_genomas:
                            genoma.fitness += 5
                    pontos += 5

        make_screen(screen, pongs, balls, pontos)

def rodar(caminho_config):
    config = neat.config.Config(neat.DefaultGenome,  neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, caminho_config)

    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())

    if ia_jogando:
        populacao.run(main, 50)
    else:
        main(None , None)

if __name__ == '__main__':
    rodar('config.txt')



