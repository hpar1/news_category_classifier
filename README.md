Files:
FinalData- zipped file containing all data - data set split into training and testing folder to be utilized by the model, then split into their individual categories

SuperConvolution.py- Optimal Model with CNN LSTM and Embedding -~100 seconds/epoch

SpicyArticleClasifier.py- Added CNN layers to model -~50seconds/epoch

LameArticleClassifier.py- base model with only LSTM -~30seconds/epoch

OneArticlePredict.py- Demo use predicting takes a file input and gives prediction

SuperConvolutionPredict.py-  data must be set up beforehand similar as classifier inorder to test the accuracy of our data, the dataset used for predict should not be used in training

CS4650 Final Presentation.pptx - presentation
Web Scraper Folder:

CutTo400words.py- python code to cut off too lengthy articles to 400 words

NYTimesCategoryScraper.py- python code to navigate NYT and grab categories, in order to utilize please install selenium web driver at http://chromedriver.chromium.org/downloads

NewYorkTimesScraper.py- python code to scrape the article from NYT

TimesNewsfirst400Words.py- python code to navigate and scrape Times

