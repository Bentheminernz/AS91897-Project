import pygame
from Components.Player import Player

pygame.init()

# Defining the screen variables
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

Player1 = Player("./Assets/Players/Player1.png", (100, 100))

running = True
clock = pygame.time.Clock()
while running:
    delta_time = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    Player1.update(delta_time, screen)

    pygame.display.flip()
    screen.fill((0, 0, 0))

pygame.quit()