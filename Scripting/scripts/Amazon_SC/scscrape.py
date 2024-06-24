import os
import time 
import logging as log
from selenium.webdriver.common.proxy import *

from variables import * 
from scrapingfunc import *
from scraper_functions import *

def bitwarden():
    # login locally
    os.popen('bw logout')
    # os.popen('fuser -k 8087/tcp')
    time.sleep(10)
    
    session_key = os.popen('bw login javeed.y@una-brands.com AGN.tft*bem5qkj7qyd').read().split('\n')[-1].split(' ')[-1]
    os.popen(f'bw serve --session {session_key}')
    os.popen('bw logout')
    time.sleep(10)

def scscrape_func(browser):
    
    bitwarden()
    
    exit()
    
    login(browser)
    
    payments_business_report(browser)
    
    # opportunity_explore(browser)

if __name__ == "__main__":
    
    log.basicConfig(format='%(asctime)s - %(message)s', level=log.INFO)    
    log.info('log at INFO level')
    log.info("Starting the Amazon Seller Central Scrape")

    browser = scrapingfunc()

    scscrape_func(browser)

