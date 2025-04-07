import subprocess

def fetch_git_commit_id():
    commit_id = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip()
    return commit_id.decode('utf-8')

if __name__ == "__main__":
    fetch_git_commit_id()