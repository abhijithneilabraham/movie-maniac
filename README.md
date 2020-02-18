# movie-maniac
Web scraping+sentiment analysis for movie review

## Prerequisites

#### Install firefox browser in your system. 

Clone the Repository:
```git clone https://github.com/abhijithneilabraham/movie-maniac```

Then go to the working directory.

```cd movie-maniac```

In the working directory,

To install all the dependencies, run:

``` pip install --user -r requirements.txt ```

Before running the programs,first run the ```firstrun.py``` .This is important for nltk to download all the required packages.

## Running the program
 
 Go to the final_version folder (If you are using windows or linux, then use this folder, else if you're using a mac,use the final version macos folder).
 
 Run ```flask run``` , or run ```python app.py```
 
 
 Go to your browser and enter ```http://127.0.0.1:5000/``` into your address bar. This is localhost.
 
Enter the filename and year as asked.
 

# Tips

There is an extra file named sentiment.py, added here, to see only the sentiment analysis results on a sample txt file. Edit the txt file name and run the program, if you want to see results of the sentiment analysis only.

