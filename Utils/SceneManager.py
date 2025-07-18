import pygame
from Utils.loggerConfig import scene_logger


# defines a base scene class, that is inherited by all scenes
class Scene:
    def __init__(self):
        pass

    def handle_events(self, events):
        pass

    def update(self, delta_time):
        pass

    def render(self, screen):
        pass


# defines a scene manager class, this manages the current scene and handles the events, update and render methods
class SceneManager:
    def __init__(self, screen):
        self.current_scene = None
        self.screen = screen

    # this method sets the current scene to the given scene and logs the switch
    def set_scene(self, scene):
        scene_logger.info(f"Scene Manager: Switching to {scene.__class__.__name__}")
        self.current_scene = scene

    # this method handles the events for the current scene
    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events)

    # this method updates the current scene with the given delta time
    def update(self, delta_time):
        if self.current_scene:
            self.current_scene.update(delta_time)

    # this method renders the current scene to the screen
    def render(self, screen):
        if self.current_scene:
            self.current_scene.render(screen)

    def quit_game(self):
        pygame.quit()
        exit(0)
