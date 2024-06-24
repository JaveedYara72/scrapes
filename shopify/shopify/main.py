import pandas as pd
from shopify_homepage_scraper import get_root_url, get_homepage
from shopify_homepage_parser import *
from shopify_products_scraper import iterate_over_urls

URLS_FILE = 'urls.txt'

def get_list_of_urls(file):
    with open(file, 'r') as file:
        # Read the contents of the file as a list of strings
        lines = file.readlines()
        # Strip whitespace from each line and convert to a list of items
        items = [line.strip() for line in lines]
        return items

def process_urls(urls):
    processed_urls = []
    for url in urls:
        root_url = get_root_url(url)
        processed_urls.append(root_url)
    return processed_urls

if __name__=='__main__':
    urls = get_list_of_urls(URLS_FILE)
    print(urls)
    urls = process_urls(urls)
    # Home page info
    urls_homepage = []
    for url in urls:
        response = get_homepage(url)
        print(response)
        if 'shopify.com' in response.content.decode('utf-8'):
            print(f"{url} -> is a shopify website.")
            soup = parse_response(response)
            home_page_dict = parse_homepage(soup, url)
            urls_homepage.append(home_page_dict)
    df = pd.DataFrame(urls_homepage)
    df.to_csv('urls_homepage.csv', index=False)

    # Product info
    df = iterate_over_urls(urls)
    df.to_csv('product-dataset.csv',index=False)
    exit()



