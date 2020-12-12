import tweepy
import pandas as pd 
import numpy as np
import time 
import re
import os 
from sqlalchemy import create_engine

### Twitter Scraping ###

#consumer keys
consumer_key = "ZdxXpiZl4OUZwYbkprXXjq3GV"
consumer_secret = "V3N91XX797pgasujNaCQ9eptopLyzESEFTnoyyZ9BUyUEucRap"
access_token = "1230175722557169666-0djDhRqeQ3pnFU5onQDdDhxXGxIoTr"
access_token_secret = "Go6iLi292E2YBOuNH1vJPJuHoFc5xdm3vL2BH98TAFXoZ"
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


username = 'Cleavon_MD'
tweets_clv = api.user_timeline(username, count = 200)
wf = extract_tweet_attributes(tweets_clv)

### Send to Database ### 

engine1 = create_engine('postgresql://postgres:noyS9oud!@localhost:5433/Data_Camp')

wf.to_sql(
    'test2', 
    engine1,
    index=False # Not copying over the index
)