import requests
from datetime import datetime

USERNAME = "mercia"
TOKEN = "iamahackerandadetective"
BASE_URL = "https://pixe.la/v1/users"

headers = {
    "X-USER-TOKEN": TOKEN
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
post_pixel("coding", 3)
post_pixel("github", 5)