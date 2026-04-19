import pygame
import random

# Movement Variables
ballXSpeed = 7 * random.choice((1, -1))
ballYSpeed = 7 * random.choice((1, -1))
playerSpeed = 7
opponentSpeed = 7

# Text Variables
playerScore = 0  # TO FUTURE SELF, MAKE MAX SCORE 100
opponentScore = 0

# Movement Functions
def ballScored(ball, screenWidth, screenHeight):
    global ballXSpeed, ballYSpeed, playerScore, opponentScore

    if ball.left <= 0: playerScore += 1
    if ball.right >= screenWidth: opponentScore += 1

    ball.center = (screenWidth/2, screenHeight/2)
    ballYSpeed *= random.choice((1, -1))
    ballXSpeed *= random.choice((1, -1))

def ballMovement(ball, player, opponent, screenWidth, screenHeight):
    global ballXSpeed, ballYSpeed
    ball.x += ballXSpeed
    ball.y += ballYSpeed

    if (ball.top <= 0 or ball.bottom >= screenHeight):
        ballYSpeed *= -1
    if (ball.left <= 0 or ball.right >= screenWidth):
        ballScored(ball, screenWidth, screenHeight)

    if (ball.colliderect(player) or ball.colliderect(opponent)):
        ballXSpeed *= -1

def playerMovement(player, keys, screenHeight):
    global playerSpeed

    if keys[pygame.K_w]: player.y -= playerSpeed
    if keys[pygame.K_s]: player.y += playerSpeed

    if player.top <= 0: player.top = 0
    if player.bottom >= screenHeight: player.bottom = screenHeight

def opponentAI(opponent, ball, screenHeight):
    global opponentSpeed

    if opponent.top < ball.y: opponent.y += opponentSpeed
    if opponent.bottom > ball.y: opponent.y -= opponentSpeed

    if opponent.top <= 0: opponent.top = 0
    if opponent.bottom >= screenHeight: opponent.bottom = screenHeight

# Text Functions
def updateScoreBoard(screen, gameFont, textColor):
    playerText = gameFont.render(f"Score: {playerScore}", False, textColor)
    screen.blit(playerText, (1160, 10))

    opponentText = gameFont.render(f"Score: {opponentScore}", False, textColor)
    screen.blit(opponentText, (10, 10))
