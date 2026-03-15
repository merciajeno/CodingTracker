import requests
import datetime
github_url = "https://api.github.com/search/commits"
today = datetime.datetime.now()
def get_commits(username):
    params = {
        "q": f"author:{username}",
        "sort": "author-date",
        "order": "desc"
    }

    headers = {
        "Accept": "application/vnd.github.cloak-preview"
    }

    response = requests.get(github_url, params=params, headers=headers)

    data = response.json()

    for item in data["items"]:
        commit = item["commit"]
        date = commit["author"]["date"]
        date=date[:date.find('T')]
        if today.strftime('%Y-%m-%d')==date:
         print(commit["author"]["date"], "-", commit["message"])

get_commits("merciajeno")