import time
import requests
import os
from urllib.parse import urlparse, parse_qs

SLEEP_BETWEEN_CALLS = 0.3

# ✅ Use environment variable instead of hardcoding
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def _headers():
    """Return headers for GitHub API requests"""
    h = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"token {GITHUB_TOKEN}"
    return h

def _get_json(url, params=None):
    """Make a GET request and return JSON"""
    r = requests.get(url, headers=_headers(), params=params, timeout=30)
    r.raise_for_status()
    return r.json(), r

def _get_all_repos_for_user(username):
    """Fetch all repositories for a given user"""
    repos = []
    page = 1
    while True:
        params = {"per_page": 100, "page": page}
        data, resp = _get_json(f"https://api.github.com/users/{username}/repos", params=params)
        if not data:
            break
        repos.extend(data)
        if len(data) < 100:
            break
        page += 1
        time.sleep(SLEEP_BETWEEN_CALLS)
    return repos

def _get_commit_count_and_latest(owner, repo_name):
    """Return number of commits and latest commit date for a repo"""
    url = f"https://api.github.com/repos/{owner}/{repo_name}/commits"
    params = {"per_page": 1}
    data, resp = _get_json(url, params=params)

    commit_count = 0
    latest_date = None

    if isinstance(data, list) and len(data) > 0:
        latest = data[0]
        latest_date = latest.get("commit", {}).get("author", {}).get("date")

    link = resp.headers.get("Link", "")
    if link:
        parts = [p.strip() for p in link.split(",")]
        last_url = None
        for p in parts:
            if 'rel="last"' in p:
                url_part = p.split(";")[0].strip()
                if url_part.startswith("<") and url_part.endswith(">"):
                    last_url = url_part[1:-1]
                    break
        if last_url:
            parsed = urlparse(last_url)
            qs = parse_qs(parsed.query)
            page_nums = qs.get("page") or qs.get("p")
            if page_nums:
                try:
                    commit_count = int(page_nums[0])
                except:
                    commit_count = 0
    else:
        if isinstance(data, list):
            commit_count = len(data)

    return commit_count, latest_date

def fetch_github_data_for_user(username):
    """Fetch all repos and commit info for a user"""
    out = {"username": username, "total_repos": 0, "repos": [], "error": None}
    try:
        repos = _get_all_repos_for_user(username)
    except Exception as e:
        out["error"] = str(e)
        return out

    out["total_repos"] = len(repos)
    for r in repos:
        repo_name = r.get("name")
        html = r.get("html_url")
        owner = r.get("owner", {}).get("login") or username
        try:
            commits, latest = _get_commit_count_and_latest(owner, repo_name)
        except:
            commits, latest = None, None

        out["repos"].append({
            "name": repo_name,
            "html_url": html,
            "commits": commits,
            "last_commit": latest
        })
        time.sleep(SLEEP_BETWEEN_CALLS)
    return out
