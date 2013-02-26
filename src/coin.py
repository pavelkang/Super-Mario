import pygame
from util import *

class LevelSprite(pygame.sprite.Sprite):
    def __init__(self, centerPoint, image):
        pygame.sprite.Sprite.__init__(self) 
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = centerPoint

class Coin(LevelSprite):
    animcycle = 4
    def __init__(self, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = load_images('coin 1.png', 'coin 2.png',
                                  'coin 3.png' ,'coin 4.png')
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = centerPoint).move(4, 0)
        self.frame = 0

    def update(self):
        self.image = self.images[self.frame/self.animcycle%4]
        self.frame += 1  

class CoinUp(pygame.sprite.Sprite):
    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = load_images('coin 1.png', 'coin 2.png',
                                  'coin 3.png' ,'coin 4.png')
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = actor.rect.center)
        self.frame = 0
        self.life = 10
        self.frame = 4

    def update(self):
        self.image = self.images[self.frame/4%4]
        self.frame += 1
        self.rect.move_ip(0, -8)
        self.life -= 1
        if self.life <= 0:
            self.kill()
