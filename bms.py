from bs4 import BeautifulSoup
from selenium import webdriver
import json
import requests
import time
import sys 
from selenium.webdriver.common.keys import Keys


testurl = "https://in.bookmyshow.com/chennai/movies/ford-v-ferrari/ET00104241/user-reviews"
XPATH_loadmore = "//*[@id='load-more-trigger']"
XPATH_grade = "//*[@class='review-container']/div[1]"
list_grades = []

driver = webdriver.Firefox()
driver.get(testurl)

last_height = driver.execute_script("return document.body.scrollHeight")

for i in range(20): # adjust integer value for need
    # you can change right side number for scroll convenience or destination 
    driver.execute_script("window.scrollBy(0, 250)")
    # you can change time integer to float or remove
    time.sleep(1)