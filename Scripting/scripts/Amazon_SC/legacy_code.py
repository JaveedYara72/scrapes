import time 
import random
from datetime import datetime,timedelta
import pandas as pd
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def bitwarden(browser):
    
    browser.get("https://vault.bitwarden.com/#/login")
    delay = 30

    # email 
    WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='login_input_email']")))
    browser.find_element(By.XPATH,"//input[@id='login_input_email']").send_keys("")
    time.sleep(5)

    # email continue
    email_continue = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Continue')]")))
    email_continue = browser.find_element(By.XPATH,"//span[contains(text(),'Continue')]").click()
    print("Email Entered")
    time.sleep(5)

    # password 
    pass_ = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"//input[@id='login_input_master-password']")))
    pass_ = browser.find_element(By.XPATH,"//input[@id='login_input_master-password']").send_keys("")
    time.sleep(5)

    # password continue
    pass_continue = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Log in with master password')]")))
    pass_continue = browser.find_element(By.XPATH,"//span[contains(text(),'Log in with master password')]").click()
    print("Password Clicked")
    time.sleep(5)

    # Click on Collections
    collections_ = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,".tw-text-start")))
    collections_ = browser.find_element(By.CSS_SELECTOR,".tw-text-start").click()
    print("Collections button succesfully clicked")
    time.sleep(1)


    # username
    copy_button_1 = browser.find_element(By.XPATH,"//div[@class='input-group-append']//button[@title='Copy username']")
    copy_button_1.click()
    root = tk.Tk()
    username = root.clipboard_get()
    print(f"The user name -> {username}")
    root.overrideredirect(1)
    root.withdraw() 
    root.deiconify()

    # password
    copy_button_2 = browser.find_element(By.XPATH,"//div[@class='input-group-append']//button[@title='Copy password']")
    copy_button_2.click()
    root = tk.Tk()
    password = root.clipboard_get()
    print(f"The password -> {password}")
    root.overrideredirect(1)
    root.withdraw() 
    root.deiconify()

    # timer
    timer_ = browser.find_element(By.XPATH,"//span[@class='totp-countdown']//span[@class='totp-sec']")
    timer_2 = timer_.text
    print(f"Timer on the code -> {timer_2}")
    if(int(timer_2)<=11):
        print("The timer is less than 11, so putting it to sleep for 20 secs")
        time.sleep(20)
    root = tk.Tk()
    root.overrideredirect(1)
    root.withdraw() 
    root.deiconify()

    # code
    copy_button_3 = browser.find_element(By.XPATH,"//button[@title='Copy verification code']")
    copy_button_3.click()
    root = tk.Tk()
    code = root.clipboard_get()
    otp = code
    print(f"The code is -> {code}")
    root.overrideredirect(1)
    root.withdraw() 
    browser.close()

    return otp

def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

full_load = 1

def scscrape_func(browser,code_browser):
    # html_content = sess.get("https://sellercentral.amazon.com/signin", timeout=10).text
    browser.get("https://sellercentral.amazon.com/signin")
    delay = 30

    # Username
    print("Entering the email")
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='ap_email']")))
        browser.find_element(By.XPATH,"//input[@id='ap_email']").send_keys("")
        print("Done with entering email")
    except Exception as e:
        print(e)
    time.sleep(random.randint(2,16))

    # password
    print("Entering Password")
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='ap_password']")))
        browser.find_element(By.XPATH,"//input[@id='ap_password']").send_keys("")
        print("Done Entering Password")
    except Exception as e:
        print(e)
    time.sleep(random.randint(2,16))

    # Submit
    print("Clicking on submit button")
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='signInSubmit']")))
        browser.find_element(By.XPATH,"//input[@id='signInSubmit']").click()
        print("Clicked on Submit button, logging in")
    except Exception as e:
        print(e)
    # time.sleep(random.randint(2,16))
    time.sleep(20)

    # getting the otp from the browser
    otp = bitwarden(code_browser)

    print(f"The OTP from the bitwarden scrape -> {otp}")

    # entering the otp in the amazon sign in box
    # print("Entering the OTP")
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='auth-mfa-otpcode']")))
        browser.find_element(By.XPATH,"//input[@id='auth-mfa-otpcode']").send_keys(otp)
        print("Entered the OTP ... ")
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='auth-signin-button']")))
        browser.find_element(By.XPATH,"//input[@id='auth-signin-button']").click()
        print("Signing in")
    except Exception as e:
        print(e)
    time.sleep(random.randint(2,16))

    # Clicking on United States
    print("Clicking on United States")
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#picker-container > div > div.picker-body > div > div:nth-child(3) > div > div:nth-child(13) > button > div > div")))
        browser.find_element(By.CSS_SELECTOR,"#picker-container > div > div.picker-body > div > div:nth-child(3) > div > div:nth-child(13) > button > div > div").click()
        print("Selected United States")
    except Exception as e:
        print(e)
    time.sleep(random.randint(2,16))
        

    # Business Report Logic
    # Download the Business Report
    print('Navigating to Business Reports')
    browser.get("https://sellercentral.amazon.com/business-reports")

    # Page sales and traffic
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//a//span[contains(text(),'Detail Page Sales and Traffic')]")))
        browser.find_element(By.XPATH,"//a//span[contains(text(),'Detail Page Sales and Traffic')]").click()
        print("Clicked on Detail Page Sales and Traffic")
    except Exception as e:
        print(e)
    time.sleep(6)
    
    # write the logic for date selection
    try:
        if(full_load == 1):
            WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//kat-button[@value='2Y']"))) 
            date = browser.find_element(By.XPATH,"//kat-button[@value='2Y']").click()
        else:
            WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//kat-button[@value='3M']")))
            date = browser.find_element(By.XPATH,"//kat-button[@value='3M']").click()
    except Exception as e:
        print("Error at Date selection in the business reports page")
        print(e)
    time.sleep(6)

    # Downloading the csv
    try:
        print("Downloading the csv")
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//kat-button[@label='Download (.csv)']")))
        browser.find_element(By.XPATH,"//kat-button[@label='Download (.csv)']").click()
    except Exception as e:
        print(e)
    time.sleep(4)


    # navigate to this url -> https://sellercentral.amazon.com/opportunity-explorer
    print("navigating to product explorer")
    try:
        browser.get("https://sellercentral.amazon.com/opportunity-explorer")
    except Exception as e:
        print(e)
    time.sleep(5)

    # Clicking on Find Opportunities by categories
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Find opportunities by categories')]")))
        browser.find_element(By.XPATH,"//span[contains(text(),'Find opportunities by categories')]").click()
        print("Clicked on Find Opportunities by categories")
    except Exception as e:
        print(e)
    time.sleep(3)

    # Clicking on Appliances
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"//li[@role='option']//span[contains(text(),'Appliances')]")))
        browser.find_element(By.XPATH,"//li[@role='option']//span[contains(text(),'Appliances')]").click()
        print("Clicked on Appliances")
    except Exception as e:
        print(e)
    time.sleep(3)

    # Clicking on See Category -> //kat-button[@type ='button' and contains(text(), 'See Category')]
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"//div[@class ='CategorySelect']//*[contains(text(), 'See Category')]")))
        browser.find_element(By.XPATH,"//div[@class ='CategorySelect']//*[contains(text(), 'See Category')]").click()
        print("Clicked on 'See Category' ")
    except Exception as e:
        print(e)
    time.sleep(4)

    # Start Scraping the entire list 
    # loop through the number of pages and scrap everything
    # for every page, load it into a df and put it inside a csv
    try:
        list_ = []
        pagination = browser.find_element(By.XPATH,'//kat-pagination')
        pagination_text = pagination.text
        print(pagination_text)
        
    except Exception as e:
        print(e)

    # pagination algorithm   
    try:
        total_items = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"//kat-pagination[@data-testid='kat-pagination']")))
        total_items = browser.find_element(By.XPATH,"//kat-pagination[@data-testid='kat-pagination']").get_attribute('total-items')
        print(total_items)

        # logic for the number of times the loop has to run
        no_of_pages = int(int(total_items)/25)
        if(int(total_items)%25 < 25):
            if(int(total_items)%25 == 0):
                pass
            else:
                no_of_pages +=1
        print(no_of_pages)
    except Exception as e:
        print(e)

    pagination = browser.find_element(By.XPATH,"//div[@class='kat-col-md-4 center']//kat-pagination[@page='1']").text
    print(pagination)

    try:
        while(no_of_pages != 0):
            for i in range(1,26):
                customer_need = browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[1]//div[@class='termTitle']").text
                
                # appending all the links
                links = []
                link1 = browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[2]//li[1]//kat-link").get_attribute('href')
                link2 = browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[2]//li[2]//kat-link").get_attribute('href')
                link3 = browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[2]//li[3]//kat-link").get_attribute('href')
                links.append(link1)
                links.append(link2)
                links.append(link3)

                search_volume_360 = browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[3]").text
                search_volume_growth_360 = browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[4]").text
                search_volume_90 = browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[5]").text
                search_volume_growth_90 = browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[6]").text
                average_units_sold = browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[7]//div//div//span[1]").text
                average_units_sold += '-'
                average_units_sold += browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[7]//div//div//span[3]").text
                number_of_products = browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[8]").text
                average_price = browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[9]").text
                price_range = browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[10]//div//div//span[1]").text
                price_range += '-'
                price_range = browser.find_element(By.XPATH,f"//table[@aria-labelledby='katal-id-4']//tbody//tr[{i}]//td[10]//div//div//span[3]").text

                print(customer_need,link1,link2,link3,search_volume_360,search_volume_growth_360,search_volume_90,search_volume_growth_90,average_units_sold,number_of_products,average_price,price_range)
                data_list=[customer_need,links,search_volume_360,search_volume_growth_360,search_volume_90,search_volume_growth_90,average_units_sold,number_of_products,average_price,price_range]
                df = pd.DataFrame(columns=["customer_need","links","search_volume_360","search_volume_growth_360","search_volume_90","search_volume_growth_90","average_units_sold","number_of_products","average_price","price_range"])
                df.loc[len(df)] = data_list
                df.to_csv('scrape_data_1.csv',header=None, mode='a')

                time.sleep(5)

            # interacting with the next button
            try:
                pagination = browser.find_element(By.XPATH,"//div[@class='kat-col-md-4 center']//kat-pagination[@page='1']")
                print(pagination.get_attribute('innerHTML'))
            except Exception as e:
                print("Not able to navigate through the next pages")
            
            try:
                pagination = browser.find_element(By.XPATH,"//*[@id='root']/div/main/div/div[2]/div[2]/div[2]/kat-pagination//nav/ul/li[2]/span").click()
                print('tejas xpath worked')
            except Exception as e:
                print("tejas xpath didnt work")

            try:
                pagination = browser.find_element(By.XPATH,"//*[@id='root']/div/main/div/div[2]/div[2]/div[2]/kat-pagination//nav/span[2]/kat-icon//i").click()
                print('second xpath worked')
            except Exception as e:
                print("second xpath didnt work")
                
            try:
                pagination = browser.find_element(By.XPATH,'/html/body/div/div[2]/div/div/main/div/div[2]/div[2]/div[2]/kat-pagination//nav/span[2]')
                print("chrome xpath worked.")
            except:
                print("didnt work")
                
            
            no_of_pages -= 1
    except Exception as e:
        print("Couldn't scrape the table")
        print(e)


if __name__ == "__main__":
    
    # Initialising the browser
    options = Options()
    # print(f"Agent for this instance -> {Random_Agent}")
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    # options.set_preference("general.useragent.override",Random_Agent )

    browser = webdriver.Firefox(options=options)
    code_browser = webdriver.Firefox(options=options)

    scscrape_func(browser,code_browser)

