import pygame

import main
from util import *
from music import *

class LevelSprite(pygame.sprite.Sprite):
    def __init__(self, centerPoint, image):
        pygame.sprite.Sprite.__init__(self) 
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = centerPoint

class BaddieBoundary(LevelSprite):
    def __init__(self, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((16,16))
        self.image.fill((0, 0, 0))
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

class BaddieSpawnPoint(LevelSprite):
    def __init__(self, world, baddie, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((16,16))
        self.image.fill((0, 0, 0))
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.world = world
        self.baddie = baddie

    def update(self):
        if self.rect.left <= main.SCREENRECT.right and self.alive():
            if self.baddie == 1:
                Goomba(self.world, self.rect.center)
            if self.baddie == 2:
                Koopa(self.rect.center)
            self.kill()

class Goomba(LevelSprite):
    animcycle = 6
    speed = -2
    def __init__(self, world, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = load_images('goomba 1 w-%d.png' % world, 'goomba 2 w-%d.png' % world)
        self.image = self.images[0]
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.rect = self.image.get_rect(topleft = (self.x, self.y))    
        self.frame = 0       

    def update(self):
        self.image = self.images[self.frame/self.animcycle%2]        
        self.frame += 1
        self.rect.move_ip(self.speed, 0)
        if not pygame.sprite.spritecollide(self, self.platforms, 0):
            self.rect.top += 8
        for platform in pygame.sprite.spritecollide(self, self.platforms, 0):
            if self.rect.bottom <= platform.rect.top + 10:
                self.rect.bottom = platform.rect.top
            else:
                if self.speed >= 1:
                    self.rect.right = platform.rect.left
                if self.speed <= -1:
                    self.rect.left = platform.rect.right
                self.speed = -self.speed
        for d in pygame.sprite.spritecollide(self, self.dirpoints,0):
            if self.speed >= 1:
                self.rect.right = d.rect.left
            if self.speed <= -1:
                self.rect.left = d.rect.right
            self.speed = -self.speed

class Koopa(LevelSprite):
    animcycle = 6
    speed = -1
    def __init__(self, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = load_images('Green Koopa 1.png', 'Green Koopa 2.png')
        self.images2 = load_images('Green Koopa 1.png', 'Green Koopa 2.png')
        self.images2[0] = pygame.transform.flip(self.images2[0], 1, 0)
        self.images2[1] = pygame.transform.flip(self.images2[1], 1, 0)
        self.image = self.images[0]
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.rect = self.image.get_rect(topleft = (self.x, self.y))    
        self.frame = 0       

    def update(self):
        if self.speed < 0:
            self.image = self.images[self.frame/self.animcycle%2]        
        if self.speed > 0:
            self.image = self.images2[self.frame/self.animcycle%2]
        self.frame += 1
        self.rect.move_ip(self.speed, 0)
        self.rect.top += 3
        for platform in pygame.sprite.spritecollide(self, self.platforms, 0):
            if self.rect.bottom <= platform.rect.top + 10:
                self.rect.bottom = platform.rect.top
            else:
                self.speed = -self.speed
        for d in pygame.sprite.spritecollide(self, self.dirpoints,0):
            if self.speed >= 1:
                self.rect.right = d.rect.left
            if self.speed <= -1:
                self.rect.left = d.rect.right
            self.speed = -self.speed

class Goombadie(pygame.sprite.Sprite):
    defaultlife = 20
    animcycle = 3
    images = []
    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image('goomba dead w-%d.png' % main.BG, -1)
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = self.defaultlife

    def update(self):
        self.life = self.life - 1
        if self.life <= 0:
            self.kill()


class Koopashell(pygame.sprite.Sprite):
    defaultlife = 20
    animcycle = 3
    images = []
    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image('Green Shell.png', -1)
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = self.defaultlife
        self.speed = 0

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.colliderect(self.player.rect):
            stomp_sound.play()
            if self.player.speed > 0:
                self.speed = self.player.speed + 1
            if self.player.speed < 0:
                self.speed = self.player.speed - 1
            if self.player.jumping == True:
                self.player.rect.bottom = self.rect.top - 2
                self.player.jump_speed = 3
        if not pygame.sprite.spritecollide(self, self.platforms, 0):
            self.rect.top += 3
        for platform in pygame.sprite.spritecollide(self, self.platforms, 0):
            if self.rect.bottom <= platform.rect.top + 10:
                self.rect.bottom = platform.rect.top
            else:
                self.speed = -self.speed
        self.life = self.life - 1
        if self.life > 0:
            self.speed = 0
