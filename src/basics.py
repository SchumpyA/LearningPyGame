import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # makes the screen
clock = pygame.time.Clock()  # sets the timing

player = pygame.Rect(100, 100, 50, 50)  # makes a rectangle to be put on the screen
enemy = pygame.Rect(random.randint(0, 750), 0, 50, 50)  # (x, y, width, height)

speed = 5
enemy_speed = 5

running = True
while running:
    clock.tick(60)  #60 fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # checks if game window has been closed, if it has been stop running
            running = False

    keys = pygame.key.get_pressed()  # gets input from keybaord
    if keys[pygame.K_w]: player.y -= speed
    if keys[pygame.K_s]: player.y += speed
    if keys[pygame.K_a]: player.x -= speed
    if keys[pygame.K_d]: player.x += speed

    enemy.y += enemy_speed
    if enemy.y > HEIGHT:
        enemy.y = 0
        enemy.x = random.randint(0, 750)

    if player.colliderect(enemy):  # checks for collision between rects
        print("Game Over")
        running = False

    screen.fill((0, 0, 0))  # clears the screen
    pygame.draw.rect(screen, (0, 255, 0), player)  # brings back the player and enemies
    pygame.draw.rect(screen, (255, 0, 0), enemy)
    pygame.display.flip()  # updates the screen as needed

pygame.quit()  # closes the game
sys.exit()     # closes the program