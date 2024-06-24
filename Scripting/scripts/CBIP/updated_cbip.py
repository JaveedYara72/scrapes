import os
import sys
import json 
import time 
import platform
import pandas as pd
from selenium import webdriver
from datetime import date, timedelta
from selenium.webdriver.common.by import By
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
from webdriver_manager.firefox import GeckoDriverManager
import io
import boto3
import re

AWS_ACCESS_KEY_ID = sys.argv[1]
AWS_SECRET_ACCESS_KEY = sys.argv[2]

link_warehouse = "http://fba.anchanto.com/login"
directoryy = os.getcwd()

vBucket = 'una-brands-ops'
s3_client = boto3.client('s3',
        aws_access_key_id= AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
s3_resource = boto3.resource('s3',
        aws_access_key_id= AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
VInputRawPrifix = 'data/prod/landing_raw/inventory_scrapes/<brand>/'

cred_username = ["yuese.teow@marvable.com"]
cred_pass = [ "Marvable@123"]
cred_email = ["sambhav.bhandari@una-brands.com"]
cred_file_name = ["Marvable"]

# UTIL
ytd_int = (date.today() - timedelta(days=1)).strftime('%-d')

def marvable(link_warehouse,cred_username,cred_pass,cred_file_name,cred_email):
    delay = 30

    # launching the browser
    browser.get(link_warehouse)

    print(f"Scrapping with -> {cred_username}")

    # Login
    browser.find_element(By.ID, "user_email").send_keys("{}".format(cred_username))
    time.sleep(3)
    browser.find_element(By.ID, "user_password").send_keys("{}".format(cred_pass))
    time.sleep(4)
    browser.find_element(By.NAME, "commit").click()
    time.sleep(5)

    # GO TO "Generate Reports"
    browser.find_element(By.LINK_TEXT, "Reports").click()
    time.sleep(3)
    browser.find_element(By.LINK_TEXT, "Generate Reports").click()
    time.sleep(4)

    # Select report to download
    dropdown = browser.find_element(By.ID, "report_type")
    time.sleep(5)
    dropdown.find_element(By.XPATH, "//option[. = 'Inventory Report']").click()
    time.sleep(4)
    browser.find_element(By.ID, "emails").click()
    time.sleep(3)
    browser.find_element(By.ID, "emails").send_keys("{}".format(cred_email))
    time.sleep(5)
    browser.find_element(By.ID, "datepicker3").click()
    time.sleep(3)
    browser.find_element(By.LINK_TEXT, ytd_int).click()
    time.sleep(4)
    browser.find_element(By.ID, "admin_report").click()
    time.sleep(20)

    # Download that file to local system
    browser.find_element(By.LINK_TEXT, "Generated Reports").click()
    time.sleep(4)
    browser.find_element(By.CSS_SELECTOR,"#admin-report-list > tbody > tr:nth-child(1) > td:nth-child(8) > a").click()
    time.sleep(5)
    
    # read the existing file into a df
    print("Reading the Excel file into a dataframe")
    # df_data=read_file(download_path)
    files_list=os.listdir()
    import datetime
    vLatestUpdatedDateTime = datetime.datetime.now()
    vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
    for name in files_list:
        if "Adhoc_WarehouseStorageWiseReport" in name:
            df_data=pd.read_csv(name,index_col=None)
            with io.StringIO() as csv_buffer:
                df_data.to_csv(csv_buffer, index=False)
                response = s3_client.put_object(
                                Bucket=vBucket, Key='{}{}/{}/WarehouseStorageWiseReport-{}.csv'.format(VInputRawPrifix,cred_file_name.split("_")[1],cred_file_name.split("_")[0],vLatestUpdatedDateTimeFile),Body=csv_buffer.getvalue())
                status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

                if status == 200:
                    print(f"Successful S3 put_object response. Status - {status}")
                else:
                    print(f"Unsuccessful S3 put_object response. Status - {status}")
            os.remove(name)

    print(f"Report from Website downloaded with the email -> {cred_email}")
    print("------------------------------------")

    # Logout
    browser.find_element(By.LINK_TEXT, f"Welcome, {cred_username}").click()
    time.sleep(2)
    browser.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(3)
    browser.close()



if __name__ == "__main__":
    download_path = directoryy
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", directoryy)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.headless = True
    options.binary_location = r'/usr/bin/firefox'
    # options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    browser = webdriver.Firefox(options=options,executable_path=GeckoDriverManager().install())
    try:
        marvable(link_warehouse, cred_username[0], cred_pass[0],cred_file_name[0],cred_email[0])
    except:
        print("couldnt scrape data for-->> ",cred_file_name[0])