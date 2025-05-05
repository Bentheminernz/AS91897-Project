import pygame
import random
from Components.Player import Player
from Components.Button import Button
from Components.QuestionBlock import QuestionBlock
from Utils.SceneManager import Scene
from Utils.fetchRandomQuestion import fetch_random_question, load_specific_question
from Utils import playerDataManagement
from Utils.loggerConfig import game_logger

class GameScene(Scene):
    def __init__(self, scene_manager, player_data):
        self.scene_manager = scene_manager
        self.player_data = player_data
        self.completed_questions = player_data.get("completed_questions", [])
        self.has_completed_all_questions = False

        self.all_sprites = pygame.sprite.Group()
        self.all_buttons = pygame.sprite.Group()
        self.question_blocks = []

        self.player = Player("./Assets/Players/Player1.png", (650, 650))
        self.all_sprites.add(self.player)

        self.save_button = Button(
            "Save Game",
            (60, 580),
            font_size=30,
            color=(255, 255, 255),
            bg_color=(0, 100, 0),
            button_action=lambda: playerDataManagement.save_player_data(self.player_data),
        )
        self.all_buttons.add(self.save_button)

        self.font = pygame.font.Font(None, 36)

        self.player_score = self.font.render(
            f"Score: {self.player_data['score']}", True, (255, 255, 255)
        )

        self.load_new_question()

    def load_new_question(self):
        for block in self.question_blocks:
            self.all_sprites.remove(block)
        self.question_blocks.clear()

        self.player.rect.topleft = (650, 650)

        attempts = 0
        max_attempts = 10
        random_question = None


        while attempts < max_attempts:
            if self.player_data.get("current_question") is not None:
                random_question = load_specific_question(
                    self.player_data["current_question"]
                )
                break

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
            return
        
        self.question_text = random_question.get("question_title", "No question found")
        question_id = random_question.get("id", "No question ID found")
        answers = random_question.get("answers", ["No answers found"])

        self.player_data["current_question"] = question_id
        playerDataManagement.save_player_data(self.player_data)

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
                playerDataManagement.save_player_data(self.player_data)
                return False
        return True
    
    def update(self, delta_time):
        self.player.gravity(delta_time, self.scene_manager.screen)

        for block in self.question_blocks:
            block.on_collision(self.player)

        self.all_sprites.update(self.scene_manager.screen, delta_time)
        self.all_buttons.update()
    
    def render(self, screen):
        screen.fill((0, 0, 0))
        
        self.all_sprites.draw(screen)
        self.all_buttons.draw(screen)
        screen.blit(self.player_score, (650, 10))
        screen.blit(self.question_surface, (10, 10))