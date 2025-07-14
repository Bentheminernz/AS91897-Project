import subprocess
from Utils.loggerConfig import utils_logger


# this function fetches the number of commits in the git repository and returns it as an integer.
def fetch_git_commit_count():
    try:
        subprocess.run(["git", "rev-list", "--count", "HEAD"], check=True)
        commit_count = subprocess.check_output(
            ["git", "rev-list", "--count", "HEAD"]
        ).strip()
        count = int(commit_count.decode("utf-8"))
        return count
    except Exception as e:
        utils_logger.error(f"Error fetching commit count: {e}")
        return "Error"


if __name__ == "__main__":
    fetch_git_commit_count()
