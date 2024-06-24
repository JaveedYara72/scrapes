import requests
from urllib.parse import urlparse

TIMEOUT = 10

# When given a URL, get its root form
def get_root_url(url):
    parsed_url = urlparse(url)
    root_url = parsed_url.scheme + "://" + parsed_url.netloc
    return root_url

def get_homepage(url):
    root_url = get_root_url(url)
    response = requests.get(root_url, timeout=TIMEOUT)
    return response

if __name__=="__main__":
    url = "https://heavenluxe.com/products/premium-bundle-set"
    print(get_root_url(url))