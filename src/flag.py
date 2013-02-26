import pygame
import util
from locals import *

class LevelSprite(pygame.sprite.Sprite):
    def __init__(self, centerPoint, image):
        pygame.sprite.Sprite.__init__(self) 
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = centerPoint

        
class Flag(LevelSprite):
    def __init__(self, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = util.load_tile('Flag.png')
        self.rect = self.image.get_rect(midleft = centerPoint).move(6, 0)

    def update(self):
        for p in pygame.sprite.spritecollide(self, self.platforms, 0):
            self.rect.bottom = p.rect.top
