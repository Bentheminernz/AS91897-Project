import pygame
from Utils.SceneManager import SceneManager
from Scenes.HomeScene import HomeScene
from Scenes.IntroScene import IntroScene
from Utils.fetchGitCommitCount import fetch_git_commit_count
from Utils.fetchGitCommitID import fetch_git_commit_id
from Utils import PlayerDataContext

# defines some variables, based on functions from my utils.
# build number based on commits in my repo
# commit id based on the last commit ID in my repo
build_number = fetch_git_commit_count()
commit_id = fetch_git_commit_id()

PlayerDataContext.initialize()

player_data = PlayerDataContext.get_data()
has_completed_intro = player_data.get("completed_intro", False)

pygame.init()

# define screen size, creates the window and makes sprite group
screen_width = 1200
screen_height = 600
min_width = 1100
min_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption(
    f"AS91897 Platformer - Based upon build: {build_number} ({commit_id})"
)

# creates a scene manager instance and makes its inital the scene based on whether the intro has been completed or not.
# the scene manager is used to handle switching between scenes, for example, from the intro to the home scene.
# it is custom written by me :)
scene_manager = SceneManager(screen)
if not has_completed_intro:
    scene_manager.set_scene(IntroScene(scene_manager))
else:
    scene_manager.set_scene(HomeScene(scene_manager))

# creates the game loop
running = True
clock = pygame.time.Clock()

# while the loop is running, run the game!
while running:
    # delta_time is time since last frame. this is used to make sure the game doesn't slow down during frame drops
    delta_time = clock.tick(60) / 1000.0
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # make sure the screen is not smaller than the minimum size
            new_width = max(event.w, min_width)
            new_height = max(event.h, min_height)
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

    # handles events, updates the scene and renders it to the screen
    scene_manager.handle_events(events)
    scene_manager.update(delta_time)
    scene_manager.render(screen)

    pygame.display.flip()

pygame.quit()
