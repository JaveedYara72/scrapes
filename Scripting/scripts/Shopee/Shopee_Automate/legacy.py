import io
import re
import os
import sys
import json 
import time 
import boto3
import datetime
import pandas as pd
from __init__ import *
import logging as log
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.scrapingFunc import * #random_func,scrapingfunc
from common.variables import *

# Incase the css selector of year navigation breaks, use this code
try:
    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, year_navigator_svg_css_2)))
    self.browser.find_element(By.CSS_SELECTOR,year_navigator_svg_css_2).click()
    log.info("Went back to the previous year using css2")
except Exception as e:
    log.error(f'exception at previous year button css2- {e}')
sleep(20,20)

                
# Export data -> If the xpath for the download data button stops working, try this.
try:
    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,download_data_2)))
    self.browser.find_element(By.XPATH,download_data_2).click()
    log.info("Clicked on export data button, it worked the second one")
except Exception as e:
    log.error("error -> Error with exporting data")
sleep(6,16) 


# RIP - My best code, Your legacy will live on when the api will get deprecated.
import io
import re
import os
import sys
import json 
import time 
import boto3
import datetime
import pandas as pd
from __init__ import *
import logging as log
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.scrapingFunc import * #random_func,scrapingfunc
from common.variables import *

def unique(list1):
	# insert the list to the set
	list_set = set(list1)
	# convert the set to the list
	unique_list = (list(list_set))
	return unique_list

def day_of_week(date_str):
    date_obj = datetime.datetime.strptime(date_str, '%Y %m %d')
    day = date_obj.day
    month = date_obj.month
    year = date_obj.year
    if month < 3:
        month += 12
        year -= 1
    century = year // 100
    year_of_century = year % 100
    day_num = (day + ((13 * (month + 1)) // 5) + year_of_century +
               (year_of_century // 4) + (century // 4) - (2 * century)) % 7-1
    day_names = ['Sunday', 'Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    return day_names[day_num]

def template_function(week_range, week_day,local_month_end):
    # there are gonna be edge cases to every day as well, 1 and 31 can be on the weekdays as well right.
    if(week_day == 'Sunday'):
        if(week_range == '1'):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-start month-start']//span[@class='shopee-date-table__cell-inner normal line-start month-start' and text()='{week_range}']"
        elif(week_range == local_month_end):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-start line-end month-end']//span[@class='shopee-date-table__cell-inner normal line-start line-end month-end' and text()='{week_range}']"
        else:
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-start']//span[@class='shopee-date-table__cell-inner normal line-start' and text()='{week_range}']"
    elif(week_day == 'Saturday'):
        if(week_range == local_month_end):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-end month-end']//span[@class='shopee-date-table__cell-inner normal line-end month-end' and text()='{week_range}']"
        elif(week_range == '1'):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-start line-end month-start']//span[@class='shopee-date-table__cell-inner normal line-start line-end month-start' and text()='{week_range}']"
        else:
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-end']//span[@class='shopee-date-table__cell-inner normal line-end' and text()='{week_range}']"
    elif(week_day == 'Friday'):
        if(week_range == '1'):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-start month-start']//span[@class='shopee-date-table__cell-inner normal line-start month-start' and text()='{week_range}']"
        elif(week_range == local_month_end):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-end month-end']//span[@class='shopee-date-table__cell-inner normal line-end month-end' and text()='{week_range}']"
        else:
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal']//span[@class='shopee-date-table__cell-inner normal' and text()='{week_range}']"
    elif(week_day == 'Thursday'):
        if(week_range == '1'):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-start month-start']//span[@class='shopee-date-table__cell-inner normal line-start month-start' and text()='{week_range}']"
        elif(week_range == local_month_end):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-end month-end']//span[@class='shopee-date-table__cell-inner normal line-end month-end' and text()='{week_range}']"
        else:
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal']//span[@class='shopee-date-table__cell-inner normal' and text()='{week_range}']"
    elif(week_day == 'Wednesday'):
        if(week_range == '1'):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-start month-start']//span[@class='shopee-date-table__cell-inner normal line-start month-start' and text()='{week_range}']"
        elif(week_range == local_month_end):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-end month-end']//span[@class='shopee-date-table__cell-inner normal line-end month-end' and text()='{week_range}']"
        else:
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal']//span[@class='shopee-date-table__cell-inner normal' and text()='{week_range}']"
    elif(week_day == 'Tuesday'):
        if(week_range == '1'):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-start month-start']//span[@class='shopee-date-table__cell-inner normal line-start month-start' and text()='{week_range}']"
        elif(week_range == local_month_end):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-end month-end']//span[@class='shopee-date-table__cell-inner normal line-end month-end' and text()='{week_range}']"
        else:
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal']//span[@class='shopee-date-table__cell-inner normal' and text()='{week_range}']"
    elif(week_day == 'Monday'):
        if(week_range == '1'):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-start month-start']//span[@class='shopee-date-table__cell-inner normal line-start month-start' and text()='{week_range}']"
        elif(week_range == local_month_end):
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal line-end month-end']//span[@class='shopee-date-table__cell-inner normal line-end month-end' and text()='{week_range}']"
        else:
            xpath = f"//div[@class='shopee-date-table__rows']//div[@class='shopee-date-table__cell normal']//span[@class='shopee-date-table__cell-inner normal' and text()='{week_range}']"
    return xpath

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
        
        # Pop up - Choose Language button
        # try:
        #     WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, languagebutton)))
        #     self.browser.find_element(By.XPATH,languagebutton).click()
        #     log.info("Chosen English Language")
        # except Exception as e:
        #     log.error(f'exception at language pop up button - {e}')
        # sleep(12,16)


        # # username
        # try:
        #     WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, username)))
        #     self.browser.find_element(By.XPATH,username).send_keys("tsm.admin+my@una-brands.com")
        #     log.info("Entered Username")
        # except Exception as e:
        #     log.error(f'exception at username button - {e}')
        # sleep(10,16)

        # # password
        # try:
        #     WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, password)))
        #     self.browser.find_element(By.XPATH,password).send_keys("JFEXoC52Msnjz6")
        #     log.info("Entered Password")
        # except Exception as e:
        #     log.error(f'exception at password button - {e}')
        # sleep(8,16)
        
        # # log in button
        # try:
        #     WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, login)))
        #     self.browser.find_element(By.XPATH,login).click()
        #     log.info("Clicked on Log In Button")
        # except Exception as e:
        #     log.error(f'exception at log in button - {e}')
        # sleep(12,16)
        
        # # Click on Shopee Ads button
        # try:
        #     WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, Shopee_ads)))
        #     self.browser.find_element(By.XPATH,Shopee_ads).click()
        #     log.info("Clicked on Shopee Ads Button")
        # except Exception as e:
        #     log.error(f'exception at shopee ads button - {e}')
        # sleep(10,16)
        
        # # click on shopee ads pop up button
        # try:
        #     WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,Shopee_ads_popup)))
        #     self.browser.find_element(By.XPATH,Shopee_ads_popup).click()
        #     log.info("Clicked on Shopee ads pop up button")
        # except Exception as e:
        #     log.error(f"exception at shopee adspop up button - {e}")
        # sleep(8,16)
        
        # date level logic 
        # figure out the day from the date range you select yourself.
        week_range = []
        week_days = []
        month_range = []
        months = {'01':'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
        today = datetime.datetime.today()
        max_days = 11

        for i in range(1,max_days):
            week_ago = today - datetime.timedelta(days=i)
            dayofweek = day_of_week(week_ago.strftime("%Y %m %d"))
            
            # minute logic handling for decimal changes in date
            if((week_ago.strftime("%d"))=='01'):
                week_range.append('1')
            elif((week_ago.strftime("%d"))=='02'):
                week_range.append('2')
            elif((week_ago.strftime("%d"))=='03'):
                week_range.append('3')
            elif((week_ago.strftime("%d"))=='04'):
                week_range.append('4')
            elif((week_ago.strftime("%d"))=='05'):
                week_range.append('5')
            elif((week_ago.strftime("%d"))=='06'):
                week_range.append('6')
            elif((week_ago.strftime("%d"))=='07'):
                week_range.append('7')
            elif((week_ago.strftime("%d"))=='08'):
                week_range.append('8')
            elif((week_ago.strftime("%d"))=='09'):
                week_range.append('9')
            else:
                week_range.append(week_ago.strftime("%d"))
                
            
            month_range.append(week_ago.strftime("%m"))
                
            week_days.append(dayofweek)
            
        print(week_range)
        print(week_ago)
        print(week_days)
        
        # getting the unique months in our iteration in the array month_range.
        months_unique = unique(month_range)
        month_range.clear()
        for month in months_unique:
            month_range.append(months[month])
        
        print(month_range)
        exit()
        
        for i in range(0,len(week_range)):
            
            local_month_end = ''
            
            # click on date picker button
            try:
                WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,calendar)))
                self.browser.find_element(By.XPATH,calendar).click()
                log.info("Clicked on calendar button")
            except Exception as e:
                log.error(f"exception at calendar date picking button - {e}")
            sleep(5,6)
            
            if(i == 0):
                xpath = template_function(week_range[i],week_days[i],local_month_end)
                print(f"Xpath of {week_range[i]},{week_days[i]},{local_month_end} ->")
                print(xpath)
                # picking the date
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,xpath)))
                    self.browser.find_element(By.XPATH,xpath).click()
                    log.info(f"clicked on the date once")
                    
                    if "normal line" in xpath:
                        s1 = "normal line"
                        s2 = "normal selected range-start line"
                        xpath = xpath.replace(s1, s2)
                    else:
                        s1 = "normal"
                        s2 = "normal selected range-start"
                        xpath = xpath.replace(s1, s2)
                    
                    self.browser.find_element(By.XPATH,xpath).click()
                    log.info(f"Clicked on the date twice")
                    log.info(f"Clicked on {week_days[i]} button")
                except Exception as e:
                    log.error(f"exception at {week_days[i]} picking button - {e}")
            else:
                if(int(week_range[i])>int(week_range[i-1])):
                    # write the code for month change
                    try:
                        WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,month_navigator_svg_css)))
                        self.browser.find_element(By.CSS_SELECTOR,month_navigator_svg_css).click()
                        log.info("Clicked on month_navigator svg css selector button")
                    except Exception as e:
                        log.error(f"exception at month_navigator svg css selector picking button - {e}")
                    sleep(5,5)            
                        
                    local_month_end = week_range[i]
                    print(local_month_end)
                    xpath = template_function(week_range[i],week_days[i],local_month_end)
                    print(xpath)
                    print(f"Xpath of {week_range[i]},{week_days[i]}, {local_month_end} ->")
                    print(xpath)
                    
                    # picking the date
                    try:
                        WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,xpath)))
                        self.browser.find_element(By.XPATH,xpath).click()
                        log.info(f"clicked on the date once")
                        
                        if "normal line" in xpath:
                            s1 = "normal line"
                            s2 = "normal selected range-start line"
                            xpath = xpath.replace(s1, s2)
                        else:
                            s1 = "normal"
                            s2 = "normal selected range-start"
                            xpath = xpath.replace(s1, s2)
                            
                        self.browser.find_element(By.XPATH,xpath).click()
                        log.info(f"Clicked on the date twice")
                        log.info(f"Clicked on {local_month_end} button")
                    except Exception as e:
                        log.error(f"exception at {local_month_end} picking button - {e}")
                else:
                    xpath = template_function(week_range[i],week_days[i],local_month_end)
                    print(f"Xpath of {week_range[i]},{week_days[i]},{local_month_end} ->")
                    print(xpath)
                    
                    # picking the date
                    try:
                        WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,xpath)))
                        self.browser.find_element(By.XPATH,xpath).click()
                        log.info(f"clicked on the date once")
                        
                        if "normal line" in xpath:
                            s1 = "normal line"
                            s2 = "normal selected range-start line"
                            xpath = xpath.replace(s1, s2)
                        else:
                            s1 = "normal"
                            s2 = "normal selected range-start"
                            xpath = xpath.replace(s1, s2)
                        
                        self.browser.find_element(By.XPATH,xpath).click()
                        log.info(f"Clicked on the date twice")
                        log.info(f"Clicked on {week_days[i]} button")
                    except Exception as e:
                        log.error(f"exception at {week_days[i]} picking button - {e}")
            
            # click on export data button
            try:
                WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, export_data)))
                self.browser.find_element(By.XPATH,export_data).click()
                log.info("clicked on export data dropdown button")
            except Exception as e:
                log.error(f'exception at export data dropdown button')
            sleep(12,16)
        
            # keyword/placement level data button
            try:
                WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, keyword)))
                self.browser.find_element(By.XPATH,keyword).click()
                log.info("clicked on keyword level data button")
            except Exception as e:
                log.error(f'exception at keyword level data button')
            sleep(12,16)
                
            # keyword pop up confirm button
            try:
                WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH, keyword_popup)))
                self.browser.find_element(By.XPATH,keyword_popup).click()
                log.info("clicked on confirm keyword/placement level data pop up")
            except Exception as e:
                log.error(f'exception at keyword level pop up button')
            sleep(14,16)
            
            # sleep for a minute, so that the website could generate the file
            log.info("sleeping for 45 seconds")
            sleep(40,45)
            
            # download file
            try:
                WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,download)))
                self.browser.find_element(By.XPATH,download).click()
                log.info("Clicked on download button")
            except Exception as e:
                log.error(f"error -> Downloading the file -> {e}")
            sleep(20,24)
    
        log.info("Done with generating shopee ads data")
        sleep(4,8)
        
        self.browser.get("https://seller.shopee.com.my/datacenter/dashboard")
        
        # flags important for scraping
        flag = 0
        business_month_flag = 0
        
        for i in range(0,len(month_range)):
            
            log.info(f"scraping the report for {month_range[i]}")
            # business month svg button
            try:
                WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,business_month_button_svg)))
                self.browser.find_element(By.XPATH,business_month_button_svg).click()
                log.info("Clicked on business month svg button")
            except Exception as e:
                log.error(f"error -> Didn't find the business month button -> {e}")
                
            # business month button
            if(business_month_flag == 0):
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,business_month_button_month)))
                    self.browser.find_element(By.XPATH,business_month_button_month).click()
                    log.info("Clicked on business month button")
                    business_month_flag = 1
                except Exception as e:
                    log.error(f"error -> Didn't find the business month button -> {e}")
                sleep(12,16)
            
            # chose the month -> currently, i have added the current class month, write an if else here for the months that are not current. Just remove that class from xpath.
            if(month_range[i] == 'Jan'):
                xpath_year = template_function_year(month_range[i],i)
                print(f"xpath_year = {xpath_year}")
                print(f"current_month for testing -> {month_range[i]}")
                print(f"current iteration -> {i}")
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,xpath_year)))
                    self.browser.find_element(By.XPATH,xpath_year).click()
                    log.info("Clicked on month button")
                except Exception as e:
                    log.error(f"error -> Selenium wasn't able to find the month -> {e}" )
                sleep(14,16)
                    
                # Business insights pop up button
                if(flag == 0):
                    try:
                        WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,business_insights_popup)))
                        self.browser.find_element(By.XPATH,business_insights_popup).click()
                        log.info("Clicked on Business insights pop up")
                        flag = 1
                    except Exception as e:
                        log.error("error->There was no pop up or selenium failed to interact with the element")
                    sleep(16,16)
                    
                    try:
                        WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,business_insights_popup_css)))
                        self.browser.find_element(By.CSS_SELECTOR,business_insights_popup_css).click()
                        log.info("Clicked on Business insights pop up css")
                        flag = 1
                    except Exception as e:
                        log.error("error->There was no pop up or selenium failed to interact with the element using css")
                    sleep(12,16)
                    
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
                    log.error("error -> Error with exporting data")
                sleep(6,16)
                
                # open the calendar again inorder to navigate it to the previous year
                # business month svg button
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,business_month_button_svg)))
                    self.browser.find_element(By.XPATH,business_month_button_svg).click()
                    log.info("Clicked on business month svg button")
                except Exception as e:
                    log.error(f"error -> Didn't find the business month svg button -> {e}")
                sleep(12,16)
                    
                if(business_month_flag == 0):
                    try:
                        WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,business_month_button_month)))
                        self.browser.find_element(By.XPATH,business_month_button_month).click()
                        log.info("Clicked on business month button")
                        business_month_flag = 1
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
            else:
                xpath_year = template_function_year(month_range[i],i)
                print(f"xpath_year = {xpath_year}")
                print(f"current_month for testing -> {month_range[i]}")
                print(f"current iteration -> {i}")
                
                try:
                    WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,xpath_year)))
                    self.browser.find_element(By.XPATH,xpath_year).click()
                    log.info("Clicked on month button")
                except Exception as e:
                    log.error(f"error -> Selenium wasn't able to find the month -> {e}" )
                sleep(8,16)
                    
                if(flag == 0):
                    try:
                        WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.XPATH,business_insights_popup)))
                        self.browser.find_element(By.XPATH,business_insights_popup).click()
                        log.info("Clicked on Business insights pop up")
                        flag = 1
                    except Exception as e:
                        log.error("error->There was no pop up or selenium failed to interact with the element")
                    sleep(16,16)
                    
                    try:
                        WebDriverWait(self.browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,business_insights_popup_css)))
                        self.browser.find_element(By.CSS_SELECTOR,business_insights_popup_css).click()
                        log.info("Clicked on Business insights pop up css")
                        flag = 1
                    except Exception as e:
                        log.error("error->There was no pop up or selenium failed to interact with the element using css")
                    sleep(12,16)
                    
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
                sleep(6,16)

if __name__ == "__main__":
    log.basicConfig(format='%(asctime)s - %(message)s', level=log.INFO)
    # log.basicConfig(level=log.INFO)
    log.info('log at DEBUG level')

    browser = scrapingfunc(AGENT_LIST)
    a = scrape(browser)
    scrape.scrape_func(a)
    log.info("Done scraping the website")
