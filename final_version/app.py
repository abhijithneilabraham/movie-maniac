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

img_folder = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = img_folder



@app.route('/',methods=['GET','POST'])
@app.route('/index')
def start_page():
    if request.method=='POST':
        fn=request.form["name"]
        im=request.form['im']
        rt=request.form['rt']
        bms=request.form['bms']
        num=request.form['num']
        combined.scraper(fn,im,rt,bms,num)
        
        

        return render_template("results.html")
    
    return render_template("index.html")

if __name__ == "__main__":
    #init()
    try:
        app.run(debug=True)
    except:
        print("Execption")

