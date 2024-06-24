import io
import re
import os
import sys 
import pytz
import time 
import boto3
import requests
import datetime
import pandas as pd
from __init__ import *
import logging as log
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from dateutil.relativedelta import relativedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.scrapingFunc import * #random_func,scrapingfunc
from common.variables import *

# # S3 Code -> Common for all
# s3_client = boto3.client('s3',
#         aws_access_key_id=sys.argv[1], 
#         aws_secret_access_key=sys.argv[2])
# s3_resource = boto3.resource('s3',
#         aws_access_key_id=sys.argv[1], 
#         aws_secret_access_key=sys.argv[2])
# VInputRawPrifix='data/prod/d2c/shopee_seller/'
# vBucket = 'una-brands-ops'

# my_bucket = s3_resource.Bucket(vBucket)

def get_start_and_end(max_days):
    log.info(f"Daily level data would be downloaded for {max_days} days")
    dic = []
    tz = pytz.timezone('Asia/Kuala_Lumpur')
    today = datetime.datetime.now(tz=tz)
    start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    for _ in range(max_days):
        start -= datetime.timedelta(days = 1)
        dic.append((int(datetime.datetime.timestamp(start)), int(datetime.datetime.timestamp(start + datetime.timedelta(days = 1, seconds = -1)))))
    return dic

def template_function_year(month_range,i):
    if(i==0):
        xpath = f"//div[@class='shopee-date-picker-panel']//div[@class='shopee-date-picker-panel__body']//div[@class='shopee-date-picker-panel__date']//div[@class='shopee-month-table']//div[@class='shopee-month-table__row']//div[@class='shopee-month-table__col current' and contains(text(),'{month_range}')]"
    else:
        xpath = f"//div[@class='shopee-date-picker-panel']//div[@class='shopee-date-picker-panel__body']//div[@class='shopee-date-picker-panel__date']//div[@class='shopee-month-table']//div[@class='shopee-month-table__row']//div[@class='shopee-month-table__col' and contains(text(),'{month_range}')]"
    return xpath

class scrape:
    def __init__(self,browser):
        self.browser = browser
        # scrape_func(browser)
    
    def scrape_func(self):
        self.browser.get(main_link)
        delay = 30
        
        # daystorun = int(sys.argv[1])
        monthstorun = 16
        
        
        
        # Pop up - Choose Language button
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, languagebutton)))
            self.browser.find_element(By.XPATH,languagebutton).click()
            log.info("Chosen English Language")
        except Exception as e:
            log.error(f'exception at language pop up button - {e}')
        sleep(12,16)


        # username
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, username)))
            self.browser.find_element(By.XPATH,username).send_keys("supermamalab@gmail.com")
            log.info("Entered Username")
        except Exception as e:
            log.error(f'exception at username button - {e}')
        sleep(10,16)

        # password
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, password)))
            self.browser.find_element(By.XPATH,password).send_keys("Un@supermama23!")
            log.info("Entered Password")
        except Exception as e:
            log.error(f'exception at password button - {e}')
        sleep(8,16)
        
        # log in button
        try:
            WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, login)))
            self.browser.find_element(By.XPATH,login).click()
            log.info("Clicked on Log In Button")
        except Exception as e:
            log.error(f'exception at log in button - {e}')
        sleep(12,16)
        
        # # date level logic 
        # all_cookies = self.browser.get_cookies()
        # cookies_dict = {}
        # print(type(all_cookies))
        # for cookie in all_cookies:
        #     cookies_dict[cookie['name']] = cookie['value']
            
        # date_dic = get_start_and_end(daystorun)
        
        # # pass the obtained date into this parameters dict
        today = datetime.datetime.now()
        
        # with requests.Session() as session:
        #     all_cookies = self.browser.get_cookies()
            
        #     cookies_dict = {}
            
        #     for cookie in all_cookies:
        #         cookies_dict[cookie['name']] = cookie['value']
                
        #     session.cookies.update(cookies_dict)
            
        #     count  = 1
            
        #     for k,v in date_dic:
        #         parameters = {
        #             'report_type' : 1,
        #             'start_time' : k,
        #             'end_time' : v
        #         }
                
        #         response = session.get("https://seller.shopee.com.my/api/marketing/v3/pas/report_file/export/", params=parameters)
                
        #         # for all the dates that dont have data or too many requests
        #         if(response.status_code != 200):
        #             log.error("No response or Data has not been generated")
        #             log.error("Navigating to Business Insights")
        #             break
            
        #         response = response.json()
        #         fileid = response['data']['fileid']
        #         file_name = response['data']['file_name'].replace('/', '-')
        #         time.sleep(10)
                
        #         response = session.get("https://seller.shopee.com.my/api/marketing/v3/pas/report_file/", params={'fileid':fileid})
        #         with open(f'test_{count}.csv', 'w',encoding='utf-8') as f:
        #             f.write(response.text)
        #             count+=1
                                
        #         # # write the code into the bucket                
        #         # response = s3_client.put_object(
        #         #     Bucket=vBucket, Key=today.strftime("%Y-%m-%d_%Hh_%Mm_%Ss"), Body=response.text
        #         # )
        #         # status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        #         # if status == 200:
        #         #     print(f"Successful S3 put_object response. Status - {status}")
        #         # else:
        #         #     print(f"Unsuccessful S3 put_object response. Status - {status}")
            
                    
        #         print_date_start = datetime.datetime.fromtimestamp(int(k)).strftime("%d-%m-%Y")
        #         print_date_end = datetime.datetime.fromtimestamp(int(v)).strftime("%d-%m-%Y")
        #         log.info(f"Caught response for the date->  {print_date_end}")
        #         sleep(60,60)
        
        # log.info("Done with generating shopee ads data")
        # sleep(4,8)
        
        self.browser.get("https://seller.shopee.com.my/datacenter/dashboard")
        sleep(10,12)
        
        months_dic = {'01':'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
        
        # flags important for scraping
        month_range = []
        
        # generating all the months
        for i in range(0,int(monthstorun)):
            month_iter = today-relativedelta(months=+i)
            month_range.append(months_dic[month_iter.strftime("%m")])
        
        for i in range(0,len(month_range)):
            
            log.info(f"scraping the report for {month_range[i]}")
            # business month svg button
            try:
                WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,business_month_button_svg)))
                self.browser.find_element(By.XPATH,business_month_button_svg).click()
                log.info("Clicked on business month svg button")
            except Exception as e:
                log.error(f"error -> Didn't find the business month button -> {e}")
            sleep(10,14)
                
            # business month button
            try:
                WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,"li.shopee-date-shortcut-item:nth-child(8) > i:nth-child(2) > svg:nth-child(1)")))
                self.browser.find_element(By.CSS_SELECTOR,"li.shopee-date-shortcut-item:nth-child(8) > i:nth-child(2) > svg:nth-child(1)").click()
                log.info("Clicked on business month button")
            except Exception as e:
                log.error("error -> Didn't find the business month button -> {e}")
            sleep(12,16)
            
            # chose the month -> currently, i have added the current class month, write an if else here for the months that are not current. Just remove that class from xpath.
            if(month_range[i] == 'Jan'):
                xpath_year = template_function_year(month_range[i],i)
                print(f"xpath_year = {xpath_year}")
                print(f"current_month for testing -> {month_range[i]}")
                print(f"current iteration -> {i}")
                
                # clicking on the year
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,xpath_year)))
                    self.browser.find_element(By.XPATH,xpath_year).click()
                    log.info("Clicked on month button")
                except Exception as e:
                    log.error(f"error -> Selenium wasn't able to find the month -> {e}" )
                sleep(14,16)
                    
                # Business insights pop up button
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,business_insights_popup_css_2)))
                    self.browser.find_element(By.CSS_SELECTOR,business_insights_popup_css_2).click()
                    log.info("Clicked on Business insights pop up css 2")
                except Exception as e:
                    log.error("error->There was no pop up or selenium failed to interact with the element using css 2")
                sleep(12,16)
                
                # Export data
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,download_data)))
                    self.browser.find_element(By.XPATH,download_data).click()
                    log.info(f"Downloading the data for {month_range[i]}")
                except Exception as e:
                    log.error("error -> Error with exporting data")
                sleep(65,65)
                
                # # file writing
                # files_list=os.listdir()
                # for name in files_list:
                #     if "Shopee-ads-Keyword_Placement-level-data" in name:
                #         df_data=pd.read_csv(name,index_col=None)
                #         with io.StringIO() as csv_buffer:
                #             df_data.to_csv(csv_buffer, index=False)
                #             response = s3_client.put_object(
                #                             Bucket=vBucket, Key=f'strftime("%Y-%m-%d_%Hh_%Mm_%Ss")',Body=csv_buffer.getvalue())
                #             status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

                #             if status == 200:
                #                 print(f"Successful S3 put_object response. Status - {status}")
                #             else:
                #                 print(f"Unsuccessful S3 put_object response. Status - {status}")
                #         os.remove(name)
                
                # open the calendar again inorder to navigate it to the previous year
                # business month svg button
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,business_month_button_svg)))
                    self.browser.find_element(By.XPATH,business_month_button_svg).click()
                    log.info("Clicked on business month svg button")
                except Exception as e:
                    log.error(f"error -> Didn't find the business month svg button -> {e}")
                sleep(12,16)
                    
                # click on by month    
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,business_month_button_month)))
                    self.browser.find_element(By.XPATH,business_month_button_month).click()
                    log.info("Clicked on business month button")
                except Exception as e:
                    log.error(f"error -> Didn't find the business month button -> {e}")
                sleep(12,16)
            
                # add year navigation
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, year_navigator_svg_css)))
                    self.browser.find_element(By.CSS_SELECTOR,year_navigator_svg_css).click()
                    log.info("Went back to the previous year")
                except Exception as e:
                    log.error(f'exception at previous year button css1')
                sleep(20,22)
                
                # close it again
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,"//div[@class='key-metric-item track-click-key-metric-item key-metric km-selectable']//div[@class='title']//span[contains(text(),'Page Views')]")))
                    self.browser.find_element(By.XPATH,"//div[@class='key-metric-item track-click-key-metric-item key-metric km-selectable']//div[@class='title']//span[contains(text(),'Page Views')]").click()
                    log.info("fake click")
                except Exception as e:
                    log.error(f"error -> Didn't find the business month svg button -> {e}")
                sleep(12,16)
            else:
                xpath_year = template_function_year(month_range[i],i)
                print(f"xpath_year = {xpath_year}")
                print(f"current_month for testing -> {month_range[i]}")
                print(f"current iteration -> {i}")
                
                # interacting with the month
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,xpath_year)))
                    self.browser.find_element(By.XPATH,xpath_year).click()
                    log.info("Clicked on month button")
                except Exception as e:
                    log.error(f"error -> Selenium wasn't able to find the month -> {e}" )
                sleep(8,16)
                    
        
                # click on business insights pop up
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,business_insights_popup_css_2)))
                    self.browser.find_element(By.CSS_SELECTOR,business_insights_popup_css_2).click()
                    log.info("Clicked on Business insights pop up css 2")
                    flag = 1
                except Exception as e:
                    log.error("error->There was no pop up or selenium failed to interact with the element using css 2")
                sleep(12,16)
                
                # Export data
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,download_data)))
                    self.browser.find_element(By.XPATH,download_data).click()
                    log.info(f"Downloading the data for {month_range[i]}")
                except Exception as e:
                    log.error("error -> Error with exporting data (final download button)")
                sleep(65,65)
                
                # # file writing
                # files_list=os.listdir()
                # for name in files_list:
                #     if "Shopee-ads-Keyword_Placement-level-data" in name:
                #         df_data=pd.read_csv(name,index_col=None)
                #         with io.StringIO() as csv_buffer:
                #             df_data.to_csv(csv_buffer, index=False)
                #             response = s3_client.put_object(
                #                             Bucket=vBucket, Key='strftime("%Y-%m-%d_%Hh_%Mm_%Ss")',Body=csv_buffer.getvalue())
                #             status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

                #             if status == 200:
                #                 print(f"Successful S3 put_object response. Status - {status}")
                #             else:
                #                 print(f"Unsuccessful S3 put_object response. Status - {status}")
                #         os.remove(name)
                

if __name__ == "__main__":
    log.basicConfig(format='%(asctime)s - %(message)s', level=log.INFO)
    # log.basicConfig(level=log.INFO)
    log.info('log at DEBUG level')

    browser = scrapingfunc(AGENT_LIST)
    a = scrape(browser)
    scrape.scrape_func(a)
    log.info("Done scraping the website")
