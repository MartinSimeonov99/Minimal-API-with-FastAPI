import requests

#PUT Method
#You can test it by choosing the id generated from the json in the GET Method and adding it in the end of the url with "/" before it
#Example - http://localhost:8000/address/id <-- you set the id here
#Finally you can change the coordinates in the data dict with another ones by your choice, as long as they are valid ones. (Existing address)

url = "http://localhost:8000/address/6"

data = {
    "address": "New Address",
    "latitude": 42.62521770636195,
    "longitude": 23.355158601013592
}

response = requests.put(url, json=data)

if response.status_code == 200:
    print(response.json())
else:
    print(f"An error occurred: {response.status_code}")
