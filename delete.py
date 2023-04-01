import requests

#DELETE Method
#You can test it by choosing the id generated from the json in the GET Method and adding it in the end of the url
#Example - http://localhost:8000/address/id <-- goes here
 

url = "http://localhost:8000/address/1"
response = requests.delete(url)

if response.status_code == 200:
    data = response.json()
    if "message" in data:
        print(data["message"])
    elif "error" in data:
        print(data["error"])
else:
    print(f"An error occurred: {response.status_code}")
