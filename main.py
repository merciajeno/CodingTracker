import requests
USERNAME = 'mercia'
TOKEN = 'iamahackerandadetective'
pixel_endpoint='https://pixe.la/v1/users'
user_params={
    'token':TOKEN,
    'username':USERNAME,
    'agreeTermsOfService':'yes',
    'notMinor':'yes'
}
#response = requests.post(pixel_endpoint,json=user_params)
#print(response.text)
graph_params = {
    "id": "coding",
    "name": "Coding Tracker",
    "unit": "commits",
    "type": "int",
    "color": "shibafu"
}

headers={
    'X-USER-TOKEN':TOKEN
}
graph_endpoint = f'{pixel_endpoint}/{USERNAME}/graphs'
response = requests.post(graph_endpoint,json=graph_params,headers=headers)
print(response.text)