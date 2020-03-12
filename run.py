# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 13:10:42 2020

"""
import os
import pandas as pd
import csv

# Changing Current Python Directory 
directory = 'D:\\UofG\\Master\\Web Science\\Emotion-Analysis2020'
os.chdir(directory)
os.getcwd()

# import other .py files (3files)
import main_ as m
import synonyms as syn
import twAPI as api

# Create new sub-directory to keep data output	
os.mkdir('output') # Run only first time & Dont change the name!

# ================================================================================ #
# load External data 
# ================================================================================ #

emo_df = pd.read_excel("NRC_Emotion_Lexicon_v0.92_Nov2017.xlsx")
NRC_Emo = emo_df[["English (en)","Positive","Negative","Anger","Anticipation","Disgust","Fear","Joy","Sadness","Surprise","Trust"]]

NRC_ht_emo = pd.read_csv("NRC_Hashtag_Emotion.txt",sep='\t',names = ["Emotion", "Hashtag", "score"])
NRC_ht_emo = pd.DataFrame(NRC_ht_emo)
NRC_ht_emo["Hashtag_new"] = NRC_ht_emo["Hashtag"].replace('#','',regex=True).str.lower() #Delete hashtag from the word
NRC_ht_emo = NRC_ht_emo[["Emotion","Hashtag_new"]].drop_duplicates(keep='last')
    
# Emoji : https://unicode.org/emoji/charts/full-emoji-list.html
Emoji_emo = pd.read_excel("Emoticon list.xlsx")

# https://pdfs.semanticscholar.org/b95c/23d16faaadf40522fadf7b2938aacc9e3e78.pdf?_ga=2.175739874.1991890535.1583618527-851810122.1582499693 
a_score = pd.read_csv("a-scores.txt",sep='\t',names = ["word", "a_score"])
a_score = pd.DataFrame(a_score)
v_score = pd.read_csv("v-scores.txt",sep='\t',names = ["word", "v_score"])
v_score = pd.DataFrame(v_score)

# ========================================================================= #
# Test the program with CSV file
# ========================================================================= #
with open('sample_input.csv', encoding="utf-8",newline='') as f:
    reader = csv.reader(f)
    sampleData = list(reader)

tweet_data=[]
for data in sampleData:
    a = [data[0],data[1],eval(data[2]),data[3]]
    tweet_data.append(a)
    
EmoClass = "TestProgram"
output_id = m.main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass)


# ========================================================================= #
# Extract using API and Label data for each class
# ========================================================================= #

consumer_key= '05QRcauWKUjmG6NdoTaJ5RJlR'
consumer_secret= 'cl0cveUs3uKwoDk6jzqMP3NQDlyZqBqjF7LPVDybJehAcyZzjC'
access_token= '1225411734606884865-MQFToe2bFpBTo2WQMe1JM45h9ewqOq'
access_token_secret= 'xgO4gi1h4HY0g20JDGbnGjomZk1ztv11tI0fzzfRU5Ciq'
date = "2020-01-01" ##Get the tweets since..

## Happy
EmoClass = "Happy"
total = 10
wordList = ["joy","happy"] #define seed words
hashTags = syn.synonyms(wordList)  #get more seed word with synonyms
tweet_data = api.twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date)
Happy_id = m.main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass)


## Fear
EmoClass = "Fear"
total = 10
wordList = ["fear","nervous","disgust","dislike"] #define seed words
hashTags = syn.synonyms(wordList)
tweet_data = api.twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date)
Fear_id = m.main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass)


## Excitement
EmoClass = "Excitement"
total = 10
wordList = ["excitement","anticipation"] #define seed words
hashTags = syn.synonyms(wordList) #get more seed word with synonyms
hashTags = hashTags+" OR #excited"
hashTags = hashTags.replace("OR #prediction ","")
tweet_data = api.twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date)
Excitement_id = m.main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass)


## Angry
EmoClass = "Angry"
total = 10
wordList = ["angry","hate","annoyed"] #define seed words
hashTags = syn.synonyms(wordList) #get more seed word with synonyms
tweet_data = api.twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date)
Angry_id = m.main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass)

## Surprise
EmoClass = "Surprise"
total = 10
wordList = ["sad","regret",'guity'] #define seed words
hashTags = syn.synonyms(wordList) #get more seed word with synonyms
tweet_data = api.twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date)
Surprise_id = m.main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass)

## Pleasant
EmoClass = "Pleasant"
total = 10
wordList = ["pleased","satisfied"] #define seed words
hashTags = syn.synonyms(wordList) #get more seed word with synonyms
tweet_data = api.twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date)
Pleasant_id = m.main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass)

# ================================================================================ #
# Check duplication
# ================================================================================ #

check = Happy_id.append([Fear_id,Excitement_id,Angry_id,Surprise_id,Pleasant_id])
if sum(check.duplicated()) == 0:
    print("There is no duplication")
else:
    print("There are some duplication")
    
# ==============================================================================#


