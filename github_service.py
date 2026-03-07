import requests

github_url = 'https://api.github.com/search/commits?q='

def get_commits(username):
    response = requests.get(github_url+f'{username}')
    print(response.json()['total_count'])
get_commits('merciajeno')