import logging as log
import random
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth

def scrapingfunc(AGENT_LIST):
    options = Options()


    # Random_Agent = random.choice(AGENT_LIST)
    # log.debug(f"Agent for this instance -> {Random_Agent}")
    options.set_capability("excludeSwitches", ["enable-automation"])
    options.set_capability('useAutomationExtension', False)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

    # options.set_preference("general.useragent.override",Random_Agent )

    browser = webdriver.Firefox(options=options)
    return browser

    


def sleep(a,b):
    return time.sleep(random.randint(a,b))
