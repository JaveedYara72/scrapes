import requests

api_url = "https://jsonplaceholder.typicode.com/todos/1"

def getData(url):
    response = requests.get(url)
    print(response.json())


    todo  = {'userId':1,'id':1,'title':'Virgil Van Dijk', 'Completed':True}
    response = requests.put(url,json=todo)
    print(response.json())

if __name__ == "__main__":
    getData(api_url)