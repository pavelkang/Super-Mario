import sys, os

import pygame
from pygame.locals import *

from locals import *
from level import *
from util import *
from menu import *

from music import *

from player import *
from platforms import *
from clouds import *
from baddies import *
from powerups import *
from coin import *
from flag import *
from ui import *
from obstacles import *
from pixelperfect import *

SCORE = SCORE
COINS = COINS
LEVEL = 1
WORLD = WORLD
TIME  = TIME
LIVES = LIVES
STATE = 1
DEAD = False
FRAME = 0
LEVEL_UP = True
BG = 1
highscore_f = os.path.join('data', 'highscore.txt')
highscore = int(open(highscore_f).read())
FULLSCREEN = False
TILE_SPACING = 32
SCALE_DIV = 1

NAME = 'MARIO'
joyLeft,joyRight = 0,0
def main():

    pygame.init()

    pygame.display.set_caption('Super Mario Bros.')
    pygame.display.set_icon(pygame.image.load(os.path.join('data', 'icon.gif')))
    screen = pygame.display.set_mode(SCREENRECT.size, HWSURFACE|HWPALETTE|DOUBLEBUF)
    pygame.mouse.set_visible(0)

    font = BitmapFont("BMP font.bmp",8,9,"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.,-?! ")

    background = load_background('Overworld Background.png')
    nintendo_logo = load_image('Nintendo Logo.png')
    lives_icon = load_image('Lives Icon.png')
    castle = load_tile('Castle.png')
    castle2 = load_tile('Castle Right Half.png')
    coin_imgs = []
    coin_imgs.append(load_image('Coin 1.png'))
    coin_imgs.append(load_image('Coin 2.png'))
    coin_imgs.append(load_image('Coin 3.png'))
    coin_imgs.append(load_image('Coin 4.png'))


    Player.containers = playerlayer
    Player.sprites = sprites
    Player.platforms = platforms
    Player.platforms3 = platforms3
    PlayerWin.containers = outerlayer, sprites
    PlayerWin.platforms = allplatforms
    PlayerWin.flags = flags
    PlayerDie.containers = outerlayer, sprites
    Ground.containers = middlelayer, sprites, topplatforms, platforms, allplatforms
    Object.containers = middlelayer, sprites, platforms, allplatforms
    Object2.containers = middlelayer, sprites, middleplatforms, allplatforms
    Object3.containers = middlelayer, sprites, platforms2, allplatforms
    Object4.containers = middlelayer, sprites, platforms3, allplatforms
    Scenery.containers = innerlayer, sprites
    QuestionBlock.containers = middlelayer, sprites, questionblocks, platforms, allplatforms
    Goomba.containers = outerlayer, sprites, goombas
    Goomba.platforms = allplatforms
    Goomba.dirpoints = dirpoints
    Koopa.containers = middlelayer, sprites, koopas
    Koopa.platforms = allplatforms
    Koopa.dirpoints = dirpoints
    Goombadie.containers = middlelayer, sprites
    BaddieSpawnPoint.containers = innerlayer, sprites
    BaddieBoundary.containers = sprites, dirpoints
    Mushroom.containers = outerlayer, sprites, mushrooms
    Mushroom.platforms = allplatforms
    CoinUp.containers = middlelayer, sprites
    Flag.containers = middlelayer, sprites, flags
    Flag.platforms = allplatforms
    BrickParticle.containers = outerlayer, sprites
    Koopashell.containers = middlelayer, sprites, shells
    Koopashell.platforms = allplatforms
    FireFlower.containers = innerlayer, sprites, fireflowers
    FireFlower.platforms = allplatforms
    Fireball.containers = middlelayer, sprites, fireballs
    Fireball.platforms = allplatforms
    Rotodisk.containers = outerlayer, rotodisks, sprites

    clock = pygame.time.Clock()

    coin_img = coin_imgs[FRAME/4%4]
    player = Player(NAME, '')
    die = PlayerDie(player)
    win = PlayerWin(player)
    global LEVEL, SCORE, LIVES, TIME, WORLD, STATE, DEAD, COINS, FRAME, BG, FULLSCREEN, NAME, LEVEL_UP,joyLeft,joyRight
    STATE = 1
    clouds = []
    clouds.append(Cloud('Cloud Medium.png'))
    clouds.append(Cloud('Cloud Small.png'))
    clouds.append(Cloud('Cloud Large.png'))
    clouds.append(Cloud('Cloud Medium.png'))
    clouds.append(Cloud('Cloud Small.png'))
    clouds.append(Cloud('Cloud Small.png'))
    clouds.append(Cloud('Cloud Medium.png'))

    highscore = int(open(highscore_f).read())

    the_level = load_level(LEVEL)
    music = load_music('World 1.ogg')
    clearlvl(player, sprites)


    menu(screen, player, sprites, music)
    LEVEL = 1

    while 1:

        Koopashell.player = player

        innerlayer.clear(screen, background)
        innerlayer.update()

        middlelayer.clear(screen, background)
        middlelayer.update()

        outerlayer.clear(screen, background)
        outerlayer.update()


        clock.tick(FPS)


        event = pygame.event.poll()

        keystate = pygame.key.get_pressed()
        defaultkeys1 = handle_input1()
        defaultkeys2 = handle_input2(keystate)

        if event.type == QUIT:
            sys.exit()
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == JOYBUTTONDOWN and event.button == 8):
            menu(screen, player, sprites, music)

        if ((event.type == KEYDOWN and event.key == K_z) or (event.type == JOYBUTTONDOWN and event.button == 2)) and player.jumping == False and player.alive():
            player.jump_speed = player.jump_power
            player.jumping = True
            player.y -= 5
            jump_sound.play()
        if ((event.type == KEYDOWN and event.key == K_x) or (event.type == JOYBUTTONDOWN and event.button == 7)) and player.alive() and STATE == 3:
            Fireball(player)
            player.throw_timer = 5

        if event.type == JOYBUTTONUP and event.button == 3 :
            joyRight,joyLeft = 0,0

        if event.type == JOYBUTTONUP and event.button == 0 :
            joyRight,joyLeft = 0,0
        
        if event.type ==JOYBUTTONDOWN and event.button == 3:
            joyRight = 1
            joyLeft = 0
        if event.type ==JOYBUTTONDOWN and event.button == 0:
            joyLeft = 1
            joyRight = 0
        moving = joyRight - joyLeft
        if player.alive():
            player.move(moving)
            screenscroll(player, sprites, moving)

            for c in clouds:
                c.xpos -= int(player.speed)

        if player.jump_speed > player.max_fall_speed and (keystate[K_z]):
            player.jump_speed -= player.keydown_fall_speed
        if player.jump_speed > player.max_fall_speed and not (keystate[K_z]):
            player.jump_speed -= player.keyup_fall_speed

        for questionblock in pygame.sprite.spritecollide(player, questionblocks, 0):
            if player.jump_speed > 0 and (player.rect.top + 18 > questionblock.rect.bottom >= player.rect.top):
                player.jump_speed = -1
                player.y += questionblock.rect.bottom - player.rect.top
                if not questionblock.hit and questionblock.type == 1:
                    COINS += 1
                    SCORE += 25
                    coin_sound.play()
                    CoinUp(questionblock)
                    questionblock.hit = True
                if not questionblock.hit and questionblock.type == 2:
                    questionblock.hit = True
                    if STATE == 1:
                        Mushroom(questionblock.rect.center)
                    else:
                        FireFlower(questionblock.rect.center)
                    item_sound.play()
                questionblock.hit = True
                player.jump_speed = -1
                player.rect.top = questionblock.rect.bottom
                questionblock.image = load_tile('Empty Block.png')
                questionblock.bounce()

        for platform in platforms:  
            if player.rect.colliderect(platform.rect):
                if player.jump_speed > 0 and (player.rect.top + 18 > platform.rect.bottom >= player.rect.top):
                    if platform.hittable:
                        platform.bounce()
                        if STATE > 1:
                            brick_sound.play()
                            platform.kill()
                            BrickParticle(platform.rect.topleft, -1, -2, 0, 2)
                            BrickParticle(platform.rect.topright, 1, -2, 0, 2)
                            BrickParticle(platform.rect.bottomleft, -1, 2, 0, 2)
                            BrickParticle(platform.rect.bottomright, 1, 2, 0, 2)
                if platform.landable:
                    player.topwallcheck(platform.rect)
                if platform.hittable:
                    player.bottomwallcheck(platform.rect)
                player.sidewallcheck(platform.rect, moving)
                if player.speed > 0 or player.speed < 0 and \
                   (platform.rect.left > player.rect.left or platform.rect.right < player.rect.right):
                    if player.rect.bottom > platform.rect.top and player.rect.top < platform.rect.bottom - 16:
                        for c in clouds:
                            c.xpos += int(player.speed)
        for platform in middleplatforms:
            if player.rect.colliderect(platform.rect):
                if platform.landable:
                    player.topwallcheck(platform.rect)
                player.sidewallcheck(platform.rect, moving)
                if player.speed > 0 or player.speed < 0 and \
                   (platform.rect.left > player.rect.left or platform.rect.right < player.rect.right):
                    if player.rect.bottom > platform.rect.top and player.rect.top < platform.rect.bottom - 16:
                        for c in clouds:
                            c.xpos += int(player.speed)
        for platform in platforms2:
            if player.rect.colliderect(platform.rect):
                if platform.landable:
                    player.topwallcheck(platform.rect)
                player.sidewallcheck(platform.rect, moving)
                if platform.hittable:
                    player.bottomwallcheck(platform.rect)
                if player.speed > 0 or player.speed < 0 and \
                    (platform.rect.left > player.rect.left or \
                    platform.rect.right < player.rect.right):
                    if player.rect.bottom > platform.rect.top and player.rect.top < platform.rect.bottom - 16:
                        for c in clouds:
                            c.xpos += int(player.speed)

        for platform in platforms3:
            if player.rect.colliderect(platform.rect):
                if player.jump_speed < 0 and \
                   (player.rect.bottom - 16 < platform.rect.top <= player.rect.bottom):
                    player.rect.bottom = platform.rect.top
                    player.jump_speed = -platform.yspeed
                    player.jumping = False
                player.sidewallcheck(platform.rect, moving)
                player.bottomwallcheck(platform.rect)
                    
                if player.speed > 0 or player.speed < 0 and \
                    (platform.rect.left > player.rect.left or platform.rect.right < player.rect.right):
                    if player.rect.bottom > platform.rect.top and player.rect.top < platform.rect.bottom - 16:
                        for c in clouds:
                            c.xpos += int(player.speed)

        if player.jump_speed < 1 and player.jumping == True:
            for g in pygame.sprite.spritecollide(player, goombas, 0):
                if player.rect.bottom >= g.rect.top + 10 and player.alive():
                    stomp_sound.play()
                    player.jump_speed = 9
                    SCORE += 100
                    g.kill()
                    Goombadie(g)
            for k in pygame.sprite.spritecollide(player, koopas, 0):
                if player.rect.bottom >= k.rect.top + 5 and player.alive():
                    stomp_sound.play()
                    player.jump_speed = 9
                    SCORE += 100
                    k.kill()
                    Koopashell(k)
        else:
            #if player.alive():
                for g in pygame.sprite.spritecollide(player, goombas, 0):
                    if STATE == 1:
                        DEAD = True
                        if player.alive():
                            LIVES -= 1
                            g.kill()
                            die = PlayerDie(player)
                            die_sound.play()
                        music.stop()
                    player.kill()
                    playery = player.rect.top
                    if not DEAD:
                        player = Player(NAME, '')
                        player.rect.top = playery
                        if STATE == 2:
                            player.transferimgs = load_images(NAME + ' stand2.png', 'Super ' + NAME + ' Stand.png')
                        if STATE == 3:
                            player.transferimgs = load_images(NAME + ' stand2.png', 'Fiery ' + NAME + ' Stand.png')
                        player.transfer()
                        pd_sound.play()
                    if STATE == 2 or STATE == 3:
                        STATE = 1
                for r in spritecollide_pp(player, rotodisks, 0):
                    if STATE == 1:
                        DEAD = True
                        if player.alive():
                            LIVES -= 1
                            die = PlayerDie(player)
                            die_sound.play()
                        music.stop()
                    player.kill()
                    playery = player.rect.top
                    if not DEAD:
                        player = Player(NAME, '')
                        player.rect.top = playery
                        if STATE == 2:
                            player.transferimgs = load_images(NAME + ' stand2.png', 'Super ' + NAME + ' Stand.png')
                        if STATE == 3:
                            player.transferimgs = load_images(NAME + ' stand2.png', 'Fiery ' + NAME + ' Stand.png')
                        player.transfer()
                        pd_sound.play()
                    if STATE == 2 or STATE == 3:
                        STATE = 1
        for g in pygame.sprite.groupcollide(goombas, fireballs, 1, 1):
            Goombadie(g)
            stomp_sound.play()

        for mushroom in pygame.sprite.spritecollide(player, mushrooms, 1):
            pu_sound.play()
            SCORE += 1000
            if STATE == 1:
                player.kill()
                playery = player.rect.top
                player = Player(NAME, 'Super ')
                player.rect.top = playery - 16
                player.transfer()
                pu_sound.play()
                STATE = 2
        for fireflower in pygame.sprite.spritecollide(player, fireflowers, 1):
            pu_sound.play()
            SCORE += 1000
            if STATE <= 2:
                player.kill()
                playery = player.rect.top
                player = Player(NAME, 'Fiery ')
                player.rect.top = playery
                player.transfer()
                pu_sound.play()
                STATE = 3

        if pygame.sprite.spritecollide(player, flags, 0):
            if player.alive():
                player.kill()
                win = PlayerWin(player)
                music.stop()
                win_music.play()
        for c in pygame.sprite.spritecollide(player, coins, 1):
            coin_sound.play()
            COINS += 1

        for g in pygame.sprite.groupcollide(goombas, shells, 1, 0):
            Goombadie(g)
            stomp_sound.play()
 
        if LEVEL_UP == True and LEVEL > 0:
            clearlvl(player, sprites)
            DEAD = False
            intermission(screen, LEVEL, WORLD, LIVES, SCORE, TIME, COINS, FRAME, coin_imgs, coin_img)
            if STATE == 1:
                player = Player(NAME, '')
            if STATE == 2:
                player = Player(NAME, 'Super ') 
            if STATE == 3:
                player = Player(NAME, 'Fiery ') 
            LEVEL_UP = False
            the_level = load_level(LEVEL)
            TIME = 201
            music = load_music('World %d.ogg' % the_level.world).play(-1)

        if not player.alive() and not die.alive() and not win.alive():
            if LIVES > 0:
                LEVEL_UP = True

        screen.blit(background, (0, 0))
        TIME -= 0.02
        BG = the_level.world
        if BG == 1:
            screen.fill((112, 168, 255))
            for c in clouds:
                c.draw(screen)
        if BG == 2:
            screen.fill((0, 0, 0))
        if BG == 3:
            screen.fill((112, 168, 255))
            for c in clouds:
                c.draw(screen)
        if BG == 4:
            screen.fill((0, 0, 0))
        if TIME <= 0:
            if player.alive():
                die = PlayerDie(player)
                music.stop()
                die_sound.play()
                player.kill()
            TIME = 0
        if player.rect.top >= 520 and player.alive():
            player.kill()
            music.stop()
            die_sound.play()
            die = PlayerDie(player)
            STATE = 1
            LIVES -= 1
        FRAME += 1

        dirty = innerlayer.draw(screen)
        middlelayer.draw(screen)
        for flag in flags:
            screen.blit(castle, (flag.rect.right + 45, flag.rect.bottom - castle.get_height() + 32))
        outerlayer.draw(screen)
        for flag in flags:
            screen.blit(castle2, (flag.rect.right + 45, flag.rect.bottom - castle.get_height() + 32))

        if player.alive():
            screen.blit(player.image, (player.rect[0] - 8, player.rect[1]))

        ren = font.render(str(NAME))
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
        ren = font.render('%03d' % TIME)
        screen.blit(ren, (420, 40))
        coin_img = coin_imgs[FRAME/4%4]
        screen.blit(coin_img, (165, 30))
        if SCORE > highscore:
            highscore = SCORE
            open(highscore_f, 'w').write(str(SCORE))

        Koopashell.player = player

        if die.life <= 1 and die.alive() and LIVES == 0:
            gameover.play()

        if not die.alive():
            if LIVES <= 0:
                screen.fill((0, 0, 0))
                ren = font.render('GAME OVER')
                screen.blit(ren, (SCREENRECT.centerx - ren.get_width()/2, SCREENRECT.centery - ren.get_height()))

        pygame.display.update(dirty)
        pygame.display.flip()


if __name__ == '__main__':
    main()      
