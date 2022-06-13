import pygame
from pygame.locals import *
pygame.init()

widht = 400
height = 400
size_pong = 50
size_ball = 10
x_pong = 2
y_pong = height//2
x_pong2 = 400-8
y_pong2 = height//2
x_ball = widht//2
y_ball = height//2
speedpong = 7
speed_ballx = 3
speed_bally = 5
pontos1 = 0
pontos2 = 0
fonte = pygame.font.SysFont('arial', 10, bold=True,italic=True)

tick = pygame.time.Clock()
screen = pygame.display.set_mode((widht, height))
pygame.display.set_caption('Pong do Turjin')
current = True

while current:
    mensagem = f'Pontos J1= {pontos1}'
    mensagem2 = f'Pontos J2= {pontos2}'
    texto_formatado = fonte.render(mensagem, True, (255, 255, 255))
    texto_formatado2 = fonte.render(mensagem2, True, (255, 255, 255))
    screen.fill((0, 0, 0))
    tick.tick(40)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            current = False
    if pygame.key.get_pressed()[K_w] and y_pong > 0:
        y_pong -= speedpong

    if pygame.key.get_pressed()[K_s] and y_pong < height-size_pong:
        y_pong += speedpong

    if pygame.key.get_pressed()[K_DOWN] and y_pong2 < height - size_pong:
        y_pong2 += speedpong
    if pygame.key.get_pressed()[K_UP] and y_pong2 > 0:
        y_pong2 -= speedpong
    x_ball += speed_ballx
    y_ball += speed_bally
    if x_ball > x_pong2:
        pontos1 = pontos1 + 1
        x_ball = widht//2
    if x_ball < x_pong:
        pontos2 = pontos2 + 1
        x_ball = widht//2
    pong = pygame.draw.rect(screen, (0, 255, 0),  (x_pong, y_pong, 6, size_pong))
    ball = pygame.draw.circle(screen, (255, 0, 0), (x_ball, y_ball), size_ball)
    pong2 = pygame.draw.rect(screen, (0, 255, 0), (x_pong2, y_pong2, 6, size_pong))
    screen.blit(texto_formatado, (20, 10))
    screen.blit(texto_formatado2, (315, 10))
    if ball.colliderect(pong) or ball.colliderect(pong2):
        speed_ballx = -speed_ballx
    if y_ball >= height-size_ball or y_ball <= 0 + size_ball:
        speed_bally = -speed_bally

    pygame.display.update()
print('Fim')