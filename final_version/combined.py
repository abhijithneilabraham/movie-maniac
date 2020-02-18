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

def scraper(movieName,year,num):
    #######################################################
    ###################imDb################################
    path="./"
    num=int(num)
    driver = webdriver.Firefox(path)
    
    imdbUrl="https://www.imdb.com/find?s=tt&q="+ "%20".join(movieName.split(" "))+ "&ref_=nv_sr_sm"
    driver.get(imdbUrl)

    list_content=[]
    for i in range(num):
        try:
            soup = bs(driver.page_source, features="html.parser")
            content = soup.find_all('td', class_=['result_text'])
            for movie in content:
                if year in (movie.get_text()):
                    print(year)
                    link="https://www.imdb.com"+ movie.a.get("href")
                    driver.get(link)
                    break

            userReviews=driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "quicklink", " " )) and (((count(preceding-sibling::*) + 1) = 5) and parent::*)]')
            userReviews.click()
            time.sleep(1)

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
        except Exception as e:
            print(e)
            break


    #Getting the required user reviews.
    soup = bs(driver.page_source, features="html.parser")
    content = soup.find_all('div', class_=['text','show-more__control'])
    list_content += [tag.get_text() for tag in content]
    # river.quit() 

    with open(movieName+".txt", 'w') as f:
        for item in list_content:
            f.write("%s\n" % item)
    print("The IMDB reviews have been saved to the file. :)")   
    list_content=[]     


    ######################################################
    ######################################################

    #######################################################
    ###################Rotten Tomatoes#####################
    path="./"
    url="https://www.rottentomatoes.com/search/?search="+movieName
    time.sleep(1)
    driver.get(url)
    try:
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
    #######################################################
    #######################################################


    #######################################################
    ##############Writing it to a file#####################
    with open(movieName+".txt", 'a') as f:
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

    file=open(movieName+".txt","r") 
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
    



