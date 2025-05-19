import pygame
import json
from Utils.SceneManager import Scene
from Utils import PlayerDataContext
from Utils.loggerConfig import game_logger
from Components.AchievementListItem import AchievementListItem

class AchievementsScene(Scene):
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.player_data = PlayerDataContext.get_data()
        self.achievements = self.fetch_achievements()
        self.unlocked_achievements = self.fetch_unlocked_achievements()

        self.window_size = pygame.display.get_surface().get_size()
        self.font = pygame.font.Font(None, int(self.window_size[1] * 0.05))
        self.all_list_items = pygame.sprite.Group()
        self.create_ui()

    def create_ui(self):
        self.all_list_items.empty()

        width, height = self.window_size
        center_x = width // 2
        start_y = height * 0.1
        item_spacing = height * 0.05

        for index, achievement in enumerate(self.unlocked_achievements):
            item = AchievementListItem(
                achievement,
                (center_x, start_y + index * item_spacing),
                font_size=int(height * 0.07),
                color=(255, 255, 255),
                bg_color=(100, 100, 0),
            )
            self.all_list_items.add(item)

    def fetch_achievements(self):
        try:
            with open("Assets/data/achievements.json", "r") as file:
                json_achievements = json.load(file)
                achievements = json_achievements.get("achievements", [])
            return achievements
        except Exception as e:
            game_logger.error(f"An unexpected error occurred: {e}")
            exit(-1)

    def fetch_unlocked_achievements(self):
        return [
            achievement for achievement in self.achievements
            if achievement["id"] in self.player_data.get("achievements", [])
        ]

    def update(self, delta_time):
        self.all_list_items.update(delta_time)

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.all_list_items.draw(screen)