###################################################
#input format: python imdb.py "movie name" api_key#
###################################################

from bs4 import BeautifulSoup
from selenium import webdriver
import json
import requests
import time
import sys 
from selenium.webdriver.common.keys import Keys

# Used omdbapi to get a list of movies.
json_object="http://www.omdbapi.com/?apikey="+sys.argv[2]+"&s=xyz".replace("xyz",sys.argv[1])
page=(requests.get(json_object))
parsed=json.loads(page.content)

#Getting the imdb id to get the link of movie.
i=0;
for movie in parsed["Search"]:
    print(i,") ",parsed["Search"][i]["Title"],parsed["Search"][i]["Year"])
    i+=1
id=int(input("Select a Movie:"))    
print(id)
imdb_id=parsed["Search"][id]["imdbID"]

#Specifying the url and some css selectors
testurl = "https://www.imdb.com/title/xyz/reviews?ref_=tt_urv".replace("xyz",imdb_id)
patience_time1 = 60
XPATH_loadmore = "//*[@id='load-more-trigger']"
XPATH_grade = "//*[@class='review-container']/div[1]"
list_grades = []

driver = webdriver.Firefox()
driver.get(testurl)

#To automatically press the load more button.
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
    time.sleep(5)

#Getting the required user reviews.
soup = BeautifulSoup(driver.page_source, features="html.parser")
content = soup.find_all('div', class_=['text','show-more__control'])
list_content = [tag.get_text() for tag in content]

#Saving it to a file.
filename=sys.argv[1]+".txt"
with open(filename+'.txt', 'w') as f:
    for item in list_content:
        if item=="\n\n\n\n":
            continue
        f.write("%s\n" % item)
driver.quit()