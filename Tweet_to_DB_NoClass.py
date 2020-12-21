import tweepy
import pandas as pd 
import numpy as np
import time 
import re
import os 
from sqlalchemy import create_engine

### Twitter Scraping ###

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

def tweet_scrape(username, count=200):
    username = str(username)
    tweets_clv = api.user_timeline(username, count)
    wf = extract_tweet_attributes(tweets_clv)
    return wf

### Send to Database ### 
def send_to_db(local_path, table_name, username, count = 200):
    df = tweet_scrape(username, count)
    engine = create_engine(local_path)
    df.to_sql(table_name, engine, index=False) # Not copying over the index

#Take tweets and puts it in DB
send_to_db('postgresql://postgres:noyS9oud!@localhost:5432/test', 'test3', 'Cleavon_MD', 200)
