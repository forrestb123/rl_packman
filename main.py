import pygame
import sys
import os
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 480))

bg = pygame.image.load(os.path.join('./background', 'background.png'))

pygame.mouse.set_visible(0)
pygame.display.set_caption('Pacman')

while True:
    clock.tick(60)
    screen.blit(bg, (0, 0))
    x, y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()
