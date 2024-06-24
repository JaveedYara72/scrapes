import time 
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def bitwarden(browser,company):
    browser.get("https://vault.bitwarden.com/#/login")
    delay = 30

    # email 
    WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='login_input_email']")))
    browser.find_element(By.XPATH,"//input[@id='login_input_email']").send_keys("javeed.y@una-brands.com")
    time.sleep(5)

    # email continue
    WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Continue')]")))
    browser.find_element(By.XPATH,"//span[contains(text(),'Continue')]").click()
    print("Email Entered")
    time.sleep(5)

    # password 
    WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"//input[@id='login_input_master-password']")))
    browser.find_element(By.XPATH,"//input[@id='login_input_master-password']").send_keys("AGN.tft*bem5qkj7qyd")
    time.sleep(5)

    # password continue
    WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Log in with master password')]")))
    browser.find_element(By.XPATH,"//span[contains(text(),'Log in with master password')]").click()
    print("Password Clicked")
    time.sleep(5)

    # Click on Collections
    WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH,"//tr[@class='tw-cursor-pointer hover:tw-bg-background-alt last:tw-border-0 tw-align-middle tw-border-0 tw-border-b tw-border-secondary-300 tw-border-solid']//td[@class='tw-break-all tw-align-middle tw-p-3']//button[contains(text(),'Heavenluxe Shopify Master Admin')]")))
    browser.find_element(By.XPATH,"//tr[@class='tw-cursor-pointer hover:tw-bg-background-alt last:tw-border-0 tw-align-middle tw-border-0 tw-border-b tw-border-secondary-300 tw-border-solid']//td[@class='tw-break-all tw-align-middle tw-p-3']//button[contains(text(),'Heavenluxe Shopify Master Admin')]").click()
    print(f"Clicked on {company}")
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
        time.sleep()
    root = tk.Tk()
    root.overrideredirect(1)
    root.withdraw() 
    root.deiconify()

    # code
    copy_button_3 = browser.find_element(By.XPATH,"//button[@title='Copy verification code']")
    copy_button_3.click()
    root = tk.Tk()
    code = root.clipboard_get()
    print(f"The code is -> {code}")
    root.overrideredirect(1)
    root.withdraw() 




if __name__ == "__main__":
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    browser = webdriver.Firefox(options=options)
    bitwarden(browser,"Heavenluxe")