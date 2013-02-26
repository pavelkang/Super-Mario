import pygame

import main
from util import *
from platforms import *

class Rotodisk(pygame.sprite.Sprite):
    def __init__(self, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image('Roto Disk.png')
        self.oldImage = self.image.copy()
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.rect = self.image.get_rect(midleft = (self.x, self.y)).move(8, 16)
        Object('Empty Block', True, True, (self.x, self.y))
        self.angle = 0

    def update(self):
        self.oldCenter = self.rect.center
        self.angle -= 3
        self.image = pygame.transform.rotate(self.oldImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.oldCenter
