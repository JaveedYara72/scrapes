import io
import re
import os
import sys
import json 
import time 
import boto3
import platform
import datetime
import pandas as pd
from __init__ import *
import logging as log
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from common.scrapingFunc import * #random_func,scrapingfunc
from common.variables import *

class scrape:
    def __init__(self,browser):
        self.browser = browser
        # scrape_func(browser)
    
    def scrape_func(self):
        self.browser.get(main_link)
        delay = 30

        # username
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, username)))
            self.browser.find_element(By.XPATH,username).send_keys("una.brands@heavenluxe.com")
        except Exception as e:
            log.error(f'exception at username button - {e}')
        sleep(10,16)

        # password
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, password)))
            self.browser.find_element(By.XPATH,password).send_keys("UnaSPV2!")
        except Exception as e:
            log.error(f'exception at password button - {e}')
        sleep(8,16)
        
        # Login Button
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, login)))
            self.browser.find_element(By.XPATH,login).click()
        except Exception as e:
            log.error(f'exception at Login Button - {e}')
        finally:
            pass
        sleep(30,33)

        # there will be a pop up for sure, wait for it and click on the close button
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,popupbutton)))
            self.browser.find_element(By.XPATH,popupbutton).click()
        except Exception as e:
            log.error(f'exception at Pop up button - {e}')
        sleep(10,16)

        # Navigate to marketing
        try:
            self.browser.get(marketing_link)
        except Exception as e:
            log.error(f'exception at Navigate to marketing - {e}')
        sleep(30,32)

        # pop up logic again
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,popupbutton)))
            self.browser.find_element(By.XPATH,popupbutton).click()
        except Exception as e:
            log.error(f'exception at Pop up button - {e}')
        sleep(16,20)

        # Reports and Insights button
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,reports)))
            self.browser.find_element(By.XPATH,reports).click()
        except Exception as e:
            log.error(f'exception at Reports and Insights - {e}')
        sleep(4,8)

        # Data Insights button
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,datainsight)))
            self.browser.find_element(By.XPATH,datainsight).click()
        except Exception as e:
            log.error(f'exception at Data insights - {e}')
        time.sleep(120)

        # sponsored discovery
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,sponsored_discovery)))
            self.browser.find_element(By.XPATH,sponsored_discovery).click()
        except Exception as e:
            log.error(f'exception at Data insights - {e}')

        # navigate to keywords
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,keywords)))
            self.browser.find_element(By.XPATH,keywords).click()
        except Exception as e:
            log.error(f'exception at Data insights - {e}')

        # Date object interaction
        try:
            WebDriverWait(self.browser,120).until(EC.presence_of_element_located((By.XPATH,"span.date-cont-item:nth-child(1) > span:nth-child(3) > i:nth-child(1)")))
            self.browser.find_element(By.XPATH,"span.date-cont-item:nth-child(1) > span:nth-child(3) > i:nth-child(1)")
            print("CSS Selector worked")
        except Exception as e:
            print("CSS Selector didnt Work")

        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/section/div[2]/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/span/input")))
            self.browser.find_element(By.XPATH,"/html/body/div/section/div[2]/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/span/input")
            print("XPATH 1 worked out")
        except Exception as e:
            print('xpath 1 didnt work')   

        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/section/div[2]/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/span/span[2]/i")))
            self.browser.find_element(By.XPATH,"/html/body/div/section/div[2]/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/span/span[2]/i")
            print("XPATH 2 didnt work")
        except Exception as e:
            print("XPATH 2 didnt work")

        # Enter Date 
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,enterdate)))
            self.browser.find_element(By.XPATH,enterdate).clear()
            self.browser.find_element(By.XPATH,enterdate).send_keys('01/01/2020')
        except Exception as e:
            log.error(f'exception at Enter Date --- {e}')

        # dowload button
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,download)))
            self.browser.find_element(By.XPATH,download).click()
        except Exception as e:
            log.error('exception at download button --- {}'.format(e))


if __name__ == "__main__":
    log.basicConfig(format='%(asctime)s - %(message)s', level=log.INFO)
    # log.basicConfig(level=log.INFO)
    log.info('log at DEBUG level')

    # browser = scrapingfunc(AGENT_LIST)
    browser = scrapingfunc_chrome(AGENT_LIST)
    browser = webdriver.Chrome(executable_path="C:/Users/Y Javeed/.cache/selenium/chromedriver/win32/111.0.5563.64/chromedriver.exe")
    a = scrape(browser)
    scrape.scrape_func(a)
    
