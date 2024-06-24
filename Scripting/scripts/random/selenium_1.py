import sys
import json 
import time 
import platform
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

browser = webdriver.Firefox()

link = "https://shopee.co.id/abadilogam"

# Scraping all the details
def scrapr_inside(link):

    delay = 5

    browser.get(link)
    # Produk
    produk = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.shop-page__info > div > div.section-seller-overview-horizontal__seller-info-list > div:nth-child(1)")))
    produk = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.shop-page__info > div > div.section-seller-overview-horizontal__seller-info-list > div:nth-child(1)").text
    print(f"The Number of products are {produk}")

    # Pengikut
    pengikut = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.shop-page__info > div > div.section-seller-overview-horizontal__seller-info-list > div:nth-child(2) > div:nth-child(2) > div.section-seller-overview__item-text-value").text
    print(f"Pengikut ->  {pengikut}")

    # Mengikuti
    Mengikuti = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.shop-page__info > div > div.section-seller-overview-horizontal__seller-info-list > div:nth-child(3) > div:nth-child(2) > div.section-seller-overview__item-text-value").text
    print(f"Mengikuti-> {Mengikuti}")

    # Penilain
    Penilain = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.shop-page__info > div > div.section-seller-overview-horizontal__seller-info-list > div:nth-child(4) > div:nth-child(2) > div.section-seller-overview__item-text-value").text
    print(f"The Number of products are {Penilain}")

    # Performa Chat
    Performa_chat = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.shop-page__info > div > div.section-seller-overview-horizontal__seller-info-list > div:nth-child(5) > div:nth-child(2) > div.section-seller-overview__item-text-value").text
    print(f"Performa chat -> {Performa_chat}")

    # Bergabung
    Bergabung = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.shop-page__info > div > div.section-seller-overview-horizontal__seller-info-list > div:nth-child(6) > div:nth-child(2) > div.section-seller-overview__item-text-value").text
    print(f"Bergabung-> {Bergabung}")

    
    product_link = link + "?page=0&sortBy=sales"
    print(f"this is the new navigating link -> {product_link}")

    browser.get(product_link)
    print("--------------------------------------------------------")

    # Top product container

    product_1_name = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(1) > a > div > div > div._2wia4m > div._3TUbqX > div._1bmKnt > div")))
    product_1_name = browser.find_element(By.CSS_SELECTOR, "#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(1) > a > div > div > div._2wia4m > div._3TUbqX > div._1bmKnt > div").text
    print(f"product name -> {product_1_name}")

    proudct_1_price = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(1) > a > div > div > div._2wia4m > div._1YWgxN > div._2AKyiQ._1UJbfe > span._2Ul3BO").text
    print(f"Price of {product_1_name} -> {proudct_1_price}")

    product_1_stock = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(1) > a > div > div > div._2wia4m > div._3q1z8m > div._36z98S._2uoHuo").text
    print(f"Quantity present in the warehouse for {product_1_name} -> {product_1_stock}")

    print("-----------------------------------------------------------------")
    # Product 2
    product_2_name = browser.find_element(By.CSS_SELECTOR, "#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(2) > a > div > div > div._2wia4m > div._3TUbqX > div._1bmKnt > div").text
    print(f"product name -> {product_2_name}")

    product_2_price = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(2) > a > div > div > div._2wia4m > div._1YWgxN > div._2AKyiQ._1UJbfe > span._2Ul3BO").text
    print(f"Price of {product_2_name} -> {product_2_price}")

    product_2_stock = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(2) > a > div > div > div._2wia4m > div._3q1z8m > div._36z98S._2uoHuo").text
    print(f"Quantity present in the warehouse for {product_2_name} -> {product_2_stock}")
    print("-----------------------------------------------------------------")
    # Product 3
    product_3_name = browser.find_element(By.CSS_SELECTOR, "#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(3) > a > div > div > div._2wia4m > div._3TUbqX > div._1bmKnt > div").text
    print(f"product name -> {product_1_name}")

    product_3_price = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(3) > a > div > div > div._2wia4m > div._1YWgxN > div._2AKyiQ._1UJbfe > span._2Ul3BO").text
    print(f"Price of {product_3_name} -> {product_3_price}")

    product_3_stock = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(3) > a > div > div > div._2wia4m > div._3q1z8m > div._36z98S._2uoHuo").text
    print(f"Quantity present in the warehouse for {product_1_name} -> {product_1_stock}")
    print("-----------------------------------------------------------------")
    # Product 4
    product_4_name = browser.find_element(By.CSS_SELECTOR, "#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(4) > a > div > div > div._2wia4m > div._3TUbqX > div._1bmKnt > div").text
    print(f"product name -> {product_4_name}")

    product_4_price = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(4) > a > div > div > div._2wia4m > div._1YWgxN > div._2AKyiQ._1UJbfe > span._2Ul3BO").text
    print(f"Price of {product_4_name} -> {product_4_price}")

    product_4_stock = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(4) > a > div > div > div._2wia4m > div._1YWgxN > div._2AKyiQ._1UJbfe > span._2Ul3BO").text
    print(f"Quantity present in the warehouse for {product_4_name} -> {product_4_stock}")
    print("-----------------------------------------------------------------")
    # Product 5
    product_5_name = browser.find_element(By.CSS_SELECTOR, "#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(5) > a > div > div > div._2wia4m > div._3TUbqX > div._1bmKnt > div").text
    print(f"product name -> {product_5_name}")

    proudct_5_price = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(5) > a > div > div > div._2wia4m > div._1YWgxN > div._2AKyiQ._1UJbfe > span._2Ul3BO").text
    print(f"Price of {product_5_name} -> {proudct_5_price}")

    product_5_stock = browser.find_element(By.CSS_SELECTOR,"#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > div.shop-search-result-view > div > div:nth-child(5) > a > div > div > div._2wia4m > div._3q1z8m > div._36z98S._2uoHuo").text
    print(f"Quantity present in the warehouse for {product_5_name} -> {product_5_stock}")
    print("-----------------------------------------------------------------")



scrapr_inside(link)

sys.modules[__name__] = scrapr_inside

