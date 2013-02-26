import sys
import pygame
from pygame.locals import *

from util import *

def load_multi_image(img,w,h,colorkey=None):
    fullimg = load_image(img,None)
    colorkey_topleft = fullimg.get_at((0,0))
    (t,t,fw,fh) = fullimg.get_rect()
	
    pieces = fw/w
    images = []
    i=0
    while i < pieces:
	new = pygame.Surface((w,h))
	new.blit(fullimg,(0,0),(i*w,0,w,h))
	new.convert()
	if colorkey is not None:
	    if colorkey == -1:
		colorkey = colorkey_topleft
	    new.set_colorkey(colorkey,pygame.RLEACCEL)
	images.append(new)
	i+=1
    return images

class BitmapFont:
    def __init__(self,file,w,h,chars):
	self.char_w = w
	self.char_h = h
	images = load_multi_image(file,w,h,-1)
	self.letters = {}
	count = 0
	for char in chars:
	    self.letters[char] = images[count]
	    count+=1
	del images
	del count
	
    def render(self,text,background=-1):
	textlen = len(text)
	surf = pygame.Surface((textlen*self.char_w,self.char_h))
	surf.fill((2,255,2))
	if textlen == 0:
	    return surf
		
	if background == -1:
	    colorkey = (2,255,2)
	    surf.set_colorkey(colorkey,pygame.RLEACCEL)
	else:
	    surf.fill(background)
			
	count = 0
	for c in text:
	    try:
		letter = self.letters[c]
	    except KeyError:
		letter = self.letters['?']
	    surf.blit(letter,(count*self.char_w,0))
	    count+=1
	surf = pygame.transform.scale(surf, (surf.get_width()*2, surf.get_height()*2))
	return surf
