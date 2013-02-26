
import pygame
from pygame.locals import *

from util import *
from locals import *
import main

class Player(pygame.sprite.Sprite):
    def __init__(self, name, state):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.name = name

        self.walkright_images    = load_images(state + '' + name + ' run 1.png', state + '' + name + ' run 2.png',
                                               state + '' + name + ' run 3.png', state + '' + name + ' run 2.png')
        self.walkleft_images     = load_images(state + '' + name + ' run 1.png', state + '' + name + ' run 2.png',
                                               state + '' + name + ' run 3.png', state + '' + name + ' run 2.png')
        
        self.walkleft_images[0]  = pygame.transform.flip(self.walkleft_images[0], True, False)
        self.walkleft_images[1]  = pygame.transform.flip(self.walkleft_images[1], True, False)
        self.walkleft_images[2]  = pygame.transform.flip(self.walkleft_images[2], True, False)
        self.walkleft_images[3]  = pygame.transform.flip(self.walkleft_images[3], True, False)

        self.skid_left_images    = load_images(state + '' + name + ' Skid Left.png')
        self.skid_right_images   = load_images(state + '' + name + ' Skid Right.png')

        self.jumpright_images    = load_images(state + '' + name + ' jump.png')
        self.jumpleft_images     = load_images(state + '' + name + ' jump.png')
        self.jumpleft_images[0]  = pygame.transform.flip(self.jumpleft_images[0], True, False)
        self.standleft_images    = load_images(state + '' + name + ' stand.png')
        self.standleft_images[0] = pygame.transform.flip(self.standleft_images[0], True, False)
        self.standright_images   = load_images(state + '' + name + ' stand.png')
        self.throw_images = load_images('Fiery Mario Throw.png')
        self.throw_images2 = load_images('Fiery Mario Throw.png')
        self.throw_images2[0] = pygame.transform.flip(self.throw_images2[0], True, False)

        if main.STATE == 1:
            self.transferimgs        = load_images(name + ' stand2.png', 'Super ' + name + ' Stand.png')
        if main.STATE == 2:
            self.transferimgs        = load_images('Super ' + name + ' Stand.png', 'Fiery ' + name + ' Stand.png')
        else:
            self.transferimgs        = load_images(name + ' Stand2.png', 'Super ' + name + ' Stand.png')

        self.rectimage = load_image(state + name + ' Rect.png')
        self.rectimage.set_colorkey((255, 255, 255), RLEACCEL)
        self.image = load_image(state + name + ' Rect.png')

        self.x = SCREENRECT.centerx
        self.y = 180
        
        self.rect = self.image.get_rect(center=(self.x, self.y))  
        self.speed = 0
        self.max_speed = 4
        self.animation_speed = 4
        self.jump_speed = 0
        self.jumping = True
        self.jump_power = 11.5
        self.keydown_fall_speed = 0.132
        self.keyup_fall_speed = 0.76
        self.max_fall_speed = -11
        self.frame = 0
        self.facing = 1
        self.transfertimer = 0
        self.transfering = False
        self.throw_timer = 0

    def topwallcheck(self, rect):
        if self.jump_speed < 0 and \
               (self.rect.bottom - 16 < rect.top <= self.rect.bottom):
            self.rect.bottom = rect.top
            self.jump_speed = 0        
            self.jumping = False

    def bottomwallcheck(self, rect):
        if self.jump_speed > 0 and \
           (self.rect.top + 18 > rect.bottom >= self.rect.top):
            self.jump_speed = -1
            self.rect.top = rect.bottom

    def sidewallcheck(self, rect, moving):
        if self.speed > 0 or self.speed < 0 and \
           (rect.left > self.rect.left or \
           rect.right < self.rect.right):
            if self.speed < 0 and self.rect.bottom > rect.top and self.rect.top < rect.bottom - 16:
                for s in self.sprites:
                    s.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.bottom > rect.top and self.rect.top < rect.bottom - 16:
                for s in self.sprites:
                    s.rect.move_ip(self.speed, 0)

    def transfer(self):
        self.transfertimer = 25
        self.transfering = True

    def move(self, moving):
        if moving: self.facing = moving        
        if not self.transfering:
            self.rect.move_ip(0, -self.jump_speed)
        
        self.frame += 1
        if self.jump_speed < 1:
            self.keyup_fall_speed = 1.2
            self.keydown_fall_speed = 1.1
        if self.jump_speed >= 1:
            self.keyup_fall_speed = 0.8
            self.keydown_fall_speed = 0.4

        if self.transfering:
            if self.transfertimer > 0:
                self.transfertimer -= 1
                self.image = self.transferimgs[self.frame/4%2]
        if self.transfertimer <= 0:
            self.transfering = False

        if not moving and not self.jumping:
            if self.speed > 0:
                self.speed -= 0.25
                self.image = self.walkleft_images[self.frame/(self.animation_speed+1)%3]
            if self.speed < 0:
                self.speed += 0.25
                self.image = self.walkleft_images[self.frame/(self.animation_speed+1)%3]

        keystate = pygame.key.get_pressed()

        if keystate[K_x] and not self.jumping:
            self.max_speed = 5
            self.animation_speed = 2
        if not (keystate[K_x]) and not self.jumping:
            self.max_speed = 4
            self.animation_speed = 4
            if self.speed > 4:
                self.speed = 4
            if self.speed < -4:
                self.speed = -4

        if self.jump_speed < -2.8 and not pygame.sprite.spritecollide(self, self.platforms3, 0):
            self.jumping = True

        if moving > 0 and self.jumping == False and not self.transfering:
            if self.speed < self.max_speed:
                self.speed += 0.1875
            if self.speed < 0:
                self.image = self.skid_left_images[0]
            else:
                self.image = self.walkright_images[self.frame/self.animation_speed%3]
        if moving < 0 and self.jumping == False and not self.transfering:
            if self.speed > -self.max_speed:
                self.speed -= 0.1875
            if self.speed > 0:
                self.image = self.skid_right_images[0]
            else:
                self.image = self.walkleft_images[self.frame/self.animation_speed%3]
        if self.facing > 0 and not moving and self.jumping == False and not self.transfering:
            self.image = self.standright_images[0]
        if self.facing < 0 and not moving and self.jumping == False and not self.transfering:
            self.image = self.standleft_images[0]
        if self.facing > 0 and self.jumping == True and not self.transfering:
            if self.speed < self.max_speed and moving > 0:
                self.speed += 0.0625
            self.image = self.jumpright_images[0] 
        if self.facing < 0 and self.jumping == True and not self.transfering:
            if self.speed > -self.max_speed and moving < 0:
                self.speed -= 0.0625
            self.image = self.jumpleft_images[0]

        if (keystate[K_x]) and main.STATE == 3 and self.throw_timer > 0:
            if self.facing > 0:
                self.image = self.throw_images[0]
            if self.facing < 0:
                self.image = self.throw_images2[0]
        self.throw_timer -= 1

class PlayerDie(pygame.sprite.Sprite):
    defaultlife = 200
    animcycle = 3
    images = []
    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = load_images(actor.name + ' dead.png')
        self.image = self.images[0]
        self.orgImage = self.image.copy()
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = self.defaultlife
        self.yspeed = -16
        self.frame = 0
        self.angle = 0

    def update(self):
        self.frame += 1
        self.rect.move_ip(0, self.yspeed)
        self.yspeed += 0.4
        self.life = self.life - 1
        if self.life <= 0:
            self.kill()

    def rotate(self, amount):
        self.oldCenter = self.rect.center
        self.angle -= -amount
        self.image = pygame.transform.rotate(self.orgImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.oldCenter

class PlayerWin(pygame.sprite.Sprite):
    animcycle = 4
    images = []
    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        if main.STATE == 1:
            self.slideimg = load_images(actor.name + ' Slide.png')
            self.fallimg = load_images(actor.name + ' Jump.png')
            self.images = load_images(actor.name + ' Run 1.png', actor.name + ' Run 2.png',
                                      actor.name + ' Run 3.png', actor.name + ' Run 2.png')
        if main.STATE == 2:
            self.slideimg = load_images('Super ' + actor.name + ' Slide.png')
            self.fallimg = load_images('Super ' + actor.name + ' Jump.png')
            self.images = load_images('Super ' + actor.name + ' Run 1.png',
                                      'Super ' + actor.name + ' Run 2.png',
                                      'Super ' + actor.name + ' Run 3.png',
                                      'Super ' + actor.name + ' Run 2.png')
        if main.STATE == 3:
            self.slideimg = load_images('Fiery Mario Slide.png')
            self.fallimg = load_images('Fiery Mario Jump.png')
            self.images = load_images('Fiery Mario Run 1.png',
                                      'Fiery Mario Run 2.png',
                                      'Fiery Mario Run 3.png',
                                      'Fiery Mario Run 2.png')
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.rect.move_ip(2, 0)
        self.yspeed = 2
        self.frame = 0

    def update(self):
        self.frame += 1
        if not pygame.sprite.spritecollide(self, self.platforms, 0):
            if pygame.sprite.spritecollide(self, self.flags, 0):
                for flag in self.flags:
                    if self.rect.left < flag.rect.left + 4:
                        self.image = self.slideimg[0]
                        self.rect.move_ip(0, self.yspeed)
                    if self.rect.right >= flag.rect.right:
                        self.image = self.fallimg[0]
                        self.rect.move_ip(0, 4)                
        else:
            for flag in self.flags:
                if self.rect.left < flag.rect.left + 4:
                    self.image = self.images[self.frame/self.animcycle%4]
                    self.rect.move_ip(2, 0)
        for platform in pygame.sprite.spritecollide(self, self.platforms, 0):
            if not pygame.sprite.spritecollide(self, self.flags, 0):
                self.rect.bottom = platform.rect.top
        for flag in self.flags:
            if self.rect.right >= flag.rect.centerx:
                self.image = self.images[self.frame/self.animcycle%4]
                self.rect.move_ip(2, 0)
        if self.rect.left > 880:
            self.kill()

