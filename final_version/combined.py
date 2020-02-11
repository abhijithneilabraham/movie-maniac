from bs4 import BeautifulSoup as bs
from selenium import webdriver
import json
import requests
import time
import sys 
from selenium.webdriver.common.keys import Keys
from nltk.stem import WordNetLemmatizer
import nltk
from nltk import tokenize
import numpy as np
from textblob import TextBlob 
import matplotlib.pyplot as plt

def scraper(fileName,imdbUrl,rtUrl,bsmUrl,num):
    print("""
    => Make sure that the current folder has 'geckodriver' file.
    => Please provide proper urls for this program to work.
    eg-
        For the movie "Birds of Prey", these are the urls for user reviews (Look for these formats of urls):
            imDb           :"https://www.imdb.com/title/tt7713068/reviews?ref_=tt_ql_3"
            Rotten Tomatoes:"https://www.rottentomatoes.com/m/birds_of_prey_2020/reviews?type=user",
            Book My Show   :"https://in.bookmyshow.com/chennai/movies/birds-of-prey/ET00112343/user-reviews" 

    """)


    #######################################################
    ###################imDb################################
    path="./"
    num=int(num)
    driver = webdriver.Firefox(path)
    driver.get(imdbUrl)

    list_content=[]
    for i in range(num):
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
    driver = webdriver.Firefox(path)
    driver.get(rtUrl)
    for i in range(num):
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
    driver = webdriver.Firefox(path)
    try:
        driver.get(bsmUrl)
        for i in range(num%10): 
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
   
    TextBlob is a Python (2 and 3) library for processing textual data. 
    It provides a simple API for diving into common natural language processing (NLP) tasks such as
    part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more.
    '''

    file=open(fileName+".txt","r") 
    read_file=file.read()
    sentences=tokenize.sent_tokenize(read_file) #tokenization means splitting into meaningful stuff,like,splitting into words.
    number_of_sentences=len(sentences)
    print("Total sentences =",number_of_sentences)
    total=0
    pos=0
    neg=0
    neutral=0
    allWords = nltk.tokenize.word_tokenize(read_file)
    stopwords =set( nltk.corpus.stopwords.words('english'))
    allWordExceptStopDist = nltk.FreqDist(w.lower() for w in allWords if w.lower() not in stopwords)   
    mostCommon= allWordExceptStopDist.most_common(10)
    garb=[".",",","'s","n't","!"]
    mostCommon=[i for i in mostCommon if i[0] not in garb]
    
    print("The most commonly used words along with their frequency count")
    for i in mostCommon:
        print("word =",i[0],"frequency =",i[1])
        
    for p in sentences: 
        q=TextBlob(p)
        senti=q.sentiment 
        
        '''
        to understand what TextBlob.sentiment does,here is an example.
        TextBlob("not a very great calculation").sentiment
     gives the result=Sentiment(polarity=-0.3076923076923077, subjectivity=0.5769230769230769)
     '''
        total=total+senti.polarity #We only want the polarity here.So  summed it up over for sentences.
        if(senti.polarity==0):
            neutral+=1
        elif(senti.polarity<0):
            neg+=1
        else:
            pos+=1
    average=total/number_of_sentences #total polarity /number of sentences gives an average polarity.
    #
    #print("average polarity =",average*100,"%")
    
    
    
    # Data to plot
    labels = 'Positive', 'Negative', 'Neutral'
    sizes = [pos, neg, neutral]
    colors = ['gold', 'yellowgreen', 'lightcoral']
    explode = (0.1, 0, 0)  # explode 1st slice
    
    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    
    plt.axis('equal')
    plt.savefig('static/img/sentiment.png')
    plt.close()
    vals = [i[0] for i in mostCommon ]
    freq = [i[1] for i in mostCommon ]
    plt.bar(vals,freq)
    plt.savefig('static/img/wordcount.png', dpi=400)
    plt.close()
#scraper('joker2019','https://www.imdb.com/title/tt7286456/reviews?ref_=tt_ql_3','https://www.rottentomatoes.com/m/joker_2019/reviews?type=user','https://in.bookmyshow.com/movies/joker/ET00100071/user-reviews',2)
    



