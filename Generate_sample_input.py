# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 00:55:06 2020

@author: User
"""

import json 
import csv

EmoClass = "Happy"
total = 20
wordList = ["joy","happy"] #define seed words
hashTags = syn.synonyms(wordList)  #get more seed word with synonyms
tweet_data = api.twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date)


data = []
for tweet in tweet_data:
    data2 = [tweet[0],tweet[1],json.dumps(tweet[2]),tweet[3]]
    data.append(data2)

with open('sample_input.csv', 'w', encoding="utf-8", newline='') as file:
    writer = csv.writer(file,delimiter=',')
    writer.writerows(data)
# =================================================================== #
