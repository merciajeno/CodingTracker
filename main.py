import requests

pixel_endpoint='https://pixe.la/v1/users'
user_params={
    'token':'iamahackerandadetective',
    'username':'mercia',
    'agreeTermsOfService':'yes',
    'notMinor':'yes'
}
response = requests.post(pixel_endpoint,json=user_params)
print(response.text)