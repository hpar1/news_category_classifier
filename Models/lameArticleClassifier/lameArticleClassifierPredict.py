
# LSTM for sequence classification in the IMDB dataset

import os
import operator
import numpy as np
import math
import csv
from keras.models import Sequential, Model
from keras.layers import LSTM, BatchNormalization, Dense, SpatialDropout1D, CuDNNLSTM, Reshape
from keras.engine.input_layer import Input
from keras.layers.embeddings import Embedding
from keras.layers.convolutional import Conv1D, Conv2D, Conv3D
from keras.layers.convolutional import MaxPooling1D, MaxPooling2D, MaxPooling3D
from keras.layers.core import Dropout, Lambda
from keras.preprocessing import sequence 
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import optimizers

#Designate hyperparamaters 
article_length = 400
batch_size = 64
epochs = 100
embedding_vector_length = 400
dictionary_size = 10000
input_dimension = int(math.sqrt(article_length))
test_data_path = "../../data/firstWords/encoded/NYtest/"
train_data = []
train_label = []
test_data = []
test_label = []
categories = next(os.walk(test_data_path))[1]
num_categories = len(categories)

#Read in pre encoded test articles and assign labels based on parent folder
i = 0
for folder in categories:
	print(folder)
	file_paths = next(os.walk(test_data_path + folder))[2]
	for path in file_paths:
		test_file = open(test_data_path + folder+ "/" + path, "r")
		test_words = test_file.readlines()[0].strip(" ").split(" ")
		while len(test_words) < article_length:
			test_words.append("2")
		test_words = test_words[:article_length]
		test_data.append(np.reshape(test_words,(input_dimension, input_dimension) ))
		new_test_label = np.zeros(num_categories)
		new_test_label[i % num_categories] = 1
		test_label.append(new_test_label)
	i += 1


#Convert data into arrays for testing and establish random seed
np.random.seed()

max_review_length = article_length
test_data = np.asarray(test_data)
test_label = np.asarray(test_label)




#Create model
inputs = Input((input_dimension,input_dimension))
m = Lambda(lambda x : x)(inputs)
m = Reshape((max_review_length,))(m)
#Embed vectors into vector space
m = Embedding(dictionary_size, embedding_vector_length, input_length=max_review_length)(m)
#LSTM
m = (CuDNNLSTM(100))(m)
#Softmax(prediction)
outputs = (Dense(num_categories, activation='softmax'))(m)
#Put together model parts
model = Model(inputs = [inputs], outputs = [outputs]) 
#Compile model
model.compile(loss='binary_crossentropy', optimizer=optimizers.SGD(lr=1e-3, momentum=0.9), metrics=['accuracy'])
output_path = "weights/"

#Output top five weights to text file for further use
for weight in next(os.walk(output_path))[2]:
	print(weight)
	model.load_weights(output_path + weight)
	score = model.evaluate(x=test_data, y=test_label, batch_size = batch_size, verbose=1)
	print(score)




