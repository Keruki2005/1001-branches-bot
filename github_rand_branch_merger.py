import requests
import random
import string
import time

GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
REPO_OWNER = "Keruki2005"
REPO_NAME = "1001-branches"
DEFAULT_BRANCH = "main"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
BRANCHES_TO_CREATE = 100
MERGES_TO_DO = 50  # Number of random merges

def random_string(n=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def get_branches():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches"
    branches = []
    page = 1
    while True:
        resp = requests.get(url, headers=HEADERS, params={'per_page': 100, 'page': page})
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        branches += [b['name'] for b in data]
        page += 1
    return branches

def get_branch_sha(branch_name):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/ref/heads/{branch_name}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["object"]["sha"]

def create_branch(new_branch, source_branch):
    sha = get_branch_sha(source_branch)
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/refs"
    payload = {
        "ref": f"refs/heads/{new_branch}",
        "sha": sha
    }
    resp = requests.post(url, json=payload, headers=HEADERS)
    if resp.status_code == 201:
        print(f"Created branch: {new_branch} from {source_branch}")
    else:
        print(f"Could not create branch {new_branch}: {resp.text}")

def merge_branches(base_branch, head_branch):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/merges"
    payload = {
        "base": base_branch,
        "head": head_branch,
        "commit_message": f"Random merge of {head_branch} into {base_branch}"
    }
    resp = requests.post(url, json=payload, headers=HEADERS)
    if resp.status_code == 201:
        print(f"Merged {head_branch} into {base_branch}")
    else:
        print(f"Could not merge {head_branch} into {base_branch}: {resp.text}")

def main():
    # Step 1: Get current branches
    branches = get_branches()
    if DEFAULT_BRANCH not in branches:
        print(f"Default branch '{DEFAULT_BRANCH}' not found.")
        return

    # Step 2: Randomly create new branches from random sources
    for _ in range(BRANCHES_TO_CREATE):
        source_branch = random.choice(branches)
        new_branch = random_string(12)
        create_branch(new_branch, source_branch)
        branches.append(new_branch)
        time.sleep(0.2)  # Avoid hitting rate limit

    # Step 3: Randomly merge branches
    for _ in range(MERGES_TO_DO):
        if len(branches) < 2:
            break
        base, head = random.sample(branches, 2)
        try:
            merge_branches(base, head)
        except Exception as e:
            print(f"Error merging {head} into {base}: {str(e)}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()