from bs4 import BeautifulSoup as bs
from selenium import webdriver
import json
import requests
import time
import sys 
from selenium.webdriver.common.keys import Keys

print("""
=> Make sure that the current folder has 'geckodriver' file.
=> Please provide proper urls for this program to work.
eg-
    For the movie "Birds of Prey", these are the urls for user reviews (Look for these formats of urls):
        imDb           :"https://www.imdb.com/title/tt7713068/?ref_=fn_al_tt_1"
        Rotten Tomatoes:"https://www.rottentomatoes.com/m/birds_of_prey_2020/reviews?type=user",
        Book My Show   :"https://in.bookmyshow.com/chennai/movies/birds-of-prey/ET00112343/user-reviews" 

""")

fileName=input("=> Enter the movie name:");
imdbUrl=input("=> Enter the imDb url for user reviews:");
rtUrl=input("=> Enter the rotten tomatoes url for user reviews:");
bsmUrl=input("=> Enter the Book my Show url for user reviews:");


#######################################################
###################imDb################################
path="./"
# driver = webdriver.Firefox(path)
# driver.get(imdbUrl)

list_content=[]
# while True:
#     try:
#         loadmore = driver.find_element_by_id("load-more-trigger")
#         time.sleep(1)
#         loadmore.click()
#         time.sleep(1)
#     except Exception as e:
#         print(e)
#         break
#     print("Collecting Reviews from imDb..... (Don't close the program)")
#     time.sleep(1)

# #Getting the required user reviews.
# soup = bs(driver.page_source, features="html.parser")
# content = soup.find_all('div', class_=['text','show-more__control'])
# list_content += [tag.get_text() for tag in content]
# driver.quit() 

# with open(fileName+".txt", 'w') as f:
#     for item in list_content:
#         f.write("%s\n" % item)
# print("The reviews have been saved to the file. :)")        


# ######################################################
# ######################################################

# #######################################################
# ###################Rotten Tomatoes#####################
# driver = webdriver.Firefox(path)
# driver.get(rtUrl)
# while True:
#     try:
#         loadmore = driver.find_element_by_xpath("//*[@id='content']/div/div/nav[3]/button[2]/span")
#         soup = bs(driver.page_source, features="html.parser")
#         content = soup.find_all('p', class_=['text','audience-reviews__review'])
#         # content = soup.select('.js-clamp')
#         # content = soup.find_all(".js-clamp")
#         list_content += [tag.get_text() for tag in content]
#         time.sleep(1)
#         loadmore.click()
#         time.sleep(1)
#     except Exception as e:
#         print(e)
#         break
#     print("Collecting Reviews from RT..... (Don't close the program)")
#     time.sleep(1)

# driver.quit()
# #######################################################
#######################################################

#######################################################
####################Book My Show#######################
driver = webdriver.Firefox(path)
driver.get(bsmUrl)
for i in range(60): 
    #You can adjust the value of range in case there are more reviews.   
    driver.find_element_by_tag_name('body').send_keys(' ')
    if i%10==0:
        print("Collecting Reviews from BookMyshow..... (Don't close the program)")
    time.sleep(0.8)

soup = bs(driver.page_source, features="html.parser")
content = soup.find_all('div', class_=['text','__reviewer-text'])
list_content += [tag.get_text() for tag in content]  
driver.quit()
#######################################################
#######################################################

#######################################################
##############Writing it to a file#####################
with open(fileName+".txt", 'w') as f:
    for item in list_content:
        f.write("%s\n" % item)
print("The reviews have been saved to the file. :)")        
#######################################################
#######################################################
