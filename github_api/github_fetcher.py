import os
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise Exception("⚠️ Please set the environment variable GITHUB_TOKEN before running.")

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def fetch_github_data_for_user(username):
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&page=1"
    try:
        repos_resp = requests.get(repos_url, headers=HEADERS)
        repos_resp.raise_for_status()
        repos = repos_resp.json()
        repo_data = []

        for repo in repos:
            name = repo.get("name")
            commits_count = repo.get("stargazers_count", 0)  # replace with your commits logic
            url = repo.get("html_url")
            
            # Get last commit date
            commits_api = f"https://api.github.com/repos/{username}/{name}/commits?per_page=1"
            commits_resp = requests.get(commits_api, headers=HEADERS)
            commits_resp.raise_for_status()
            commits_json = commits_resp.json()
            last_commit = commits_json[0]["commit"]["committer"]["date"] if commits_json else "N/A"

            repo_data.append({
                "name": name,
                "commits_count": commits_count,
                "last_commit": last_commit,
                "url": url
            })

        return {"repos": repo_data}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
