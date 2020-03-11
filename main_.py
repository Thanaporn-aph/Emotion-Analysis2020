# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 00:06:23 2020

@author: User
"""

def main(tweet_data,NRC_Emo,NRC_ht_emo,Emoji_emo,a_score,v_score,EmoClass):
    FinalData = pd.DataFrame(columns=["tweet_id","OriginalText","CleanedText","ClassLabel","created_at"])
    i=0
    j=0
    total = 0
    for tweet in tweet_data: 
        total+=1
        print(total)
        last_indice = len(tweet[1])
        separate = end_hashtags(tweet[2],last_indice)
        endHashtag = separate[0]
        Point = separate[1]
        Type =  separate[2] 
        text = text_tweet(tweet[1],Point,Type)
        cleaned_text = clean_text(text)
        if not(less3Eng(cleaned_text)):
            #save clean text, hashtag, class
            final_class = class_label(text,cleaned_text,endHashtag,NRC_Emo,NRC_ht_emo,Emoji_emo,stop_words,a_score,v_score)
            Data = pd.DataFrame([[str(tweet[0]),tweet[1],cleaned_text,final_class,tweet[-1]]],columns=["tweet_id","OriginalText","CleanedText","ClassLabel","created_at"])
            FinalData = pd.concat([FinalData,Data])
            if final_class == EmoClass:
                i+=1
                if i == 150:
                    break;
        else:
            j+=1
                    
    stat = FinalData.groupby(['ClassLabel']).count()["tweet_id"]
    stat = stat.append(pd.Series([j,total], index=["less_3eng","total_tweets"]))
    # write csv statistics for the process
    filename = "D:\\UofG\\Master\\Web Science\\Emotion Analysis\\\EmotionData\\stat\\" + EmoClass + "1_stat.csv"           
    stat.to_csv(filename)
    data = FinalData[FinalData["ClassLabel"]==EmoClass]
    # write the tweet for specific class to csv 
    filename2 = "D:\\UofG\\Master\\Web Science\\Emotion Analysis\\EmotionData\\data\\"+EmoClass+"1.csv"
    data.to_csv(filename2, index=False, encoding="utf-8")
    return(data["tweet_id"])
