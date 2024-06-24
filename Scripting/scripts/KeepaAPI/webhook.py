import requests
import json

webhook_url = "localhost/"

data = {
    'name': 'Javeed Yara',
    'subject': "Testing the webhook on webhook site, this is without the local server setup -> 19:01"
}

requests.post(webhook_url,data=json.dumps(data),headers = {'Content-Type':'application/json'})

