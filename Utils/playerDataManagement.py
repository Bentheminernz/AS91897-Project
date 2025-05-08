import os
import json
from Utils.loggerConfig import save_logger
import uuid

default_player_data = {
    "id": str(uuid.uuid4()),
    "player_name": "Player",
    "score": 0,
    "completed_questions": [],
    "current_question": None,
    "completed_intro": False,
}

def validate_player_data(player_data):
    save_logger.info("Validating player data...")
    required_keys = [
        "id",
        "player_name",
        "score",
        "completed_questions",
        "current_question",
        "completed_intro",
    ]

    for key in required_keys:
        if key not in player_data:
            save_logger.error(f"Missing key: {key}")
            return False

    if not isinstance(player_data["id"], str):
        save_logger.error("ID must be a string.")
        return False

    if not isinstance(player_data["player_name"], str):
        save_logger.error("Player name must be a string.")
        return False

    if not isinstance(player_data["score"], int):
        save_logger.error("Score must be an integer.")
        return False

    if not isinstance(player_data["completed_questions"], list):
        save_logger.error("Completed questions must be a list.")
        return False

    if not isinstance(player_data["current_question"], (int, type(None))):
        save_logger.error("Current question must be an integer or None.")
        return False

    if not isinstance(player_data["completed_intro"], bool):
        save_logger.error("Completed intro must be a boolean.")
        return False

    save_logger.info("Player data validation successful.")
    return True

def save_player_data(player_data):
    save_logger.info("Saving player data...")
    if not os.path.exists("./SaveData/player_data.json"):
        save_logger.info("Creating SaveData directory...")
        os.makedirs("./SaveData", exist_ok=True)

    with open("./SaveData/player_data.json", "w") as f:
        save_logger.info("Writing player data to JSON file...")
        try:
            if not validate_player_data(player_data):
                save_logger.error("Player data validation failed. Saving default data.")
                player_data = default_player_data
        except Exception as e:
            save_logger.error(f"Error during validation: {e}")
            player_data = default_player_data

        save_logger.info(f"Writing player data: {player_data}")
        json.dump(player_data, f, indent=4)

def load_player_data():
    save_logger.info("Loading player data...")
    if os.path.exists("./SaveData/player_data.json"):
        save_logger.info("Player data file found.")
        with open("./SaveData/player_data.json", "r") as f:
            save_logger.info("Reading player data from JSON file...")
            try:
                player_data = json.load(f)
                save_logger.info("Player data loaded successfully.")
                if not validate_player_data(player_data):
                    save_logger.error("Player data validation failed. Creating new player data.")
                    save_player_data(default_player_data)
                    return default_player_data
                return player_data
            except json.JSONDecodeError as e:
                save_logger.error(f"Error decoding JSON: {e}")
                player_data = default_player_data
                save_player_data(player_data)
                return player_data
    else:
        save_logger.info("No player data file found.")

        save_player_data(default_player_data)

        return default_player_data
