import pygame
from Components.Player import Player
from Components.QuestionBlock import QuestionBlock
from Components.Button import Button
from Utils.fetchGitCommitCount import fetch_git_commit_count
from Utils.fetchRandomQuestion import fetch_random_question
from Utils.fetchGitCommitID import fetch_git_commit_id
from Utils import playerDataManagement

# defines some variables, based on functions from my utils.
# build number based on commits in my repo
# commit id based on the last commit in my repo
# random question from `./Assets/data/questions.json`
build_number = fetch_git_commit_count()
commit_id = fetch_git_commit_id()
random_question = fetch_random_question()

global player_data
player_data = playerDataManagement.load_player_data()

pygame.init()

# define screen size, creates the window and makes sprite group
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(f"2.6 Platformer Build {build_number} ({commit_id})")
all_sprites = pygame.sprite.Group()
all_buttons = pygame.sprite.Group()

# create player and adds to all sprites group
Player1 = Player("./Assets/Players/Player1.png", (650, 650))
all_sprites.add(Player1)

# gets the question text and answers from the random question
question_text = random_question.get("question_title", "No question found")
answers = random_question.get("answers", ["No answers found"])


question_blocks = []
start_x = 125
start_y = 200
spacing = 225

for i, answer in enumerate(answers):
    answer_text = answer.get("answer_text", "No answer text found")
    is_correct = answer.get("isCorrect", False)
    print(answer_text)
    block_x = start_x + (i * spacing)
    block_y = start_y
    block = QuestionBlock(
        "./Assets/QuestionBlocks/QuestionBlock1.png",
        (block_x, block_y),
        answer_text,
        is_correct,
        player_data,
    )
    all_sprites.add(block)
    question_blocks.append(block)

print(f"Question Blocks: {question_blocks}")

save_button = Button(
    "Save",
    (100, 100),
    font_size=24,
    color=(255, 255, 255),
    bg_color=(0, 0, 0),
    button_action=lambda: playerDataManagement.save_player_data(player_data),
)
all_buttons.add(save_button)

font = pygame.font.Font(None, 36)
question_surface = font.render(question_text, True, (255, 255, 255))

running = True
clock = pygame.time.Clock()

while running:
    delta_time = clock.tick(60) / 1000.0

    player_score = font.render(
        f"Score: {player_data['score']}", True, (255, 255, 255)
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    Player1.gravity(delta_time, screen)

    for block in question_blocks:
        block.on_collision(Player1)

    all_sprites.update(screen, delta_time)
    all_buttons.update()
    screen.fill((0, 0, 0))

    all_sprites.draw(screen)
    all_buttons.draw(screen)
    screen.blit(question_surface, (10, 10))
    screen.blit(player_score, (675, 10))

    pygame.display.flip()

pygame.quit()
