import subprocess

# this function fetches the short commit ID of the current git repository and returns it as a string.
def fetch_git_commit_id():
    commit_id = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip()
    return commit_id.decode("utf-8")


if __name__ == "__main__":
    print(fetch_git_commit_id())
