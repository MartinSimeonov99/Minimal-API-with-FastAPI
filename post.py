import requests

#POST Method
#You can test it with different coordinates (replace the vaulues of the variables in the data dict below)

url = "http://localhost:8000/address"

data = {
    "address": "Sofia, Bulgaria",
    "latitude": 42.62521770636195,
    "longitude": 23.355158601013592
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print(response.json())
else:
    print(f"An error occurred: {response.status_code}")
