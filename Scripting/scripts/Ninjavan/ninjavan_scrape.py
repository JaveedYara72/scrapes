import os
import sys
import json 
import time 
import platform
import pandas as pd
from selenium import webdriver
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

link_warehouse = "https://wms.anchanto.com/login"
directoryy = os.getcwd()

vBucket = 'una-brands-ops'
s3_client = boto3.client('s3',
        aws_access_key_id= AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
s3_resource = boto3.resource('s3',
        aws_access_key_id= AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
VInputRawPrifix = 'data/prod/landing_raw/inventory_scrapes/ninjavan/'


cred_email = ["lester.teng+sg@una-brands.com","lester.teng@una-brands.com","jujuadmin@juju.com.au", "tsm.admin+indo@una-brands.com","tsm.admin+ph@una-brands.com"]
cred_pass = [ "7uKa2RGaB!trDmr","7uKa2RGaB!trDmr","E4JaJ8wGB9o@WR", "85vYkd%La&iBJ%", "Nhv9@4i3Xn$y*V"]
cred_file_name = ["TSM_SG","TSM_MY","JUJU_MY","TSM_ID","TSM_PH"]

def get_scrape_data(link_warehouse,cred_email,cred_pass,cred_file_name):

    delay = 30

    # launching the browser
    browser.get(link_warehouse)

    print(f"Scrapping with -> {cred_email}")

    # login
    # email
    email_ = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-login/div/div/div[2]/div[2]/div/div/form/div[3]/input")))
    email_ = browser.find_element(By.XPATH,"/html/body/app-root/app-login/div/div/div[2]/div[2]/div/div/form/div[3]/input").send_keys("{}".format(cred_email))
    time.sleep(5)

    # password
    pass_ = browser.find_element(By.XPATH,"/html/body/app-root/app-login/div/div/div[2]/div[2]/div/div/form/div[4]/input").send_keys("{}".format(cred_pass))
    time.sleep(5)

    # click on the submit button
    submit_ = browser.find_element(By.XPATH,"/html/body/app-root/app-login/div/div/div[2]/div[2]/div/div/form/div[6]/button").click()
    time.sleep(5)


    # click on inventory
    inventory_ = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"/html/body/app-root/app-customers/div/app-menu/div/div/div[2]/ul/li[4]/a/i")))
    inventory_ = browser.find_element(By.XPATH,"/html/body/app-root/app-customers/div/app-menu/div/div/div[2]/ul/li[4]/a/i" ).click()
    time.sleep(5)

    # click on download button
    download_1_ = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"/html/body/app-root/app-inventory/div/app-product/div/div[2]/app-all/div/div/app-filter/div/div[1]/div/div[2]/div/app-inventory-common-actions/div/div[1]/button")))
    download_1_ = browser.find_element(By.XPATH,"/html/body/app-root/app-inventory/div/app-product/div/div[2]/app-all/div/div/app-filter/div/div[1]/div/div[2]/div/app-inventory-common-actions/div/div[1]/button").click()
    time.sleep(5)

    # click on close pop up after the first download button
    pop_up_ = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"/html/body/ngb-modal-window/div/div/div/div[1]/button/span")))
    pop_up_ = browser.find_element(By.XPATH,"/html/body/ngb-modal-window/div/div/div/div[1]/button/span").click()
    time.sleep(5)

    # redirecting to reports page, because reports button was n ot being found by selenium
    browser.get("https://wms.anchanto.com/reports/report-management/all")
    print("On the reports page")

    # Create reports button
    create_report = WebDriverWait(browser,delay).until(EC.presence_of_element_located,((By.XPATH,"/html/body/app-root/app-reports/div/app-grids-report/div/div[2]/app-all-report/div/div/app-filter/div/div[1]/div/div[2]/div/app-reports-common-actions/div/div/button")))
    print("found create_report button")
    create_report = browser.find_element(By.XPATH,"/html/body/app-root/app-reports/div/app-grids-report/div/div[2]/app-all-report/div/div/app-filter/div/div[1]/div/div[2]/div/app-reports-common-actions/div/div/button").click()
    time.sleep(5)

    # select an option from dropdown
    dropdown_1 = WebDriverWait(browser,delay).until(EC.presence_of_element_located,((By.ID,"report_type_select")))
    dropdown_1 = browser.find_element(By.ID,"report_type_select").click()
    print("Drop down selected")
    time.sleep(5)

    # Warehouse Report 
    warehouse_1 = WebDriverWait(browser,delay).until(EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/ng-dropdown-panel[1]/div[1]/div[2]/div[6]/span[1]")))
    warehouse_1 = browser.find_element(By.XPATH,"/html[1]/body[1]/ng-dropdown-panel[1]/div[1]/div[2]/div[6]/span[1]")
    warehouse_1.click()
    print("Warehouse selected")
    time.sleep(5)

    # warehouse brand dropdown select
    dropdown_2 = WebDriverWait(browser,delay).until(EC.presence_of_element_located,((By.ID,"company_select")))
    dropdown_2 = browser.find_element(By.ID,"company_select").click()
    print("Warehouse brand Drop down selected")
    time.sleep(5)

    # warehouse brand select
    brand_ = WebDriverWait(browser,delay).until(EC.visibility_of_element_located((By.XPATH, "/html/body/ng-dropdown-panel/div/div[2]/div/span")))
    brand_.click()
    print("Warehouse Brand selected")
    time.sleep(5)

    # Select all check box 
    select_all = WebDriverWait(browser,delay).until(EC.visibility_of_element_located((By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[3]/div[1]/div/label/span")))
    select_all = browser.find_element(By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[3]/div[1]/div/label/span").click()
    print("Select all option selected")
    time.sleep(5)

    # Occurence dropdown
    occurence_ = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[4]/div[1]/ng-select/div/span")))
    occurence_ = browser.find_element(By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[4]/div[1]/ng-select/div/span").click()
    print("Occurence dropdown selected")
    time.sleep(5)

    # adhoc option select
    adhoc_ = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"/html/body/ng-dropdown-panel/div/div[2]/div[4]/span")))
    adhoc_ = browser.find_element(By.XPATH,"/html/body/ng-dropdown-panel/div/div[2]/div[4]/span").click()
    print("Adhoc option selected")
    time.sleep(5)

    # Date start select
    date_click = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[4]/div[2]/div[1]/input")))
    date_click = browser.find_element(By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[4]/div[2]/div[1]/input").click()
    date_start = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.CLASS_NAME,"today")))
    date_start = browser.find_element(By.CLASS_NAME,"today").click()
    apply_ = browser.find_element(By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[4]/div[2]/div[1]/ngx-daterangepicker-material/div/div[3]/div/button[2]").click()
    print("Clicked the start date")
    time.sleep(5)

    # Date end select
    date_click = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[4]/div[3]/div/input")))
    date_click = browser.find_element(By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[4]/div[3]/div/input").click()
    date_end = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.CLASS_NAME,"today")))
    apply_2 = browser.find_element(By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[4]/div[3]/div[1]/ngx-daterangepicker-material/div/div[3]/div/button[2]").click()
    print("Clicked the end date")
    time.sleep(5)

    # Report format select
    report_format = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[4]/div[4]/ng-select")))
    report_format = browser.find_element(By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[4]/div[4]/ng-select").click()
    print("Print format selected")
    time.sleep(5)

    # csv option select
    csv_ = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[4]/div[4]/ng-select/ng-dropdown-panel/div/div[2]/div[2]/span")))
    csv_ = browser.find_element(By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[4]/div[4]/ng-select/ng-dropdown-panel/div/div[2]/div[2]/span").click()
    print("CSV Format selected")
    time.sleep(5)

    # Create a new report button
    create_report_2 = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[5]/button[1]")))
    create_report_2 = browser.find_element(By.XPATH,"/html/body/ngb-modal-window/div/div/form/div[5]/button[1]").click()
    print("New Report successfully created")
    time.sleep(20)


    # download the top file
    try:
        browser.refresh()
        time.sleep(20)
        download_2_ = WebDriverWait(browser,60).until(EC.presence_of_element_located((By.CSS_SELECTOR,"tr.table-row:nth-child(1) > td:nth-child(10) > app-report-actions:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > span:nth-child(1)")))
        time.sleep(10)
        download_2_ = browser.find_element(By.CSS_SELECTOR,"tr.table-row:nth-child(1) > td:nth-child(10) > app-report-actions:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > span:nth-child(1)").click()
        browser.quit()
    except Exception as error:
        print(f"{error} -> Downloading taking too long")

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


for i in range(0,len(cred_email)):
    download_path = directoryy
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", directoryy)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.headless = True
    options.binary_location = r'/usr/bin/firefox'
    # options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    browser = webdriver.Firefox(options=options,executable_path=GeckoDriverManager().install())

    get_scrape_data(link_warehouse, cred_email[i], cred_pass[i],cred_file_name[i])