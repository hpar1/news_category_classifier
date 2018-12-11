# -*- coding: utf-8 -*-
"""
Scrape the NY Times Category page for article links
"""

from bs4 import BeautifulSoup
from selenium import webdriver # for dynamic web scraping
import time
import numpy as np

# also requires the use of the Chrome or Firefox web driver
# Chrome driver: http://chromedriver.chromium.org/downloads
driver = webdriver.Chrome('webdriver/chromedriver.exe') # initialize chrome webdriver
driver.get('https://www.nytimes.com/section/health') # get the current page

# get page source of website after loading it fully
for i in range(115):
    driver.find_element_by_xpath('//button[text()="Show More"]').click() # click the show more button on the bottom
    time.sleep(7) # sleeps for 7 seconds to avoid getting kicked
    print(i+1)

res = driver.execute_script("return document.documentElement.outerHTML") # get the current HTML
driver.quit() # exit the driver

soup = BeautifulSoup(res, 'lxml') # parse through HTML

box = soup.find('div', {'class': 'css-13mho3u'}) # find all divs for the list at the bottom
links = box.find_all('a') # get all of the links

someList = [] # list to store the links
# iterate through links
for a in links:
    # if the link is not in the list add it
    if a['href'] not in someList:
        someList.append(a['href'])
# print the list of links
for i in someList:
    print(i)

NPlist = np.asarray(someList, dtype=str) # make the list into an np array to be saved and loaded
