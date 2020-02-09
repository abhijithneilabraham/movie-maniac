from bs4 import BeautifulSoup as bs
from selenium import webdriver
import json
import requests
import time
import sys 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


print("""
=> Make sure that the current folder has 'geckodriver' file.
=> Please provide proper urls for this program to work.
eg-
    For the movie "Birds of Prey", these are the urls for user reviews (Look for these formats of urls):
        imDb           :"https://www.imdb.com/title/tt7713068/?ref_=fn_al_tt_1"
        Rotten Tomatoes:"https://www.rottentomatoes.com/m/birds_of_prey_2020/reviews?type=user",
        Book My Show   :"https://in.bookmyshow.com/chennai/movies/birds-of-prey/ET00112343/user-reviews" 
Enter Nil if you dont have a url available for a particular choice.

""")

fileName=input("=> Enter the movie name:");
imdbUrl=input("=> Enter the imDb url for user reviews:");
rtUrl=input("=> Enter the rotten tomatoes url for user reviews:");
bsmUrl=input("=> Enter the Book my Show url for user reviews:");
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True


#######################################################
###################imDb################################
path="/usr/local/bin/geckodriver"
driver = webdriver.Firefox(executable_path=path)
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
    print("Collecting Reviews from imDb..... (Don't close the program)")
    time.sleep(1)

#Getting the required user reviews.
soup = bs(driver.page_source, features="html.parser")
content = soup.find_all('div', class_=['text','show-more__control'])
list_content += [tag.get_text() for tag in content]
driver.quit() 

with open(fileName+".txt", 'w') as f:
    for item in list_content:
        f.write("%s\n" % item)
print("The IMDB reviews have been saved to the file. :)")        


######################################################
######################################################

#######################################################
###################Rotten Tomatoes#####################
driver = webdriver.Firefox(executable_path=path)
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
    print("Collecting Reviews from RT..... (Don't close the program)")
    time.sleep(1)

driver.quit()
# #######################################################
#######################################################

#######################################################
####################Book My Show#######################
driver = webdriver.Firefox(executable_path=path)
try:
    driver.get(bsmUrl)
    for i in range(60): 
#You can adjust the value of range in case there are more reviews.   
        driver.find_element_by_tag_name('body').send_keys(' ')
        if i%10==0:
            print("Collecting Reviews from BookMyshow..... (Don't close the program)")
        time.sleep(0.8)
except Exception as e:
    print("No url available for Bookmyshow")




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
    
'''
sentiment analysis part
'''
from nltk.stem import WordNetLemmatizer
import nltk
from nltk import tokenize
import numpy as np
from textblob import TextBlob 
'''
TextBlob is a Python (2 and 3) library for processing textual data. 
It provides a simple API for diving into common natural language processing (NLP) tasks such as
part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more.
'''

file=open(fileName+".txt","r") 
read_file=file.read()
print('total sentences    ', read_file.count('.')) #simply used the Fullstops to find the number of sentences.
number_of_sentences=read_file.count('.')
if number_of_sentences>0:
    sentences=tokenize.sent_tokenize(read_file) #tokenization means splitting into meaningful stuff,like,splitting into words.
    total=0
    for p in sentences: 
        q=TextBlob(p)
        senti=q.sentiment 
        '''
        to understand what TextBlob.sentiment does,here is an example.
        TextBlob("not a very great calculation").sentiment
     gives the result=Sentiment(polarity=-0.3076923076923077, subjectivity=0.5769230769230769)
     '''
        total=total+senti.polarity #I only want the polarity here.So I summed it up over for a sentence
        
    
    average=total/number_of_sentences #total polarity /number of sentences gives an average polarity.
else:
    print("Not enough reviews generated to do sentiment analysis.")
if average>0:
    print("positive")
else:
    print("negative")  