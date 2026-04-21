import pygame, sys
import random

# Colors in game
backgroundColor = (150, 150, 175)
ballColor = (200,200,200)
lineColor = (255, 255, 255)
textColor = (50, 50, 50)

# Movement Variables
ballXSpeed = 7 * random.choice((1, -1))
ballYSpeed = 7 * random.choice((1, -1))
playerSpeed = 7
opponentSpeed = 7

# Text Variables
playerScore = 0
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
        return True

    if (ball.colliderect(player) or ball.colliderect(opponent)):
        ballXSpeed *= -1

    return False

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

def opponentMovement(opponent, keys, screenHeight):
    global opponentSpeed

    if keys[pygame.K_UP]:
        opponent.y -= opponentSpeed
    if keys[pygame.K_DOWN]:
        opponent.y += opponentSpeed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screenHeight:
        opponent.bottom = screenHeight

# Text Functions
def updateScoreBoard(screen, gameFont, textColor):
    playerText = gameFont.render(f"Score: {playerScore}", False, textColor)
    screen.blit(playerText, (1160, 10))

    opponentText = gameFont.render(f"Score: {opponentScore}", False, textColor)
    screen.blit(opponentText, (10, 10))

def startGame(gameState, screen, gameFont, screenWidth, screenHeight):
    screen.fill(backgroundColor)

    title = gameFont.render("PONG", False, textColor)
    option1 = gameFont.render("Press 1: Play vs AI", False, textColor)
    option2 = gameFont.render("Press 2: 2 Player Mode", False, textColor)

    screen.blit(title, (screenWidth//2 - 40, screenHeight//3))
    screen.blit(option1, (screenWidth//2 - 120, screenHeight//2))
    screen.blit(option2, (screenWidth//2 - 140, screenHeight//2 + 40))
    pygame.display.flip()

def scoreScreen(gameState, screen, gameFont, screenWidth, screenHeight):
    screen.fill(backgroundColor)

    title = gameFont.render("Choose Win Condition", False, textColor)
    option1 = gameFont.render("Press 1: First to 1", False, textColor)
    option2 = gameFont.render("Press 2: First to 10", False, textColor)
    option3 = gameFont.render("Press 3: First to 25", False, textColor)

    screen.blit(title, (screenWidth//2 - 120, screenHeight//3))
    screen.blit(option1, (screenWidth//2 - 120, screenHeight//2))
    screen.blit(option2, (screenWidth//2 - 120, screenHeight//2 + 40))
    screen.blit(option3, (screenWidth//2 - 120, screenHeight//2 + 80))

    pygame.display.flip()

def resetScores():
    global playerScore, opponentScore
    playerScore = 0
    opponentScore = 0