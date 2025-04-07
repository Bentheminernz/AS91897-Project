import json
import random
import os

def fetch_random_question():
    json_file_path = "./Assets/data/questions.json"
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"JSON file not found at {json_file_path}")
    
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        questions = data.get("questions", [])
        if not questions:
            raise ValueError("No questions found in the JSON file.")
        random_question = random.choice(questions)
        return random_question
        
if __name__ == "__main__":
    try:
        question = fetch_random_question()
        print("Random Question:", question)
    except Exception as e:
        print("Error:", e)