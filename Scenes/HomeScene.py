import pygame
from Utils.SceneManager import Scene
from Components.Button import Button
from Components.VerticalGradient import VerticalGradient
from Scenes.GameScene import GameScene
from Scenes.SettingsScene import SettingsScene
from Scenes.AchievementsScene import AchievementsScene
from Utils import PlayerDataContext


class HomeScene(Scene):
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.player_data = PlayerDataContext.get_data()
        self.all_buttons = pygame.sprite.Group()
        self.all_textfields = pygame.sprite.Group()
        self.player_name = PlayerDataContext.get_player_name()

        self.window_size = pygame.display.get_surface().get_size()

        self.create_ui()

    def create_ui(self):
        self.all_buttons.empty()
        self.all_textfields.empty()

        width, height = self.window_size

        center_x = width // 2
        start_y = height * 0.5
        button_spacing = height * 0.08

        self.start_button = Button(
            "Start Game" if self.player_data.get("score", 0) == 0 else "Continue",
            (center_x, start_y),
            font_size=int(height * 0.06),
            color=(255, 255, 255),
            bg_color=(0, 100, 0),
            button_action=self.start_game,
        )
        self.all_buttons.add(self.start_button)

        self.settings_button = Button(
            "Settings",
            (center_x, start_y + button_spacing),
            font_size=int(height * 0.05),
            color=(255, 255, 255),
            bg_color=(0, 0, 100),
            button_action=lambda: self.scene_manager.set_scene(
                SettingsScene(self.scene_manager)
            ),
        )
        self.all_buttons.add(self.settings_button)

        self.achievements_button = Button(
            "Achievements",
            (center_x, start_y + button_spacing * 2),
            font_size=int(height * 0.05),
            color=(255, 255, 255),
            bg_color=(100, 100, 0),
            button_action=lambda: self.scene_manager.set_scene(
                AchievementsScene(self.scene_manager)
            ),
        )
        self.all_buttons.add(self.achievements_button)

        self.quit_button = Button(
            "Quit Game",
            (center_x, start_y + button_spacing * 3),
            font_size=int(height * 0.05),
            color=(255, 255, 255),
            bg_color=(100, 0, 0),
            button_action=self.scene_manager.quit_game,
        )
        self.all_buttons.add(self.quit_button)

        title_font_size = int(height * 0.1)
        self.title_text = pygame.font.Font(None, title_font_size).render(
            f"Welcome {self.player_name}", True, (255, 255, 255)
        )
        self.title_pos = (center_x * 0.75, height * 0.15)

        self.gradient = VerticalGradient((0, 0, 0), (0, 0, 100), width, height)

    def start_game(self):
        self.scene_manager.set_scene(GameScene(self.scene_manager))

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

    def update(self, delta_time):
        current_size = pygame.display.get_surface().get_size()
        if current_size != self.window_size:
            self.window_size = current_size
            self.create_ui()

        self.all_buttons.update()

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.gradient.gradient_surface, (0, 0))
        screen.blit(self.title_text, self.title_pos)
        self.all_buttons.draw(screen)
