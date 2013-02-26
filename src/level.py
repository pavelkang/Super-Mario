import pygame, os, sys
import main

import main
from util import *
from platforms import *
from baddies import *
from coin import *
from flag import *
from ui import *
from obstacles import *

def intermission(screen, LEVEL, WORLD, LIVES, SCORE, TIME, COINS, FRAME, coin_imgs, coin_img):
    font = BitmapFont("BMP font.bmp",8,9,"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.,-?! ")
    TIMER = 100
    global TIMER
    clock = pygame.time.Clock()
    while 1:
        screen.fill((0, 0, 0))
        event = pygame.event.poll()
        ren = font.render('WORLD 1-1')
        screen.blit(ren, (screen.get_width()/2 - ren.get_width()/2, screen.get_height()/2-15))
        ren = font.render('LIVES X%d' % LIVES)
        screen.blit(ren, (screen.get_width()/2 - ren.get_width()/2, screen.get_height()/2+5))
        ren = font.render(str(main.NAME))
        screen.blit(ren, (40, 25))
        ren = font.render('%06d' % SCORE)
        screen.blit(ren, (40, 40))
        ren = font.render('X%02d' % COINS)
        screen.blit(ren, (190, 40))
        ren = font.render('WORLD')
        screen.blit(ren, (280, 25))
        ren = font.render('1-1')
        screen.blit(ren, (295, 40))
        ren = font.render('TIME')
        screen.blit(ren, (410, 25))
        coin_img = coin_imgs[FRAME/4%4]
        screen.blit(coin_img, (165, 30))
        FRAME += 1
        clock.tick(50)

        pygame.display.flip()

        TIMER -= 1
        if TIMER <= 0:
            break
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()


class load_level:
    def __init__(self, level):
        map_file = open(os.path.join('data', 'levels', 'level 1.txt'), 'r')

        section = None
        row = 0
        column = 0
        self.world = 1
        while 1:
            # per line
            line = map_file.readline()
            if line == '':
                break
            else:
                line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            if line.endswith('-1'):
                self.world = 1
                continue
            if line.endswith('-2'):
                self.world = 2
                continue
            if line.endswith('-3'):
                self.world = 3
                continue
            if line.endswith('-4'):
                self.world = 4
                continue
            if line.startswith('Layout'):
                section = 'layout'
                continue

            groundimg = 'Ground World %d' % self.world
            brickimg = 'Brick World %d' % self.world
            blockimg = 'Block World %d' % self.world

            if section == 'layout':
                column = 0
                for char in line:

                    if char == "G":
                        Object(str(groundimg), True, False, (column, row))
                    if char == "g":
                        Object(str(groundimg), False, False, (column, row))

                    if char == "B":
                        Object(str(brickimg), True, True, (column, row))
                    if char == "b":
                        Object(str(brickimg), False, True, (column, row))
                    if char == "M":
                        Object(str(brickimg), True, False, (column, row))
                    if char == "m":
                        Object(str(brickimg), False, False, (column, row))

                    if char == "C":
                        block = Object3(str(blockimg), True, False, (column, row))
                    if char == "c":
                        block = Object3(str(blockimg), False, False, (column, row))
                    if char == "(":
                        block = Object3(str(blockimg), False, True, (column, row))
                    if char == ")":
                        block = Object3(str(blockimg), True, True, (column, row))


                    if char == "L":
                        Object3('Grass Left', True, True, (column, row))
                    if char == "W":
                        Object3('Grass Middle', True, True, (column, row))
                    if char == "R":
                        Object3('Grass Right', True, True, (column, row))
                    if char == "D":
                        Scenery('Dirt', (column, row))

                    if char == "P":
                        pipe = Object2('Pipe Top', True, False, (column, row))
                    if char == "p":
                        pipe = Object2('Pipe Middle', False, False, (column, row))

                    if char == "Q":
                        QuestionBlock(1, (column, row))
                    if char == "q":
                        QuestionBlock(2, (column, row))

                    if char == "_":
                        Object4('Platform Large', 0, 2, (column, row))
                    if char == "-":
                        Object4('Platform Large', 0, -2, (column, row))

                    if char == "f":
                        Scenery('Castle', (column, row + 4))
                    if char == "h":
                        Scenery('Hill Small', (column, row))
                    if char == "H":
                        Scenery('Hill Large', (column, row))
                    if char == "s":
                        Scenery('Bush Small', (column, row))
                    if char == "S":
                        Scenery('Bush Medium', (column, row))

                    if char == "1":
                        Coin((column, row))
                    if char == "2":
                        BaddieSpawnPoint(self.world, 1, (column, row))
                    if char == "3":
                        BaddieSpawnPoint(self.world, 2, (column, row))
                    if char == "0":
                        BaddieBoundary((column, row))

                    if char == "F":
                        Flag((column, row))
                    if char == "r":
                        Rotodisk((column, row))
                    if char == "d":
                        Object3('Empty Block', True, True, (column, row))

                    column += main.TILE_SPACING
                row += main.TILE_SPACING
                column = -main.TILE_SPACING
