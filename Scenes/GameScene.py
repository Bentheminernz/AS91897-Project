import pygame
import random
from Components.Player import Player
from Components.Button import Button
from Components.QuestionBlock import QuestionBlock
from Utils.SceneManager import Scene
from Utils.fetchRandomQuestion import fetch_random_question, load_specific_question
from Utils import PlayerDataContext
from Utils.loggerConfig import game_logger

class GameScene(Scene):
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.player_data = PlayerDataContext.get_data()
        self.completed_questions = self.player_data.get("completed_questions", [])
        self.has_completed_all_questions = False

        self.window_size = pygame.display.get_surface().get_size()
        
        # Initialize the font here, before using it
        height = self.window_size[1]
        self.font = pygame.font.Font(None, int(height * 0.05))
        
        self.is_first_load = True

        self.all_sprites = pygame.sprite.Group()
        self.all_buttons = pygame.sprite.Group()
        self.question_blocks = []

        self.player = Player("./Assets/Players/Player1.png", (650, 650))
        self.all_sprites.add(self.player)

        self.load_new_question(use_current=self.is_first_load)
        self.is_first_load = False

        self.create_ui()

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

        center_x = width // 2
        start_y = height * 0.5
        button_spacing = height * 0.08

        self.font = pygame.font.Font(None, int(height * 0.05))

        self.save_button = Button(
            "Save Game",
            (center_x * 2 - 75, start_y * 2 - 25),
            font_size=30,
            color=(255, 255, 255),
            bg_color=(0, 100, 0),
            button_action=lambda: PlayerDataContext.update_data(self.player_data),
        )
        self.all_buttons.add(self.save_button)

        self.player_score = self.font.render(
            f"Score: {self.player_data['score']}", True, (255, 255, 255)
        )
        self.player_score_rect = self.player_score.get_rect(topright=(width - 10, 10))

    def load_new_question(self, use_current=False):
        for block in self.question_blocks:
            self.all_sprites.remove(block)
        self.question_blocks.clear()

        self.player.rect.topleft = (650, 650)

        attempts = 0
        max_attempts = 10
        random_question = None

        if use_current and self.player_data.get("current_question") is not None:
            game_logger.info(f"Loading existing question: {self.player_data['current_question']}")
            random_question = load_specific_question(
                self.player_data["current_question"]
            )
        else:
            while attempts < max_attempts:
                random_question = fetch_random_question()
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
            game_logger.info("All questions completed.")
            self.player_data["current_question"] = None
            PlayerDataContext.update_data(self.player_data)
            return
        
        self.question_text = random_question.get("question_title", "No question found")
        question_id = random_question.get("id", "No question ID found")
        answers = random_question.get("answers", ["No answers found"])

        if not use_current:
            self.player_data["current_question"] = question_id
            PlayerDataContext.update_data(self.player_data)

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
            )
            self.all_sprites.add(block)
            self.question_blocks.append(block)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                PlayerDataContext.update_data(self.player_data)
                return False
        return True
    
    def update(self, delta_time):
        current_size = pygame.display.get_surface().get_size()
        if current_size != self.window_size:
            self.window_size = current_size
            self.create_ui()

        self.player.gravity(delta_time, self.scene_manager.screen)

        for block in self.question_blocks:
            block.on_collision(self.player)

        self.all_sprites.update(self.scene_manager.screen, delta_time)
        self.all_buttons.update()
    
    def render(self, screen):
        screen.fill((0, 0, 0))
        
        self.all_sprites.draw(screen)
        self.all_buttons.draw(screen)
        screen.blit(self.player_score, self.player_score_rect)
        screen.blit(self.question_surface, (10, 10))