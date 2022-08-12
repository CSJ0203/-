import selenium
import time
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

#driver = webdriver.Chrome("C:/Users/CSJ/Downloads/python/chromedriver.exe")
driver = webdriver.Chrome("./chromedriver")

driver.get("https://www.naver.com/")

#time.sleep(100)
