import requests
from datetime import datetime
from dotenv import load_dotenv
from scripts.github_service import get_commits
from scripts.leetcode_service import return_submissions
load_dotenv()
import os
BASE_URL= os.getenv('BASE_URL')
USERNAME = 'mercia'
print(USERNAME)
headers = {
    "X-USER-TOKEN": os.getenv('TOKEN')
}

today = datetime.now().strftime("%Y%m%d")

# --------- GRAPH DEFINITIONS ----------
graphs = [
    {
        "id": "coding",
        "name": "Coding Tracker",
        "unit": "commits",
        "type": "int",
        "color": "shibafu"
    },
    {
        "id": "github",
        "name": "Github Tracker",
        "unit": "commits",
        "type": "int",
        "color": "kuro"
    }
]


# --------- FUNCTIONS ----------

def create_graph(graph_data):
    endpoint = f"{BASE_URL}/{USERNAME}/graphs"
    response = requests.post(endpoint, json=graph_data, headers=headers)
    print(f"Create graph {graph_data['id']} -> {response.text}")


def post_pixel(graph_id, quantity):
    endpoint = f"{BASE_URL}/{USERNAME}/graphs/{graph_id}"
    data = {
        "date": today,
        "quantity": str(quantity)
    }
    response = requests.post(endpoint, json=data, headers=headers)
    print(f"Post pixel to {graph_id} -> {response.text}")


# --------- CREATE GRAPHS ----------
# for graph in graphs:
#     create_graph(graph)


# --------- ADD PIXELS ----------
post_pixel("coding", get_commits('merciajeno'))
post_pixel("github", return_submissions())