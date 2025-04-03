import pygame
from Components.Player import Player
from Components.QuestionBlock import QuestionBlock

pygame.init()

# Defining the screen variables
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
all_sprites = pygame.sprite.Group()

Player1 = Player("./Assets/Players/Player1.png", (500, 100))
QuestionBlock1 = QuestionBlock("./Assets/QuestionBlocks/QuestionBlock1.png", (100, 100), "Hello World!")
all_sprites.add([Player1, QuestionBlock1])

running = True
clock = pygame.time.Clock()
while running:
    delta_time = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    Player1.gravity(delta_time, screen)
    QuestionBlock1.on_collision(Player1)

    all_sprites.update(screen, delta_time)
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit() 