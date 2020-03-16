# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 23:00:17 2020

@author: User
"""
import pandas as pd
Happy_id = pd.read_csv("Emotions_6Class\\Happy.csv")
Fear_id = pd.read_csv("Emotions_6Class\\Fear.csv")
Excitement_id = pd.read_csv("Emotions_6Class\\Excitement.csv")
Angry_id = pd.read_csv("Emotions_6Class\\Angry.csv")
Surprise_id = pd.read_csv("Emotions_6Class\\Surprise.csv")
Pleasant_id = pd.read_csv("Emotions_6Class\\Pleasant.csv")

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
