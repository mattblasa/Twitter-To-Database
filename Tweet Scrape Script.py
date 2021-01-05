
'''  _______                _      _____                                
 |__   __|              | |    / ____|                               
    | |_      _____  ___| |_  | (___   ___ _ __ __ _ _ __   ___ _ __ 
    | \ \ /\ / / _ \/ _ \ __|  \___ \ / __| '__/ _` | '_ \ / _ \ '__|
    | |\ V  V /  __/  __/ |_   ____) | (__| | | (_| | |_) |  __/ |   
    |_| \_/\_/ \___|\___|\__| |_____/ \___|_|  \__,_| .__/ \___|_|   
                                                    | |              
                                                    |_|              
'''

'''
This program will run a constant scrape of twitter accounts. Inputs such as user name, number of tweets will be determined by the user. 
Road Map: 
1. Save output as CSV on local file path 
2. Save output as a table within a DB. 
3. Append new tweets as rows, tweets after the last recorded scrape time. 
4. Same as #4, but with and added program to check if added rows are duplicates of current rows. (Check on Tweet ID )
'''

import pandas as pd 
import pyautogui
from pynput.keyboard import *
import numpy as np
import os 
import re
from sqlalchemy import create_engine
import time 
import tweepy


# ================================================= Terminal ===================================================== 
#  ======== settings ========
delay = 1  # in seconds
resume_key = Key.f1
pause_key = Key.f2
exit_key = Key.esc
#  ==========================

pause = True
running = True

def on_press(key):
    global running, pause

    if key == resume_key:
        pause = False
        print("[Resumed]")
    elif key == pause_key:
        pause = True
        print("[Paused]")
    elif key == exit_key:
        running = False
        print("[Exit]")


def display_controls():
    print("// AutoClicker by iSayChris")
    print("// - Settings: ")
    print("\t delay = " + str(delay) + ' sec' + '\n')
    print("// - Controls:")
    print("\t F1 = Resume")
    print("\t F2 = Pause")
    print("\t F3 = Exit")
    print("-----------------------------------------------------")
    print('Press F1 to start ...')

# ===================================================== Tweet Scrape ==============================================================
#consumer keys
consumer_key = your_key_here
consumer_secret = your_key_here
access_token = your_key_here
access_token_secret = your_key_here
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

#convert tweet to data frame 

def extract_tweet_attributes(tweet_object):
    # create empty list
    tweet_list =[]
    # loop through tweet objects
    for tweet in tweet_object:
        tweet_id = tweet.id # unique integer identifier for tweet
        text = tweet.text # utf-8 text of tweet
        favorite_count = tweet.favorite_count
        retweet_count = tweet.retweet_count
        created_at = tweet.created_at # utc time tweet created
        source = tweet.source # utility used to post tweet
        reply_to_status = tweet.in_reply_to_status_id # if reply int of orginal tweet id
        reply_to_user = tweet.in_reply_to_screen_name # if reply original tweets screenname
        retweets = tweet.retweet_count # number of times this tweet retweeted
        favorites = tweet.favorite_count # number of time this tweet liked
        # append attributes to list
        tweet_list.append({'tweet_id':tweet_id, 
                          'text':text, 
                          'favorite_count':favorite_count,
                          'retweet_count':retweet_count,
                          'created_at':created_at, 
                          'source':source, 
                          'reply_to_status':reply_to_status, 
                          'reply_to_user':reply_to_user,
                          'retweets':retweets,
                          'favorites':favorites})
    # create dataframe   
    df = pd.DataFrame(tweet_list) #removed extra columns, which are already rendered 
    return df

def tweet_scrape(username, tweets_count=200):
    username = str(username)
    tweets_clv = api.user_timeline(username, count = tweets_count)
    wf = extract_tweet_attributes(tweets_clv)
    return wf

### Create CSV from Scraped Tweets 
def create_csv(username, count = 200):
    intial_scrape = tweet_scrape(username, count)
    _csv_ = intial_scrape.to_csv(index = False)
    #need to add localpath to download the csv. add one into the method 
    return _csv_ 

# ===== Run Program ========

def main():
    lis = Listener(on_press=on_press)
    lis.start()

    display_controls()
    while running:
        if not pause:
            df.to_csv(index = False) 
            pyautogui.PAUSE = delay
    lis.stop()

    


if __name__ == "__main__":
    main()