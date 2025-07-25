import pygame
from Utils.SceneManager import Scene
from Components.Button import Button
from Components.Textfield import TextField
from Scenes.HomeScene import HomeScene
from Utils.loggerConfig import game_logger
from Utils import PlayerDataContext


# this is the intro scene of the game, where the player can enter their name and continue to the home scene
class IntroScene(Scene):
    # initializes the intro scene
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.player_data = PlayerDataContext.get_data()

        self.all_buttons = pygame.sprite.Group()
        self.all_textfields = pygame.sprite.Group()

        self.font = pygame.font.Font(None, 36)
        self.intro_text = self.font.render(
            "Welcome to the Game!", True, (255, 255, 255)
        )

        self.name_textfield = TextField(
            self.font,
            None,
            "What's your name?",
            (200, 200),
            max_length=20,
        )
        self.all_textfields.add(self.name_textfield)

        self.continue_button = Button(
            "Continue",
            (400, 300),
            font_size=30,
            color=(255, 255, 255),
            bg_color=(0, 100, 0),
            button_action=self.continue_action,
        )
        self.all_buttons.add(self.continue_button)

    # function to check if the player has completed the intro
    def continue_action(self):
        if not self.name_textfield.text:
            game_logger.error("Player name is empty. Exiting.")
            return

        self.player_data["player_name"] = self.name_textfield.text
        self.player_data["completed_intro"] = True
        PlayerDataContext.update_data(self.player_data)
        self.scene_manager.set_scene(HomeScene(self.scene_manager))

    # function to create the UI for the intro scene
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False

            for button in self.all_buttons:
                if hasattr(button, "handle_event"):
                    button.handle_event(event)

            for textfield in self.all_textfields:
                textfield.handle_event(event)

        return True

    # renders the intro scene
    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.intro_text, (200, 100))
        self.all_buttons.draw(screen)
        self.all_textfields.draw(screen)

    # updates the intro scene every frame
    def update(self, delta_time):
        self.all_buttons.update()
        self.all_textfields.update()
