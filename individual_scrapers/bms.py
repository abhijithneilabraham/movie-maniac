from bs4 import BeautifulSoup as bs
from selenium import webdriver
import json
import requests
import time
import sys 
from selenium.webdriver.common.keys import Keys


testurl = "https://in.bookmyshow.com/ahmedabad/movies/jawaani-jaaneman/ET00104334/user-reviews"

driver = webdriver.Firefox()
driver.get(testurl)

last_height = driver.execute_script("return document.body.scrollHeight")

for i in range(60):    
     # adjust integer value for need
    # driver.sendKeys(Keys.DOWN);
    driver.find_element_by_tag_name('body').send_keys(' ')
    # you can change right side number for scroll convenience or destination 
    # driver.execute_script("window.scrollBy(0, 250)")
    # you can change time integer to float or remove
    time.sleep(0.8)

list_content=[]
soup = bs(driver.page_source, features="html.parser")
content = soup.find_all('div', class_=['text','__reviewer-text'])
list_content = [tag.get_text() for tag in content]    


with open('newy.txt', 'w') as f:
    for item in list_content:
        f.write("%s\n" % item)
driver.quit()
