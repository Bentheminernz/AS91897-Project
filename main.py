import pygame
from Utils.SceneManager import SceneManager
from Scenes.HomeScene import HomeScene
from Scenes.IntroScene import IntroScene
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

global player_data
player_data = playerDataManagement.load_player_data()
has_completed_intro = player_data.get("completed_intro", False)

pygame.init()

# define screen size, creates the window and makes sprite group
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption(f"2.6 Platformer - Based upon build: {build_number} ({commit_id})")

scene_manager = SceneManager(screen)
if not has_completed_intro:
    scene_manager.set_scene(IntroScene(scene_manager, player_data))
else:
    scene_manager.set_scene(HomeScene(scene_manager, player_data))

running = True
clock = pygame.time.Clock()

while running:
    delta_time = clock.tick(60) / 1000.0
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    scene_manager.handle_events(events)
    scene_manager.update(delta_time)
    scene_manager.render(screen)

    pygame.display.flip()

pygame.quit()