import pygame
import json
from Utils.SceneManager import Scene
from Utils import PlayerDataContext
from Utils.loggerConfig import game_logger

class AchievementsScene(Scene):
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.player_data = PlayerDataContext.get_data()
        self.achievements = self.fetch_achievements()
        self.unlocked_achievements = self.fetch_unlocked_achievements()

        self.window_size = pygame.display.get_surface().get_size()
        self.font = pygame.font.Font(None, int(self.window_size[1] * 0.05))
        self.all_list_items = pygame.sprite.Group()

    def fetch_achievements(self):
        try:
            with open("Assets/data/achievements.json", "r") as file:
                achievements = json.load(file)
            return achievements
        except FileNotFoundError:
            game_logger.error("Achievements file not found.")
            exit(-1)
        except json.JSONDecodeError:
            game_logger.error("Error decoding JSON from achievements file.")
            exit(-1)
        except Exception as e:
            game_logger.error(f"An unexpected error occurred: {e}")
            exit(-1)

    def fetch_unlocked_achievements(self):
        unlocked = []
        for achievement in self.achievements:
            if achievement["id"] in self.player_data.get("achievements", []):
                unlocked.append(achievement)
        return unlocked
    
    def display_achievements(self):
        # This method would handle the display of achievements on the screen.
        # For now, we will just log the achievements to the console.
        for achievement in self.unlocked_achievements:
            game_logger.info(f"Unlocked Achievement: {achievement['name']}")