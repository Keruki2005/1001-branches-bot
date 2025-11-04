import requests
import base64
import random
import string
import time

GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
REPO_OWNER = "Keruki2005"
REPO_NAME = "1001-branches"
README_PATH = "README.md"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def random_string(n=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def get_branches():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches"
    branches = []
    page = 1
    while True:
        r = requests.get(url, headers=HEADERS, params={'per_page': 100, 'page': page})
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        branches += [b['name'] for b in data]
        page += 1
    return branches

def get_readme_content(branch):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{README_PATH}?ref={branch}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(f"Could not read README.md on branch {branch}")
        return None, None
    data = r.json()
    content = base64.b64decode(data["content"]).decode()
    sha = data["sha"]
    return content, sha

def update_readme(branch):
    content, sha = get_readme_content(branch)
    if content is None:
        return
    addition = f"\nEdited by bot: {random_string()}\n"
    new_content = content + addition
    commit_message = f"Bot edit README.md on branch {branch}"
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{README_PATH}"
    payload = {
        "message": commit_message,
        "content": base64.b64encode(new_content.encode()).decode(),
        "branch": branch,
        "sha": sha
    }
    r = requests.put(url, json=payload, headers=HEADERS)
    if r.status_code in [200, 201]:
        print(f"Updated README.md on {branch}")
    else:
        print(f"Failed to update README.md on {branch}: {r.text}")

def main():
    branches = get_branches()
    print(f'Editing {len(branches)} branches...')
    for branch in branches:
        update_readme(branch)
        time.sleep(0.2) # Avoid GitHub API rate limits

if __name__ == "__main__":
    main()