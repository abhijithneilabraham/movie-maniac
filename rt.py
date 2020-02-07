#######################################################################################################
## input_format: python rt.py https://www.rottentomatoes.com/m/($MOVIE_NAME_YEAR)/reviews?type=user  #
#####################################################################################################
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import json
import requests
import time
import sys 
from selenium.webdriver.common.keys import Keys

#Specifying the url and some css selectors
testurl =sys.argv[1]
patience_time1 = 60
# XPATH_loadmore = "//*[@id='.prev-next-paging__button-text']"
# XPATH_grade = "//*[@class='review-container']/div[1]"
# list_grades = []


driver = webdriver.Firefox()
driver.get(testurl)

list_content=[]
while True:
    try:
        loadmore = driver.find_element_by_xpath("//*[@id='content']/div/div/nav[3]/button[2]/span")
        soup = bs(driver.page_source, features="html.parser")
        content = soup.find_all('p', class_=['audience-reviews__review'])
        # content = soup.select('.js-clamp')
        # content = soup.find_all(".js-clamp")
        list_content = [tag.get_text() for tag in content]
        time.sleep(1)
        loadmore.click()
        time.sleep(3)
    except Exception as e:
        print(e)
        break
    print("Loaded")
    time.sleep(1)

# urlMovie="https://www.rottentomatoes.com/m/birds_of_prey_2020/reviews?type=user"
# page=requests.get(urlMovie)
# soup=bs(page.content,'html.parser')
# content = soup.select('.js-clamp')
# list_content = [tag.get_text() for tag in content]

name=input("Enter file name:")
i=0
with open(name+'.txt', 'w') as f:
    for item in list_content:
        if i%2!=0:
            continue
        f.write("%s\n" % item)
driver.quit()
