import pygame
import sys
import os
from pygame.locals import *

WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE * BLOCK_SIZE
HEIGHT = WORLD_SIZE * BLOCK_SIZE
SPEED = 2

char_to_image = {
    '.' : "dot.png",
    '=' : "wall.png",
    '*' : "powerup.png",
    'g' : "ghost1.png",
    'G' : "ghost2.png",
}

class Player:
    def __init__(self, screenheight, screenwidth, imagefile):
        self.shape = pygame.image.load(imagefile)
        self.top = screenheight - self.shape.get_height()
        self.left = screenwidth/2
        self.speed = SPEED

    def show(self, surface):
        surface.blit(self.shape, (self.left, self.top))

    def update_coords(self, x):
        self.left = x - self.shape.get_width()/2

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

def draw(screen, world):
    screen.clear()
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            imagefile = char_to_image[block]
            image = pygame.image.load(os.path.join('./sprites', imagefile))
            screen.blit(image, (x*32, y*32))

pacman = pygame.image.load(os.path.join('./sprites', 'pacman_o.png'))

level = 1
world = load_level(level)
for row in world:
    print(row)

# pygame.init()
# clock = pygame.time.Clock()
# screenwidth, screenheight = (480, 600)
# screen = pygame.display.set_mode((screenwidth, screenheight))

# framerate = 60
# bg_speed = 100

# background = ScrollingBackground(screenheight, os.path.join('./backgrounds', 'space_bg.jpg'))
# player = Player(screenheight, screenwidth, os.path.join('./sprites', 'pacman.png'))

# pygame.mouse.set_visible(0)
# pygame.display.set_caption('Pacman')

# while True:
#     time = clock.tick(framerate)/1000.0
#     x, y = pygame.mouse.get_pos()
#     player.update_coords(x)
#     player.show(screen)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             print("Exiting...")
#             sys.exit()
    
    
#     background.update_coords(bg_speed, time)
#     background.show(screen)
#     pygame.display.update()
