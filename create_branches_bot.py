import requests

GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
REPO_OWNER = "your github user name"
REPO_NAME = "your repo name"
DEFAULT_BRANCH = "main"
NUMBER_OF_BRANCHES = 1000  # Change as needed

def get_sha():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/ref/heads/{DEFAULT_BRANCH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["object"]["sha"]

def create_branch(branch_name, sha):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/refs"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": sha
    }
    r = requests.post(url, json=data, headers=headers)
    if r.status_code == 201:
        print(f"Created branch: {branch_name}")
    else:
        print(f"Failed: {branch_name}: {r.text}")

if __name__ == "__main__":
    sha = get_sha()
    for i in range(1, NUMBER_OF_BRANCHES + 1):
        branch_name = f"bot-branch-{i}"
        create_branch(branch_name, sha)
