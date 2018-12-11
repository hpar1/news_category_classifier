CS4650 Project- News Category Classifier


By Hamza Parekh, Carlos Olea, Matthew Li


Goal:
The goal of the project was to build a Neural Network Model that could predict the category for a given article.

###################################################################

Main Files:
superConvolution.py- Optimal Model with CNN LSTM and Embedding -~50 seconds/epoch

FinalData- zipped file containing all data - data set split into training and testing folder to be utilized by the model, then split into their individual categories

oneArticlePredict.py- Demo use predicting takes a file input and gives prediction 

superConvolutionPredict.py-  data must be set up beforehand similar as classifier inorder to test the accuracy of our data, the dataset used for predict should not be used in training (there is a similar one for old model)

dataBalance.py- padding the data, utilized in prepping data for model

encodeWords.py - maps words to a value utilized in prepping data for model

###################################################################

Web Scraper Folder:

CutTo400words.py- python code to cut off too lengthy articles to 400 words

NYTimesCategoryScraper.py- python code to navigate NYT and grab categories, in order to utilize please install selenium web driver at http://chromedriver.chromium.org/downloads

NewYorkTimesScraper.py- python code to scrape the article from NYT

TimesNewsfirst400Words.py- python code to navigate and scrape Times

###################################################################

Additional info:

CS4650 Final Presentation.pptx - presentation

cs4650projecthistory.xlsx - log of accuracy and lost of the 3 models

###################################################################

Old Model:
spicyArticleClasifier.py- Added CNN layers to model -~15seconds/epoch

lameArticleClassifier.py- base model with only LSTM -~30seconds/epoch



