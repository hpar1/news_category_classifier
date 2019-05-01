# -*- coding: utf-8 -*-
"""
BeautifulSoup4 to web scrape:
    Time magazine news
    For Text and Authors
    Initial version in which a summary was made
"""

from bs4 import BeautifulSoup
import requests # use get to get articles and post to send data
import collections
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import json

# Scrapes a particular article from Time.com
def scrapeArticle(res):

    soup = BeautifulSoup(res.text, 'lxml') # lxml is the parser library for struct data
    
    # Title of the article
    title = soup.find('h1')
    print("Title: "+ title.text)
    
    # Authors of the article
    authorsList = []
    authors = soup.find_all('a', {'class': 'author-name'})
    print("Author(s): ", end='')
    for a in authors:
        authorsList.append(a.text.strip())
    print(authorsList)
    
    # Date when Article was published
    date = soup.find('div', {'class': 'timestamp'})
    da = date.text.replace('\n', '').strip()
    print("Date: " + da) # replace new line with empty string; strip to remove any extra spaces
    
    # Categories that the article is in
    categoryList = []
    category = soup.find('div', {'class': 'intro-top'})
    cat = category.find_all('span') # all span tags inside intro-top div
    for i in cat:
        categoryList.append(i.text.strip())
        #print(i.text, end='     ')
    print("Categories: " + str(categoryList))
    
    # The Article's body text
    long_string = ""
    paragraph_text = soup.find_all('p')
    for p in paragraph_text:
        long_string += p.text
        long_string += " "
    
    lengthOfArticle = str(len(long_string.split()))
    print("Length of Article: "+ lengthOfArticle +" words") # length of article
   
    stop_words = stopwords.words('english') # common words in english
    text_list = word_tokenize(long_string) # tokenize the list using Natural Lang ToolKit
    text_list = [word for word in text_list if word.isalpha()] # remove punctuation
    text_list = [word.lower() for word in text_list] # make all words lower case
    text_list = [word for word in text_list if not word in stop_words] # remove stop words after lower case
    
    count = collections.Counter(text_list).most_common(10) # count frequency of words and keep top 10 as tuples
    countDict = json.dumps(dict(count)) # convert list of tuples to a dictionary; json dumps puts dict in json format
    print("\n" + str(countDict) + "\n")
       
    ####################################################################
    # SUMMARIZER
    words = word_tokenize(long_string) # tokenize all text using NLTK
    freqTable = {} # empty dictionary for Frequency Table
    
    for word in words: # iterate through text
        word = word.lower() # make the word lower case
        if word in stop_words:
            continue # go to next word
        if word in freqTable:
            freqTable[word] += 1 # incr val in freqTable if word already exists
        else:
            freqTable[word] = 1 # create new pair is frequency table
    
    sentences = sent_tokenize(long_string) # tokenize sentences
    sentenceValue = {} # empty dict for sentence ranking
    for sentence in sentences: # iterate through the sentence
        for wordValue in freqTable: # for each word-value pair in freqTable iterate through keys
            if wordValue in sentence.lower(): # if word is in sentence (wordValue key)
                if sentence in sentenceValue: # if sentence is already in dictionary
                    sentenceValue[sentence] += freqTable[wordValue] # add word value to existing sentence
                else:
                    sentenceValue[sentence] = freqTable[wordValue] # create a sentence pair and add word value
    
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence] # get sum of all of the values from Sentence Dictionary
    # Average value of a sentence from original text
    average = int(sumValues / len(sentenceValue)) # divide by amount of sentences
    
    summary = ''
    for sentence in sentences: # iterate through all of the sentences in order
        if sentence in sentenceValue and sentenceValue[sentence] > (1.5 * average): # value of sentence is 1.5 x average
            summary += " " + sentence
    # if the summary is still empty
    if summary == '':
        for sentence in sentences: # iterate through all of the sentences in order
            if sentence in sentenceValue and sentenceValue[sentence] > (1.25 * average): # value of sentence is 1.25 x average
                summary += " " + sentence
    print()
    print("Summary:")
    print(summary)
    print()
    print("Full Text:")
    print(long_string)
    #################################################################### 
    
    #r = 
    # use requests to post (send data) to node server as json
    # For Local use Use 'http://localhost:3000/sendArticle'
    """
    requests.post('http://localhost:3000/sendArticle',
                  json={
                          "title": title.text,
                          "authors": authorsList,
                          "date": da,
                          "categories": categoryList,
                          "length": lengthOfArticle,
                          "frequency": countDict,
                          "summary": summary
                          })
    """
###########################################################################################
# SCRAPE AUTHOR PAGE

# loop to get all of the articles of the author
def authorPageLoop(allArticlesList, soup, res):
    articlesDiv = soup.find_all('div', {'class': 'headline'}) # find all of the divs with links
    # for each div in the div list
    for a in articlesDiv:
        if len(allArticlesList) == 10:
            return None # break out of function if there are already 10 articles in the list
        link = a.find('a') # find the a (link tag)
        allArticlesList.append(link['href']) # append the url to the articleList
    try:
        nextPage = soup.find('a', {'class': 'pagination-next'})
        print(nextPage['href'])
        res = requests.get('http://time.com/' + nextPage['href'])
        soup = BeautifulSoup(res.text, 'lxml') # lxml is the parser library for struct data
        authorPageLoop(allArticlesList, soup, res)
    except:
        return None # break out of function when there is no next page
        
#############################################################################################
# DRIVER CALLS
"""
authorURL = input("Please enter the link of the Author Profile you want to scrape: ")
res = requests.get(authorURL)#'http://time.com/author/ryan-teague-beckwith/?page=1')#'http://time.com/author/w-j-hennigan/?page=5') # get the page
soup = BeautifulSoup(res.text, 'lxml') # lxml is the parser library for struct data

# List of Author's articles
articleList = []
authorPageLoop(articleList, soup, res) # initially pass in empty list

for article in articleList:
    res = requests.get('http://time.com/' + article)
    scrapeArticle(res)
    print()
"""

# test one article
singleURL = input("Please enter the link of the Article you want to scrape: ")
res = requests.get(singleURL)#http://time.com/5574154/kai-fu-lee-time-100-summit/ #http://time.com/5566756/march-madness-brackets-random/ # get the page
soup = BeautifulSoup(res.text, 'lxml') # lxml is the parser library for struct data
scrapeArticle(res)
###############################################################################