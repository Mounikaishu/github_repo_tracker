import os
import requests

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise Exception("⚠️ Please set the environment variable GITHUB_TOKEN before running.")

HEADERS = {"Authorization": f"token {TOKEN}"}

def fetch_github_data_for_user(username):
    """
    Returns a dict:
    {
        "repos": [
            {
                "name": ...,
                "commits_count": ...,
                "last_commit_date": ...,
                "url": ...
            },
            ...
        ]
    }
    """
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    repos_resp = requests.get(repos_url, headers=HEADERS)
    if repos_resp.status_code != 200:
        print(f"❌ Error fetching repos for {username}: {repos_resp.status_code}")
        return {"repos": []}

    repos_data = []
    for repo in repos_resp.json():
        repo_name = repo.get("name")
        full_name = repo.get("full_name")
        html_url = repo.get("html_url")

        # Count total commits correctly using the GitHub API "commits" link
        commits_count = 0
        last_commit_date = ""
        commits_url = f"https://api.github.com/repos/{full_name}/commits?per_page=1"
        commits_resp = requests.get(commits_url, headers=HEADERS)
        if commits_resp.status_code == 200 and commits_resp.json():
            last_commit_date = commits_resp.json()[0].get("commit", {}).get("committer", {}).get("date", "")
            
            # Get total commits using "Link" header for pagination
            if "Link" in commits_resp.headers:
                links = commits_resp.headers["Link"].split(",")
                for link in links:
                    if 'rel="last"' in link:
                        # Extract page number from URL
                        last_page_url = link.split(";")[0].strip()[1:-1]
                        commits_count = int(last_page_url.split("page=")[-1])
                        break
                else:
                    commits_count = 1  # only one commit
            else:
                commits_count = len(commits_resp.json())
        repos_data.append({
            "name": repo_name,
            "commits_count": commits_count,
            "last_commit_date": last_commit_date,
            "url": html_url
        })

    return {"repos": repos_data}
