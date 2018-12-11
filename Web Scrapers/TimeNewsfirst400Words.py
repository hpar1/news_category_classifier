# -*- coding: utf-8 -*-
"""
BeautifulSoup4 to web scrape:
    Time magazine news.
    Get first 400 words, if less than 400 will be padded later, if more than 400 words then cut.
"""

from bs4 import BeautifulSoup
import requests # use get to get articles and post to send data
from nltk.tokenize import word_tokenize

# Scrapes any article from Time.com
def scrapeArticle(res, checkCategory):

    soup = BeautifulSoup(res.text, 'lxml') # lxml is the parser library for struct data

    # The Article's body text
    long_string = ""
    paragraph_text = soup.find_all('p')
    for p in paragraph_text[:-1]:
        long_string += p.text
        long_string += " "
     
    long_string = long_string.encode(encoding='ascii', errors='ignore') # converts to bytes and remove non-ascii chars
    long_string = long_string.decode('utf-8', 'ignore') # convert back to utf to remove b'   '  prefix
    #print(long_string)
    
    long_list = word_tokenize(long_string) # tokenize using nltk splits at spaces
    long_list = [word.lower() for word in long_list] # make all words lower case
    long_list = [word for word in long_list if word.isalpha()] # remove all non-alphabetic words; remove punctuation
    
    lengthOfArticle = len(long_list)
    print("Length of Article (with stopwords): "+ str(lengthOfArticle) +" words") # length of article
    
    if lengthOfArticle == 0:
        return 'length of 0'
        
    short_string = ""
    for word in long_list[:400]:
        short_string += (word + " ")
    
    return short_string

###########################################################################################
# SCRAPE Category PAGE
# loop to get all of the articles of the Category
def authorPageLoop(allArticlesList, soup, res, stopAt):
    articlesDiv = soup.find_all('div', {'class': 'headline'}) # find all of the divs with links
    # for each div in the div list
    for a in articlesDiv:
        if len(allArticlesList) == stopAt:
            return None # break out of function if there are already n articles in the list
        link = a.find('a') # find the a (link tag)
        allArticlesList.append(link['href']) # append the url to the articleList
    try:
        nextPage = soup.find('a', {'class': 'pagination-next'})
        print(nextPage['href'])
        res = requests.get('http://time.com/' + nextPage['href'])
        soup = BeautifulSoup(res.text, 'lxml') # lxml is the parser library for struct data
        authorPageLoop(allArticlesList, soup, res, stopAt)
    except:
        return None # break out of function when there is no next page
        
#############################################################################################
def scrapeArticles(categoryToCheck, authorURL):
   
    res = requests.get(authorURL) # get the article HTML
    soup = BeautifulSoup(res.text, 'lxml') # lxml is the parser library for struct data
    
    print('_______________________________________________________________')
    # List of Author's articles
    articleList = []
    stop = 15000 # stop at the nth article
    authorPageLoop(articleList, soup, res, stop) # initially pass in empty list
    
    count = 1
    for i, article in enumerate(articleList):
        print(article)
        res = requests.get('http://time.com/' + article)
        output = scrapeArticle(res, categoryToCheck)
        if output == 'length of 0':
            print('Article has been skipped!')
        else:
            with open('first400words/'+categoryToCheck+'/'+categoryToCheck+str(count)+'.txt', 'w', encoding='ascii') as file:
                file.write(output)
            print(str(count) + ' saved. On article ' + str(i+1) + ' out of 10')
            count = count + 1
        print()

###############################################################################
# Driver (Make function calls)
scrapeArticles('politics', 'http://time.com/section/politics/')
scrapeArticles('tech', 'http://time.com/section/tech/')
scrapeArticles('health', 'http://time.com/section/health/')
