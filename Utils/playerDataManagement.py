import os
import json


def save_player_data(player_data):
    print("Saving player data...")
    if not os.path.exists("./SaveData/player_data.json"):
        print("Creating SaveData directory...")
        os.makedirs("./SaveData", exist_ok=True)

    with open("./SaveData/player_data.json", "w") as f:
        print("Writing player data to JSON file...")
        json.dump(player_data, f, indent=4)


def load_player_data():
    print("Loading player data...")
    if os.path.exists("./SaveData/player_data.json"):
        print("Found existing player data file.")
        with open("./SaveData/player_data.json", "r") as f:
            print("Reading player data from JSON file...")
            return json.load(f)
    else:
        print("No player data file found. Creating new player data.")

        default_player_data = {
            "player_name": "Player",
            "score": 0,
            "completed_questions": [],
            "current_question": None,
            "completed_intro": False,
        }

        save_player_data(default_player_data)

        return default_player_data
