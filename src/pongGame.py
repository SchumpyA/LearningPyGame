import pygame
import sys
from pongFunctions import *

pygame.init()

# Screen and Clock set-up
WIDTH, HEIGHT = 1280, 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # makes the screen
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()  # sets the timing

# Game State work
gameState = "menu"   # menu -> start -> playing, score_pause
timerStart = pygame.time.get_ticks()
countdownTime = 3000  # 3 seconds for starting wait
gameMode = None

# Game Components
ball = pygame.Rect(WIDTH/2 - 15, HEIGHT/2 -15, 30, 30)
player = pygame.Rect(10, HEIGHT/2 - 70, 10, 149)
opponent = pygame.Rect(WIDTH - 20, HEIGHT/2 - 70, 10, 149)

gameFont = pygame.font.Font(None, 32)

running = True
while running:
    clock.tick(60)  #60 fps

    if(gameState == "menu"):
        startGame(gameState, screen, gameFont, WIDTH, HEIGHT)
        waiting = True  
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # checks if game window has been closed, if it has been stop running
                    pygame.quit()  # closes the game
                    sys.exit()     # closes the program
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        gameMode = "AI"
                        gameState = "start"
                        waiting = False
                    if event.key == pygame.K_2:
                        gameMode = "PVP"
                        gameState = "start"
                        waiting = False

    screen.fill(backgroundColor)    # Set up screen with components and clean line to seperate the midpoint
    pygame.draw.ellipse(screen, ballColor, ball)
    pygame.draw.rect(screen, ballColor, player)
    pygame.draw.rect(screen, ballColor, opponent)
    pygame.draw.aaline(screen, lineColor, (WIDTH/2, 0), (WIDTH/2, HEIGHT))

    # Gameplay
    keys = pygame.key.get_pressed()  # gets input from keybaord
    if gameState == "playing":
        scored = ballMovement(ball, player, opponent, WIDTH, HEIGHT) # moves ball unless ball is scored
        if scored:
            gameState = "score_pause"
            timerStart = pygame.time.get_ticks()
            countdownTime = 500  # 1 second pause after score
    playerMovement(player, keys, HEIGHT)
    if gameMode == "AI":
        opponentAI(opponent, ball, HEIGHT)
    elif gameMode == "PVP":
        opponentMovement(opponent, keys, HEIGHT)
    updateScoreBoard(screen, gameFont, textColor)

    currentTime = pygame.time.get_ticks()

    if gameState in ["start", "score_pause"]:
        elapsed = currentTime - timerStart
        if elapsed >= countdownTime:
            gameState = "playing"
        elif elapsed < countdownTime and gameState == "start":
            secondsLeft = (countdownTime - elapsed) // 1000 + 1
            countdownText = gameFont.render(str(secondsLeft), False, textColor)
            screen.blit(countdownText, (WIDTH//2 - 6, HEIGHT//2 - 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # checks if game window has been closed, if it has been stop running
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameState = "menu"
    
    pygame.display.flip()

pygame.quit()  # closes the game
sys.exit()     # closes the program