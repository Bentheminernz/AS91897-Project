import pygame

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

    def set_scene(self, scene):
        self.current_scene = scene

    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self, delta_time):
        if self.current_scene:
            self.current_scene.update(delta_time)

    def render(self, screen):
        if self.current_scene:
            self.current_scene.render(screen)