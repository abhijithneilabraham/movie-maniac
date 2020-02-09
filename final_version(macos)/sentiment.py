#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 03:05:44 2020

@author: abhijithneilabraham

"""
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

file=open("hellboy.txt","r") 
read_file=file.read()
print('total sentences    ', read_file.count('.')) #simply used the Fullstops to find the number of sentences.
number_of_sentences=read_file.count('.')
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
if average>0:
    print("positive")
else:
    print("negative")    



        