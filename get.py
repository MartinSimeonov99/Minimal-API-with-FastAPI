import requests

#GET Method
#You can try with different coordinates (replace the latitude={}, longitude={} and the radius={})

latitude = 42.62521770636195
longitude = 23.355158601013592
radius = 10

url = f"http://localhost:8000/addresses?latitude={latitude}&longitude={longitude}&radius={radius}"
response = requests.get(url)

if response.status_code == 200:
    print(response.json())
else:
    print(f"An error occurred: {response.status_code}")
