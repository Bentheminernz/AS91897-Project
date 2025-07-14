import json
import random
import os
from Utils.loggerConfig import utils_logger


# function for loading a random question from my questions.json file
def fetch_random_question():
    # check if it exists, otherwise throw an error
    json_file_path = "./Assets/data/questions.json"
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"JSON file not found at {json_file_path}")

    # open the json file
    with open(json_file_path, "r") as file:
        data = json.load(file)
        questions = data.get("questions", [])
        if not questions:
            raise ValueError("No questions found in the JSON file.")

        # selects a random question from the json file
        random_question = random.choice(questions)
        return random_question


def load_specific_question(question_id):
    # check if it exists, otherwise throw an error
    json_file_path = "./Assets/data/questions.json"
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"JSON file not found at {json_file_path}")

    # open the json file
    with open(json_file_path, "r") as file:
        data = json.load(file)
        questions = data.get("questions", [])
        if not questions:
            raise ValueError("No questions found in the JSON file.")

        # selects a specific question from the json file
        for question in questions:
            if question.get("id") == question_id:
                return question

    raise ValueError(f"Question with ID {question_id} not found.")


if __name__ == "__main__":
    try:
        question = fetch_random_question()
        utils_logger.info(f"Random Question: {question}")
    except Exception as e:
        utils_logger.error(f"Error fetching random question: {e}")
