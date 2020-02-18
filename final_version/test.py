from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

num=1
movieName="Joker"
year="2019"
path="./"
num=int(num)
driver = webdriver.Firefox(path)
imdbUrl="https://www.imdb.com/find?s=tt&q="+ "%20".join(movieName.split(" "))+ "&ref_=nv_sr_sm"

path="./"
url="https://www.rottentomatoes.com/search/?search="+movieName
driver.get(url)
try:
    time.sleep(1)
    soup = bs(driver.page_source, features="html.parser")
    content = soup.find_all('div', class_=['search__results-item-info-top'])
    for movie in content:
        if year in (movie.span.get_text()):
            link="https://www.rottentomatoes.com"+movie.a.get("href")
            driver.get(link)
            break
    userReviews=link+"/reviews?type=user"
    driver.get(userReviews)      

    for i in range(num):
        try:
            loadmore = driver.find_element_by_xpath("//*[@id='content']/div/div/nav[3]/button[2]/span")
            soup = bs(driver.page_source, features="html.parser")
            content = soup.find_all('p', class_=['text','audience-reviews__review'])
            list_content += [tag.get_text() for tag in content]
            time.sleep(1)
            loadmore.click()
            time.sleep(1)
        except Exception as e:
            print(e)
            break
        print("Collecting Reviews from RT..... (Don't close the program)")
    time.sleep(1)
except Exception as e:
    print(e)

driver.quit()    
# #Getting the required user reviews.
# soup = bs(driver.page_source, features="html.parser")
# content = soup.find_all('div', class_=['text','show-more__control'])
# list_content += [tag.get_text() for tag in content]
# driver.quit() 

# with open(fileName+".txt", 'w') as f:
#     for item in list_content:
#         f.write("%s\n" % item)
# print("The IMDB reviews have been saved to the file. :)")        

