import pygame
import sys
from pongFunctions import *

pygame.init()

# Screen and Clock set-up
WIDTH, HEIGHT = 1280, 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # makes the screen
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()  # sets the timing

# Game Components
ball = pygame.Rect(WIDTH/2 - 15, HEIGHT/2 -15, 30, 30)
player = pygame.Rect(WIDTH - 20, HEIGHT/2 - 70, 10, 149)
opponent = pygame.Rect(10, HEIGHT/2 - 70, 10, 149)

# Colors in game
backgroundColor = (100, 100, 125)
ballColor = (200,200,200)
lineColor = (255, 255, 255)
textColor = (50, 50, 50)

gameFont = pygame.font.Font(None, 32)

running = True
while running:
    clock.tick(60)  #60 fps

    screen.fill(backgroundColor)    # Set up screen with components and clean line to seperate the midpoint
    pygame.draw.ellipse(screen, ballColor, ball)
    pygame.draw.rect(screen, ballColor, player)
    pygame.draw.rect(screen, ballColor, opponent)
    pygame.draw.aaline(screen, lineColor, (WIDTH/2, 0), (WIDTH/2, HEIGHT))

    # Gameplay
    keys = pygame.key.get_pressed()  # gets input from keybaord
    ballMovement(ball, player, opponent, WIDTH, HEIGHT)
    playerMovement(player, keys, HEIGHT)
    opponentAI(opponent, ball, HEIGHT)
    updateScoreBoard(screen, gameFont, textColor)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # checks if game window has been closed, if it has been stop running
            running = False
    
    pygame.display.flip()

pygame.quit()  # closes the game
sys.exit()     # closes the program