import pygame
from Components.Player import Player
from Components.QuestionBlock import QuestionBlock
from Utils.fetchGitCommitCount import fetch_git_commit_count
from Utils.fetchRandomQuestion import fetch_random_question

build_number = fetch_git_commit_count()
random_question = fetch_random_question()
question_title = random_question.get("question", "No question found")
pygame.init()

# Defining the screen variables
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(f"2.6 Platformer Build {build_number}")
all_sprites = pygame.sprite.Group()

Player1 = Player("./Assets/Players/Player1.png", (500, 100))
QuestionBlock1 = QuestionBlock("./Assets/QuestionBlocks/QuestionBlock1.png", (100, 100), "Hello World!")
all_sprites.add([Player1, QuestionBlock1])

font = pygame.font.Font(None, 36)
text = font.render(question_title, True, (255, 255, 255))

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
    screen.blit(text, (10, 10))  # Draw the text on the screen

    pygame.display.flip()

pygame.quit()