import io
import re
import os
import sys 
import pytz
import time 
import boto3
import requests
import datetime
import tkinter as tk
import pandas as pd
from lxml import html
import logging as log
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from dateutil.relativedelta import relativedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from __init__ import *

from common.scrapingfunc import * #random_func,scrapingfunc
from common.variables import *

# vBucket = 'una-brands-ops'
# AWS_ACCESS_KEY_ID = sys.argv[1]
# AWS_SECRET_ACCESS_KEY = sys.argv[2]
# s3_client = boto3.client('s3',
#         aws_access_key_id= AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
# s3_resource = boto3.resource('s3',
#         aws_access_key_id= AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
# VInputRawPrifix = 'data/prod/landing_raw/inventory_scrapes/westbound/US/'


class scrape:
    def __init__(self,browser2):
        self.browser2 = browser2
    
    def scrape_func(self):
        delay = 30
        
        browser2.get(main_link)
        
        brand_list = ['Velener','Samuel_World','Gobam','Jocuu','Unjumbly','Finerware','Hookeze','ZooSnoods','Bellaforte','Viverie','Mydethun','Kadams','Inaya']
        username = ['UVE3pllax','UNS3pllax','UGO3pllax','JOC3pllax','UUN3plax','fiw3pllax','hoo3pllax','UNZS3plax','BELL3pllax','VIV3pllax','myd3pllax','UNK3pllax','UNI3pllax']
        password = ['uve3pl123','UNS3pl123','UGO3pl123','JOC3pl123','uun3pl123','fiw3pl123','hoo3pl123','UNZS3pl123','bell3pl123','viv3pl123','myd3pl123','unk3pl123','UNI3pl123']
                        
        for i in range(0,len(brand_list)):
            
            log.info(f"Downoading data for {brand_list[i]}")
            
            # log in with email
            try:
                WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,login_email)))
                browser2.find_element(By.XPATH,login_email).send_keys(f"{username[i]}")
                log.info("Email Entered in Westbound")
            except Exception as e:
                log.error("Error ocurred while entering email in Westbound")
            sleep(5,5)
                
            # Password
            try:
                WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,password)))
                browser2.find_element(By.XPATH,password).send_keys(f"{password[i]}")
                log.info("Password Entered in Westbound")
            except Exception as e:
                try:
                    WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,password_2)))
                    browser2.find_element(By.XPATH,password_2).send_keys(f"{password[i]}")
                    log.info("Password Entered in Westbound")
                except Exception as e:
                    log.error("Error ocurred while entering password in Westbound")
            sleep(5,5)
                
            # login button
            try:
                WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,login)))
                browser2.find_element(By.XPATH,login).click()
                log.info("login button clicked in Westbound")
            except Exception as e:
                log.error("Error ocurred while clicking on login button on Westbound")
            sleep(5,5)
                
            # Inventory button
            try:
                WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,inventory)))
                browser2.find_element(By.XPATH,inventory).click()
                log.info("Inventory button clicked in Westbound")
            except Exception as e:
                log.error("Error ocurred while clicking on Inventory button on Westbound")
            sleep(5,5)
                
            # Manage Inventory button
            try:
                WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,manage_inventory)))
                browser2.find_element(By.XPATH,manage_inventory).click()
                log.info("manage_inventory button clicked in Westbound")
            except Exception as e:
                log.error("Error ocurred while clicking on manage_inventory button on Westbound")
            sleep(20,25)
                
            # options dropdown button
            try:
                WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,options_dropdown_css2)))
                browser2.find_element(By.CSS_SELECTOR,options_dropdown_css2).click()
                log.info("options_dropdown button clicked in Westbound")
                
            except Exception as e:
                log.error("Error ocurred while clicking on options_dropdown_css2 button on Westbound")
            sleep(5,5)
            
            # button
            try:
                WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,download_button_1)))
                browser2.find_element(By.CSS_SELECTOR,download_button_1).click()
            except Exception as e:
                log.error("Error ocurred while clicking on download_button_1 button on Westbound")
            sleep(5,5)
            
            # export to excel
            try:
                WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,download_button_2)))
                browser2.find_element(By.XPATH,download_button_2).click()
                log.info("Clicked on Export to Excel")
            except Exception as e:
                sleep(5,5)
                try:
                    WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,download_button_3)))
                    browser2.find_element(By.XPATH,download_button_3).click()
                    log.info("Clicked on Export to Excel")
                    sleep(5,5)
                except Exception as e:
                    log.error("Error ocurred while clicking on Export to Excel using download button 3")
            sleep(5,5)
            
            # Uploading it to AWS s3
            # try:
            #     files_list=os.listdir()
            #     import datetime
            #     vLatestUpdatedDateTime = datetime.datetime.now()
            #     vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
            #     for name in files_list:
            #         if "inventoryGridExport-" in name:
            #             df=pd.read_excel(name,index_col=None)
            #             fname = brand_list[i] + ".xlsx"
            #             with io.BytesIO() as output:
            #                 with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            #                     df.to_excel(writer)
            #                 data = output.getvalue()
            #                 response = s3_client.put_object(
            #                     Bucket=vBucket, Key='{}{}/inventoryGridExport-{}-US.xlsx'.format(VInputRawPrifix,brand_list[i],vLatestUpdatedDateTimeFile), Body=data
            #                 )

            #                 status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

            #                 if status == 200:
            #                     print(f"Successful S3 put_object response. Status - {status}")
            #                 else:
            #                     print(f"Unsuccessful S3 put_object response. Status - {status}")
            #             os.remove(name)
            # except Exception as e:
            #     log.error(f"Couldn't scrape westbound data for {brand_list[i]}")
                    
            # profile button
            try:
                WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,profile)))
                browser2.find_element(By.XPATH,profile).click()
                log.info("profile button clicked in Westbound")
            except Exception as e:
                log.error("Error ocurred while clicking on profile button on Westbound")
            sleep(5,5)

            # Sign out button
            try:
                WebDriverWait(browser2,delay).until(EC.presence_of_element_located((By.XPATH,log_out)))
                browser2.find_element(By.XPATH,log_out).click()
                log.info("log_out button clicked in Westbound")
            except Exception as e:
                log.error("Error ocurred while clicking on log_out button on Westbound")
            sleep(5,5)
            
            log.info("-----------------------------------------------------------------------------------------")


if __name__ == "__main__":
    log.basicConfig(format='%(asctime)s - %(message)s', level=log.INFO)
    # log.basicConfig(level=log.INFO)
    log.info('log at DEBUG level')
    log.info("Starting the Westbound scrape")

    browser2 = scrapingfunc(AGENT_LIST)
    
    a = scrape(browser2)
    scrape.scrape_func(a)
    browser2.quit()
    log.info("Done scraping the website")
