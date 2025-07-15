import pygame
from Utils.loggerConfig import component_logger
from Utils import PlayerDataContext


# this is a custom question block class that is used to create question blocks in the game
# it inherits from the pygame sprite class, so it can be used in sprite groups
# it has an image, a position, a text, a color, a background color and a button action
class QuestionBlock(pygame.sprite.Sprite):
    # initialises the question block and sets its variables
    def __init__(
        self,
        image_path,
        position,
        text,
        is_correct,
        player_data,
        on_correct_answer,
        question_id,
        topic_id,
        max_questions,
    ):
        super().__init__()
        self.original_image = pygame.image.load(image_path)
        self.original_image = pygame.transform.scale(self.original_image, (100, 100))
        self.text = str(text)
        self.is_killed = False
        self.is_correct = is_correct
        self.player_data = player_data
        self.on_correct_answer = on_correct_answer
        self.question_id = question_id
        self.topic_id = topic_id
        self.max_questions = max_questions
        self.correct_audio = pygame.mixer.Sound("./Assets/Audio/Correct.wav")
        self.incorrect_audio = pygame.mixer.Sound("./Assets/Audio/Incorrect.wav")
        self.audio_volume = 1.0 if PlayerDataContext.is_sound_enabled() else 0.0
        self.correct_audio.set_volume(self.audio_volume)
        self.incorrect_audio.set_volume(self.audio_volume)

        self.image = self.original_image.copy()
        font = pygame.font.Font(None, 18)
        text_color = (0, 255, 0) if is_correct else (255, 255, 255)
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=(50, 50))
        self.image.blit(text_surface, text_rect)
        self.rect = self.image.get_rect(topleft=position)

    # this function is called upon every frame to check for collisions
    # if the player is colliding with the question block, it kills the block
    # and adds the score to the player data, if the answer is correct
    def on_collision(self, player):
        if self.rect.colliderect(player.rect) and not self.is_killed:
            component_logger.info(f"Player collided with question block: {self.text}")
            component_logger.info(f"The answer was {self.is_correct}")
            if self.is_correct:
                component_logger.info("Correct answer!")

                score_entries = self.player_data.get("score", [])
                for score_entry in score_entries:
                    if score_entry.get("topic") == self.topic_id:
                        score_entry["score"] += 1
                        break

                self.player_data["completed_questions"].append(self.question_id)

                high_scores = self.player_data.get("high_scores", [])

                topic_score_entry = None
                for topic_score in high_scores:
                    if topic_score.get("topic") == self.topic_id:
                        topic_score_entry = topic_score
                        break

                if topic_score_entry:
                    topic_score_entry["score"] = min(
                        topic_score_entry["score"] + 1, self.max_questions
                    )
                else:
                    high_scores.append({"topic": self.topic_id, "score": 1})

                self.player_data["high_scores"] = high_scores

                if 1 not in self.player_data["achievements"]:
                    PlayerDataContext.achievement_granter(1)

                if (
                    2 not in self.player_data["achievements"]
                    and len(self.player_data["completed_questions"]) >= 10
                ):
                    PlayerDataContext.achievement_granter(2)

                if (
                    3 not in self.player_data["achievements"]
                    and len(self.player_data["completed_questions"]) >= 20
                ):
                    PlayerDataContext.achievement_granter(3)

                self.correct_audio.play()

                if self.on_correct_answer:
                    self.on_correct_answer()

            else:
                component_logger.info("Incorrect answer!")
                self.incorrect_audio.play()

            self.is_killed = True
            self.kill()
