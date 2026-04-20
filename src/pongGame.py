import pygame
import sys
import pongFunctions as pf

pygame.init()

# Screen and Clock set-up
WIDTH, HEIGHT = 1280, 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # makes the screen
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()  # sets the timing

# Game State work
gameState = "menu_mode"   # menu_mode -> menu_score -> start -> playing, score_pause
timerStart = pygame.time.get_ticks()
countdownTime = 3000  # 3 seconds for starting wait
gameMode = None
maxScore = 0
winner = None

# Game Components
ball = pygame.Rect(WIDTH/2 - 15, HEIGHT/2 -15, 30, 30)
player = pygame.Rect(10, HEIGHT/2 - 70, 10, 149)
opponent = pygame.Rect(WIDTH - 20, HEIGHT/2 - 70, 10, 149)

gameFont = pygame.font.Font(None, 32)

running = True
while running:
    clock.tick(60)

    # ===================== EVENTS =====================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # ---- MENU: MODE SELECTION ----
            if gameState == "menu_mode":
                if event.key == pygame.K_1:
                    gameMode = "AI"
                    gameState = "menu_score"
                elif event.key == pygame.K_2:
                    gameMode = "PVP"
                    gameState = "menu_score"

            # ---- MENU: SCORE SELECTION ----
            elif gameState == "menu_score":
                if event.key == pygame.K_1:
                    maxScore = 1
                elif event.key == pygame.K_2:
                    maxScore = 10
                elif event.key == pygame.K_3:
                    maxScore = 25

                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    pf.resetScores()
                    ball.center = (WIDTH//2, HEIGHT//2)

                    gameState = "start"
                    timerStart = pygame.time.get_ticks()
                    countdownTime = 3000

            # ---- GAME OVER: RESTART ----
            elif gameState == "game_over":
                if event.key == pygame.K_r:
                    gameState = "menu_mode"

            # ---- GLOBAL ----
            if event.key == pygame.K_ESCAPE:
                gameState = "menu_mode"

    # ===================== DRAW / LOGIC =====================

    screen.fill(pf.backgroundColor)

    # ---- MENU: MODE ----
    if gameState == "menu_mode":
        title = gameFont.render("PONG", False, pf.textColor)
        option1 = gameFont.render("1: Play vs AI", False, pf.textColor)
        option2 = gameFont.render("2: 2 Player Mode", False, pf.textColor)

        screen.blit(title, (WIDTH//2 - 40, HEIGHT//3))
        screen.blit(option1, (WIDTH//2 - 120, HEIGHT//2))
        screen.blit(option2, (WIDTH//2 - 140, HEIGHT//2 + 40))

    # ---- MENU: SCORE ----
    elif gameState == "menu_score":
        title = gameFont.render("Choose Win Condition", False, pf.textColor)
        option1 = gameFont.render("1: First to 1", False, pf.textColor)
        option2 = gameFont.render("2: First to 10", False, pf.textColor)
        option3 = gameFont.render("3: First to 25", False, pf.textColor)

        screen.blit(title, (WIDTH//2 - 120, HEIGHT//3))
        screen.blit(option1, (WIDTH//2 - 120, HEIGHT//2))
        screen.blit(option2, (WIDTH//2 - 120, HEIGHT//2 + 40))
        screen.blit(option3, (WIDTH//2 - 120, HEIGHT//2 + 80))

    # ---- GAME OVER ----
    elif gameState == "game_over":
        if gameMode == "AI":
            text = "You Win" if winner == "player" else "You Lose"
        else:
            text = "Player 1 Wins" if winner == "player" else "Player 2 Wins"

        winText = gameFont.render(text, False, pf.textColor)
        restartText = gameFont.render("Press R to Restart", False, pf.textColor)

        screen.blit(winText, (WIDTH//2 - 100, HEIGHT//2))
        screen.blit(restartText, (WIDTH//2 - 140, HEIGHT//2 + 40))
        pygame.display.flip()
        continue

    # ---- GAMEPLAY STATES ----
    else:
        # Draw game objects
        pygame.draw.ellipse(screen, pf.ballColor, ball)
        pygame.draw.rect(screen, pf.ballColor, player)
        pygame.draw.rect(screen, pf.ballColor, opponent)
        pygame.draw.aaline(screen, pf.lineColor, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

        keys = pygame.key.get_pressed()

        # ---- PLAYING ----
        if gameState == "playing":
            scored = pf.ballMovement(ball, player, opponent, WIDTH, HEIGHT)

            if scored:
                if pf.playerScore >= maxScore:
                    winner = "player"
                    gameState = "game_over"
                    continue
                elif pf.opponentScore >= maxScore:
                    winner = "opponent"
                    gameState = "game_over"
                    continue
                else:
                    gameState = "score_pause"
                    timerStart = pygame.time.get_ticks()
                    countdownTime = 500

        # ---- PLAYER MOVEMENT ----
        pf.playerMovement(player, keys, HEIGHT)

        if gameMode == "AI":
            pf.opponentAI(opponent, ball, HEIGHT)
        else:
            pf.opponentMovement(opponent, keys, HEIGHT)

        # ---- SCOREBOARD ----
        pf.updateScoreBoard(screen, gameFont, pf.textColor)

        # ---- TIMERS (start + pause) ----
        if gameState in ["start", "score_pause"]:
            elapsed = pygame.time.get_ticks() - timerStart

            if elapsed >= countdownTime:
                gameState = "playing"
            elif gameState == "start":
                secondsLeft = (countdownTime - elapsed) // 1000 + 1
                countdownText = gameFont.render(str(secondsLeft), False, pf.textColor)
                screen.blit(countdownText, (WIDTH//2 - 6, HEIGHT//2 - 10))

    pygame.display.flip()

pygame.quit()  # closes the game
sys.exit()     # closes the program