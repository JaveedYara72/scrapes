import time 
import random
import pandas as pd
from datetime import datetime,timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from variables import * 

def date_generator():
    # Get today's date
    today = datetime.today()

    # Calculate the first day of the current month
    first_day_current_month = today.replace(day=1)

    # Subtract one day to get the last day of the previous month
    last_day_previous_month = first_day_current_month - timedelta(days=1)

    # Get the previous month's 1st date and last date
    previous_month_first_date = last_day_previous_month.replace(day=1)
    previous_month_last_date = last_day_previous_month

    # Format the dates as dd/mm/yyyy strings
    previous_month_first_date_str = previous_month_first_date.strftime('%m/%d/%Y')
    previous_month_last_date_str = previous_month_last_date.strftime('%m/%d/%Y')
    
    return previous_month_first_date_str,previous_month_last_date_str

def month_year_generator():
    # Get today's date
    today = datetime.today()

    # Calculate the first day of the current month
    first_day_current_month = today.replace(day=1)

    # Subtract one day to get the last day of the previous month
    last_day_previous_month = first_day_current_month - timedelta(days=1)

    # Get the previous month
    previous_month = last_day_previous_month.strftime('%B')
    previous_year = last_day_previous_month.strftime('%Y')
    
    return previous_month,previous_year

def login(browser):
    # html_content = sess.get("https://sellercentral.amazon.com/signin", timeout=10).text
    browser.get("https://sellercentral.amazon.com/signin")
    delay = 30

    # Username
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='ap_email']")))
        browser.find_element(By.XPATH,"//input[@id='ap_email']").send_keys("jujuamazonusa@juju.com.au")
        print("Entered email")
    except Exception as e:
        print(e)
    time.sleep(random.randint(2,16))

    # password
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='ap_password']")))
        browser.find_element(By.XPATH,"//input[@id='ap_password']").send_keys("NCLqAd8uxy$dgH")
        print("Entered Password")
    except Exception as e:
        print(e)
    time.sleep(random.randint(2,16))

    # Submit
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='signInSubmit']")))
        browser.find_element(By.XPATH,"//input[@id='signInSubmit']").click()
        print("Clicked on Submit button, logging in")
    except Exception as e:
        print(e)
    # time.sleep(random.randint(2,16))
    time.sleep(60)
    
    # Enter OTP from authenticator
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='a-radio auth-TOTP']//input")))
        browser.find_element(By.XPATH,"//div[@class='a-radio auth-TOTP']//input").click()
        print("Clicked on Enter OTP from Authenticator option")
    except Exception as e:
        print(e)
    
    # Send otp
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='auth-send-code']")))
        browser.find_element(By.XPATH,"//input[@id='auth-send-code']").click()
        print("Clicked on Send OTP")
    except Exception as e:
        print(e)
    
    # add otp logic here

    # Clicking on United States and Select Account
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#picker-container > div > div.picker-body > div > div:nth-child(3) > div > div:nth-child(13) > button > div > div")))
        browser.find_element(By.CSS_SELECTOR,"#picker-container > div > div.picker-body > div > div:nth-child(3) > div > div:nth-child(13) > button > div > div").click()
        print("Selected United States")
    except Exception as e:
        print(e)
    time.sleep(random.randint(2,16))
    
    # Clicking on the Select account
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#picker-container > div > div.picker-footer > div > button")))      
        browser.find_element(By.CSS_SELECTOR,"#picker-container > div > div.picker-footer > div > button").click()
        print("Clicked on Select Account")
    except Exception as e:
        print(e)
    time.sleep(random.randint(2,16))

def opportunity_explore(browser):
    delay = 30
    
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

def expand_shadow_element(browser,element):
    shadow_root = browser.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root

def payments_business_report(browser):
    full_load = 1
    
    delay = 30
    
    # Payments Report Logic
    print('Navigating to Payment Reports')
    browser.get("https://sellercentral.amazon.com/payments/reports-repository/")
    time.sleep(30)
    
    previous_month_first,previous_month_last = date_generator()
    
    # skip button
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"//button[contains(text(),'Skip')]")))      
        browser.find_element(By.XPATH,"//button[contains(text(),'Skip')]").click()
        print("Clicked on skip button")
    except Exception as e:
        print("Unable to click on skip button")
        
    # close button
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,".react-joyride__tooltip > button:nth-child(3) > svg:nth-child(1)")))      
        browser.find_element(By.CSS_SELECTOR,".react-joyride__tooltip > button:nth-child(3) > svg:nth-child(1)").click()
        print("Clicked on close button")
    except Exception as e:
        pass    
    
    # sleep
    time.sleep(10)
    
    # select first date
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,firstdate_box_wrapper_ul)))      
        first_element = browser.find_element(By.XPATH,firstdate_box_wrapper_ul)
        first_element_root = first_element.shadow_root
        second_element_root = first_element_root.find_element(By.CSS_SELECTOR,'kat-input')
        shadow_root2 = expand_shadow_element(browser,second_element_root)
        third_element_root_input = shadow_root2.find_element(By.CSS_SELECTOR,'input')
        third_element_root_input.send_keys(previous_month_first)
        print(f'entered month start date -> {previous_month_first}')
    except Exception as e:
        print("Exception occurred:", str(e))
    time.sleep(random.randint(2,16))
    
    # select last date
    try:
        WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,lastdate_box_wrapper_ul)))      
        first_element = browser.find_element(By.XPATH,lastdate_box_wrapper_ul)
        first_element_root = first_element.shadow_root
        second_element_root = first_element_root.find_element(By.CSS_SELECTOR,'kat-input')
        shadow_root2 = expand_shadow_element(browser,second_element_root)
        third_element_root_input = shadow_root2.find_element(By.CSS_SELECTOR,'input')        
        third_element_root_input.send_keys(previous_month_last)
        print(f'entered month end date -> {previous_month_last}')
    except Exception as e:
        print("Exception occurred:", str(e))
    time.sleep(random.randint(2,16))
    
    # Generate report
    try:
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='button-container filters-container-innerbox']//kat-button[@id='filter-generate-button']")))
        parent_element = browser.find_element(By.XPATH, "//div[@class='button-container filters-container-innerbox']//kat-button[@id='filter-generate-button']")
        parent_element.click()
        print("Clicked on Generate report")
    except Exception as e:
        print(e)
    time.sleep(random.randint(2,16))
    
    
    # sleep to generate the report
    time.sleep(120)
    browser.refresh()
    time.sleep(10)
    
    # click on refresh the report
    try:
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//kat-button[@label='Refresh']")))
        browser.find_element(By.XPATH, "//kat-button[@label='Refresh']").click()
        print("Clicked on Refresh")
    except Exception as e:
        pass
    time.sleep(5)
        
    # click on download the report
    try:
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//kat-button[@label='Download CSV']")))
        buttons = browser.find_elements(By.XPATH, "//kat-button[@label='Download CSV']")
        if buttons:
            buttons[0].click()
    except Exception as e:
        print(e)
    
    # Business Report Logic
    # Download the Business Report
    print('Navigating to Business Reports')
    try:
        browser.get("https://sellercentral.amazon.com/business-reports")
    except Exception as e:
        print(e)
    time.sleep(5)

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
    