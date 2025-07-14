import subprocess
from Utils.loggerConfig import utils_logger


# this function fetches the short commit ID of the current git repository and returns it as a string.
def fetch_git_commit_id():
    try:
        commit_id = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"]
        ).strip()
        return commit_id.decode("utf-8")
    except Exception as e:
        utils_logger.error(f"Error fetching commit ID: {e}")
        return "error"


if __name__ == "__main__":
    commit_id = fetch_git_commit_id()
    utils_logger.info(f"Current Git Commit ID: {commit_id}")
