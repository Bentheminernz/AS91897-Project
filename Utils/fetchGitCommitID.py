import subprocess
from Utils.loggerConfig import utils_logger


# this function fetches the short commit ID of the current git repository and returns it as a string.
# this function is used for the window title bar of the game :)
def fetch_git_commit_id():
    try:
        # using a subprocess it executes the git command to get the short commit ID
        commit_id = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"]
        ).strip()
        return commit_id.decode("utf-8")  # return the commit ID as a string
    except Exception as e:
        utils_logger.error(f"Error fetching commit ID: {e}")
        return "error"


if __name__ == "__main__":
    commit_id = fetch_git_commit_id()
    utils_logger.info(f"Current Git Commit ID: {commit_id}")
