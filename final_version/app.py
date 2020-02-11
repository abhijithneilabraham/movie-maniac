from flask import Flask,request,jsonify,render_template,redirect,url_for
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import json
import requests
import time
import sys 
import combined
from selenium.webdriver.common.keys import Keys

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def start_page():
    if request.method=='POST':
        fn=request.form["name"]
        im=request.form['im']
        rt=request.form['rt']
        bms=request.form['bms']

        return combined.scraper(fn,im,rt,bms)

        
            
    return render_template('index.html')

if __name__ == "__main__":
    #init()
    try:
        app.run(debug=True)
    except:
        print("Execption")

