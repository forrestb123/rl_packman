import pygame
from pygame.locals import *

COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
WIDTH = 500
HEIGHT = 500
NUM_GHOSTS = 3

class Sprite(pygame.sprite.Sprite):
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

    def move_forward(self, speed):
        self.rect.y += speed * speed/10
    
    def move_backward(self, speed):
        self.rect.y -= speed * speed/10

    # def move_up(self, pixels):
    #     self.rect.y += pixels

    # def move_down(self, pixels):
    #     self.rect.y -= pixels

pygame.init()

RED = (255, 0, 0)
BLUE = (0, 0, 255)

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sprite Example")

all_sprites_list = pygame.sprite.Group()

player1 = Sprite(RED, 20, 30)
player1.rect.x = 200
player1.rect.y = 300

ghosts = [Sprite(BLUE, 20, 30) for _ in range(NUM_GHOSTS)]
for i, ghost in enumerate(ghosts):
    ghost.rect.x = 100 + i * 50
    ghost.rect.y = 100 + i * 50

# player2 = Sprite(BLUE, 20, 30)

# player2.rect.x = 100
# player2.rect.y = 100

platform = Sprite(BLUE, 50, 200)
platform.rect.x = 100
platform.rect.y = 150

all_sprites_list.add(player1)
all_sprites_list.add(ghosts)
all_sprites_list.add(platform)

speed_a = 8
speed_bs = [-7 for _ in range(NUM_GHOSTS)]

exit = True
clock = pygame.time.Clock()

while exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                exit = False

    player1.rect.bottom += speed_a
    # player2.rect.top += speed_b
    for i, ghost in enumerate(ghosts):
        ghost.rect.top += speed_bs[i]
        collide = pygame.sprite.collide_rect(player1, ghost)
        if collide:
            speed_a *= -1
            speed_bs[i] *= -1

    collide_platform = pygame.sprite.collide_rect(player1, platform)

    if collide_platform:
        # if player1.rect.bottom >= platform.rect.top:
        #     player1.rect.bottom = platform.rect.top
        # elif player1.rect.top < platform.rect.bottom:
        #     player1.rect.top = platform.rect.bottom
        speed_a = 0

    if player1.rect.bottom > HEIGHT or player1.rect.top < 0 or player1.rect.right > WIDTH or player1.rect.left < 0:
        speed_a *= -1
    for i, ghost in enumerate(ghosts):
        if ghost.rect.bottom > HEIGHT or ghost.rect.top < 0 or ghost.rect.right > WIDTH or ghost.rect.left < 0:
            speed_bs[i] *= -1

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and player1.rect.left > 0:
        player1.move_left(10)
    if key[pygame.K_RIGHT] and player1.rect.right < WIDTH:
        player1.move_right(10)
    if key[pygame.K_DOWN] and player1.rect.bottom < HEIGHT:
        player1.move_forward(10)
    if key[pygame.K_UP] and player1.rect.top > 0:
        player1.move_backward(10)


    all_sprites_list.update()
    screen.fill(SURFACE_COLOR)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()