import pygame
import json
from Utils.SceneManager import Scene
from Utils import PlayerDataContext
from Utils.loggerConfig import game_logger
from Components.Button import Button
from Components.AchievementListItem import AchievementListItem


class AchievementsScene(Scene):
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.player_data = PlayerDataContext.get_data()
        self.achievements = self.fetch_achievements()
        self.unlocked_achievements = self.fetch_unlocked_achievements()

        self.window_size = pygame.display.get_surface().get_size()
        self.font = pygame.font.Font(None, int(self.window_size[1] * 0.05))
        self.title_font = pygame.font.Font(None, int(self.window_size[1] * 0.08))
        self.unlocked_list_items = pygame.sprite.Group()
        self.locked_list_items = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.unlocked_scroll_y = 0
        self.locked_scroll_y = 0
        self.scroll_speed = 20

        self.create_ui()

    def return_home(self):
        from Scenes.HomeScene import HomeScene

        self.scene_manager.set_scene(HomeScene(self.scene_manager))

    def create_ui(self):
        self.unlocked_list_items.empty()
        self.locked_list_items.empty()
        self.buttons.empty()

        width, height = self.window_size
        center_x = width // 2

        self.unlocked_header = self.title_font.render(
            "Unlocked Achievements", True, (255, 255, 255)
        )
        self.unlocked_header_rect = self.unlocked_header.get_rect(
            center=(center_x, height * 0.1)
        )

        self.locked_header = self.title_font.render(
            "Locked Achievements", True, (255, 255, 255)
        )
        self.locked_header_rect = self.locked_header.get_rect(
            center=(center_x, height * 0.55)
        )

        unlocked_start_y = height * 0.20
        item_spacing = height * 0.12

        for index, achievement in enumerate(self.unlocked_achievements):
            item = AchievementListItem(
                achievement,
                (center_x, unlocked_start_y + index * item_spacing),
                font_size=int(height * 0.04),
                color=(255, 255, 255),
                bg_color=(0, 100, 0),
            )
            self.unlocked_list_items.add(item)

        locked_start_y = height * 0.65

        locked_achievements = [
            a for a in self.achievements if a not in self.unlocked_achievements
        ]
        for index, achievement in enumerate(locked_achievements):
            item = AchievementListItem(
                achievement,
                (center_x, locked_start_y + index * item_spacing),
                font_size=int(height * 0.04),
                color=(200, 200, 200),
                bg_color=(100, 0, 0),
            )
            self.locked_list_items.add(item)

        self.unlocked_scroll_area = pygame.Rect(
            0,
            self.unlocked_header_rect.bottom,
            width,
            self.locked_header_rect.top - self.unlocked_header_rect.bottom,
        )
        self.locked_scroll_area = pygame.Rect(
            0,
            self.locked_header_rect.bottom,
            width,
            height - self.locked_header_rect.bottom,
        )

        self.back_button = Button(
            "Back",
            (width * 0.1, height * 0.05),
            font_size=int(height * 0.04),
            color=(255, 255, 255),
            bg_color=(100, 0, 0),
            button_action=self.return_home,
        )
        self.buttons.add(self.back_button)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from Scenes.HomeScene import HomeScene

                    self.scene_manager.set_scene(HomeScene(self.scene_manager))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if self.unlocked_scroll_area.collidepoint(event.pos):
                        self.unlocked_scroll_y += self.scroll_speed
                    elif self.locked_scroll_area.collidepoint(event.pos):
                        self.locked_scroll_y += self.scroll_speed
                elif event.button == 5:
                    if self.unlocked_scroll_area.collidepoint(event.pos):
                        self.unlocked_scroll_y -= self.scroll_speed
                    elif self.locked_scroll_area.collidepoint(event.pos):
                        self.locked_scroll_y -= self.scroll_speed

            for button in self.buttons:
                if hasattr(button, "handle_event"):
                    button.handle_event(event)

        return True

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
            achievement
            for achievement in self.achievements
            if achievement["id"] in self.player_data.get("achievements", [])
        ]

    def update(self, delta_time):
        for item in self.unlocked_list_items:
            item.rect.y = item.rect.y + self.unlocked_scroll_y

        for item in self.locked_list_items:
            item.rect.y = item.rect.y + self.locked_scroll_y

        self.unlocked_scroll_y = 0
        self.locked_scroll_y = 0

        current_size = pygame.display.get_surface().get_size()
        if current_size != self.window_size:
            self.window_size = current_size
            self.create_ui()

        self.buttons.update()

    def render(self, screen):
        screen.fill((0, 0, 0))

        screen.blit(self.unlocked_header, self.unlocked_header_rect)
        screen.blit(self.locked_header, self.locked_header_rect)

        unlocked_surface = pygame.Surface(
            (self.unlocked_scroll_area.width, self.unlocked_scroll_area.height)
        )
        unlocked_surface.fill((0, 0, 0))

        locked_surface = pygame.Surface(
            (self.locked_scroll_area.width, self.locked_scroll_area.height)
        )
        locked_surface.fill((0, 0, 0))

        for item in self.unlocked_list_items:
            if self.unlocked_scroll_area.colliderect(item.rect):
                adjusted_rect = item.rect.copy()
                adjusted_rect.y -= self.unlocked_scroll_area.top
                unlocked_surface.blit(item.image, adjusted_rect)

        for item in self.locked_list_items:
            if self.locked_scroll_area.colliderect(item.rect):
                adjusted_rect = item.rect.copy()
                adjusted_rect.y -= self.locked_scroll_area.top
                locked_surface.blit(item.image, adjusted_rect)

        self.buttons.draw(screen)
        screen.blit(unlocked_surface, self.unlocked_scroll_area)
        screen.blit(locked_surface, self.locked_scroll_area)
