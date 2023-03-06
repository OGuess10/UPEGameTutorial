import sys
import random
import time
import pygame
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

# set screen height and width
HEIGHT = 450
WIDTH = 400
# gravity constants for later
ACC = 0.5
FRIC = -0.12
# frames per second
FPS = 60
 
# set up clock
FramePerSec = pygame.time.Clock()
 
# display the window and set the title to game
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect()

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100),12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
    
    def move(self):
        pass

PT1 = platform()
P1 = Player()

# add sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

# game loop
while True:
    
    for event in pygame.event.get():
        #when x button is clicked, exit game
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # display background color
    displaysurface.fill((0,0,0))

    #display the sprites
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)
