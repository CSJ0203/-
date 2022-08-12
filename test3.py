from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
import time

# Setup opitons 
option = Options()
option.add_argument("disable-infobars")
option.add_argument("disable-extensions")
option.add_argument("disable-gpu")

# Selenium 4.0 - load webdriver 
try: 
    s = Service(ChromeDriverManager().install()) 
    browser = webdriver.Chrome(service=s, options=option) 
except Exception as e: 
    print(e) 


def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

driver = webdriver.Chrome("C:/Users/CSJ/Downloads/python/chromedriver.exe")

driver.get("https://www.naver.com/")

time.sleep(100)


