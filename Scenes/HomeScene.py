import pygame
from Utils.SceneManager import Scene
from Components.Button import Button
from Components.Textfield import TextField
from Scenes.GameScene import GameScene

class HomeScene(Scene):
    def __init__(self, scene_manager, player_data):
        self.scene_manager = scene_manager
        self.player_data = player_data
        self.has_completed_intro = player_data.get("completed_intro", False)
        self.all_buttons = pygame.sprite.Group()
        self.all_textfields = pygame.sprite.Group()

        self.start_button = Button(
            "Start Game",
            (400, 300),
            font_size=30,
            color=(255, 255, 255),
            bg_color=(0, 100, 0),
            button_action=self.start_game,
        )
        self.all_buttons.add(self.start_button)

        self.quit_button = Button(
            "Quit Game",
            (400, 400),
            font_size=30,
            color=(255, 255, 255),
            bg_color=(100, 0, 0),
            button_action=self.scene_manager.quit_game,
        )
        self.all_buttons.add(self.quit_button)

        if not self.has_completed_intro:
            self.intro_text = TextField(
                pygame.font.Font(None, 36),
                "Welcome to the game!",
                "what is your name?",
                (200, 200),
                max_length=50
            )
            textfield_instance = self.intro_text
            value = textfield_instance.text

        self.title_font = pygame.font.Font(None, 74)
        self.title_text = self.title_font.render("Home Scene", True, (255, 255, 255))

    def start_game(self):
        self.scene_manager.set_scene(GameScene(self.scene_manager, self.player_data))

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
        self.all_buttons.update()

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.title_text, (200, 100))
        self.all_buttons.draw(screen)
        if not self.has_completed_intro:
            self.all_textfields.update()
            self.all_textfields.draw(screen)