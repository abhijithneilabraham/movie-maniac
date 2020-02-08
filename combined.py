from bs4 import BeautifulSoup as bs
from selenium import webdriver
import json
import requests
import time
import sys 
from selenium.webdriver.common.keys import Keys

filename=sys.argv[1]
imdbUrl=sys.argv[2]
rtUrl=sys.argv[3]
bsmUrl=sys.argv[4]

driver = webdriver.Firefox()
driver.get(imdbUrl)

list_content=[]
while True:
    try:
        loadmore = driver.find_element_by_id("load-more-trigger")
        time.sleep(1)
        loadmore.click()
        time.sleep(1)
    except Exception as e:
        print(e)
        break
    print("Loaded")
    time.sleep(1)

#Getting the required user reviews.
soup = bs(driver.page_source, features="html.parser")
content = soup.find_all('div', class_=['text','show-more__control'])
list_content += [tag.get_text() for tag in content]
driver.quit()

driver = webdriver.Firefox()
driver.get(rtUrl)
while True:
    try:
        loadmore = driver.find_element_by_xpath("//*[@id='content']/div/div/nav[3]/button[2]/span")
        soup = bs(driver.page_source, features="html.parser")
        content = soup.find_all('p', class_=['text','audience-reviews__review'])
        # content = soup.select('.js-clamp')
        # content = soup.find_all(".js-clamp")
        list_content += [tag.get_text() for tag in content]
        time.sleep(1)
        loadmore.click()
        time.sleep(1)
    except Exception as e:
        print(e)
        break
    print("Loaded")
    time.sleep(1)

driver.quit()


driver = webdriver.Firefox()
driver.get(bsmUrl)
for i in range(60):    
     # adjust integer value for need
    # driver.sendKeys(Keys.DOWN);
    driver.find_element_by_tag_name('body').send_keys(' ')
    # you can change right side number for scroll convenience or destination 
    # driver.execute_script("window.scrollBy(0, 250)")
    # you can change time integer to float or remove
    time.sleep(0.8)

soup = bs(driver.page_source, features="html.parser")
content = soup.find_all('div', class_=['text','__reviewer-text'])
list_content += [tag.get_text() for tag in content]  
driver.quit()

with open(filename+".txt", 'w') as f:
    for item in list_content:
        f.write("%s\n" % item)
