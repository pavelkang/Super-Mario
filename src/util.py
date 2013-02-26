import pygame, os, main
from pygame.locals import *

def load_image(file, colorkey=None):
    "Loads an image with transparency."
    file = os.path.join('data', 'images', file)
    try:
        image = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, 'Image, "%s" not found'%(file)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    image = pygame.transform.scale(image, (image.get_width()/main.SCALE_DIV, image.get_height()/main.SCALE_DIV))
    return image.convert_alpha()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

def load_images_alpha(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file, colorkey = -1))
    return imgs

def load_image_reg(file):
    "Loads an image without transparency."
    file = os.path.join('data', 'images', file)
    try:
        image = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, 'Image, "%s" not found'%(file)
    image = pygame.transform.scale(image, (image.get_width()/main.SCALE_DIV, image.get_height()/main.SCALE_DIV))
    return image.convert()

def load_tile(file):
    "Loads a tile. All white in the image is transparent."
    file = os.path.join('data', 'scenery', file)
    try:
        image = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, 'Image, "%s" not found'%(file)
    colorkey = (255,255,255)
    image.set_colorkey(colorkey)
    image = pygame.transform.scale(image, (image.get_width()/main.SCALE_DIV, image.get_height()/main.SCALE_DIV))
    return image.convert_alpha()

def load_background(file):
    "Loads a background file."
    file = os.path.join('data', 'scenery', file)
    try:
        image = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, 'Image, "%s" not found'%(file)
    image = pygame.transform.scale(image, (image.get_width()/main.SCALE_DIV, image.get_height()/main.SCALE_DIV))
    return image.convert_alpha()

def load_sound(file):
    'Loads a sound'
    file = os.path.join('data', 'sounds', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print 'Warning, unable to load,', file

def load_music(file):
    'Loads a sound'
    file = os.path.join('data', 'music', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print 'Warning, unable to load,', file

def load_font(file, size):
    'Load\'s awesome fonts!'
    file = os.path.join('data', 'fonts', file)
    try:
        font = pygame.font.Font(file, size)
    except pygame.error:
        print 'There\'s  either an error in the program or a font\'s missing'
    return font

def screenscroll(player, sprites, moving):
    for sprite in sprites:
        sprite.rect.move_ip(-player.speed, 0)

def clearlvl(player, sprites):
    player.kill()
    for s in sprites:
        s.kill()
