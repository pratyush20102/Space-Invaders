import pygame
import random
import math
from pygame import mixer

# Initializing pygame()
pygame.init()

# Creating screen and setting dimensions (width,height)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Changing Title and Icon of the game window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370  # x-coordinate
playerY = 480  # y-coordinate
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0  # x-coordinate
bulletY = 480  # y-coordinate
bulletX_change = 0
bulletY_change = 10
# Bullet States- 1.Ready-> Bullet isn't visible  2.Fire-> Bullet is moving
bullet_state = "ready"
# Score
score_value = 0
# Setting Font Size and Style
font = pygame.font.Font('font.otf', 40)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('font.otf', 80)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    # Blit used to draw in game window- (image, (x-coordinate, y-coordinate))
    screen.blit(playerImg, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (100, 250))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Function to confirm collision by making use of distance between the coordinates of enemy and bullet
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    # Setting background color in RGB Code (0-255)
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    # Ensuring game window is closed only on pressing cross button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # If theres a keystroke, checks whether its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        # KEYDOWN checks whether key is pressed, KEYUP checks whether pressed key is released
        # Movement of player is controlled by change in x-coordinate of the player
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    # Boundary Conditions so that the spaceship doesnt cross the boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736  # 736 because player.png is of 64 pixels we do not want it to cross the boundary thus (800-64)

    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    show_score(textX, textY)
    # Updates display regularly- compulsory function
    pygame.display.update()
