import pygame
import sys
import os
from pygame.locals import *

WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE * BLOCK_SIZE
HEIGHT = WORLD_SIZE * BLOCK_SIZE
SPEED = 2

COLOR = (255, 100, 98)
SURFACE_COLOR = (0, 0, 0)
# WIDTH = 500
# HEIGHT = 500
NUM_GHOSTS = 3

char_to_image = {
    '.' : "dot.png",
    '=' : "wall.png",
    '*' : "powerup.png",
    'g' : "ghost1.png",
    'G' : "ghost2.png",
}


class Player(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
    
        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)

        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()

    def move_right(self, pixels):
        self.rect.x += pixels
    
    def move_left(self, pixels):
        self.rect.x -= pixels

    # def move_forward(self, speed):
    #     self.rect.y += speed * speed/10
    
    # def move_backward(self, speed):
    #     self.rect.y -= speed * speed/10

    def move_up(self, pixels):
        self.rect.y += pixels

    def move_down(self, pixels):
        self.rect.y -= pixels

    def move(self, dx, dy, sprites):
        if dx != 0:
            self.move_single_axis(dx, 0, sprites)
        if dy != 0:
            self.move_single_axis(0, dy, sprites)
    
    def move_single_axis(self, dx, dy, sprites):
        self.rect.x += dx
        self.rect.y += dy

        for sprite in sprites:
            if self.rect.colliderect(sprite.rect):
                if sprite.type == '=':
                    if dx > 0:
                        self.rect.right = sprite.rect.left
                    if dx < 0:
                        self.rect.left = sprite.rect.right
                    if dy > 0:
                        self.rect.bottom = sprite.rect.top
                    if dy < 0:
                        self.rect.top = sprite.rect.bottom
                if sprite.type == '.':
                    sprite.kill()
                if sprite.type == '*':
                    sprites.remove(sprite)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)

        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()

def load_level(number):
    world = []
    file = os.path.join('./levels', 'level' + str(number) + '.txt')
    with open(file, 'r') as f:
        for line in f:
            row = []
            for block in line:
                row.append(block)
            world.append(row)
    return world

def draw_world(world):
    sprites = []
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            color = (0, 0, 0)
            size = BLOCK_SIZE, BLOCK_SIZE
            if block == '.':
                color = (255, 255, 255)
                size = BLOCK_SIZE // 2, BLOCK_SIZE // 2
            elif block == '=':
                color = (0, 0, 255)
            elif block == '*':
                color = (255, 0, 0)
            sprite = Sprite(color, size[0], size[1], block)
            sprite.rect.x = x * BLOCK_SIZE
            sprite.rect.y = y * BLOCK_SIZE
            sprites.append(sprite)
    return sprites


level = 1
world = load_level(level)
for row in world:
    print(row)

pygame.init()
pygame.display.set_caption("Packman")

speed = 10
clock = pygame.time.Clock()
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

all_sprites_list = pygame.sprite.Group()
sprites= draw_world(world)
pacman = Player((255, 255, 0), BLOCK_SIZE*0.75, BLOCK_SIZE*0.75)
pacman.rect.x = WIDTH // 2 - BLOCK_SIZE 
pacman.rect.y = HEIGHT // 2

all_sprites_list.add(sprites)
all_sprites_list.add(pacman)

exit = False

while not exit:
    direction = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                exit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                exit = True

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        pacman.move(-speed, 0, sprites)
    if key[pygame.K_RIGHT]:
        pacman.move(speed, 0, sprites)
    if key[pygame.K_DOWN]:
        pacman.move(0, speed, sprites)
    if key[pygame.K_UP]:
        pacman.move(0, -speed, sprites)

    all_sprites_list.update()
    screen.fill(SURFACE_COLOR)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

