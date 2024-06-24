import requests

name = "brad pitt"
URL = f"https://api.agify.io?name={name}"

# sending get request and saving the response as response object
r = requests.get(url= URL)

data = r.json()

print(data)
