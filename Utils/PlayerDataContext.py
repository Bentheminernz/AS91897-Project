from Utils.loggerConfig import utils_logger
from Utils import playerDataManagement

_player_data = None

def initialize():
    global _player_data
    utils_logger.info("Initializing player data...")
    _player_data = playerDataManagement.load_player_data()
    utils_logger.info(f"Player data initialized: {_player_data.get('player_name', 'Unknown')}")

def get_data():
    global _player_data
    if _player_data is None:
        utils_logger.error("Player data not initialized.")
        initialize()
    return _player_data

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

def is_sound_enabled():
    utils_logger.info("Checking sound setting...")
    return get_data().get("settings", {}).get("sound", True)

def is_music_enabled():
    return get_data().get("settings", {}).get("music", True)

def get_player_name():
    return get_data().get("player_name", "Player")

def get_score():
    return get_data().get("score", 0)

def save():
    global _player_data
    if _player_data is not None:
        playerDataManagement.save_player_data(_player_data)
        utils_logger.info("Global player data saved")

def achievement_granter(achievement_id):
    global _player_data
    if _player_data is None:
        initialize()

    player_achievements = _player_data.get("achievements", [])
    if achievement_id not in player_achievements:
        player_achievements.append(achievement_id)
        _player_data["achievements"] = player_achievements
        playerDataManagement.save_player_data(_player_data)
        utils_logger.info(f"Granted achievement: {achievement_id}")
    else:
        utils_logger.info(f"Achievement {achievement_id} already granted")

def reset_completed_questions():
    global _player_data
    if _player_data is None:
        initialize()

    _player_data["completed_questions"] = []
    playerDataManagement.save_player_data(_player_data)
    utils_logger.info("Reset completed questions in player data")

def quit_and_save(player_data, scene_manager):
    if player_data is not None:
        playerDataManagement.save_player_data(player_data)
        utils_logger.info("Player data saved on quit")
        scene_manager.quit_game()
    else:
        utils_logger.warning("No player data to save on quit")