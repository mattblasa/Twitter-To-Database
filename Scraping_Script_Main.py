#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 12/12/2020 
@author: Matt B.
The ultimate goal of this is to create a script to scrape a Twitter user's tweets and place it a SQL database. 
Tools used will be tweepy and sqlalchemy.
Goal Features: 
    1. Scrape 200 Tweets from a user chosen Twitter user.
    2. Clean the Tweets, removing emojis, hashtags, and urls. 
    3. Push to a SQL database.
  	
"""


import tweepy
import pandas as pd 
import numpy as np
import time 
import re
import os 
from sqlalchemy import create_engine

class Auth:
    '''
    Object will take in user's Twitter API consumer key, consumer secret, access secret, and access_token. It will then extract tweets from a selected user, then 
    place it into a database using SQL Alchemy. 
    '''
    def __init__(self, consumer_key, consumer_secret, access_secret, access_token_secret): #may need to add 
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_secret = access_secret
        self.access_token_secret = access_token_secret
    
    def tweet_obj(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit=True)

    def extract_tweet_attributes(tweet_obj):
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

    def tweet_extract(self):
        #enter twitter username
        username = 'Cleavon_MD'
        #specify the number of tweets to scrape
        tweets_clv = api.user_timeline(username, count = 200)
        wf = extract_tweet_attributes(tweets_clv)

    def push_to_db(self):
        #add postgre database, login, password, and database
        engine1 = create_engine('postgresql://postgres:noyS9oud!@localhost:5433/Data_Camp')

        wf.to_sql(
            'test2', 
            engine1,
            index=False # Not copying over the index
        )
## Print time process started to terminal

## On end: print complete, along with file path that it printed to. 