from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os


def scrapingfunc():
    options = Options()
    directory = os.getcwd()
    options.headless = True
    options.set_capability("excludeSwitches", ["enable-automation"])
    options.set_capability('useAutomationExtension', False)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    options.set_preference("browser.download.dir", directory)

    browser = webdriver.Firefox(options=options)
    return browser