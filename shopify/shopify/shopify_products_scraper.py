# This script is to obtain a dataset of products from a list of clean shopify urls

import requests
import pandas as pd

TIMEOUT = 10
LIMIT_PER_PAGE = 250
PAGES = 4

# Takes a url string, # of products per page and page number as input 
# outputs list of product JSON objects
def get_products_data(base_url, limit=LIMIT_PER_PAGE, page_number=1):
    url = f'{base_url}/products.json?limit={limit}&page={page_number}'
    response = requests.get(url, timeout=TIMEOUT)
    data = response.json()
    return data['products']

# iterate through multiple pages of product information to get a full list of products
def iterate_over_products(base_url, limit=LIMIT_PER_PAGE, pages=PAGES):
    products_list = []
    for page in range(1, pages+1):
        products = get_products_data(base_url, limit=limit, page_number = page)
        products_list.extend(products)
    return products_list

# Create a dataframe from a list of product JSON objects
def create_products_dataframe(base_url, product_list):
    products = []
    for item in product_list:
        title = item['title']
        handle = item['handle']
        created = item['created_at']
        product_type = item['product_type']
        vendor = item['vendor']
        for variant in item['variants']:
            price = variant['price']
            sku = variant['sku']
            available = variant['available']
            product = {
                'title': title,
                'handle': handle,
                'created': created,
                'product_type': product_type,
                'price': price,
                'sku': sku,
                'available': available,
                'vendor': vendor,
            }

            products.append(product)
        df = pd.DataFrame(products)
        df['base_url'] = base_url
    return df

# iterate over a list of urls to return a list of products
def iterate_over_urls(urls, limit=LIMIT_PER_PAGE, pages=PAGES):
    dfs = []
    for url in urls:
        products = iterate_over_products(url, limit=limit, pages=pages)
        df = create_products_dataframe(url, products)
        dfs.append(df)
    return pd.concat(dfs)

if __name__=='__main__':
    urls = ['https://heavenluxe.com', 'https://ilovelinen.com.au']
    df = iterate_over_urls(urls)
    df.to_csv('product-dataset.csv',index=False)