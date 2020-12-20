import tweepy
import pandas as pd 
import numpy as np
import time 
import re
import os 
from sqlalchemy import create_engine

class ToDatabase:
    '''
    Object will take in user's Twitter API consumer key, consumer secret, access secret, and access_token. It will then extract tweets from a selected user, then 
    place it into a database using SQL Alchemy. 
    '''
    #set the Twitter API keys
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret): #may need to add 
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        
    #Takes in output of tweet objects, and creates a dataframe. 
    def extract_tweet_attributes(self, tweet_obj):
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

    #Send Request to API, render as dataframe. 
    def tweet_scrape(self, username, count=200):
        username = str(username)
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret) #consumer key 1
        auth.set_access_token(self.access_token, self.access_token_secret)  #consumer key 2
        api = tweepy.API(auth,wait_on_rate_limit=True)
        tweets_clv = api.user_timeline(username, count)
        wf = extract_tweet_attributes(tweets_clv)
        return wf
    
    ### Send to Database ### 
    def send_to_db(self, local_path, table_name, username, count = 200):
        df = self.tweet_scrape(username, count) #render using tweet_scrape method, refer to self
        engine = create_engine(local_path) #create SQL engine using SQL Alchemy
        df.to_sql(table_name, engine, index=False) # Not copying over the index