import requests
import json

url = "https://leetcode.com/graphql"

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

variables = {
    "username": "Mercia_Jeno"
}

payload = {
    "query": query,
    "variables": variables
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

data = response.json()

submissions = data["data"]["recentAcSubmissionList"]
print(len(submissions))
print(json.dumps(submissions, indent=2))