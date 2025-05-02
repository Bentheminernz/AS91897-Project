import logging
import os

# This module sets up logging for the game, scene, and component modules.
# It creates a logger for each component and sets the log level to INFO.
# The log messages are formatted to include the timestamp, logger name, log level, and message.
def setup_logger(name, log_file, level=logging.INFO):
    log_file_path = f"./Logs/"
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)
        
    log_file_path = os.path.join(log_file_path, log_file)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(log_file_path)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

# creates a logger for each component
game_logger = setup_logger('game', 'game.log')
scene_logger = setup_logger('scene', 'scene.log')
component_logger = setup_logger('component', 'component.log')
utils_logger = setup_logger('utils', 'utils.log')