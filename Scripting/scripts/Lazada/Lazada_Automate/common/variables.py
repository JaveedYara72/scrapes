# lazada scrape variables
main_link = "https://sellercenter.lazada.sg/apps/seller/login"
username = "//input[@id='account']"
password = "//input[@id='password']"
login = "//span[@class='next-btn-helper' and contains(text(),'Login')]"
popupbutton = "//a[@class='next-dialog-close']"
reports = "//div[@class='next-tabs-tab-inner']//button[@id='menu-label']//span[contains(text(),'Reports & Insights')]"
datainsight = "//div[@class='next-menu-item-inner']//span[@class='next-menu-item-text']//span[contains(text(),'Data Insights')]"
enterdate = "//div[@class='rc-calendar-input-wrap']//div[@class='rc-calendar-date-input-wrap']//input[@class='rc-calendar-input ']"
download = "//div//button[@class='next-btn next-medium next-btn-normal']//span[contains(text(),'download')]"
sponsored_discovery = "//li[@class='next-tabs-tab']//div[@class='next-tabs-tab-inner' and contains(text(),'Sponsored Discovery')]"
keywords = "//li[@class='next-tabs-tab']//div[@class='next-tabs-tab-inner' and contains(text(),'Keywords')]"

marketing_link = "https://sellercenter.lazada.sg/sponsor/solutions/ads/productads/#!/overview"