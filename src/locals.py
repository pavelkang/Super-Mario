import pygame
from pygame.locals import *
pygame.init()

SCREENRECT = pygame.Rect(0, 0, 256*2, 240*2)

FPS = 50

SCORE = 0
COINS = 0
LEVEL = 1
WORLD = 1
TIME  = 200
LIVES = 5

def handle_input1():
    
    MOVE_KEYS = (K_LEFT, K_RIGHT)
    JUMP_KEY  = K_SPACE
    MENU_KEYS = (K_UP, K_DOWN, K_RETURN)
    RUN_KEY   = K_DOWN
    THROW_KEY = K_LCTRL

def handle_input2(keystate):
    
    MOVE_KEYS = (keystate[K_LEFT], keystate[K_RIGHT])
    JUMP_KEY  = keystate[K_SPACE]
    MENU_KEYS = (keystate[K_UP], keystate[K_DOWN], keystate[K_RETURN])
    RUN_KEY   = keystate[K_DOWN]
    THROW_KEY = keystate[K_LCTRL]

playerlayer = pygame.sprite.RenderUpdates()
innerlayer  = pygame.sprite.RenderUpdates()
middlelayer = pygame.sprite.RenderUpdates()
outerlayer  = pygame.sprite.RenderUpdates()

sprites         = pygame.sprite.Group()
platforms       = pygame.sprite.Group()
allplatforms    = pygame.sprite.Group()
topplatforms    = pygame.sprite.Group()
middleplatforms = pygame.sprite.Group()
platforms2      = pygame.sprite.Group()
platforms3      = pygame.sprite.Group()
questionblocks  = pygame.sprite.Group()
coins           = pygame.sprite.Group()
flags           = pygame.sprite.Group()
dirpoints       = pygame.sprite.Group()
goombas         = pygame.sprite.Group()
blocks          = pygame.sprite.Group()
mushrooms       = pygame.sprite.Group()
koopas          = pygame.sprite.Group()
shells          = pygame.sprite.Group()
fireflowers     = pygame.sprite.Group()
fireballs       = pygame.sprite.Group()
rotodisks       = pygame.sprite.Group()
