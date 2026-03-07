import requests

leetcode_url=''

response = requests.get(leetcode_url)
print(response.text)