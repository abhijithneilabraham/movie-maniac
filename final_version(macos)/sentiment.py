

from nltk.stem import WordNetLemmatizer
import nltk
from nltk import tokenize
import numpy as np
from textblob import TextBlob 
#nltk.download ()
'''
TextBlob is a Python (2 and 3) library for processing textual data. 
It provides a simple API for diving into common natural language processing (NLP) tasks such as
part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more.
'''

file=open("Hellboy.txt","r") 
read_file=file.read()
sentences=tokenize.sent_tokenize(read_file) #tokenization means splitting into meaningful stuff,like,splitting into words.
number_of_sentences=len(sentences)
print("Total sentences =",number_of_sentences)
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
if average>0:
    print("positive")
else:
    print("negative")    



        
