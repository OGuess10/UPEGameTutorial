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

# add player and platform classes
# --------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        # create a surface object with fixed size
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255,255,0)) # we fill them with a color, yellow. RGB
        self.rect = self.surf.get_rect() # create a rectangle object from the surface

        self.pos = vec((10, 360)) # starting position, vel, and acc
        self.vel = vec(0,0) # 2-d vectors, so along x and along y
        self.acc = vec(0,0)
        self.jumping = False

    def move(self):
        self.acc = vec(0,0.5) # starting acceleration with vertical acceleration
        pressed_keys = pygame.key.get_pressed()    
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC 
        self.acc.x += self.vel.x * FRIC # friction decrease velocity so player can de-accelerate
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # screen warping-- aka player can go to left side of screen and pop up on right
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos # update the rect object of player to new position after movement

    # def update(self):
    #     hits = pygame.sprite.spritecollide(self, platforms, False)
    #     if hits:
    #         self.vel.y = 0
    #         self.pos.y = hits[0].rect.top + 1

    def update(self):
        # check if sprite has hit another sprite, so player hits platform
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
    
    def jump(self):
        # collide so that player can't double jump. can only jump if touching playform
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15 # player goes up
 
    # the longer you hold the space bar, the more you jump
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100),12))
        self.surf.fill((0,255,0))
        #self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
        # add this later
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),random.randint(0,HEIGHT-30)))
    
    def move(self):
        pass

# this is to check if platforms are placed too close together
# takes newly generated platform as input and groupies, sprite group of all platforms
# we check if the platform collides
# we check if there are platforms nearby
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False

# added later
# random plate generation. this will generate new platforms above the screen
# when the player moves up, the screen shifts and the platforms become visible
def plat_gen():
    while len(platforms) < 7 : # when there are less than 7 platforms on screen
    # when I set this value at 6 instead of 7, new platform doesn't generate until player has reached HEIGHT / 3 on screen, so player could not move up to next platform in single jump
        width = random.randrange(50,100) # assigns random width for platform
        p  = platform()      
        C = True
        while C:           
             p = platform()
             p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
                             # creates platform right above visible part of screen
             C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p) # add platforms to both sprite groups

# --------------------------------------
 
PT1 = platform()
P1 = Player()

#add this later
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT-10))

# add sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

# add platform sprite group later
platforms = pygame.sprite.Group()
platforms.add(PT1)

# add this later
# generate platforms to add in random positions
for x in range(random.randint(4,5)):
    C = True
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)

#now game loop
while True:
    
    for event in pygame.event.get():
        #when x button is clicked, exit game
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # add this later
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    # add later
    # game moves up as player jumps
    if P1.rect.top <= HEIGHT/3: # check position of player with respect to the screen
        P1.pos.y += abs(P1.vel.y) # now we update position of player as screen moves
        # now we need to update all the other platforms as well
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill() # destroys any platform that goes off screen at the bottom, otherwise the number of platforms would keep adding up and would slow down the game

    # add later
    # game over screen
    if P1.rect.top > HEIGHT: # once player has gone below the screen
        for entity in all_sprites: # loop which kills each sprite
            entity.kill()
            time.sleep(1)
            displaysurface.fill((255,0,0)) # fill screen with red
            pygame.display.update()
            time.sleep(1) # wait one second then game exits
            pygame.quit()
            sys.exit()

    #aadd this later
    plat_gen()

    # refresh screen every iteration
    displaysurface.fill((0,0,0))

    # draw each sprite to the screen
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        # add this later
        entity.move()

    # add this later
    P1.update()
    
    # add new PT1.surf code

    # add entity.move to display sprites

    # now show game with moving square

    # add platforms sprite group

    # add P1.update() after display sprites

    # show game now

    # add player jump event to game event

    # now randomize platform self.rect

    # add for x in range(randomerkg)... for platforms

    # add if P1.rect.top <= HEIGHT ...

    # add platform gen function
    # add plat_gen to game loop

    # add if P1.rect.top > HEIGHT function for game over

    # push all changes to the screen and update
    pygame.display.update()
    FramePerSec.tick(FPS)