import pygame

import main, locals
from util import *

class LevelSprite(pygame.sprite.Sprite):
    def __init__(self, centerPoint, image):
        pygame.sprite.Sprite.__init__(self) 
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = centerPoint

class Mushroom(LevelSprite):
    animcycle = 6
    speed = 2
    def __init__(self, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = load_images('Mushroom.png')
        self.image = self.images[0]
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.rect = self.image.get_rect(center = (self.x, self.y))    
        self.frame = 0
        self.immuneTimer = 10

    def update(self):
        self.immuneTimer -= 1
        if self.immuneTimer > 0:
            self.speed = 2
        self.image = self.images[self.frame/self.animcycle%1]        
        self.frame += 1
        self.rect.move_ip(self.speed, 0)
        if not pygame.sprite.spritecollide(self, self.platforms, 0):
            self.rect.top += 8
        for platform in pygame.sprite.spritecollide(self, self.platforms, 0):
            if self.rect.bottom <= platform.rect.bottom and self.rect.top >= platform.rect.top:
                self.speed = -self.speed
            else:
                self.rect.bottom = platform.rect.top


class FireFlower(LevelSprite):
    animcycle = 6
    speed = 2
    def __init__(self, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = load_images('Fire Flower 1.png', 'Fire Flower 2.png',
                                  'Fire Flower 3.png', 'Fire Flower 4.png')
        self.image = self.images[0]
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.rect = self.image.get_rect(center = (self.x, self.y))    
        self.frame = 0
        self.immuneTimer = 10

    def update(self):
        self.frame += 1
        self.image = self.images[self.frame/3%4]
        for platform in pygame.sprite.spritecollide(self, self.platforms, 0):
            self.rect.bottom -= 1


class Fireball(LevelSprite):
    animcycle = 6
    speed = 2
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = load_images('Fireball.png')
        self.image = self.images[0]
        self.orgImage = self.image.copy()
        self.x = player.rect[0]
        self.y = player.rect[1]
        if player.facing > 0:
            self.rect = self.image.get_rect(midleft = player.rect.midright)    
            self.speed = 6
        if player.facing < 0:
            self.rect = self.image.get_rect(midright = player.rect.midleft) 
            self.speed = -6
        self.frame = 0
        self.immuneTimer = 10
        self.yspeed = -5
        self.angle = 0
        self.sound = load_sound('fireball.wav')
        self.sound.play()

    def update(self):
        self.image = self.images[self.frame/self.animcycle%1]        
        self.frame += 1
        self.rect.move_ip(self.speed, -self.yspeed)
        self.yspeed -= 1
        for platform in pygame.sprite.spritecollide(self, self.platforms, 0):
            if self.rect.bottom <= platform.rect.bottom and self.rect.top >= platform.rect.top:
                self.kill()
            else:
                self.yspeed = 10
        self.rotate(15)
        if not locals.SCREENRECT.contains(self.rect):
            self.kill()

    def rotate(self, amount):
        self.oldCenter = self.rect.center
        self.angle -= -amount
        self.image = pygame.transform.rotate(self.orgImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.oldCenter
