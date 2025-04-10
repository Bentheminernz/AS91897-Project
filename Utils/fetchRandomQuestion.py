import json
import random
import os

# function for loading a random question from my questions.json file
def fetch_random_question():
    # check if it exists, otherwise throw an error
    json_file_path = "./Assets/data/questions.json"
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"JSON file not found at {json_file_path}")
    
    # open the json file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        questions = data.get("questions", [])
        if not questions:
            raise ValueError("No questions found in the JSON file.")
        
        # selects a random question from the json file
        random_question = random.choice(questions)
        return random_question
        
if __name__ == "__main__":
    try:
        question = fetch_random_question()
        print("Random Question:", question)
    except Exception as e:
        print("Error:", e)