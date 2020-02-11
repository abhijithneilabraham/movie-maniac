

from nltk.stem import WordNetLemmatizer
import nltk
from nltk import tokenize
import numpy as np
from textblob import TextBlob 
import matplotlib.pyplot as plt
import io
#nltk.download ()
'''
TextBlob is a Python (2 and 3) library for processing textual data. 
It provides a simple API for diving into common natural language processing (NLP) tasks such as
part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more.
'''

file=open("joker2019.txt","r") 
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
#average=total/number_of_sentences #total polarity /number of sentences gives an average polarity.
#
#print("average polarity =",average*100,"%")



# Data to plot
labels = 'Positive', 'Negative', 'Neutral'
sizes = [pos, neg, neutral]
colors = ['gold', 'yellowgreen', 'lightcoral']
explode = (0.1, 0, 0)  # explode 1st slice

# Plot
pi=plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.savefig('sentiment.png')
plt.show()

vals = [i[0] for i in mostCommon ]
freq = [i[1] for i in mostCommon ]
#plt.bar(vals,freq)
#plt.savefig('wordcount.png')
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])

ax.bar(vals,freq)
plt.savefig('wordcount.png')
        