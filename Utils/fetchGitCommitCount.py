import subprocess

# this function fetches the number of commits in the git repository and returns it as an integer.
def fetch_git_commit_count():
    subprocess.run(["git", "rev-list", "--count", "HEAD"], check=True)
    commit_count = subprocess.check_output(
        ["git", "rev-list", "--count", "HEAD"]
    ).strip()
    count = int(commit_count.decode("utf-8"))
    return count


if __name__ == "__main__":
    fetch_git_commit_count()
