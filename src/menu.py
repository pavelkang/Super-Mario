import pygame, os, sys
from pygame.locals import *

from util import *
from music import *
from locals import *
import main
from ui import *

TIMER = 50

def menu(screen, player, sprites, play_music):
    background = load_background('Title Screen.png')
    cursor = load_image('Cursor.png', -1)
    font = BitmapFont("BMP font.bmp",8,9,"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.,-?! ")

    coin_imgs = []
    coin_imgs.append(load_image('Coin 1.png'))
    coin_imgs.append(load_image('Coin 2.png'))
    coin_imgs.append(load_image('Coin 3.png'))
    coin_imgs.append(load_image('Coin 4.png'))

    clock = pygame.time.Clock()
    play_music.stop()
    win_music.stop()
    die_music.stop()
    title_music.play(-1)
    clearlvl(player, sprites)

    TIMER = 50
    MENU_OPTION = 2
    CURSORPOS = 100

    highscore_f = os.path.join('data', 'highscore.txt')
    highscore = int(open(highscore_f).read())

    global LEVEL_UP, LEVEL, TIME, SCORE, LIVES, COINS, FRAME, TIMER, MENU_OPTION

    main.LEVEL_UP = True
    main.LEVEL = 1
    main.SCORE = 0
    main.TIME  = 0
    main.COINS = 0
    main.LIVES = 5
    main.WORLD = 1
    main.STATE = 1

    while 1:

        clock.tick(50)
        event = pygame.event.poll()


        if event.type == QUIT or \
            (event.type == KEYDOWN and event.key == K_ESCAPE) or \
            (event.type == JOYBUTTONDOWN and event.button == 9):
                sys.exit()

        if (event.type == KEYDOWN and event.key == K_RETURN): 
            title_music.stop()
            main.NAME = 'MARIO'
            break

        screen.blit(background, (0, 0))
        screen.blit(cursor, (150, CURSORPOS))
        CURSORPOS = 304

        ren = font.render('TOP-%06d' % highscore)
        screen.blit(ren, (screen.get_width()/2 - ren.get_width()/2, 380))
        ren = font.render('MARIO GAME')
        screen.blit(ren, (screen.get_width()/2 - ren.get_width()/2, 305))

        ren = font.render(str(main.NAME))
        screen.blit(ren, (40, 25))
        ren = font.render('%06d' % SCORE)
        screen.blit(ren, (40, 40))
        ren = font.render('X%02d' % COINS)
        screen.blit(ren, (190, 40))
        ren = font.render('WORLD')
        screen.blit(ren, (280, 25))
        ren = font.render('%d-%d' % (WORLD, LEVEL))
        screen.blit(ren, (295, 40))
        ren = font.render('TIME')
        screen.blit(ren, (410, 25))
        coin_img = coin_imgs[TIMER/4%4]
        screen.blit(coin_img, (165, 30))

        
        TIMER += 1

        pygame.display.flip()
