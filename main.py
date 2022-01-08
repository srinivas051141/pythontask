# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 22:19:41 2022

@author: CNU
"""

from fastapi import FastAPI
from typing import Optional
import requests
import json
import pandas as pd
import numpy as np
import random

app = FastAPI()

@app.get('/')
def index():
    return "heyy";

@app.get('/match_words')
def get_words(q: Optional[str] = None):
    #getting all the information in the link
    r =  requests.get('https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json')
    
    #only taking json part of the link's information
    data =  r.json() 
    
    #words is a list of all the words
    words = data.keys() 
    
    # values is a list of random values
    values = data.values() 
    
    # df is a dataframe of all the words in the link
    df = pd.DataFrame(list(zip(words, values)),columns =['Name', 'val']) 
   
    match_words= []
    for key in df["Name"]:
        if key.find(q) != -1:
            match_words.append(key)
    
    #print(list)
    if len(match_words) == 0:
        
        return("message : No words found with given input string")
        
    else:
        return match_words[0:5]  
    
@app.get('/retrive_by_values')
def get_words_by_value(q: Optional[str] = None): # q is the input string
    
    #getting all the information in the link
    r =  requests.get('https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json')
    
    #only taking json part of the link's information
    data =  r.json() 
    
    #assigning the values randomly in the range(0,11) for all the words 
    for key in data:
        data[key] = random.randrange(1,11) 
    
    #words is a list of all the words
    words = data.keys() 
    
    # values is a list of random values
    values = data.values() 
    
    # df is a dataframe of all the words in the link
    df = pd.DataFrame(list(zip(words, values)),columns =['Name', 'val']) 
    

    match_words = {} #new dictinory with all the matching words
    for i in range(len(df)):
        if df.iloc[i,0].find(q) != -1:
            match_words[df.iloc[i,0]] = df.iloc[i,1]  
        
    df2 = pd.DataFrame(list(zip(match_words.keys(),match_words.values()))) #creating a new dataframe which contains all the matching words
    df2 = df2.sort_values(by=[1], ascending= False) # sorted the dataframe based on the random values
    #for i in range(5):
     #   print(str(i)+". "+df2.head().loc[:,0][i]) #printing the top 5 words
    final_list =[]
    for i in range(5):
        final_list.append(((str(i+1)+'. '+df2.head().iloc[:,0].values[i])))
    return (final_list)

