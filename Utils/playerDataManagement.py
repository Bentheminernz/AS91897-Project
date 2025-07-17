import os
import json
from Utils.loggerConfig import save_logger
import uuid
import hashlib
import time

default_player_data = {
    "id": str(uuid.uuid4()),
    "player_name": "Player",
    "score": [
        {
            "topic": 1,
            "score": 0,
        },
        {
            "topic": 2,
            "score": 0,
        },
    ],
    "completed_questions": [
        {
            "topic": 1,
            "questions": [],
        },
        {
            "topic": 2,
            "questions": [],
        },
    ],
    "completed_intro": False,
    "settings": {
        "sound": True,
    },
    "achievements": [],
    "high_scores": [
        {
            "topic": 1,
            "score": 0,
        },
        {
            "topic": 2,
            "score": 0,
        },
    ],
}


def validate_player_data(player_data):
    save_logger.info("Validating player data...")
    required_top_keys = [
        "id",
        "player_name",
        "score",
        "completed_questions",
        "completed_intro",
        "settings",
        "achievements",
        "high_scores",
    ]

    for key in required_top_keys:
        if key not in player_data:
            save_logger.error(f"Missing key: {key}")
            return False

    if "settings" in player_data:
        if "sound" not in player_data["settings"]:
            save_logger.error("Missing key: settings.sound")
            return False

    if "high_scores" in player_data:
        for score in player_data["high_scores"]:
            if "topic" not in score or "score" not in score:
                save_logger.error("High scores must contain 'topic' and 'score'.")
                return False
            if not isinstance(score["topic"], int) or not isinstance(
                score["score"], int
            ):
                save_logger.error("High scores 'topic' and 'score' must be integers.")
                return False

    if "score" in player_data:
        for score in player_data["score"]:
            if "topic" not in score or "score" not in score:
                save_logger.error("Score must contain 'topic' and 'score'.")
                return False
            if not isinstance(score["topic"], int) or not isinstance(
                score["score"], int
            ):
                save_logger.error("Score 'topic' and 'score' must be integers.")
                return False

    if not isinstance(player_data["id"], str):
        save_logger.error("ID must be a string.")
        return False

    if not isinstance(player_data["player_name"], str):
        save_logger.error("Player name must be a string.")
        return False

    if not isinstance(player_data["completed_questions"], list):
        save_logger.error("Completed questions must be a list.")
        return False

    if not all(isinstance(q, dict) for q in player_data["completed_questions"]):
        save_logger.error("Each completed question must be a dictionary.")
        return False

    if not isinstance(player_data["completed_intro"], bool):
        save_logger.error("Completed intro must be a boolean.")
        return False

    if not isinstance(player_data["settings"], dict):
        save_logger.error("Settings must be a dictionary.")
        return False

    if not isinstance(player_data["achievements"], list):
        save_logger.error("Achievements must be a list.")
        return False

    if not isinstance(player_data["high_scores"], list):
        save_logger.error("High scores must be a list.")
        return False

    save_logger.info("Player data validation successful.")
    return True


def calculate_checksum(player_data):
    serialized = json.dumps(player_data, sort_keys=True)
    save_logger.info("Calculating checksum for player data")
    return hashlib.sha256(serialized.encode()).hexdigest()


def save_player_data(player_data):
    save_logger.info("Saving player data...")
    if not os.path.exists("./SaveData"):
        save_logger.info("Creating SaveData directory...")
        os.makedirs("./SaveData", exist_ok=True)

    try:
        if not validate_player_data(player_data):
            save_logger.error("Player data validation failed. Saving default data.")
            player_data = default_player_data

        save_wrapper = {
            "data": player_data,
            "metadata": {
                "timestamp": time.time(),
                "game_version": "1.0.0",
            },
        }

        save_wrapper["checksum"] = calculate_checksum(player_data)

        with open("./SaveData/player_data.json", "w") as f:
            save_logger.info("Writing player data to JSON file...")
            json.dump(save_wrapper, f, indent=4)

        with open("./SaveData/player_data_backup.json", "w") as f:
            json.dump(save_wrapper, f, indent=4)

    except Exception as e:
        save_logger.error(f"Error saving player data: {e}")
        save_wrapper = {
            "data": default_player_data,
            "metadata": {
                "timestamp": time.time(),
                "game_version": "1.0.0",
            },
            "checksum": calculate_checksum(default_player_data),
        }
        with open("./SaveData/player_data.json", "w") as f:
            json.dump(save_wrapper, f, indent=4)


def load_player_data():
    save_logger.info("Loading player data...")
    player_data_file = "./SaveData/player_data.json"
    backup_file = "./SaveData/player_data_backup.json"

    main_data = None
    if os.path.exists(player_data_file):
        save_logger.info("Player data file found.")
        try:
            with open(player_data_file, "r") as f:
                save_logger.info("Reading player data from JSON file...")
                file_content = json.load(f)

                if (
                    isinstance(file_content, dict)
                    and "data" in file_content
                    and "checksum" in file_content
                ):
                    player_data = file_content["data"]
                    stored_checksum = file_content["checksum"]

                    calculated_checksum = calculate_checksum(player_data)
                    if calculated_checksum != stored_checksum:
                        save_logger.error(
                            "Checksum verification failed! Save file may have been tampered with."
                        )
                        main_data = None
                    else:
                        if validate_player_data(player_data):
                            main_data = player_data
                else:
                    save_logger.warning("Loading legacy save format")
                    if validate_player_data(file_content):
                        main_data = file_content
        except Exception as e:
            save_logger.error(f"Error loading main save file: {e}")

    if main_data is None and os.path.exists(backup_file):
        save_logger.info("Trying backup save file...")
        try:
            with open(backup_file, "r") as f:
                file_content = json.load(f)
                if (
                    isinstance(file_content, dict)
                    and "data" in file_content
                    and "checksum" in file_content
                ):
                    player_data = file_content["data"]
                    stored_checksum = file_content["checksum"]

                    if calculate_checksum(
                        player_data
                    ) == stored_checksum and validate_player_data(player_data):
                        main_data = player_data
                        save_logger.info("Restored from backup save file")
        except Exception as e:
            save_logger.error(f"Error loading backup save file: {e}")

    if main_data is None:
        save_logger.info("Using default player data")
        main_data = default_player_data
        save_player_data(main_data)

    return main_data


def delete_player_data():
    save_logger.info("Deleting player data...")
    if os.path.exists("./SaveData/player_data.json"):
        os.remove("./SaveData/player_data.json")
        save_logger.info("Player data file deleted.")
    if os.path.exists("./SaveData/player_data_backup.json"):
        os.remove("./SaveData/player_data_backup.json")
        save_logger.info("Player data backup file deleted.")
    else:
        save_logger.info("No player data files found to delete.")
