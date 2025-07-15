import pygame
import random
from Components.Player import Player
from Components.Button import Button
from Components.QuestionBlock import QuestionBlock
from Utils.SceneManager import Scene
from Utils import PlayerDataContext
from Utils.loggerConfig import game_logger
from Utils.fetchRandomQuestion import fetch_random_question


class GameScene(Scene):
    def __init__(self, scene_manager, topic_id):
        self.scene_manager = scene_manager
        self.topic_id = topic_id
        self.player_data = PlayerDataContext.get_data()
        self.completed_questions = self.player_data.get("completed_questions", [])
        self.has_completed_all_questions = False

        self.paused = False
        self.pause_overlay = None
        self.pause_buttons = pygame.sprite.Group()

        self.window_size = pygame.display.get_surface().get_size()

        height = self.window_size[1]
        self.font = pygame.font.Font(None, int(height * 0.05))

        self.is_first_load = True

        self.all_sprites = pygame.sprite.Group()
        self.all_buttons = pygame.sprite.Group()
        self.question_blocks = []

        self.player = Player("./Assets/Players/StandingA.png", (650, 650))
        self.all_sprites.add(self.player)

        self.load_new_question()

        self.create_ui()
        self.create_pause_menu()

    def reset_game(self):
        PlayerDataContext.reset_completed_questions()
        self.completed_questions = []
        self.has_completed_all_questions = False
        self.load_new_question()

    def load_new_question(self):
        for block in self.question_blocks:
            self.all_sprites.remove(block)
        self.question_blocks.clear()

        self.player.rect.topleft = (650, 650)

        attempts = 0
        max_attempts = 10
        random_question = None
        max_questions = 0

        while attempts < max_attempts:
            random_question_raw = fetch_random_question(self.topic_id)
            random_question = random_question_raw.get("question", {})
            max_questions = random_question_raw.get("max_questions", 0)
            question_id = random_question.get("id", "No question ID found")

            if question_id not in self.completed_questions:
                break
            attempts += 1

        if attempts >= max_attempts:
            self.has_completed_all_questions = True
            self.question_text = "All questions completed."
            self.question_surface = self.font.render(
                self.question_text, True, (255, 255, 255)
            )

            self.replay_buttons = pygame.sprite.Group()

            self.replay_button = Button(
                "Replay",
                (self.window_size[0] // 2 - 100, self.window_size[1] // 2),
                font_size=40,
                color=(255, 255, 255),
                bg_color=(0, 100, 0),
                button_action=lambda: self.reset_game(),
            )
            self.replay_buttons.add(self.replay_button)

            game_logger.info("All questions completed.")
            return

        self.question_text = random_question.get("question_title", "No question found")
        question_id = random_question.get("id", "No question ID found")
        answers = random_question.get("answers", ["No answers found"])

        self.question_surface = self.font.render(
            self.question_text, True, (255, 255, 255)
        )

        start_x = 125
        start_y = 200
        spacing = 225

        random.shuffle(answers)
        for i, answer in enumerate(answers):
            answer_text = answer.get("answer_text", "No answer text found")
            is_correct = answer.get("isCorrect", False)
            block_x = start_x + (i * spacing)
            block_y = start_y
            block = QuestionBlock(
                "./Assets/QuestionBlocks/QuestionBlock1.png",
                (block_x, block_y),
                answer_text,
                is_correct,
                self.player_data,
                on_correct_answer=self.load_new_question,
                question_id=question_id,
                topic_id=self.topic_id,
                max_questions=max_questions,
            )
            self.all_sprites.add(block)
            self.question_blocks.append(block)

    def create_pause_menu(self):
        from Scenes.HomeScene import HomeScene

        self.pause_overlay = pygame.Surface(self.window_size, pygame.SRCALPHA)
        self.pause_overlay.fill((0, 0, 0, 128))

        self.pause_buttons.empty()

        width, height = self.window_size
        center_x = width // 2
        center_y = height // 2
        button_spacing = 60

        resume_button = Button(
            "Resume",
            (center_x - 100, center_y - button_spacing),
            font_size=40,
            color=(255, 255, 255),
            bg_color=(0, 100, 0),
            button_action=self.toggle_pause,
        )

        save_button = Button(
            "Save Game",
            (center_x - 100, center_y),
            font_size=40,
            color=(255, 255, 255),
            bg_color=(0, 100, 150),
            button_action=lambda: PlayerDataContext.update_data(self.player_data),
        )

        menu_button = Button(
            "Main Menu",
            (center_x - 100, center_y + button_spacing),
            font_size=40,
            color=(255, 255, 255),
            bg_color=(150, 0, 0),
            button_action=lambda: self.scene_manager.set_scene(
                HomeScene(self.scene_manager)
            ),
        )

        exit_button = Button(
            "Exit Game",
            (center_x - 100, center_y + button_spacing * 2),
            font_size=40,
            color=(255, 255, 255),
            bg_color=(150, 0, 0),
            button_action=lambda: PlayerDataContext.quit_and_save(
                self.player_data, self.scene_manager
            ),
        )

        self.pause_buttons.add(resume_button)
        self.pause_buttons.add(save_button)
        self.pause_buttons.add(menu_button)
        self.pause_buttons.add(exit_button)

    def toggle_pause(self):
        self.paused = not self.paused
        game_logger.info(f"Game {'paused' if self.paused else 'resumed'}")

    def create_ui(self):
        self.all_buttons.empty()

        important_sprites = []
        for sprite in self.all_sprites:
            if isinstance(sprite, Player) or isinstance(sprite, QuestionBlock):
                important_sprites.append(sprite)

        self.all_sprites.empty()
        for sprite in important_sprites:
            self.all_sprites.add(sprite)

        width, height = self.window_size

        self.font = pygame.font.Font(None, int(height * 0.05))

        topic_score = 0
        for score_entry in self.player_data.get("score", []):
            if score_entry.get("topic") == self.topic_id:
                topic_score = score_entry.get("score", 0)
                break

        self.player_score = self.font.render(
            f"Score: {topic_score}", True, (255, 255, 255)
        )
        self.player_score_rect = self.player_score.get_rect(topright=(width - 10, 10))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                PlayerDataContext.update_data(self.player_data)
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    self.toggle_pause()

            if self.paused and event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.pause_buttons:
                    if hasattr(button, "handle_event"):
                        button.handle_event(event)

            if (
                self.has_completed_all_questions
                and event.type == pygame.MOUSEBUTTONDOWN
            ):
                if hasattr(self, "replay_buttons"):
                    for button in self.replay_buttons:
                        if hasattr(button, "handle_event"):
                            button.handle_event(event)

        return True

    def update(self, delta_time):
        current_size = pygame.display.get_surface().get_size()
        if current_size != self.window_size:
            self.window_size = current_size
            self.create_ui()
            self.create_pause_menu()

        if not self.paused:
            self.player.gravity(delta_time, self.scene_manager.screen)

            for block in self.question_blocks:
                block.on_collision(self.player)
                self.player_data = PlayerDataContext.get_data()

            topic_score = 0
            for score_entry in self.player_data.get("score", []):
                if score_entry.get("topic") == self.topic_id:
                    topic_score = score_entry.get("score", 0)
                    break
            self.player_score = self.font.render(
                f"Score: {topic_score}", True, (255, 255, 255)
            )
            self.player_score_rect = self.player_score.get_rect(
                topright=(self.window_size[0] - 10, 10)
            )

            self.all_sprites.update(self.scene_manager.screen, delta_time)
            self.all_buttons.update()

            if self.has_completed_all_questions and hasattr(self, "replay_buttons"):
                self.replay_buttons.update()
        else:
            self.pause_buttons.update()

    def render(self, screen):
        screen.fill((0, 0, 0))

        self.all_sprites.draw(screen)
        self.all_buttons.draw(screen)
        screen.blit(self.player_score, self.player_score_rect)
        screen.blit(self.question_surface, (10, 10))

        if self.has_completed_all_questions and hasattr(self, "replay_buttons"):
            self.replay_buttons.draw(screen)

        if self.paused:
            screen.blit(self.pause_overlay, (0, 0))

            pause_font = pygame.font.Font(None, 80)
            pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
            text_rect = pause_text.get_rect(
                center=(self.window_size[0] // 2, self.window_size[1] // 4)
            )
            screen.blit(pause_text, text_rect)

            self.pause_buttons.draw(screen)
