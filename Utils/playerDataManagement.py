import os
import json
from Utils.loggerConfig import utils_logger
import uuid


def save_player_data(player_data):
    utils_logger.info("Saving player data...")
    if not os.path.exists("./SaveData/player_data.json"):
        utils_logger.info("Creating SaveData directory...")
        os.makedirs("./SaveData", exist_ok=True)

    with open("./SaveData/player_data.json", "w") as f:
        utils_logger.info("Writing player data to JSON file...")
        json.dump(player_data, f, indent=4)


def load_player_data():
    utils_logger.info("Loading player data...")
    if os.path.exists("./SaveData/player_data.json"):
        utils_logger.info("Player data file found.")
        with open("./SaveData/player_data.json", "r") as f:
            utils_logger.info("Reading player data from JSON file...")
            return json.load(f)
    else:
        utils_logger.info("No player data file found.")

        default_player_data = {
            "id": str(uuid.uuid4()),
            "player_name": "Player",
            "score": 0,
            "completed_questions": [],
            "current_question": None,
            "completed_intro": False,
        }

        save_player_data(default_player_data)

        return default_player_data
