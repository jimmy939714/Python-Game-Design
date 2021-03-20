# Import pygame module
import pygame
# Import random and math
import random
from math import *
# add bgm and sound effect
from pygame import mixer

# initialize the pygame
pygame.init()

# create window size 800 pixel width and 600 pixel height
# the origin (0,0) start from the point on top left of the window
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)


# Background
background = pygame.image.load("pinksky.png")

# BGM
mixer.music.load("Haikyuu ost Above.wav")
mixer.music.play(-1)
ending = mixer.Sound("yourlie.wav")

# Tittle and Icon
pygame.display.set_caption("MEOW MEOW Shooting!")
icon = pygame.image.load('Donutkun.png')
pygame.display.set_icon(icon)

# Player
player_icon = pygame.image.load('Donutkun 64x64.png')
playerX_change = 0
playerY_change = 0
playerX = 0
playerY = 300
body_state = "ready"

# Enemy
enemy_icon = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 13
passed_enemies = 0

for i in range(num_of_enemies):
    enemy_icon.append(pygame.image.load('nyan dog.png'))  # .append add single item to existing list
    enemyX.append(random.randint(700, 736))
    enemyY.append(random.randint(0, 536))
    enemyX_change.append(-0.9)
    enemyY_change.append(0.9)  # first movement of enemy, if = 0 enemy cannot move

# Bullet
bullet_icon = pygame.image.load("donutbullet.png")
bulletX = 0
bulletY = 0
bulletX_change = 8
bulletY_change = 0
bullet_state = "ready"  # ready- toy cannot see the bullet on the screen, fire - the bullet is currently moving.

# Score
score_value = 0
# Font
font = pygame.font.Font('Brokenbrush.ttf', 44)
textX = 10
textY = 10
text2X = 240
text2Y = 10

# Game Over Text
over_font = pygame.font.Font('Brokenbrush.ttf', 80)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (220, 250))


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_passed_enemies_limit(x, y):
    limit = font.render("Limit:" + str(passed_enemies) + "/" + str(20), True, (255, 255, 255))
    screen.blit(limit, (x, y))


def player(x, y):
    global body_state
    body_state = "touch"
    screen.blit(player_icon, (x, y))  # Draw character png


def enemy(x, y, i):
    screen.blit(enemy_icon[i], (x, y))  # Draw enemy png


def bullet(x, y):
    global bullet_state  # global is keyword allows you to modify the variable outside the current scope
    bullet_state = "fire"
    screen.blit(bullet_icon, (x + 10, y + 16))  # Draw bullet png


def Collision(enemyX, enemyY, bulletX, bulletY):
    distance = sqrt(pow(enemyX - bulletX, 2) + pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


def Body_Collision(enemyX, enemyY, playerX, playerY):
    distance = sqrt(pow(enemyX - playerX, 2) + pow(enemyY - playerY, 2))
    if distance < 40:
        return True
    else:
        return False


# Game infinity while loop
running = True  # Identify variable
while running:  # create while loop to run infinitely
    # the three number indicate RGB of the game (red, green, blue)
    # refer to online RGB of each colour. Update is necessary for RGB. Make sure it is in the background
    screen.fill((255, 204, 255))
    # add background above of the RGB, when we insert background we need to increase the speed of the movement
    # the adding of background is heavy for the game
    screen.blit(background, (0, 0))
    for event in pygame.event.get():  # event that are happening inside window
        if event.type == pygame.QUIT:  # if close button has been pressed = quit
            exit()  # end while loop, can use 'running = False' instead of exit()
        # Keystroke by using if function
        # video resize keystroke is to make sure when it is full screen
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 4.5
            if event.key == pygame.K_UP:
                playerY_change = -4.5
            if event.key == pygame.K_DOWN:
                playerY_change = +4.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("throwdonut.wav")
                    bullet_sound.play()
                    # get the current Y coordinate of player
                    bulletX = playerX
                    bulletY = playerY
                    bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP \
                    or event.key == pygame.K_DOWN or event.key == pygame.K_SPACE:
                playerX_change = 0
                playerY_change = 0

    # Create window boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800 - 64 = 736
        playerX = 736
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:  # 600 - 64 = 536
        playerY = 536
    # Create window boundary for enemy
    for i in range(num_of_enemies):
        # Game Over
        if passed_enemies == 20:
            mixer.music.unload()
            ending.play()
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]  # enemy will move depend on the enemyX_change
        enemyY[i] += enemyY_change[i]  # enemy will move depend on the enemyY_change
        if enemyX[i] <= 0:
            enemyX[i] = -64
        if enemyX[i] >= 736:  # 800 - 64 = 736
            enemyX[i] = 736
        if enemyY[i] <= 70:
            enemyY_change[i] = 0.9
        elif enemyY[i] >= 536:  # 600 - 64 = 536
            enemyY_change[i] = -0.9
        # Collision
        collision = Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        body_collision = Body_Collision(enemyX[i], enemyY[i], playerX, playerY)
        if collision or body_collision:
            collision_sound = mixer.Sound("scorehit.wav")
            collision_sound.play()
            bulletX = playerX
            bullet_state = "ready"
            body_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(800, 825)
            enemyY[i] = random.randint(0, 536)
        if enemyX[i] == -64:
            enemyX[i] = random.randint(800, 825)
            enemyY[i] = random.randint(0, 536)
            score_value -= 1
            passed_enemies += 1
        enemy(enemyX[i], enemyY[i], i)  # use the enemy function define in above in while loop

    # Bullet movement
    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletX += bulletX_change
    if bulletX >= 800:
        bulletX = playerX
        bullet_state = "ready"

    playerX += playerX_change  # x-axis will move depend on the keystroke
    playerY += playerY_change  # y-axis will move depend on the keystroke
    player(playerX, playerY)  # use the player function define in above in while loop
    show_score(textX, textY)
    show_passed_enemies_limit(text2X, text2Y)
    pygame.display.update()  # update display
