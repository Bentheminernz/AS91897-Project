from Utils.loggerConfig import utils_logger
from Utils import playerDataManagement

_player_data = None


# this module manages the player data context, allowing access to player data across the game
def initialize():
    global _player_data
    utils_logger.info("Initializing player data...")
    _player_data = playerDataManagement.load_player_data()
    utils_logger.info(
        f"Player data initialized: {_player_data.get('player_name', 'Unknown')}"
    )


# this function returns the player data, initializing it if it hasn't been done yet
def get_data():
    global _player_data
    if _player_data is None:
        utils_logger.error("Player data not initialized.")
        initialize()
    return _player_data


# this function updates the player data with new data or keyword arguments
# it merges the new data with the existing data and saves it
def update_data(new_data=None, **kwargs):
    global _player_data
    if new_data is None:
        initialize()

    if new_data:
        _player_data.update(new_data)

    for key, value in kwargs.items():
        if key == "settings":
            if "settings" not in _player_data:
                _player_data["settings"] = {}
            _player_data["settings"].update(value)
        else:
            _player_data[key] = value

    playerDataManagement.save_player_data(_player_data)
    utils_logger.info("Global player data updated.")


# function to check if sound is enabled in the player data
def is_sound_enabled():
    return get_data().get("settings", {}).get("sound", True)


# function to get the player's name from the player data
def get_player_name():
    return get_data().get("player_name", "Player")


# function to get the player's score from the player data
def get_score():
    return get_data().get("score", 0)


# function to grant an achievement to the player
def achievement_granter(achievement_id):
    global _player_data
    if _player_data is None:
        initialize()

    player_achievements = _player_data.get("achievements", [])
    if achievement_id not in player_achievements:
        player_achievements.append(achievement_id)
        _player_data["achievements"] = player_achievements
        playerDataManagement.save_player_data(_player_data)
        utils_logger.info(f"Achievement {achievement_id} granted")
    else:
        utils_logger.info(f"Achievement {achievement_id} already granted")


# function to reset the player data, clearing all achievements and scores
def reset_completed_questions():
    global _player_data
    if _player_data is None:
        initialize()

    _player_data["completed_questions"] = [
        {"topic": 1, "questions": []},
        {"topic": 2, "questions": []},
    ]
    playerDataManagement.save_player_data(_player_data)
    utils_logger.info("Reset completed questions in player data")


# function to quit the game and save player data
def quit_and_save(player_data, scene_manager):
    if player_data is not None:
        playerDataManagement.save_player_data(player_data)
        utils_logger.info("Player data saved on quit")
        scene_manager.quit_game()
    else:
        utils_logger.warning("No player data to save on quit")


# function to save the player data
def save():
    global _player_data
    if _player_data is not None:
        playerDataManagement.save_player_data(_player_data)
        utils_logger.info("Global player data saved")


# function to get the completed questions for a specific topic
def get_completed_questions(topic_id):
    global _player_data
    if _player_data is None:
        initialize()

    completed_questions = _player_data.get("completed_questions", [])
    for topic in completed_questions:
        if topic.get("topic") == topic_id:
            return topic.get("questions", [])

    return []


# function to add a completed question to the player's data
def add_completed_question(topic_id, question_id):
    global _player_data
    if _player_data is None:
        initialize()

    completed_questions = _player_data.get("completed_questions", [])
    for topic in completed_questions:
        if topic.get("topic") == topic_id:
            topic["questions"].append(question_id)
            playerDataManagement.save_player_data(_player_data)
            utils_logger.info(
                f"Added completed question {question_id} to topic {topic_id}"
            )
            return

    utils_logger.warning(f"Topic {topic_id} not found in completed questions")
