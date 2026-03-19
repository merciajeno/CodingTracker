import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

#TOKEN = os.getenv("GITHUB_TOKEN")
today = datetime.datetime.now().strftime('%Y-%m-%d')
repos = dict()
headers = {
    "Accept": "application/vnd.github.cloak-preview",
    #"Authorization": f"Bearer {TOKEN}"  # add this — unauthenticated = 60 req/hr, authenticated = 5000
}

VAGUE_MESSAGES = {"fix", "update", "misc", "changes", "wip", "test", "commit", "done", "edit"}

def get_commit_detail(repo_full_name, sha):
    # second call — this is where diff lives
    url = f"https://api.github.com/repos/{repo_full_name}/commits/{sha}"
    response = requests.get(url, headers=headers)
    return response.json()

def get_commits(username):
    search_url = "https://api.github.com/search/commits"
    params = {
        "q": f"author:{username} author-date:{today}",  # filter by today directly in query
        "sort": "author-date",
        "order": "desc"
    }

    response = requests.get(search_url, params=params, headers=headers)
    data = response.json()

    results = []

    for item in data["items"]:
        commit = item["commit"]
        sha = item["sha"]
        repo_full_name = item["repository"]["full_name"]  # e.g. "merciajeno/my-project"

        # second call per commit to get diff details
        detail = get_commit_detail(repo_full_name, sha)

        files_changed = len(detail.get("files", []))
        total_lines = detail.get("stats", {}).get("total", 0)
        message = commit["message"].strip().lower().split("\n")[0]  # first line only

        commit_data = {
            "repo": repo_full_name,
            "message": message,
            "files_changed": files_changed,
            "total_lines": total_lines,
            "flags": []
        }

        # --- rules ---
        if message in VAGUE_MESSAGES or len(message.split()) == 1:
            commit_data["flags"].append("vague message")
        if files_changed == 1:
            commit_data["flags"].append("only 1 file changed")
        if total_lines < 3:
            commit_data["flags"].append("diff under 3 lines")

        results.append(commit_data)
        print(f"{repo_full_name}  | {message} | lines: {total_lines} | files: {files_changed} | flags: {commit_data['flags']}")

    return results  # list of dicts, not just a count anymore


get_commits('merciajeno')

## What changed and why

# **The search API gives you this per commit:**
# ```
# sha, message, date, repo name  ← that's it
# ```
#
# **The detail API gives you this:**
# ```
# files[], stats.total, stats.additions, stats.deletions