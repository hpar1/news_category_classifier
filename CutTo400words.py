# -*- coding: utf-8 -*-
"""
Read in files and reduce them to 400 words
"""
import os
from nltk.tokenize import word_tokenize

# read in file, save to new location with first 400 words
def cutAndCopy(inPath,outPath):
    for file in os.listdir(inPath):
        with open(inPath + '/' + file, encoding='ascii') as input:
            long_string = input.read()
        # The Article's body text
        print('Input length: ' + str(len(long_string.split())))
        long_list = word_tokenize(long_string) # tokenize using nltk splits at spaces    
        short_string = ""
        for word in long_list[:400]:
            short_string += (word + " ")
        print('Output length: '+ str(len(short_string.split())))
        print()
        with open(outPath + '/' + file, 'w', encoding='ascii') as output:
            output.write(short_string)
###############################################################################
inputPathpol = 'newYorkTimesArticles/politics'
outputPathpol = 'newYorkTimes400words/politics'
inputPathhe = 'newYorkTimesArticles/health'
outputPathhe = 'newYorkTimes400words/health'
inputPathte = 'newYorkTimesArticles/tech'
outputPathte = 'newYorkTimes400words/tech'

cutAndCopy(inputPathpol,outputPathpol)
cutAndCopy(inputPathhe,outputPathhe)
cutAndCopy(inputPathte,outputPathte)