import random, os

import pygame
from pygame.locals import *

import main
from util import *


class Cloud:
    def __init__(self, image):
        self.image = pygame.image.load(os.path.join('data', 'scenery', image)).convert_alpha()
        self.xpos = random.randrange(640)
        self.ypos = random.randrange(300)
        self.speed = random.choice([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9])

    def draw(self, screen, paused=False):
        screen.blit(self.image, (self.xpos, self.ypos))
        if not paused:
            self.xpos -= self.speed
        if self.xpos < -self.image.get_width():
            self.xpos = 640
    



