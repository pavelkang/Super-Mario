import pygame
from pygame.locals import *

def _pixelPerfectCollisionDetection(sp1,sp2):

    rect1 = sp1.rect;     
    rect2 = sp2.rect;                            
    rect  = rect1.clip(rect2)
            
    x1 = rect.x-rect1.x
    y1 = rect.y-rect1.y
    x2 = rect.x-rect2.x
    y2 = rect.y-rect2.y

    for r in xrange(0,rect.height):      
        for c in xrange(0,rect.width):

            if sp1.image.get_at((c+x1, r+y1))[3] & sp2.image.get_at((c+x2, r+y2))[3]:
                return 1        

    return 0

def spritecollide_pp(sprite, group, dokill):

    crashed = []
    spritecollide = sprite.rect.colliderect
    ppcollide = _pixelPerfectCollisionDetection
    if dokill:
        for s in group.sprites():
            if spritecollide(s.rect):
                if ppcollide(sprite,s):
                    s.kill()
                    crashed.append(s)
    else:
        for s in group.sprites():
            if spritecollide(s.rect):
                if ppcollide(sprite,s):
                    crashed.append(s)
    return crashed


def groupcollide_pp(groupa, groupb, dokilla, dokillb):

    crashed = {}
    SC = spritecollide_pp
    if dokilla:
        for s in groupa.sprites():
            c = SC(s, groupb, dokillb)
            if c:
                crashed[s] = c
                s.kill()
    else:
        for s in groupa.sprites():
            c = SC(s, groupb, dokillb)
            if c:
                crashed[s] = c
    return crashed

def spritecollideany_pp(sprite, group):

    spritecollide = sprite.rect.colliderect
    ppcollide = _pixelPerfectCollisionDetection    
    for s in group.sprites():
        if spritecollide(s.rect):
            if ppcollide(sprite,s):
                return s
    return None
