# -*- coding: utf-8 -*-
"""
DSC540 10.2 Logging Automation
Holly Erickson

Add Python logging to previous code that you have written. In your logging, include a note to yourself 
with the area of the code writing the message so you know where the error occurred. 
An example of this can be found on page 406-408 of your text, Data Wrangling with Python.

Add an automated message to previous code that you have written. 
You can choose to do an email, text or call. Make sure to include the failure/success in your message. 
Include your code and output in your submitted assignment. An example of this can be found on page 408-412 
of your text Data Wrangling with Python.

Using previous code for assignment 9.2 Accessing Twitter API
"""
APP_KEY = "muoNZiZsbjioa4TGzgj4zAwwY"
APP_SECRET = "v9f5wqEKh4vSUt894tJN6tMf0W0G3vN2D9PVLDHKzdimlaq27x"
OAUTH_TOKEN = "838081010193547264-rE7o5rSPlMwibMTVVaPN2SjG8JZX9zP" 
OAUTH_TOKEN_SECRET = "CM9RRtrWf1OsaRB5PV6sIRzUs7iaGXlXqBCfj2eK74Zub"

#%%
#Do a single data pull from Twitter’s REST API (Data Wrangling with Python, pg. 366 – 368).

from twython import Twython # Used twython library to simplify integration into my Anaconda environment
import json as json

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
search = twitter.search(q='childlabor', count=1) # Just pulled first tweet as data is long

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(search['statuses']) 

#%%
import pandas as pd
#Execute multiple queries at a time from Twitter’s REST API (Data Wrangling with Python, pg. 368 – 371).
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
results = twitter.cursor(twitter.search, q='childlabor') # I used Twythons cursor generator

all_results = []
for result in results:
    #print(result)
    # Results are very long so instead I am saving each result 
    df = pd.DataFrame.from_dict(result, orient = 'index')
    all_results.append(df)

new = pd.concat(all_results, axis =1)
data = new.T
print(data.info()) # Dataframe of all 253 results

#%%
#Do a data pull from Twitter’s Streaming API (Data Wrangling with Python, pg. 372 – 374).

from twython import TwythonStreamer # Sticking with Twythons library

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print(data['text'])

    def on_error(self, status_code, data):
        print(status_code)

stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track='baseball') # Thought it would be fun to see latest tweets about baseball
