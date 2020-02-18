from flask import Flask,request,jsonify,render_template,redirect,url_for
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import json
import requests
import time
import sys 
import combined
import os
from selenium.webdriver.common.keys import Keys

app=Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/',methods=['GET','POST'])
def start_page():
    if request.method=='POST':
        fn=request.form["name"]
        yr=request.form["year"]
        num=request.form['num']
        combined.scraper(fn,yr,num)
        
        

        return render_template("results.html")
    
    return render_template("index.html")

if __name__ == "__main__":
    #init()
    try:
        app.run(debug=True)
    except:
        print("Execption")

