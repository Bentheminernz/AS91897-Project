import pygame
from Components.Button import Button
from Components.Textfield import TextField
from Components.Checkbox import Checkbox
from Utils.SceneManager import Scene
from Utils.loggerConfig import utils_logger
from Utils import PlayerDataContext
from Utils import playerDataManagement


# this is the settings scene of the game, players can change their name, toggle sound effects, reset the game, or return to the home scene
class SettingsScene(Scene):
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager

        self.player_data = PlayerDataContext.get_data()

        self.all_sprites = pygame.sprite.Group()
        self.all_buttons = pygame.sprite.Group()
        self.all_checkboxes = pygame.sprite.Group()
        self.all_textfields = pygame.sprite.Group()

        self.window_size = pygame.display.get_surface().get_size()

        self.create_ui()

    # function to return to the home scene
    def create_ui(self):
        self.all_buttons.empty()
        self.all_checkboxes.empty()
        self.all_textfields.empty()
        self.all_sprites.empty()

        width, height = self.window_size

        center_x = width // 2
        start_y = height * 0.5
        item_spacing = height * 0.08

        self.font = pygame.font.Font(None, int(height * 0.05))

        self.name_textfield = TextField(
            self.font,
            self.player_data.get("player_name", ""),
            "Player Name",
            (center_x - 100, start_y - item_spacing),
            max_length=20,
        )
        self.all_textfields.add(self.name_textfield)

        sound_checkbox = Checkbox(
            "Sound Effects",
            (center_x, start_y + item_spacing),
            size=20,
            font_size=30,
            text_color=(255, 255, 255),
            border_color=(255, 255, 255),
            check_color=(0, 255, 0),
            bg_color=(0, 0, 0),
            initial_state=self.player_data.get("settings", {}).get("sound", False),
            on_toggle=self.toggle_sound,
        )
        self.all_checkboxes.add(sound_checkbox)
        reset_button = Button(
            "Reset Game",
            (center_x, start_y + item_spacing * 2),
            font_size=30,
            color=(255, 255, 255),
            bg_color=(255, 0, 0),
            button_action=self.reset_game,
        )
        self.all_buttons.add(reset_button)

        save_button = Button(
            "Return to Home and Save",
            (center_x, start_y + item_spacing * 4),
            font_size=30,
            color=(255, 255, 255),
            bg_color=(0, 100, 0),
            button_action=lambda: self.return_to_home(save=True),
        )
        self.all_buttons.add(save_button)

        back_button = Button(
            "Return to Home without Saving",
            (center_x, start_y + item_spacing * 4.75),
            font_size=20,
            color=(255, 255, 255),
            bg_color=(0, 0, 100),
            button_action=lambda: self.return_to_home(save=False),
        )
        self.all_buttons.add(back_button)

        title_font_size = int(height * 0.1)
        self.title_text = pygame.font.Font(None, title_font_size).render(
            "Settings", True, (255, 255, 255)
        )
        self.title_pos = (center_x * 0.75, height * 0.15)

    # function to toggle sound effects
    def toggle_sound(self, is_checked):
        if "settings" not in self.player_data:
            self.player_data["settings"] = {}
        self.player_data["settings"]["sound"] = is_checked
        utils_logger.info(f"Sound setting changed to: {is_checked}")

    # function to return to the home scene, optionally saving the settings
    def return_to_home(self, save=True):
        from Scenes.HomeScene import HomeScene

        if save:
            self.player_data["player_name"] = self.name_textfield.text
            PlayerDataContext.update_data(self.player_data)
            utils_logger.info("Settings saved successfully.")

        self.scene_manager.set_scene(HomeScene(self.scene_manager))

    # function to reset the game data
    def reset_game(self):
        playerDataManagement.delete_player_data()
        exit(0)

    # function to handle events in the settings scene
    def handle_events(self, events):
        for event in events:
            for button in self.all_buttons:
                if hasattr(button, "handle_event"):

                    button.handle_event(event)

            for checkbox in self.all_checkboxes:
                if hasattr(checkbox, "handle_event"):
                    checkbox.handle_event(event)

            for textfield in self.all_textfields:
                if hasattr(textfield, "handle_event"):
                    textfield.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from Scenes.HomeScene import HomeScene

                    self.scene_manager.set_scene(HomeScene(self.scene_manager))

        return True

    # updates the settings scene every frame
    def update(self, delta_time):
        current_size = pygame.display.get_surface().get_size()
        if current_size != self.window_size:
            self.window_size = current_size
            self.create_ui()

        self.all_buttons.update()
        self.all_checkboxes.update()
        self.all_textfields.update()

    # renders the settings scene
    def render(self, screen):
        screen.fill((0, 0, 0))

        screen.blit(self.title_text, self.title_pos)

        self.all_buttons.draw(screen)
        self.all_checkboxes.draw(screen)
        self.all_textfields.draw(screen)
