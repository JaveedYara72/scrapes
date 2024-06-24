import io
import re
import os
import sys 
import pytz
import time 
import boto3
import requests
import datetime
import itertools
import pyperclip
import pandas as pd
import tkinter as tk
import logging as log
from __init__ import *
from pathlib import Path
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from dateutil.relativedelta import relativedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.scrapingfunc import * #random_func,scrapingfunc
from common.variables import *

# # S3 Code -> Common for all
# s3_client = boto3.client('s3',
#         aws_access_key_id=sys.argv[1], 
#         aws_secret_access_key=sys.argv[2])
# s3_resource = boto3.resource('s3',
#         aws_access_key_id=sys.argv[1], 
#         aws_secret_access_key=sys.argv[2])
# VInputRawPrifix='data/prod/d2c/shopify_seller/'
# vBucket = 'una-brands-ops'

# my_bucket = s3_resource.Bucket(vBucket)

def download_func(browser,month_range):
    delay = 30
    
    # export button
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,export_button)))
        browser.find_element(By.XPATH,export_button).click()
        log.info(f"Downloaded the file for {month_range}")
        sleep(8,10)
    except Exception as e:
        log.info("Not able to download the data")
        
    # click on profile
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,profile_button)))
        browser.find_element(By.XPATH,profile_button).click()
        log.info(f"clicked on profile button")
        sleep(8,10)
    except Exception as e:
        log.info("Error while clicking on profile button")
        
    # click on log out
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,logout)))
        browser.find_element(By.XPATH,logout).click()
        log.info(f"Logging out")
        sleep(8,10)
    except Exception as e:
        log.info("Unable to log out")
    

class scrape:
    def __init__(self,browser2):
        self.browser2 = browser2
        # scrape_func(browser)
        
    def scrape_func(self):    
        delay = 30
        
        no_of_months = 1 #sys.argv[1]
        
        bitwarden = {
            'tiktok':
                {
                    ('tsm.admin@una-brands.com', 'TikTok Seller (TSM SG)'):{
                        'link':'https://seller-sg.tiktok.com/account/login',
                        'country':['SG'],
                        'brand':'TSM SG'
                    },
                    ('tsm.admin+my@una-brands.com', 'TikTok Seller (TSM MY)'):{
                        'link':'https://seller-my.tiktok.com/account/login',
                        'country':['MY'],
                        'brand':'TSM MY'
                    },
                }
        }
        
        password_bit = ''
        otp = ''
        
        browser2.get("https://vault.bitwarden.com/#/login")
        delay = 30
        
        # bitwarden email 
        try:
            WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='login_input_email']")))
            browser2.find_element(By.XPATH,"//input[@id='login_input_email']").send_keys("javeed.y@una-brands.com")
        except Exception as e:
            log.info("Error ocurred while entering in the email logging in")
        time.sleep(5)

        # bitwarden email continue
        try:
            WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Continue')]")))
            browser2.find_element(By.XPATH,"//span[contains(text(),'Continue')]").click()
            log.info("Email Entered in bitwarden")
        except Exception as e:
            log.info("Error ocurred while clicking on 'Continue' whilst logging in")
        
        time.sleep(5)
        
        # bitwarden password 
        try:
            WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,"//input[@id='login_input_master-password']")))
            browser2.find_element(By.XPATH,"//input[@id='login_input_master-password']").send_keys("AGN.tft*bem5qkj7qyd")
        except Exception as e:
            log.info("Error whilst entering the bitwarden password")
        time.sleep(5)

        # bitwarden password continue
        try:
            WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Log in with master password')]")))
            browser2.find_element(By.XPATH,"//span[contains(text(),'Log in with master password')]").click()
            log.info("Password Clicked in bitwarden")
        except Exception as e:
            log.info("Error whilst clicking on Password")
        time.sleep(5)
        
        # iterate over the buttons and spans available
        table = browser2.find_element(By.XPATH,"//table[@class='tw-w-full tw-leading-normal tw-text-main tw-table-fixed']//tbody")
        button_values = table.find_elements(By.XPATH,"//td[@class='tw-break-all tw-align-middle tw-p-3']//button")
        span_values = table.find_elements(By.XPATH,"//td[@class='tw-break-all tw-align-middle tw-p-3']//span")
        
        button_values_list = []
        span_values_list = []
        
        for a in  button_values:
            button_values_list.append(a.text)
        for b in span_values:
            span_values_list.append(b.text)
            
        log.info(button_values_list)
        log.info(span_values_list)
            
        for (a, b) in itertools.zip_longest(span_values_list,button_values_list):
            password_bit = ''
            otp = ''
            
            a_text = a
            b_text = b
        
            if((a_text,b_text) in bitwarden['tiktok']):
                log.info("------------------------------------------------------")
                log.info((a_text,b_text))
                log.info(f"Trying to pull data for -> {bitwarden['tiktok'][(a_text,b_text)]['brand']}")
                log.info(bitwarden['tiktok'][(a_text,b_text)]['link'])
                sleep(20,20)
                
                # country and brand initialization
                country = bitwarden['tiktok'][(a_text,b_text)]['country']
                brand = bitwarden['tiktok'][(a_text,b_text)]['brand']
                
                log.info(country)
                log.info(brand)
                
                # opening a browser session -> will only open for 7 times in all the time
                browser = scrapingfunc_2()
                browser.get(bitwarden['tiktok'][(a_text,b_text)]['link'])
                sleep(10,15)
                
                months_to_run = no_of_months
                
                # Iterate over row buttons, so that we can check if the creds are matching or not
                for j in range(0,len(button_values)):
                    
                    # if('login' in browser.current_url):
                    #     # bitwarden password 
                    #     try:
                    #         WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,"//input[@id='login_input_master-password']")))
                    #         browser2.find_element(By.XPATH,"//input[@id='login_input_master-password']").send_keys("AGN.tft*bem5qkj7qyd")
                    #         sleep(5,8)
                    #     except Exception as e:
                    #         pass
                        

                    #     # bitwarden password continue
                    #     try:
                    #         WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Log in with master password')]")))
                    #         browser2.find_element(By.XPATH,"//span[contains(text(),'Log in with master password')]").click()
                    #         sleep(5,8)
                    #     except Exception as e:
                    #         pass
                    
                    # Click on Edit Item
                    try:
                        WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,f"tr.tw-cursor-pointer:nth-child({j+1}) > td:nth-child(3) > button")))
                        browser2.find_element(By.CSS_SELECTOR, f"tr.tw-cursor-pointer:nth-child({j+1}) > td:nth-child(3) > button").click()
                        sleep(3,4)
                    except Exception as e:
                        log.info("Error clicking on the button element")
                        sleep(4,5)
                    
                    # name
                    try:
                        name_input = browser2.find_element(By.ID,"name")
                        name_text = name_input.get_attribute("value")
                        log.info(f"name found on bitwarden -> {name_text}")
                        sleep(3,4)
                    except Exception as e:
                        log.info("Error at Extracting Name data")
                        sleep(3,4)
                        
                    # username
                    try:
                        copy_button_1 = browser2.find_element(By.XPATH,"//div[@class='input-group-append']//button[@title='Copy username']")
                        copy_button_1.click()
                        username = Keys.CONTROL + 'v'
                        log.info(username)
                        # root = tk.Tk()
                        # username = root.clipboard_get()
                        # log.info(f"The user name found on bitwarden -> {username}")
                        # root.overrideredirect(1)
                        # root.withdraw() 
                        # root.deiconify()
                        sleep(3,5)
                    except Exception as e:
                        try:
                            copy_button_1 = browser2.find_element(By.CSS_SELECTOR,"div.row:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)")
                            copy_button_1.click()
                            username = Keys.CONTROL + 'v'
                            log.info(username)
                            # root = tk.Tk()
                            # log.info(f"The user name found on bitwarden -> {username}")
                            # root.overrideredirect(1)
                            # root.withdraw() 
                            # root.deiconify()
                            sleep(3,5)
                        except Exception as e:
                            log.info("Username not clickable.")
                        
                        
                    if(b_text == name_text and a_text == username):
                        log.info("Found the Match")
                        log.info(f"This is the pair -> {b_text} and {a_text}")
                            
                            
                        # login with email
                        try:
                            WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,login_email)))
                            browser.find_element(By.XPATH,login_email).click()
                            log.info("Clicked on login_email")
                            sleep(3,4)
                        except Exception as e:
                            log.info("Error clicking on the login_email element")
                            sleep(4,5)
                        
                        # email
                        try:
                            WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,email)))
                            browser.find_element(By.XPATH,email).send_keys(Keys.CONTROL+'v')
                            sleep(3,4)
                        except Exception as e:
                            log.info("Error clicking on the button element")
                            sleep(4,5)
                        
                        # password
                        try:
                            copy_button_2 = browser2.find_element(By.XPATH,"//div[@class='input-group-append']//button[@title='Copy password']")
                            copy_button_2.click()
                            # root = tk.Tk()
                            # password_bit = root.clipboard_get()
                            # root.overrideredirect(1)
                            # root.withdraw() 
                            # root.deiconify()
                            time.sleep(5)
                        except Exception as e:
                            log.info("Error while copying the password")
                            
                        # enter password in the tiktok website
                        try:
                            WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,password)))
                            browser.find_element(By.XPATH,password).send_keys(Keys.CONTROL+'v')
                            log.info("Entered password in the main website")
                            sleep(6,8)
                        except Exception as e:
                            log.info("Error entering the password in the main website")
                            sleep(4,5)
                        
                        # Domain copy
                        try:
                            copy_button_4 = browser2.find_element(By.XPATH,"//div[@class='input-group-append']//button[@title='Copy URI']")
                            copy_button_4.click()
                            root = tk.Tk()
                            domain = root.clipboard_get()
                            root.overrideredirect(1)
                            root.withdraw() 
                            root.deiconify()
                            time.sleep(5)
                        except Exception as e:
                            log.info("Error while copying the URI")
                            
                            
                        # Log in, finally
                        try:
                            WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,login)))
                            browser.find_element(By.XPATH,login).click()
                            log.info("logging in")
                            sleep(6,8)
                        except Exception as e:
                            log.info("Error Logging in ")
                            sleep(4,5)
                            
                        # otp login
                        # bitwarden timer
                        timer_ = browser2.find_element(By.XPATH,"//span[@class='totp-countdown']//span[@class='totp-sec']")
                        timer_2 = timer_.text
                        log.info(f"Timer on the code -> {timer_2}")
                        if(int(timer_2)<=11):
                            log.info("The timer is less than 11, so putting it to sleep for 10 secs")
                            time.sleep(10)
                        
                        root = tk.Tk()
                        root.overrideredirect(1)
                        root.withdraw() 
                        root.deiconify()

                        # bitwarden otp
                        copy_button_3 = browser2.find_element(By.XPATH,"//button[@title='Copy verification code']")
                        copy_button_3.click()
                        root = tk.Tk()
                        code = root.clipboard_get()
                        otp = code
                        log.info(f"The code is -> {code}")
                        root.overrideredirect(1)
                        root.withdraw()
                        
                        # put the otp in 2 step verification of tiktok
                        try:
                            WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,otp_input)))
                            browser.find_element(By.XPATH,otp_input).send_keys(otp)
                            log.info("putting otp in")
                        except Exception as e:
                            log.info("Error Logging in with otp")
                            sleep(4,5)
                            
                        # click on confirm after otp
                        try:
                            WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,Confirm)))
                            browser.find_element(By.XPATH,Confirm).click()
                            log.info("Clicking on Confirm")
                            sleep(20,30)
                        except Exception as e:
                            log.info("Error whilst clicking on Confirm")                    
                        
                        # redirecting to data compass 
                        browser.get(f"{domain}compass/data-overview")
                        sleep(20,30)
                        
                        # handle all the popups
                        # shopping center popup
                        try:
                            WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,shopping_center_popup)))
                            browser.find_element(By.XPATH,shopping_center_popup).click()
                            log.info("Clicked on shopping center pop up")
                            sleep(2,3)
                        except Exception as e:
                            sleep(4,5)
                        
                        
                        # defected orders popup
                        try:
                            WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,defected_orders_popup)))
                            browser.find_element(By.XPATH,defected_orders_popup).click()
                            log.info("Clicked on defected orders pop up")
                            sleep(2,3)
                        except Exception as e:
                            sleep(4,5)
                        
                        # notification pop up
                        try:
                            WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,notification_popup)))
                            browser.find_element(By.XPATH,notification_popup).click()
                            log.info("Clicked on notification pop up")
                            sleep(2,3)
                        except Exception as e:
                            sleep(4,5)
                        
                        # Date picker notification
                        try:
                            WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,datepicker_popup)))
                            browser.find_element(By.XPATH,datepicker_popup).click()
                            log.info("Clicked on date picker pop up")
                            sleep(2,3)
                        except Exception as e:
                            sleep(4,5)
                        
                        # academy pop up
                        try:
                            WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,academy_popup)))
                            browser.find_element(By.XPATH,academy_popup).click()
                            log.info("Clicked on academy pop up")
                            sleep(2,3)
                        except Exception as e:
                            sleep(4,5)    
                            
                        # click on the span element
                        months_dic = {'01':'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
                        
                        # flags important for scraping
                        month_range = []
                        today = datetime.datetime.now()
                        
                        # generating all the months
                        for i in range(0,int(months_to_run)):
                            month_iter = today-relativedelta(months=+i)
                            month_range.append(months_dic[month_iter.strftime("%m")])
                            
                        for i in range(0,len(month_range)):
                            # click on month 
                            # xpath for the month -> //div[@class='compass-arco-space-item']//div[@class='compass-m4b-date-picker-range-mode-item' and contains(text(),'Month')]
                            # click on calendar button
                            try:
                                WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,calendar_button)))
                                browser.find_element(By.XPATH,calendar_button).click()
                                log.info("Clicked on calendar")
                                sleep(2,3)
                            except Exception as e:
                                sleep(4,5)
                                
                            # Click on Months Navigation
                            try:
                                WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,month_button)))
                                browser.find_element(By.XPATH,month_button).click()
                                log.info("Clicked on Month")
                                sleep(2,3)
                            except Exception as e:
                                sleep(4,5)
                                
                            
                            # try changing the logic of Jan here because, the calendar doesn't hold that state, so write it for dec.
                            if(month_range[i] == 'Dec'):
                                # year navigation comes here
                                try:
                                    WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,year_navigator_svg_css)))
                                    browser.find_element(By.CSS_SELECTOR,year_navigator_svg_css).click()
                                    log.info("Navigated back an year")
                                    sleep(8,10)
                                except Exception as e:
                                    try:
                                        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,year_navigator_svg_css_2)))
                                        browser.find_element(By.CSS_SELECTOR,year_navigator_svg_css_2).click()
                                        log.info("Navigated back an year (_2)")
                                        sleep(8,10)
                                    except Exception as e:
                                        log.info("Not able to Navigate to the previous year")
                                
                                try:
                                    WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,f"//div[@class='compass-arco-picker-cell compass-arco-picker-cell-in-view']//div[@class='compass-arco-picker-date']//div[@class='compass-arco-picker-date-value' and contains(text(),{month_range[i]})]")))
                                    browser.find_element(By.XPATH,f"//div[@class='compass-arco-picker-cell compass-arco-picker-cell-in-view']//div[@class='compass-arco-picker-date']//div[@class='compass-arco-picker-date-value' and contains(text(),{month_range[i]})]").click()
                                    log.info(f"Clicked on {month_range[i]}")
                                    sleep(8,10)
                                except Exception as e:
                                    log.info("Not able to click on month, perhaps it is the current month")
                                    try:
                                        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,f"//div[@class='compass-arco-picker-cell compass-arco-picker-cell-in-view compass-arco-picker-cell-today']//div[@class='compass-arco-picker-date']//div[@class='compass-arco-picker-date-value' and contains(text(),{month_range[i]})]")))
                                        browser.find_element(By.XPATH,f"//div[@class='compass-arco-picker-cell compass-arco-picker-cell-in-view compass-arco-picker-cell-today']//div[@class='compass-arco-picker-date']//div[@class='compass-arco-picker-date-value' and contains(text(),{month_range[i]})]").click()
                                        log.info(f"Clicked on {month_range[i]}")
                                        sleep(8,10)
                                    except Exception as e:
                                        log.info(f"Clicked on {month_range[i]}")
                                        
                                download_func(browser,month_range[i])
                            else:
                                try:
                                    WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,f"//div[@class='compass-arco-picker-cell compass-arco-picker-cell-in-view']//div[@class='compass-arco-picker-date']//div[@class='compass-arco-picker-date-value' and contains(text(),{month_range[i]})]")))
                                    browser.find_element(By.XPATH,f"//div[@class='compass-arco-picker-cell compass-arco-picker-cell-in-view']//div[@class='compass-arco-picker-date']//div[@class='compass-arco-picker-date-value' and contains(text(),{month_range[i]})]").click()
                                    log.info(f"Clicked on {month_range[i]}")
                                    sleep(8,10)
                                except Exception as e:
                                    log.info("Not able to click on month, perhaps it is the current month")
                                    try:
                                        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,f"//div[@class='compass-arco-picker-cell compass-arco-picker-cell-in-view compass-arco-picker-cell-today']//div[@class='compass-arco-picker-date']//div[@class='compass-arco-picker-date-value' and contains(text(),{month_range[i]})]")))
                                        browser.find_element(By.XPATH,f"//div[@class='compass-arco-picker-cell compass-arco-picker-cell-in-view compass-arco-picker-cell-today']//div[@class='compass-arco-picker-date']//div[@class='compass-arco-picker-date-value' and contains(text(),{month_range[i]})]").click()
                                        log.info(f"Clicked on {month_range[i]}")
                                        sleep(8,10)
                                    except Exception as e:
                                        log.info(f"Clicked on {month_range[i]}")     
                                download_func(browser,month_range[i])
                        # finally break this for loop -> break, so that it could go to the next store iteration that it has
                        
                        # save button
                        try:
                            browser2.find_element(By.XPATH,"//div[@class='modal-footer']//button[@class='btn btn-primary btn-submit']").click()
                            log.info("Clicked on save button in bitwarden")
                        except Exception as e:
                            log.info("Error clicking on save button, retrying with a class appended")
                            try:
                                browser2.find_element(By.XPATH,"//div[@class='modal-footer']//button[@class='btn btn-primary btn-submit ng-star-inserted']").click()
                                log.info("Clicked on save button in bitwarden")
                            except Exception as e:
                                log.info("Error Clicking on Save button with the appended class")
                        
                        # Redirecting to Main Vault    
                        try:
                            browser2.get("https://vault.bitwarden.com/#/vault")
                            log.info("Redirecting to the main vault")
                        except Exception as e:
                            log.info("Error Redirecting to the main vault")
                        
                        # closing the browser
                        browser.quit()
                        break
                
                    # save button
                    try:
                        browser2.find_element(By.XPATH,"//div[@class='modal-footer']//button[@class='btn btn-primary btn-submit']").click()
                        log.info("Clicked on save button in bitwarden")
                    except Exception as e:
                        log.info("Error clicking on save button, retrying with a class appended")
                        try:
                            browser2.find_element(By.XPATH,"//div[@class='modal-footer']//button[@class='btn btn-primary btn-submit ng-star-inserted']").click()
                            log.info("Clicked on save button in bitwarden")
                        except Exception as e:
                            log.info("Error Clicking on Save button with the appended class")
                    
                    # Redirecting to Main Vault    
                    try:
                        browser2.get("https://vault.bitwarden.com/#/vault")
                        log.info("Redirecting to the main vault")
                    except Exception as e:
                        log.info("Error Redirecting to the main vault")
                    sleep(6,8)
            
        
        
if __name__ == "__main__":
    log.basicConfig(format='%(asctime)s - %(message)s', level=log.INFO)
    
    # log.basicConfig(level=log.INFO)
    log.info('log at DEBUG level')
    log.info("Starting the Tiktok Scrape")
    
    browser2 = scrapingfunc(AGENT_LIST)
    a = scrape(browser2)
    scrape.scrape_func(a)
    log.info("Done scraping the website")
