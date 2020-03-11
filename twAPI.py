# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 13:08:20 2020

@author: User
"""

import tweepy as tw

def twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date):
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth)
    # Define the search term and the date_since date as variables
    search = hashTags + " -filter:retweets  -filter:links"
    date_since = date
    
    tweets = tw.Cursor(api.search,
                  q=search,
                  lang="en",
                  since=date_since,
                  tweet_mode="extended").items(total)
    
    tweet_data = []
    for tweet in tweets:
        tweet_data.append([tweet.id_str,tweet.full_text,tweet.entities["hashtags"],tweet.created_at])
    return(tweet_data)