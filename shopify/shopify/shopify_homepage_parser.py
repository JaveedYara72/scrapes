from datetime import datetime
import ast
from bs4 import BeautifulSoup
import re

def parse_response(response):
    try:
        soup = BeautifulSoup(response.content, "html.parser")
    except:
        return None
    return soup

def get_shopify_string_from_soup(soup):
    pattern = re.compile(r'var Shopify ')
    try:
        script = soup.find("script", text=pattern)
        if script:
            return script.string
    except:
        print('Incorrect response object')
        return None

def get_shopify_dict_from_string(script_string):

    if not script_string:
        return None

    shop_list = script_string.split(';')
    shop_list = [elem.strip().replace(":null",":None") for elem in shop_list if elem.strip()]
    shop_dict = {}
    for i in range(1, len(shop_list)):
        try:
            line = shop_list[i]
            key, val = line.split(" = ")
            key = key.lstrip("Shopify.")
            shop_dict[key] = ast.literal_eval(val)
        except:
            continue
        return shop_dict

def get_meta_properties(soup, property):
    if soup is not None:
        object = soup.find('meta',{'property': property})
        if object is not None:
            return object['content']
# example:
# result['site_name'] = get_meta_properties(soup, 'og:site_name')

def get_socials(soup):
    urls = soup.find("script",  {"type":"application/ld+json"})
    urls = str(urls).split() #need to split into string here to iterate through and get links #urls = urls['contactPoint']['sameAs']
    for link in urls:
        print("inside get socials function",link)
        if 'facebook' in link:
            fb_url = link[1:-2].replace("\\", "") or None
        if 'instagram' in link:
            insta_url = link[1:-2] or None
        if 'pinterest' in link:
            pinterest_url = link[1:-2] or None
        if 'youtube' in link:
            yt_url = link[1:-2] or None
        # if 'tiktok' in link:
        #     tiktok_url = link[1:-2] or None
        if 'snapchat' in link:
            snapchat_url = link[1:-2] or None
                
    res = [fb_url, insta_url, pinterest_url, yt_url,snapchat_url]
    res = [url for url in res if url is not None]
    return res

def get_mail_and_tel(soup):
    mails = []
    numbers = []
    mailtos = soup.select('a[href^=mailto]')
    for mailto in mailtos:
        href=mailto['href']
        try:
            _, str2 = href.split(':')
        except ValueError:
            break
        mails.append(str2)
            
    tel_nos = soup.select('a[href^=tel]')
    for tel_no in tel_nos:
        href=tel_no['href']
        try:
            _, str2 = href.split(':')
        except ValueError:
            break
        mails.append(str2)
            
            
    mails = "Unavailable" if len(mails) == 0 else mails
    numbers = "Unavailable" if len(numbers) == 0 else numbers
    return [mails, numbers]

def parse_homepage(soup, base_url):
    res = {}
    # og:site_name == Fashion Nova
    # og:url == fashionnova.com
    # og:title == Nova
    # og:description == Fashion Nova | Fashion Online For Women | Affordable Women's Clothing | Fashion Nova
    properties = ['og:site_name', 'og:url','og:title','og:description']
    res['scraped_url'] = base_url

    try:
        for property in properties:
            res[property] = get_meta_properties(soup, property) or None
        res['social_media_links'] = get_socials(soup)
        res['mail_and_tell_no'] = get_mail_and_tel(soup)
        res['date_scraped'] = datetime.now().strftime('%d-%m-%Y')
    except:
        print("Missing parameter for get_meta properties")

    try:
        script_string = get_shopify_string_from_soup(soup)
        shopify_dict = get_shopify_dict_from_string(script_string) 
        res['host'] = shopify_dict.get('shop')
        res['lang'] = shopify_dict.get('locale')
        theme = shopify_dict.get('theme') or {}
        res['theme'] = theme.get('name')
        currency = shopify_dict.get('currency') or {}
        res['currency'] = currency.get('active')
    except:
        print("Missing fields in var Shopify")
    return res
