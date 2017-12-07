###########################################################################
#   Simple Shooting Game
#
#   Programmed by Fangwulf 2017-11-07
#
#   Dependancies: Python 3.6 and Pygame 1.9.3
#
#   Description: Simple game where the player can aim and shoot at
#       enemies that spawn endlessly
###########################################################################
# import needed modules
import pygame, sys, random, time, math
from pygame.locals import * # instead of typing pygame.locals.X everytime
###########################################################################
# frames per second the screen updates
FPS = 60
# create clock for FPS
FPS_CLOCK = pygame.time.Clock()
# set game window width and height
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
AREA_RECT = pygame.Rect(-200, -200,
    WINDOW_WIDTH + 300, WINDOW_HEIGHT + 300)
# defines RGB values for colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
# number of enemies to spawn
NUM_ENEMIES_MIN = 1
NUM_ENEMIES_MAX = 5
# player values
PLAYER_SPEED = 5
PLAYER_HEALTH_MAX = 3
# enemy values
ENEMY_SPEED_MIN = 1
ENEMY_SPEED_MAX = 5
# load image files
ENEMY_IMG = pygame.image.load('assets/enemy.png')
BULLET_IMG = pygame.image.load('assets/bullet.png')
PLAYER_IMG = pygame.image.load('assets/player.png')
###########################################################################
# defines main function
def main ():
    # global use variables
    global window, textFont, textFontSmall
    # initialize pygame
    pygame.init()
    # create game window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    # set game window title
    pygame.display.set_caption('Simple Shooting Game')
    # creates text font
    textFont = pygame.font.Font('assets/freesansbold.ttf', 24)
    textFontSmall = pygame.font.Font('assets/freesansbold.ttf', 18)
    # runs game function
    while True:
        game()
    return
###########################################################################
# defines game function
def game ():
    # global use variables
    global playerWidth, playerHeight
    # assign game screen boolean
    startGame = False
    gameOver = False
    # dimensions of player image
    playerWidth = PLAYER_IMG.get_width()
    playerHeight = PLAYER_IMG.get_height()
    # starting x and y position of player
    playerX = (WINDOW_WIDTH / 2) - (playerWidth / 2)
    playerY = (WINDOW_HEIGHT / 2) - (playerHeight / 2)
    playerAngle = 0
    # assign player health
    playerHealth = PLAYER_HEALTH_MAX
    # assign score
    score = 0
    # stores objects
    enemyObjs = []
    bulletObjs = []
    # main loop
    while True:
        # game window background
        window.fill(BLACK)
        # get pressed keyboard keys list
        keys = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos()
        # create player rectangle
        playerRect = pygame.Rect(playerX, playerY,
            playerWidth, playerHeight)
        playerCenter = (playerX + (playerWidth / 2),
            playerY + (playerHeight / 2))
        # draw score
        if (not gameOver) and startGame:
            scoreScreen(score)
            healthScreen(playerHealth)
        # move bullet(s)
        if  (not gameOver) and startGame:
            for bullet in bulletObjs:
                bullet['x'] += bullet['moveX'] * 2
                bullet['y'] += bullet['moveY'] * 2
                bullet['rect'] = pygame.Rect((bullet['x'], bullet['y'],
                    bullet['width'], bullet['height']))
        # move enemy towards player
        if  (not gameOver) and startGame:
            for enemy in enemyObjs:
                enemyX = enemy['x'] - playerX
                enemyY = enemy['y'] - playerY
                enemyDist = math.hypot(enemyX, enemyY)
                enemyX = enemyX / enemyDist
                enemyY = enemyY / enemyDist
                enemy['x'] -= enemyX * enemy['speed']
                enemy['y'] -= enemyY * enemy['speed']
        # draw bullet
        if (not gameOver) and startGame:
            for bullet in bulletObjs:
                window.blit(bullet['image'], bullet['rect'])
        # draw enemy facing player
        if (not gameOver) and startGame:
            for enemy in enemyObjs:
                enemyAngle = (360 - ((math.atan2(playerCenter[1] - enemy['y'],
                    playerCenter[0] - enemy['x']) * 180) / math.pi))
                enemyImgRot = pygame.transform.rotate(ENEMY_IMG,
                    (enemyAngle + 180))
                enemyRect = enemyImgRot.get_rect(center = (enemy['x'] +
                    (enemy['width'] / 2), enemy['y'] + (enemy['height'] / 2)))
                window.blit(enemyImgRot, enemyRect)
        # replace deleted enemies
        if len(enemyObjs) < random.randint(NUM_ENEMIES_MIN,
            NUM_ENEMIES_MAX):
            enemyObjs.append(spawnEnemy())
        # delete bullet once outside game window
        for i in range(len(bulletObjs) -1, -1, -1):
            if not collision(AREA_RECT, bulletObjs[i]['rect']):
                del bulletObjs[i]
        # delete enemy once outside game window
        for i in range(len(enemyObjs) -1, -1, -1):
            if not collision(AREA_RECT, enemyObjs[i]['rect']):
                del enemyObjs[i]
        # delete enemy on bullet collision
        for i in range(len(bulletObjs) -1, -1, -1):
            bulletRect = pygame.Rect(bulletObjs[i]['x'], bulletObjs[i]['y'],
                bulletObjs[i]['width'], bulletObjs[i]['height'])
            for n in range(len(enemyObjs) -1, -1, -1):
                enemyRect = pygame.Rect(enemyObjs[n]['x'], enemyObjs[n]['y'],
                    enemyObjs[n]['width'], enemyObjs[n]['height'])
                if collision(bulletRect, enemyRect):
                    try:
                        del enemyObjs[n]
                        del bulletObjs[i]
                    except:
                        print('Collision exception!')
                        pass
                    score += 1
        # decrease player health if enemy collides with player
        for i in range(len(enemyObjs) -1, -1, -1):
            enemyRect = pygame.Rect(enemyObjs[i]['x'], enemyObjs[i]['y'],
                enemyObjs[i]['width'], enemyObjs[i]['height'])
            if collision(enemyRect, playerRect):
                del enemyObjs[i]
                window.fill(RED)
                playerHealth -= 1
        # set game over if player looses all health
        if playerHealth <= 0:
            gameOver = True
        # check for keyboard input
        # move player up
        if (not gameOver) and startGame:
            if keys[K_UP] or keys[K_w]:
                playerY -= PLAYER_SPEED
                # prevent player leaving screen upwards
                if playerY < 0:
                    playerY = 0
            # move player down
            if keys[K_DOWN] or keys[K_s]:
                playerY += PLAYER_SPEED
                # prevent player leaving screen down
                if (playerY + playerHeight) > WINDOW_HEIGHT:
                    playerY = WINDOW_HEIGHT - playerHeight
            # move player left
            if keys[K_LEFT] or keys[K_a]:
                playerX -= PLAYER_SPEED
                # prevent player leaving screen left
                if playerX < 0:
                    playerX = 0
            # move player right
            if keys[K_RIGHT] or keys[K_d]:
                playerX += PLAYER_SPEED
                # prevent player leving screen right
                if (playerX + playerWidth) > WINDOW_WIDTH:
                    playerX = WINDOW_WIDTH - playerWidth
            # rotate player
            playerAngle = (360 - ((math.atan2(mousePos[1] - playerY,
                mousePos[0] - playerX) * 180) / math.pi))
            playerImgRot = pygame.transform.rotate(PLAYER_IMG, playerAngle)
            playerRect = playerImgRot.get_rect(center = (playerCenter))
            # draw player
            window.blit(playerImgRot, playerRect)
        # show start screen
        elif not startGame:
            startGameScreen()
        # show game over screen
        elif gameOver:
            gameOverScreen(score)
        # start game
        if keys[K_RETURN] and not startGame:
            startGame = True
        # restart game after game over
        if keys[K_RETURN] and gameOver:
            playerX = (WINDOW_WIDTH / 2) - (playerWidth / 2)
            playerY = (WINDOW_HEIGHT / 2) - (playerHeight / 2)
            playerHealth = PLAYER_HEALTH_MAX
            score = 0
            enemyObjs = []
            bulletObjs = []
            gameOver = False
        # exit game on key press
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        # scan pygame events
        for event in pygame.event.get():
            # exit game loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # create bullet on button press or mouse click
            if (not gameOver) and startGame:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    bulletObjs.append(spawnBullet(playerCenter))
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        bulletObjs.append(spawnBullet(playerCenter))
        # update the window
        pygame.display.update()
        # add tick to FPS_CLOCK
        FPS_CLOCK.tick(FPS)
    return
###########################################################################
# defines enemy spawn function
def spawnEnemy ():
    enemy = {}
    enemy['width'] = ENEMY_IMG.get_width()
    enemy['height'] = ENEMY_IMG.get_height()
    # get random screen edge at witch to spawn enemy
    randomEdge = random.randint(1, 4)
    if randomEdge == 1:
        enemy['x'] = 0 - (enemy['width'] + 20)
        enemy['y'] = random.randint(0, (WINDOW_HEIGHT - enemy['height']))
    if randomEdge == 2:
        enemy['x'] = random.randint(0, (WINDOW_WIDTH - enemy['width']))
        enemy['y'] = 0 - (enemy['width'] + 20)
    if randomEdge == 3:
        enemy['x'] = WINDOW_WIDTH + enemy['width']
        enemy['y'] = random.randint(0, (WINDOW_HEIGHT - enemy['width']))
    if randomEdge == 4:
        enemy['x'] = random.randint(0, (WINDOW_WIDTH- enemy['width']))
        enemy['y'] = WINDOW_HEIGHT + enemy['height']
    # get random enemy speed, within set global values
    enemy['speed'] = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
    enemy['rect'] = pygame.Rect(enemy['x'], enemy['y'],
        enemy['width'], enemy['height'] )
    return enemy
###########################################################################
# defines bullet spawn function, takes player center
def spawnBullet (playerCenter):
    bullet = {}
    bullet['width'] = BULLET_IMG.get_width()
    bullet['height'] = BULLET_IMG.get_height()
    bullet['x'] = playerCenter[0]
    bullet['y'] = playerCenter[1]
    bullet['speed'] = 15
    # set bullet trajectory based on mouse position
    mousePos = pygame.mouse.get_pos()
    bulletDistX = mousePos[0] - bullet['x']
    bulletDistY = mousePos[1] - bullet['y']
    vector = math.sqrt(bulletDistX**2 + bulletDistY**2)
    bullet['moveX'] = (bulletDistX / vector) * 5
    bullet['moveY'] = (bulletDistY / vector) * 5
    bulletAngle = (360 - ((math.atan2(mousePos[1] - bullet['y'],
        mousePos[0] - bullet['x']) * 180) / math.pi))
    bullet['image'] = pygame.transform.rotate(BULLET_IMG, bulletAngle)
    bullet['rect'] = bullet['image'].get_rect(center = (bullet['x'],
        bullet['y']))
    return bullet
###########################################################################
# defines object collision, takes two object rect attributes
def collision (rect1, rect2):
    return rect1.colliderect(rect2)
###########################################################################
# defines screen that shows at start
def startGameScreen ():
    startText1 = textFont.render('Simple Shooter Game', True, WHITE)
    startRect1 = startText1.get_rect()
    startRect1.center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) - 100)
    startText2 = textFont.render('WASD or ARROW keys move, use mouse to aim',
        True, WHITE)
    startRect2 = startText2.get_rect()
    startRect2.center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) - 50)
    startText3 = textFont.render('SPACE key or Mouse Left Click shoots.',
        True, WHITE)
    startRect3 = startText3.get_rect()
    startRect3.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    startText4 = textFont.render('Press ENTER to start.', True, WHITE)
    startRect4 = startText4.get_rect()
    startRect4.center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) + 50)
    window.blit(startText1, startRect1)
    window.blit(startText2, startRect2)
    window.blit(startText3, startRect3)
    window.blit(startText4, startRect4)
    return
###########################################################################
# defines game over screen, takes score
def gameOverScreen (score):
    gameOverText1 = textFont.render('GAME OVER', True, WHITE)
    gameOverRect1 = gameOverText1.get_rect()
    gameOverRect1.center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) - 100)
    gameOverText2 = textFont.render(('Your final score is ' +
        str(score) + '.'), True, WHITE)
    gameOverRect2 = gameOverText2.get_rect()
    gameOverRect2.center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) - 50)
    gameOverText3 = textFont.render('Press ENTER to restart.', True, WHITE)
    gameOverRect3 = gameOverText3.get_rect()
    gameOverRect3.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    gameOverText4 = textFont.render('Press ESCAPE to exit.', True, WHITE)
    gameOverRect4 = gameOverText4.get_rect()
    gameOverRect4.center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) + 50)
    window.blit(gameOverText1, gameOverRect1)
    window.blit(gameOverText2, gameOverRect2)
    window.blit(gameOverText3, gameOverRect3)
    window.blit(gameOverText4, gameOverRect4)
    return
###########################################################################
# defines score text box
def scoreScreen (score):
    scoreText = textFontSmall.render(('Score: ' + str(score)),
        True, WHITE)
    scoreRect = scoreText.get_rect()
    scoreRect.x = 5
    scoreRect.y = 5
    window.blit(scoreText, scoreRect)
    return
###########################################################################
# definse health text box
def healthScreen (playerHealth):
    healthText = textFontSmall.render(('Health: ' + str(playerHealth)),
        True, WHITE)
    healthRect = healthText.get_rect()
    healthRect.x = 5
    healthRect.y = 30
    window.blit(healthText, healthRect)
    return
###########################################################################
# run main function
if __name__ == '__main__':
    main()
###########################################################################
