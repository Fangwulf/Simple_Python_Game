###########################################################################
#   Simple Shooting Game
#
#   Programmed by Fangwulf 2017-11-07
#
#   Dependancies: Python 3 and Pygame 1.9.3
#
###########################################################################
# import needed modules
import pygame, sys, random, time, math
from pygame.locals import * # instead of typing pygame.locals.X everytime
###########################################################################
# frames per second the screen updates
FPS = 60
# set width of game window
WINDOW_WIDTH = 500
# set height of game window
WINDOW_HEIGHT = 500
# defines RGB values for colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# keyboard button assignments
KEY_QUIT = K_ESCAPE
KEY_UP = K_w
KEY_DOWN = K_s
KEY_LEFT = K_a
KEY_RIGHT = K_d
# number of enemies to spawn
NUM_ENEMIES = 1
# player speed
PLAYER_SPEED = 5
###########################################################################
# defines main function
def main ():
    # global use variables
    global fpsClock, window, enemyImg, bulletImg, playerImg
    # initialize pygame
    pygame.init()
    # create clock for FPS
    fpsClock = pygame.time.Clock()
    # create game window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    # set game window title
    pygame.display.set_caption('Simple Shooting Game')
    # load enemy image file
    enemyImg = pygame.image.load('assets/enemy.png')
    # load bullet projectile image file
    bulletImg = pygame.image.load('assets/bullet.png')
    # load player image file
    playerImg = pygame.image.load('assets/player.png')
    # runs game function
    while True:
        game()
###########################################################################
# defines game function
def game ():
    # global use variables
    global playerWidth, playerHeight
    # dimensions of player image
    playerWidth = playerImg.get_width()
    playerHeight = playerImg.get_height()
    enemyWidth = enemyImg.get_width()
    enemyHeight = enemyImg.get_height()
    # starting x and y position of player
    playerX = 0
    playerY = (WINDOW_HEIGHT / 2) - (playerHeight / 2)
    # stores objects
    enemyObjs = []
    bulletObjs = []
    # main loop
    while True:
        # game window background
        window.fill(BLACK)
        # get mouse cursor position [x,y]
        mousePos = pygame.mouse.get_pos()
        # get pressed keyboard keys list
        keys = pygame.key.get_pressed()
        # initilaize bullet direction variables
        bChangex = 0
        bChangey = 0
        # move bullet(s)
        for bObj in bulletObjs:
            '''budx, budy = bObj['x'] - mousePos[0], bObj['y'] - mousePos[1]
            budist = math.hypot(budx, budy)
            budx, budy = budx / budist, budy / budist
            bObj['x'] -= budx * bObj['speed']
            bObj['y'] -= budy * bObj['speed']'''
            bVx = mousePos[0] - playerX
            bVy = mousePos[1] - playerY
            vLength = math.sqrt(bVx**2 + bVy**2)
            bVx = (bVx / vLength) * 5
            bVy = (bVy / vLength) * 5
            bObj['x'] += bVx
            bObj['y'] += bVy
        # move enemy towards player
        for eObj in enemyObjs:
            endx, endy = eObj['x'] - playerX, eObj['y'] - playerY
            endist = math.hypot(endx, endy)
            endx, endy = endx / endist, endy / endist
            eObj['x'] -= endx * eObj['speed']
            eObj['y'] -= endy * eObj['speed']
        # draw bullet
        for bObj in bulletObjs:
            bObj['rect'] = pygame.Rect((bObj['x'], bObj['y'],
                bObj['width'], bObj['height']))
            window.blit(bulletImg, bObj['rect'])
        # draw enemy
        for eObj in enemyObjs:
            eObj['rect'] = pygame.Rect((eObj['x'], eObj['y'],
                eObj['width'], eObj['height']))
            window.blit(enemyImg, eObj['rect'])
        # replace deleted enemies
        if len(enemyObjs) < NUM_ENEMIES:
            enemyObjs.append(spawnEnemy(enemyWidth, enemyHeight, WINDOW_WIDTH))
        # delete bullet once outside game window
        for i in range(len(bulletObjs) -1, -1, -1):
            if offScreen(WINDOW_WIDTH, WINDOW_HEIGHT, bulletObjs[i]):
                del bulletObjs[i]
        # delete enemy once outside game window
        for i in range(len(enemyObjs) -1, -1, -1):
            if offScreen(WINDOW_WIDTH, WINDOW_HEIGHT, enemyObjs[i]):
                del enemyObjs[i]
        '''for i in range(len(enemyObjs) -1, -1, -1):
            enObj = enemyObjs[i]
            buObj = bulletObjs[i]
            if 'rect' in enObj and bulletObjs['rect'].colliderect(enObj['rect']):
                del enemyObjs[i]'''
        # delete enemy on bullet collision
        for eObj in enemyObjs:
            enemyOb = pygame.Rect((eObj['x'], eObj['y'],
                eObj['width'], eObj['height']))
            for bObj in bulletObjs:
                bulletOb = pygame.Rect((bObj['x'], bObj['y'], bObj['width'],
                    bObj['height']))
                if bulletOb.colliderect(enemyOb):
                    del enemyObjs[i]
                    del bulletObjs[i]
        # check for keyboard input
        # move player up
        if keys[KEY_UP]:
            playerY -= PLAYER_SPEED
            # prevent player leaving screen upwards
            if playerY < 0:
                playerY = 0
        # move player down
        if keys[KEY_DOWN]:
            playerY += PLAYER_SPEED
            # prevent player leaving screen down
            if (playerY + playerHeight) > WINDOW_HEIGHT:
                playerY = WINDOW_HEIGHT - playerHeight
        # move player left
        if keys[KEY_LEFT]:
            playerX -= PLAYER_SPEED
            # prevent player leaving screen left
            if playerX < 0:
                playerX = 0
        # move player right
        if keys[KEY_RIGHT]:
            playerX += PLAYER_SPEED
            # prevent player leving screen right
            if (playerX + playerWidth) > WINDOW_WIDTH:
                playerX = WINDOW_WIDTH - playerWidth
        # draw player
        window.blit(playerImg, (playerX, playerY))
        # exit game on key press
        if keys[KEY_QUIT]:
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            # exit game loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # create bullet on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bulletObjs.append(spawnBullet(playerX, playerY, mousePos))
        # update the window
        pygame.display.update()
        # add tick to fpsClock
        fpsClock.tick(FPS)
###########################################################################
# defines enemy spawn function
def spawnEnemy (enemyWidth, enemyHeight, WINDOW_WIDTH):
    enemy = {}
    enemy['width'] = enemyImg.get_width()
    enemy['height'] = enemyImg.get_height()
    enemy['x'] = WINDOW_WIDTH - enemy['width']
    enemy['y'] = random.randint(0, (WINDOW_HEIGHT - enemy['width']))
    enemy['speed'] = random.randint(1, 3)
    return enemy
###########################################################################
# defines bullet spawn function
def spawnBullet (playerX, playerY, mousePos):
    bullet = {}
    bullet['width'] = bulletImg.get_width()
    bullet['height'] = bulletImg.get_height()
    bullet['x'] = playerX + playerWidth
    bullet['y'] = playerY + (playerHeight/2)
    bullet['speed'] = 15
    return bullet
###########################################################################
'''def bulletHit (enemyx, enemyy, enemyWidth, enemyHeight, obj):
    enemyRect = pygame.Rect(enemyx, enemyy, enemyWidth, enemyHeight)
    objRect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    return enemyRect.colliderect(objRect)'''
###########################################################################
# defines function to check if object is outside screen bounds
def offScreen (WINDOW_WIDTH, WINDOW_HEIGHT, obj):
    screenRect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    objRect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    return not screenRect.colliderect(objRect)
###########################################################################
# run main function
if __name__ == '__main__':
    main()
###########################################################################
