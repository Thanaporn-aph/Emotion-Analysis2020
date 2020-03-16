# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 13:09:45 2020

@author: User
"""

from nltk.corpus import wordnet 

def synonyms(wordList):
    synonyms = [] 
    str_syns = ""
    for word in wordList:
        for syn in wordnet.synsets(word): 
            for a in syn.lemmas(): 
                synonyms.append(a.name()) 
    syns = list(set(synonyms))
    for word in syns:
        str_syns += "#"+word+" OR "
    return(str_syns[0:-4])