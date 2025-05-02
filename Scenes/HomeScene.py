import pygame
from Utils.SceneManager import Scene
from Components.Button import Button
from Components.Textfield import TextField
from Scenes.GameScene import GameScene

class HomeScene(Scene):
    def __init__(self, scene_manager, player_data):
        self.scene_manager = scene_manager
        self.player_data = player_data
        self.all_buttons = pygame.sprite.Group()
        self.all_textfields = pygame.sprite.Group()
        self.player_name = player_data.get("player_name", "Player")

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
        
        self.title_text = pygame.font.Font(None, 72).render(
            f"Welcome {self.player_name}", True, (255, 255, 255)
        )

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