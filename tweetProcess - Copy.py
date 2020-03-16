# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 17:44:50 2020

@author: User
"""

import tweepy as tw
import pandas as pd
import numpy as np
from autocorrect import Speller
import contractions
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import words
from nltk.corpus import stopwords
from string import punctuation 
import demoji

## keep only begin or end set of hashtags
def end_hashtags(hashtagSet,last_indice):
    if len(hashtagSet)==0:
        return([],0,2)
    i=len(hashtagSet)-1
    hashtags = []
    for hashtag in reversed(hashtagSet):
        if hashtag["indices"][0]-hashtagSet[i-1]["indices"][1] == 1 :
            hashtags.append(hashtagSet[i-1])
            i=i-1
        else:
            hashtags.append(hashtagSet[len(hashtagSet)-1])
            if(hashtags[0]["indices"][0]==0):
                Point =hashtags[-1]["indices"][1]
                cutType = 1 #Begin point (start hashtag)
            else:
                Point = hashtag["indices"][0]
                cutType = 0 #last point (end hashtag)
            
            if (cutType==0)&(hashtags[-1]["indices"][1]-last_indice==0):
                return(hashtags,Point,cutType)
                break;
            else:
                return([],0,2)
                break;
        
# =====================================================================#        

def text_tweet(fullText,Point,Type):
    if Type == 2:
        text = fullText
    elif (Type==0): #Begin point
        text = fullText[0:Point]
    else:
        text = fullText[Point:] #last point
    return(text)

# =====================================================================#

#middle hashrags considers as a word in the text         
def clean_text(text):
    clean = text.lower() #convert to lowercase
    clean = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', clean) # remove URLs
    clean = re.sub(r'#([^\s]+)', r'\1',clean) #remove hashtag
    clean = contractions.fix(clean) #linguistic anomalies we're -> we are
    clean = re.sub(r'(.)\1+', r'\1\1', clean) #replace duplicate characters with double chars ie. loooove -> loove 
    speller = Speller(lang='en')
    clean   = speller(clean) #fix the misspelling
    clean = clean.replace("\n"," ") #remove new line
    return(clean)

# =====================================================================#
# we will discard the text that has less than 3 english words 
def less3Eng(text):
    eng = 0
    tokenize = word_tokenize(text)
    for word in tokenize:
        if word in words.words():
            eng = eng+1
    return(eng<3)
            
# ======================================================================#

def pre_lex(cleaned_text):
    stop_words = stopwords.words('english') 
    cleaned_text = re.sub('@[^\s]+', 'AT_USER', cleaned_text) # replace @username with AT_USER
    tokenize = word_tokenize(cleaned_text)
    word = [word for word in tokenize if word not in stop_words] #remove stop word
    word = [word for word in word if word not in ["URL","AT_USER"]] # remove usernames, URL
    word1 = [word1 for word1 in word if word1 not in list(punctuation)] #remove special character
    word1 = pd.DataFrame(word1).rename(columns={0: "word"})
    return(word1)

# ==========================================================================#

def text_lexicon(pre_text,NRC_Emo,stop_words):
    merged_inner = pd.merge(left=pre_text, right=NRC_Emo, left_on='word', right_on='English (en)')
    merged_inner.columns = [x.lower() for x in merged_inner.columns]
    
    yes = (merged_inner["surprise"]+merged_inner["sadness"])>0
    no  = (merged_inner["sadness"])>0
    merged_inner["Surprise"] = np.where(merged_inner["negative"]+merged_inner["surprise"]==2, yes, no)
    
    yes2 = (merged_inner["anticipation"]+merged_inner["surprise"])>0
    no2 =  (merged_inner["anticipation"])>0
    merged_inner["Excitement"]  = np.where(merged_inner["positive"]+merged_inner["surprise"]==2, yes2, no2)
    
    merged_inner["Fear"] = (merged_inner["disgust"]+merged_inner["fear"])>0 
    merged_inner["Angry"] = merged_inner["anger"]>0
    merged_inner["Happy"] = merged_inner["joy"]>0
    merged_inner["Negative"] = merged_inner["negative"]>0
    merged_inner["Positive"] = merged_inner["positive"]>0
    return(merged_inner.sum(axis = 0)["Surprise":"Positive"].astype(int))


#==============================================================================#

def hashtag_lexicon(endHashtag,NRC_Emo,NRC_ht_emo):
    if len(endHashtag)==0:
        return(0)
    Hashtags=[]
    for tag in endHashtag:
        Hashtags.append(tag["text"].lower())
    Hashtags = pd.DataFrame(Hashtags).rename(columns={0: "word"})
    
    # merge with NRC Emotion first
    merged_inner = pd.merge(left=Hashtags, right=NRC_Emo, left_on='word', right_on='English (en)',how="left")
    merged_inner.columns = [x.lower() for x in merged_inner.columns]
    yes = (merged_inner["surprise"]+merged_inner["sadness"])>0
    no  = (merged_inner["sadness"])>0
    merged_inner["Surprise"] = np.where(merged_inner["negative"]+merged_inner["surprise"]==2, yes, no)
    yes2 = (merged_inner["anticipation"]+merged_inner["surprise"])>0
    no2 =  (merged_inner["anticipation"])>0
    merged_inner["Excitement"]  = np.where(merged_inner["positive"]+merged_inner["surprise"]==2, yes2, no2)
    merged_inner["Fear"] = (merged_inner["disgust"]+merged_inner["fear"])>0 
    merged_inner["Angry"] = merged_inner["anger"]>0
    merged_inner["Happy"] = merged_inner["joy"]>0
    merged_inner["Negative"] = merged_inner["negative"]>0
    merged_inner["Positive"] = merged_inner["positive"]>0
    score1 = merged_inner.sum(axis = 0)["Surprise":"Positive"].astype(int)
    
    # merge the remaining with NRC Hashtag Emotion
    if any(merged_inner['english (en)'].isnull()):
        step2 = merged_inner[merged_inner['english (en)'].isnull()]['word']
        merged_inner2 = pd.merge(left=step2, right=NRC_ht_emo, left_on='word', right_on='Hashtag_new')[['word','Emotion']]
        if merged_inner2.shape[0]==0:
            return(score1)
        score2 = merged_inner2[["word","Emotion"]].groupby('word')['Emotion'].value_counts().unstack().fillna(0)
        score3 = pd.DataFrame(np.zeros(shape=(1,10)).astype(int),
                             columns=["positive","negative","anger","anticipation","disgust","fear","joy","sadness","surprise","trust"])
        score2 = score3.append(score2).fillna(0)
        yes = (score2["surprise"]+score2["sadness"])>0
        no  = (score2["sadness"])>0
        score2["Surprise"] = np.where(score2["negative"]+score2["surprise"]==2, yes, no)
        yes2 = (score2["anticipation"]+score2["surprise"])>0
        no2 =  (score2["anticipation"])>0
        score2["Excitement"]  = np.where(score2["positive"]+score2["surprise"]==2, yes2, no2)
        score2["Fear"] = (score2["disgust"]+score2["fear"])>0 
        score2["Angry"] = score2["anger"]>0
        score2["Happy"] = score2["joy"]>0
        score2["Negative"] = score2["negative"]>0
        score2["Positive"] = score2["positive"]>0
        score2 = score2.sum(axis = 0)["Surprise":"Positive"].astype(int)

        total = score1+score2
        return(total)
    return(score1)    
    

# ======================================================================= #

# https://pypi.org/project/demoji/
# demoji.download_codes() #run only for the first time

def emoji(cleaned_text,Emoji_emo):
    emoji = demoji.findall(cleaned_text)
    score = pd.DataFrame(np.zeros(shape=(1,6)).astype(int),
                         columns=['Happy','Excitement','Pleasant','Surprise','Fear','Angry'])
    for emo in emoji:
        if Emoji_emo["Happy"].str.contains(emoji[emo]).sum()>0 :
            score["Happy"] += 1
        if Emoji_emo["Excitement"].str.contains(emoji[emo]).sum()>0 :
            score["Excitement"] += 1
        if Emoji_emo["Pleasant"].str.contains(emoji[emo]).sum()>0 :
            score["Pleasant"] += 1
        if Emoji_emo["Surprise"].str.contains(emoji[emo]).sum()>0 :
            score["Surprise"] += 1
        if Emoji_emo["Fear"].str.contains(emoji[emo]).sum()>0 :
            score["Fear"] += 1
        if Emoji_emo["Angry"].str.contains(emoji[emo]).sum()>0 :
            score["Angry"] += 1
    return(score)

# =====================================================================
    
def emoticon(text):
    score = pd.DataFrame(np.zeros(shape=(1,6)).astype(int),
                             columns=['Happy','Excitement','Pleasant','Surprise','Fear','Angry'])
    happy = [':‑)',':)',':-]',':]',':->',':>','8-)','8)',':-}',':}',':o)',':c)',':^)','=]','=)']
    for each in happy:
        if each in text:
            score["Happy"] += 1   
    surprise = [":'‑(", ":'(", ':‑(', ':(',':‑c',':c',':‑<',':<', ':‑[', ':[', ':{',':‑O',':O',':‑o',':o',':-0','8‑0','>:O']
    for each in surprise:
        if each in text:
            score["Surprise"] += 1     
    angry = [':-||','>:[', ':@', '>:(']
    for each in angry:
        if each in text:
            score["Angry"] += 1       
    excited = ['＼(~o~)／','＼(^o^)／','＼(-o-)／','ヽ(^。^)ノ','ヽ(^o^)丿','(*^0^*)']
    for each in excited:
        if each in text:
            score["Excitement"] += 1 
    fear = ["D‑':",'D:<','D:','D8','D;','D=','DX']
    for each in fear:
        if each in text:
            score["Fear"] += 1    
    pleasant = [':-3',':3']
    for each in pleasant:
        if each in text:
            score["Pleasant"] += 1
    return(score)
    
# ======================================================================= #

def total_score(text_score,hashtag_score,emoji_score,emoticon_score):
    score1 = text_score+hashtag_score
    score1["Pleasant"] = 0
    score2 = emoji_score+emoticon_score
    score2["Positive"] = 0
    score2["Negative"] = 0
    total_sc = score1+score2
    return(total_sc)



# ======================================================================== #

def class_label(text,cleaned_text,endHashtag,NRC_Emo,NRC_ht_emo,Emoji_emo,stop_words,a_score,v_score):
    pre_text = pre_lex(cleaned_text)
    text_score = text_lexicon(pre_text,NRC_Emo,stop_words)
    hashtag_score = hashtag_lexicon(endHashtag,NRC_Emo,NRC_ht_emo)
    emoji_score = emoji(cleaned_text,Emoji_emo)
    emoticon_score = emoticon(cleaned_text)
    score = total_score(text_score,hashtag_score,emoji_score,emoticon_score)
    max_score = score.loc[0][score.loc[0]==(max(score.loc[0]))]
    if ("Positive" in max_score)&("Negative" in max_score):
        class_ = "None"
    elif ("Positive" in max_score)|("Negative" in max_score):
        class_ = VA_score(a_score,v_score,pre_text)
    elif len(max_score) == 1:
        class_  = max_score.index[0]
    else:
        class_ = "None"
    return(class_)


# ========================================================================= #

def VA_score(a_score,v_score,pre_text):
    merged_a = pd.merge(left=pre_text, right=a_score, left_on='word', right_on='word')
    merged_v = pd.merge(left=pre_text, right=v_score, left_on='word', right_on='word')
    mean_v=merged_v["v_score"].mean()
    mean_a=merged_a["a_score"].mean()
    if mean_v >  0.5 : #Positive
        if (mean_a >= 0.75):
            return("Excitement")
        elif (mean_a >= 0.5):
            return("Happy")
        else:
            return("Pleasant")
    else: #Negative
        if (mean_a >= 0.75):
            return("Angry")
        elif (mean_a>= 0.5):
            return("Fear")
        else:
            return("Surprise")
        
# ========================================================================= #    
