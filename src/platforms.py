import pygame
import util
from locals import *
import main

class LevelSprite(pygame.sprite.Sprite):
    def __init__(self, centerPoint, image):
        pygame.sprite.Sprite.__init__(self) 
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = centerPoint

class Ground(LevelSprite):
    def __init__(self, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = util.load_tile('Ground.png')
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

class Object(LevelSprite):
    def __init__(self, image, landable, hittable, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = util.load_tile(image + '.png')
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.oldy = centerPoint[1]
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.bouncespeed = 0
        self.bouncing = False
        self.landable = landable
        self.hittable = hittable

    def update(self):
        self.rect.top += self.bouncespeed
        if self.bouncing:
            if self.bouncespeed < 5:
                self.bouncespeed += 0.75
            if self.bouncespeed >= 5:
                self.rect.top = self.oldy
        if self.bouncespeed >= 5:
            self.bouncing = False
            self.rect.top = self.oldy

    def bounce(self):
        self.bouncespeed = -4
        self.bouncing = True

class Object2(LevelSprite):
    def __init__(self, image, landable, hittable, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = util.load_tile(image + '.png')
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.landable = landable
        self.hittable = hittable

class Object3(LevelSprite):
    def __init__(self, image, landable, hittable, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = util.load_tile(image + '.png')
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.landable = landable
        self.hittable = hittable

class Object4(LevelSprite):
    def __init__(self, image, xspeed, yspeed, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = util.load_tile(image + '.png')
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.xspeed = xspeed
        self.yspeed = yspeed

    def update(self):
        self.rect.move_ip(self.xspeed, self.yspeed)
        if self.yspeed > 0:
            if self.rect.top >= SCREENRECT.bottom:
                self.rect.bottom = SCREENRECT.top
        if self.yspeed < 0:
            if self.rect.bottom <= SCREENRECT.top:
                self.rect.top = SCREENRECT.bottom

class Scenery(LevelSprite):
    def __init__(self, image, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = util.load_tile(image + '.png')
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

class QuestionBlock(LevelSprite):
    def __init__(self, type, centerPoint):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = []
        self.images.append(util.load_tile('Question Block 1.png'))
        self.images.append(util.load_tile('Question Block 2.png'))
        self.images.append(util.load_tile('Question Block 3.png'))
        self.image = self.images[2]
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        self.oldy = centerPoint[1]
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.frame = 0
        self.hit = False
        self.bouncespeed = 0
        self.bouncing = False
        self.type = type
        self.landable = True
        self.hittable = True

    def update(self):
        self.frame += 1
        if self.hit == False:
            self.image = self.images[self.frame/5%3]
        self.rect.top += self.bouncespeed
        if self.bouncing:
            if self.bouncespeed < 5:
                self.bouncespeed += 0.75
            if self.bouncespeed >= 5:
                self.rect.top = self.oldy
        if self.bouncespeed >= 5:
            self.bouncing = False
            self.rect.top = self.oldy

    def bounce(self):
        self.bouncespeed = -4
        self.bouncing = True


class BrickParticle(pygame.sprite.Sprite):
    def __init__(self, pos, vx, vy, ax, ay):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.vx, self.vy, self.ax, self.ay = vx, vy, ax, ay
        self.images = []
        self.image = util.load_tile('Brick Destroyed World %d.png' % main.BG)
        self.rect = self.image.get_rect(center = pos)
    def update(self):
        self.rect.move_ip(self.vx/4, self.vy/4)
        self.vx = self.vx + self.ax
        self.vy = self.vy + self.ay
        if not SCREENRECT.contains(self.rect):
            self.kill()
