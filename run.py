# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 13:10:42 2020

@author: User
"""

#Load file

import os

# detect the current working directory and print it
path = os.getcwd()
print ("The current working directory is %s" % path)

import os

# define the name of the directory to be created
path = "/tmp/year"

try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)




stop_words = stopwords.words('english') 

path = "../NRC_Emotion_Lexicon_v0.92_Nov2017.xlsx"
emo_df = pd.read_excel(path)
NRC_Emo = emo_df[["English (en)","Positive","Negative","Anger","Anticipation","Disgust","Fear","Joy","Sadness","Surprise","Trust"]]

path = r"D:\UofG\Master\Web Science\NRC-Hashtag-Emotion-Lexicon\NRC-Hashtag-Emotion-Lexicon-v0.2\NRC_Hashtag_Emotion.txt"
NRC_ht_emo = pd.read_csv(path,sep='\t',names = ["Emotion", "Hashtag", "score"])
NRC_ht_emo = pd.DataFrame(NRC_ht_emo)
#Delete hashtag from the word
NRC_ht_emo["Hashtag_new"] = NRC_ht_emo["Hashtag"].replace('#','',regex=True).str.lower()
NRC_ht_emo = NRC_ht_emo[["Emotion","Hashtag_new"]].drop_duplicates(keep='last')
    
# Emoji : https://unicode.org/emoji/charts/full-emoji-list.html
path = r"D:\UofG\Master\Web Science\Emotican list.xlsx"
Emoji_emo = pd.read_excel(path)


# https://pdfs.semanticscholar.org/b95c/23d16faaadf40522fadf7b2938aacc9e3e78.pdf?_ga=2.175739874.1991890535.1583618527-851810122.1582499693 
path_a = r"C:\Users\User\Downloads\NRC-VAD-Lexicon-Aug2018Release\NRC-VAD-Lexicon-Aug2018Release\OneFilePerDimension\a-scores.txt"
a_score = pd.read_csv(path_a,sep='\t',names = ["word", "a_score"])
a_score = pd.DataFrame(a_score)
path_v =  r"C:\Users\User\Downloads\NRC-VAD-Lexicon-Aug2018Release\NRC-VAD-Lexicon-Aug2018Release\OneFilePerDimension\v-scores.txt"
v_score = pd.read_csv(path_v,sep='\t',names = ["word", "v_score"])
v_score = pd.DataFrame(v_score)

# ========================================================= #
consumer_key= '05QRcauWKUjmG6NdoTaJ5RJlR'
consumer_secret= 'cl0cveUs3uKwoDk6jzqMP3NQDlyZqBqjF7LPVDybJehAcyZzjC'
access_token= '1225411734606884865-MQFToe2bFpBTo2WQMe1JM45h9ewqOq'
access_token_secret= 'xgO4gi1h4HY0g20JDGbnGjomZk1ztv11tI0fzzfRU5Ciq'
date = "2020-01-01"

## Happy
total = 5
wordList = ["joy","happy"]
hashTags = synonyms(wordList)
EmoClass = "Happy"
tweet_data = twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date)
Happy_id = main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass)


## Fear
total = 1000
wordList = ["fear","nervous","disgust","dislike"]
hashTags = synonyms(wordList)
EmoClass = "Fear"
tweet_data = twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date)
Fear_id = main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass)


## Excitement
date = "2020-01-01"
total = 1500
wordList = ["excitement","anticipation"]
hashTags = synonyms(wordList)
hashTags = hashTags+" OR #excited"
hashTags = hashTags.replace("OR #prediction ","")
EmoClass = "Excitement"
tweet_data = twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date)
Excitement_id = main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass)


## Angry
total = 1500
wordList = ["angry","hate","annoyed"]
hashTags = synonyms(wordList)
EmoClass = "Angry"
tweet_data = twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date)
Angry_id = main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass)

## Surprise
total = 1500
wordList = ["sad","regret",'guity']
hashTags = synonyms(wordList)
EmoClass = "Surprise"
tweet_data = twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date)
Surprise_id = main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass)

## Pleasant
total = 1000
wordList = ["pleased","satisfied"]
hashTags = synonyms(wordList)
EmoClass = "Pleasant"
tweet_data = twAPI(consumer_key,consumer_secret,access_token,access_token_secret,hashTags,total,date)
Pleasant_id = main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass)


# ============================================================================

Happy_id = pd.read_csv("D:\\UofG\\Master\\Web Science\\Emotion Analysis\\EmotionData\\data\\Happy.csv")
Fear_id = pd.read_csv("D:\\UofG\\Master\\Web Science\\Emotion Analysis\\EmotionData\\data\\Fear.csv")
Excitement_id = pd.read_csv("D:\\UofG\\Master\\Web Science\\Emotion Analysis\\EmotionData\\data\\Excitement.csv")
Angry_id = pd.read_csv("D:\\UofG\\Master\\Web Science\\Emotion Analysis\\EmotionData\\data\\Angry.csv")
Surprise_id = pd.read_csv("D:\\UofG\\Master\\Web Science\\Emotion Analysis\\EmotionData\\data\\Surprise.csv")
Pleasant_id = pd.read_csv("D:\\UofG\\Master\\Web Science\\Emotion Analysis\\EmotionData\\data\\Pleasant.csv")

check = Happy_id.append([Fear_id,Excitement_id,Angry_id,Surprise_id,Pleasant_id])[["tweet_id","ClassLabel"]]
sum(check["tweet_id"].duplicated())

sample1 = Happy_id.sample(n = 20)
sample2 = Fear_id.sample(n = 20)
sample3 = Excitement_id.sample(n = 20)
sample4 = Angry_id.sample(n = 20)
sample5 = Surprise_id.sample(n = 20)
sample6 = Pleasant_id.sample(n = 20)

sample_data = sample1.append([sample2,sample3,sample4,sample5,sample6])
path = "D:\\UofG\\Master\\Web Science\\Emotion Analysis\\EmotionData\\data\\sample120.csv"
sample_data = sample_data.sample(frac=1)
sample_data.to_csv(path,index=False, encoding="utf-8")

sample = pd.read_csv(path)["CleanedText"]

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

sample_cleaned = pd.DataFrame(columns=["text"])
for text in sample:
    deEmo = pd.DataFrame([deEmojify(text)],columns=["text"])
    sample_cleaned = pd.concat([sample_cleaned,deEmo])

path2 = "D:\\UofG\\Master\\Web Science\\Emotion Analysis\\EmotionData\\data\\sample.csv"
sample_cleaned.to_csv(path2,index=False, encoding="utf-8")
