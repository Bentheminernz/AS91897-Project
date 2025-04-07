import pygame
from Components.Player import Player
from Components.QuestionBlock import QuestionBlock
from Utils.fetchGitCommitCount import fetch_git_commit_count
from Utils.fetchRandomQuestion import fetch_random_question
from Utils.fetchGitCommitID import fetch_git_commit_id

build_number = fetch_git_commit_count()
commit_id = fetch_git_commit_id()
random_question = fetch_random_question()

pygame.init()

# Defining the screen variables
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(f"2.6 Platformer Build {build_number} ({commit_id})")
all_sprites = pygame.sprite.Group()

Player1 = Player("./Assets/Players/Player1.png", (550, 50))
all_sprites.add(Player1)

question_text = random_question.get("question_title", "No question found")
answers = random_question.get("answers", ["No answers found"])

question_blocks = []
start_x = 100
start_y = 250
spacing = 150

for i, answer in enumerate(answers):
    answer_text = answer.get("answer_text", "No answer text found")
    print(answer_text)
    block_x = start_x + (i * spacing)
    block_y = start_y
    block = QuestionBlock("./Assets/QuestionBlocks/QuestionBlock1.png", (block_x, block_y), answer_text)
    all_sprites.add(block)
    question_blocks.append(block)

print(f"Question Blocks: {question_blocks}")

font = pygame.font.Font(None, 36)
question_surface = font.render(question_text, True, (255, 255, 255))

running = True
clock = pygame.time.Clock()
while running:
    delta_time = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    Player1.gravity(delta_time, screen)
    
    for block in question_blocks:
        block.on_collision(Player1)

    all_sprites.update(screen, delta_time)
    screen.fill((0, 0, 0))

    all_sprites.draw(screen)
    screen.blit(question_surface, (10, 10))

    pygame.display.flip()

pygame.quit()