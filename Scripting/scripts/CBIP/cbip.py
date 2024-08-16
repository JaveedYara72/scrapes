import time
from datetime import date, timedelta
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# CONFIG
EXEC_PATH = "/Users/sambhavbhandari/Documents/chromedriver"
HOME_PAGE = "http://fba.anchanto.com/login"
USERNAME = ""
PASSWORD = ""
EMAIL = ""

# UTIL
ytd_int = (date.today() - timedelta(days=1)).strftime('%-d')

# Spin up browser
service = Service(EXEC_PATH)
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get(HOME_PAGE)

# LOGIN
driver.find_element(By.ID, "user_email").send_keys("")
time.sleep(0.5)
driver.find_element(By.ID, "user_password").send_keys("")
time.sleep(0.5)
driver.find_element(By.NAME, "commit").click()
time.sleep(0.5)

# GO TO "Generate Reports"
driver.find_element(By.LINK_TEXT, "Reports").click()
time.sleep(0.5)
driver.find_element(By.LINK_TEXT, "Generate Reports").click()
time.sleep(0.5)

# Select report to download
dropdown = driver.find_element(By.ID, "report_type")
time.sleep(0.5)
dropdown.find_element(By.XPATH, "//option[. = 'Inventory Report']").click()
time.sleep(0.5)
driver.find_element(By.ID, "emails").click()
time.sleep(0.5)
driver.find_element(By.ID, "emails").send_keys("sambhav.bhandari@una-brands.com")
time.sleep(0.5)
driver.find_element(By.ID, "datepicker3").click()
time.sleep(0.5)
driver.find_element(By.LINK_TEXT, ytd_int).click()
time.sleep(0.5)
driver.find_element(By.ID, "admin_report").click()
time.sleep(0.5)



# LOGOUT
driver.find_element(By.LINK_TEXT, "Welcome, ").click()
time.sleep(0.5)
driver.find_element(By.LINK_TEXT, "Logout").click()
time.sleep(0.5)
driver.close()
