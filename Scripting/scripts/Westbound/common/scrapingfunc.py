import time
import random
import logging as log
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options

def scrapingfunc(AGENT_LIST):
    options = Options()

    Random_Agent = random.choice(AGENT_LIST)
    log.debug(f"Agent for this instance -> {Random_Agent}")
    # options.headless = True
    # add the local download folder
    options.set_capability("excludeSwitches", ["enable-automation"])
    options.set_capability('useAutomationExtension', False)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    options.set_preference("general.useragent.override",Random_Agent )
    

    browser = webdriver.Firefox(options=options)
    return browser

def scrapingfunc_2():
    options = Options()
    # options.headless = True
    options.set_capability("excludeSwitches", ["enable-automation"])
    options.set_capability('useAutomationExtension', False)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    

    browser = webdriver.Firefox(options=options)
    return browser

def sleep(a,b):
    return time.sleep(random.randint(a,b))
