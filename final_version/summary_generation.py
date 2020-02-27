#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:43:05 2020

@author: abhijithneilabraham
"""

from gensim.summarization.summarizer import summarize

file=open("joker.txt","r") 
read_file=file.read()
print(summarize(read_file,ratio=0.005))
