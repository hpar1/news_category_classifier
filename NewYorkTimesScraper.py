# -*- coding: utf-8 -*-
"""
New York Time Article Scraper
"""

from bs4 import BeautifulSoup
import requests # use get to get articles and post to send data
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import time

# Scrapes any article from paragraph tags
def scrapeArticle(res):

    soup = BeautifulSoup(res.text, 'lxml') # lxml is the parser library for struct data

    # The Article's body text
    long_string = ""
    paragraph_text = soup.find_all('p',{'class': 'css-1ygdjhk'})
    for p in paragraph_text:
        long_string += p.text
        long_string += " "
     
    long_string = long_string.encode(encoding='ascii', errors='ignore') # converts to bytes and remove non-ascii chars
    long_string = long_string.decode('utf-8', 'ignore') # convert back to utf to remove b'   '  prefix
    #print(long_string)
    
    long_list = word_tokenize(long_string) # tokenize using nltk splits at spaces
    long_list = [word.lower() for word in long_list] # make all words lower case
    long_list = [word for word in long_list if word.isalpha()] # remove all non-alphabetic words; remove punctuation
    
    lengthOfArticle = len(long_list)
    print("\nLength of Article (with stopwords): "+ str(lengthOfArticle) +" words") # length of article
    
    if lengthOfArticle == 0:
        return 'length of 0'
    
    stop_words = stopwords.words('english') # common words in english; from nltk
    long_list_without_stopwords = [word for word in long_list if not word in stop_words] # remove stop words; removes common words
    lengthOfArticleNoStopWords = len(long_list_without_stopwords)
    print("Length of Article (without stopwords): "+ str(lengthOfArticleNoStopWords) +" words") # length of article
        
    out_string = ""
    for word in long_list:
        out_string += (word + " ")
    print()
    print(out_string)
    return out_string

###############################################################################
# Takes in a list of article links and iterates through them and scrapes the articles
def scrapeArticles(categoryToCheck, Links):
    count = 1
    for i, article in enumerate(Links):
        print(article)
        res = requests.get('https://www.nytimes.com/' + article)
        output = scrapeArticle(res)
        #print('\n' + str(i) + '\n')
        if output == 'length of 0':
            print('Article has been skipped!')
        else:
            with open('newYorkTimesArticles/'+categoryToCheck+'/'+categoryToCheck+str(count)+'.txt', 'w', encoding='ascii') as file:
                file.write(output)
            print(str(count) + ' saved. On article ' + str(i+1) + ' out of ' + str(len(Links)))
            count = count + 1
        print()
        time.sleep(2) # sleeps for 2 seconds to avoid getting kicked

###############################################################################
# Driver (Make function calls)
# load in npy array from the Dynamic Web Scraper
healthList = np.load('newYorkTimesArticles/health1000.npy')
category = 'health'
scrapeArticles(category, healthList)