import requests
from datetime import datetime, timezone

url = "https://leetcode.com/graphql"
count =0
query = """
query recentAcSubmissions($username: String!) {
  recentAcSubmissionList(username: $username) {
    id
    title
    titleSlug
    timestamp
  }
}
"""

variables = {"username": "Mercia_Jeno"}

payload = {"query": query, "variables": variables}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

submissions = data["data"]["recentAcSubmissionList"]

today = datetime.now(timezone.utc).date()
solved_today = False

def return_submissions():
 global solved_today, count
 for sub in submissions:
    submission_time = datetime.fromtimestamp(int(sub["timestamp"]), tz=timezone.utc)
    if submission_time.date() < today:
        break
    if submission_time.date() == today:
        solved_today = True
        count = count+1
 return count

return_submissions()
if solved_today:
    print("You solved at least one problem today")
else:
    print("No problems solved today")